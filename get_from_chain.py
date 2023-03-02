import decimal
import hashlib
import json
import logging
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from common import HASH_FILE, ORD_DATA_DIR, STATS_FILE, RawProxy, rpc_connection
from ord_stats import Inscription


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


@dataclass
class Content:
    content_length: int
    content_type: str
    content_hash: str
    payload: bytes


HERE = Path(__file__).parent

verified_file = HERE / "verified.txt"

log_file_path = HERE / "verify.log"
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)


def save_verified(tx_id: str) -> None:
    with open(verified_file, "a") as f:
        f.write(tx_id + "\n")


def load_verified() -> set[str]:
    if not verified_file.exists():
        return set()
    with open(verified_file, "r") as f:
        return set(f.read().splitlines())


def save_data(tx_id: str, content: Content) -> None:
    (ORD_DATA_DIR / f"{tx_id}.dat").write_bytes(content.payload)
    with open(HASH_FILE, "a") as f:
        f.write(content.content_hash + "\n")


# first_block = 767430
# OP_FALSE (0x00) OP_IF (0x63) OP_PUSHBYTES3 (0x03) "ord" (0x6f7264) OP_1 (0x01) https://docs.ordinals.com/inscriptions.html
# ORD_IDENTIFIER = "0063036f726401"

# p = connection()

# def get_block_hash(block_num: int) -> str:
#     return p.getblockhash(block_num)


# def get_block(block_hash: str) -> dict:
#     return p.getblock(block_hash, 2)


def get_tx(tx_id: str, conn: RawProxy) -> dict:
    raw_tx = conn.getrawtransaction(tx_id)
    return conn.decoderawtransaction(raw_tx)


def verify_ordinal(
    tx: dict, conn: RawProxy, inscription: Inscription | None = None
) -> Content | None:
    tx_id = tx["txid"]
    try:
        witness_script = tx["vin"][0]["txinwitness"][1]

        decoded_script = conn.decodescript(witness_script)["asm"]

        script_parts = decoded_script.split(" ")
        print("script_parts", script_parts)

        assert len(script_parts[0]) == 64, "first part is not 64"
        assert script_parts[-1] == "OP_ENDIF", "no OP_ENDIF"
        assert script_parts[1] == "OP_CHECKSIG", "no OP_CHECKSIG"
        assert script_parts[2] == "0", "no 2"
        assert script_parts[3] == "OP_IF", "no OP_IF"
        assert script_parts[4] == "6582895", "no 6582895"
        assert script_parts[5] == "1", "no 5"

        content_type = script_parts[6]
        content_type_ascii = bytes.fromhex(content_type).decode("ascii")
        if inscription:
            assert (
                content_type_ascii == inscription["content_type"]
            ), "Content types do not match"

        assert script_parts[7] == "0", "no 7"

        # cleanup
        if script_parts[-2] == "-2":
            # pop this one
            script_parts.pop(-2)

        data_parts = script_parts[8:-1]
        hex_data = "".join(data_parts)

        content_length = len(hex_data) // 2
        if inscription:
            assert (
                abs(content_length - inscription["content_length"]) < 5
            ), f"Content length do not match - {content_length} vs {inscription['content_length']}"

        try:
            payload = bytes.fromhex(hex_data)
        except ValueError:
            first_index = len(witness_script) - (content_length * 2) - 2
            data = witness_script[first_index:-2]
            payload = bytes.fromhex(data)

        return Content(
            content_length=content_length,
            content_type=content_type_ascii,
            content_hash=hashlib.md5(payload).hexdigest(),
            payload=payload,
        )
    except AssertionError as e:
        logging.error(f"AssertionError {tx_id} : {e}")
        return None
    except Exception as e:
        # logging.exception(f"Exception {tx_id} : {e}")
        logging.error(f"Exception {tx_id} : {e}")
        return None


with open(STATS_FILE, "r") as f:
    STATS: dict[str, Inscription] = json.load(f)


already_verified = load_verified()
all_unverified = (
    inscr for inscr in STATS.values() if inscr["tx_id"] not in already_verified
)


def analyze_inscription(inscription: Inscription, conn: RawProxy) -> None:
    tx_id = inscription["tx_id"]
    if tx_id in already_verified:
        return

    tx = get_tx(tx_id, conn)
    result = verify_ordinal(tx, conn, inscription)
    if not result:
        print("FAIL", tx_id)
    else:
        save_verified(tx_id)
        save_data(tx_id, result)


def run_until_finished() -> None:
    conn = rpc_connection()
    while True:
        try:
            inscription = next(all_unverified)
        except StopIteration:
            break

        try:
            analyze_inscription(inscription, conn)
        except Exception as e:
            logging.exception(f"Unexpected ERROR: {e}")


if __name__ == "__main__":
    no_of_threads = 3
    for _ in range(no_of_threads):
        new_thread = threading.Thread(target=run_until_finished)
        new_thread.start()
        time.sleep(0.1)

    # tx_id = "a672be7f248eb10b923ea2658de7beddfca8783dca417168a4705bd1c9625370"
    # conn = rpc_connection()
    # tx = get_tx(tx_id, conn)
    # result = verify_ordinal(tx, conn)

    # # for counter, inscription in enumerate(list(stats.values())[:5]):
    # for counter, inscription in enumerate(stats.values()):
    #     tx_id = inscription["tx_id"]
    #     if tx_id in already_verified:
    #         continue

    #     tx = get_tx(tx_id)
    #     # print(json.dumps(tx, indent=4, cls=DecimalEncoder))
    #     # if ORD_IDENTIFIER in str(tx):
    #     #     print("yes")
    #     # else:
    #     #     print("no")

    #     result = verify_ordinal(tx, inscription)
    #     if not result:
    #         print("FAIL", tx_id)
    #     else:
    #         save_verified(tx_id)
    #         save_data(tx_id, result)

    #     if counter % 100 == 0:
    #         logging.info(counter)
