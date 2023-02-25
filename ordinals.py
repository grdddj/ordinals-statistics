from rpc import connection
from pathlib import Path
import datetime
import logging
from decimal import Decimal

HERE = Path(__file__).parent


p = connection()


def is_ordinal(decoded_tx: dict) -> bool:
    # for vin in decoded_tx["vin"]:
    #     witness = vin.get("txinwitness", [])
    #     if len(witness) == 3:
    #         return False

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

def all_transactions_from_block(block_hash: str) -> None:
    res = p.getblock(block_hash, 2)
    for tx in res["tx"]:
        tx_id = tx["txid"]
        if is_ordinal(tx):
            print(tx_id)
  
if __name__ == "__main__":
    all = True

    if all:
        block = "00000000000000000006af3ce7cdbe82a0b0521e2951ce882c2de18ecbd1e540"
        all_transactions_from_block(block)
    else:
        txid = "7484cf16beb6ee85a0bad92335ddb388c93b73b60e5ed06987365eab6b51e986"
        raw_tx = p.getrawtransaction(txid)
        decoded_tx = p.decoderawtransaction(raw_tx)
        # print("decoded_tx", decoded_tx)
        for vin in decoded_tx["vin"]:
            witness = vin.get("txinwitness", [])
            print(len(witness))
            # if len(witness) > 1:
            #     print(witness[1])
            # type = vin.get("type", "")
            # if type == "witness_v1_taproot":
            #     witness = vin.get("txinwitness", [])
            #     print(len(witness))
        vout = decoded_tx["vout"]
        if len(vout) == 1 and vout[0]["value"] == Decimal('0.00010000'):
            print("OP_RETURN")
