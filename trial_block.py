from pathlib import Path

from common import rpc_connection

HERE = Path(__file__).parent

p = rpc_connection()


def all_transactions_from_block(block_hash: str) -> None:
    res = p.getblock(block_hash, 2)
    for tx in res["tx"]:
        tx_id = tx["txid"]
        if "OP_RETURN" in str(tx["vout"]):
            print(tx["vout"])
            print(tx_id)
            for out in tx["vout"]:
                if "OP_RETURN" in str(out):
                    asm = out.get("scriptPubKey", {}).get("asm", "")
                    if asm.startswith("OP_RETURN"):
                        print(asm)


if __name__ == "__main__":
    block = "00000000000000000006af3ce7cdbe82a0b0521e2951ce882c2de18ecbd1e540"
    all_transactions_from_block(block)
