import decimal
import json
import logging
import threading
import time
from pathlib import Path

from common import (
    HASH_FILE,
    ORD_DATA_DIR,
    STATS_FILE,
    InscriptionContent,
    OrdinalTx,
    RawProxy,
    rpc_connection,
)
from ord_stats import InscriptionDict


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


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


def save_data(tx_id: str, content: InscriptionContent) -> None:
    (ORD_DATA_DIR / f"{tx_id}.dat").write_bytes(content.payload)
    with open(HASH_FILE, "a") as f:
        f.write(content.content_hash + "\n")


# first_block = 767430
# OP_FALSE (0x00) OP_IF (0x63) OP_PUSHBYTES3 (0x03) "ord" (0x6f7264) OP_1 (0x01) https://docs.ordinals.com/inscriptions.html
# ORD_IDENTIFIER = "0063036f726401"


with open(STATS_FILE, "r") as f:
    STATS: dict[str, InscriptionDict] = json.load(f)


already_verified = load_verified()
all_unverified = (
    inscr for inscr in STATS.values() if inscr["tx_id"] not in already_verified
)


def analyze_inscription(inscription: InscriptionDict, conn: RawProxy) -> None:
    tx_id = inscription["tx_id"]
    if tx_id in already_verified:
        return

    tx = OrdinalTx.from_tx_id(tx_id, conn)
    result = tx.get_inscription(conn)
    # tx = get_tx(tx_id, conn)
    # result = verify_ordinal(tx, conn, inscription)
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
