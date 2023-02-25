import datetime
import logging
from pathlib import Path

from rpc import connection

HERE = Path(__file__).parent

log_file_path = HERE / "btc.log"
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

p = connection()


def file() -> Path:
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d_%H-%M-%S")
    return HERE / f"op_return_{now}.txt"


OP_FILE = file()


def save(txid: str) -> None:
    with open(OP_FILE, "a") as f:
        f.write(txid + "\n")


def all_transactions_from_block(block_hash: str) -> None:
    res = p.getblock(block_hash, 2)
    logging.info("extracted")
    for tx in res["tx"]:
        tx_id = tx["txid"]
        if "OP_RETURN" in str(tx["vout"]):
            save(tx_id)


if __name__ == "__main__":
    block_amount = p.getblockchaininfo()["blocks"]
    for i in range(block_amount, 0, -1):
        logging.info(f"block {i}")
        block_hash = p.getblockhash(i)
        save(f"----------{block_hash}")
        all_transactions_from_block(block_hash)
