import threading
from rpc import connection
from pathlib import Path
import datetime
import logging
import sys
import time
from decimal import Decimal

HERE = Path(__file__).parent

log_file_path = HERE / "btc.log"
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d_%H-%M-%S")

def save_op_return(payload: str, ident: int) -> None:
    path = HERE / f"op_return_{now}-{ident}.txt"
    with open(path, "a") as f:
        f.write(payload + "\n")      


def save_ordinal(payload: str, ident: int) -> None:
    path = HERE / f"ordinal_{now}-{ident}.txt"
    with open(path, "a") as f:
        f.write(payload + "\n")      

if len(sys.argv) > 1 and sys.argv[1].isdigit():
    block_amount = int(sys.argv[1])
else:
    block_amount = connection().getblockchaininfo()["blocks"]

all_blocks = iter(range(block_amount, 0, -1))

no_of_threads = 2


def is_ordinal(decoded_tx: dict) -> bool:
    txin_count = len(decoded_tx["vin"])
    txout_count = len(decoded_tx["vout"])
    tx_count = txin_count + txout_count

    weight = decoded_tx["weight"]

    if weight > 5000 and tx_count < 5:
        return True

    for vout in decoded_tx["vout"]:
        if vout["value"] == Decimal('0.00010000'):
            return True

    return False


def analyze_blocks():
    conn = connection()
    ident = threading.get_ident()
    while True:
        try:
            block = next(all_blocks)
            logging.info(f"block {block}, {ident}")
            block_hash = conn.getblockhash(block)
            # save_ordinal(f"----------{block_hash}", ident)
            save_op_return(f"----------{block_hash}", ident)
            res = conn.getblock(block_hash, 2)
            for tx in res["tx"]:
                tx_id = tx["txid"]
                # if is_ordinal(tx):
                #     save_ordinal(tx_id, ident)
                if "OP_RETURN" in str(tx["vout"]):
                    for out in tx["vout"]:
                        if "OP_RETURN" in str(out):
                            asm = out.get("scriptPubKey", {}).get("asm", "")
                            if asm.startswith("OP_RETURN"):
                                save_op_return(f"{tx_id}--{asm}", ident)
        except StopIteration:
            break

if __name__ == "__main__":
    for _ in range(no_of_threads):
        new_thread = threading.Thread(target=analyze_blocks)
        new_thread.start()
        time.sleep(1)