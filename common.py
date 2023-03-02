from __future__ import annotations

import json
from pathlib import Path

from typing_extensions import TypedDict

from bitcoin.rpc import RawProxy

HERE = Path(__file__).parent

STATS_FOLDER = HERE / "ordinals_stats"
MAPPING_FILE = STATS_FOLDER / "ord_id_to_tx_id.json"
STATS_FILE = STATS_FOLDER / "stats_ordinals_com.json"

OP_RETURN_DATA_DIR = Path("/mnt/bitcoin2/op_return_data")

# ORD_DATA_DIR = Path("/mnt/bitcoin2/ord_data")
ORD_DATA_DIR = HERE / "ordinals"
HASH_FILE = ORD_DATA_DIR / "all_hashes.txt"

MISSING_FILE = HERE / "missing.txt"


# TODO: create a speed experiment comparing TypedDict vs @dataclass
# TODO: load the data into sqlite3 and compare it with JSON file and in-python dict
class Inscription(TypedDict):
    index: int
    tx_id: str
    minted_address: str
    content_type: str
    content_hash: str
    timestamp: str
    content_length: int
    genesis_fee: int
    genesis_height: int
    output_value: int
    sat_index: int

    # TODO: add the overall size of transaction
    # TODO: add the overall size of parent transaction
    # TODO: add the current owner - or at least whether it was already sent to other address
    # (bcli gettxout tx_id tx_output_index)
    # TODO: add collection name, if any


def rpc_connection() -> RawProxy:
    return RawProxy(service_port=8332, btc_conf_file="mainnet.conf")


def load_stats_json() -> dict[str, Inscription]:
    with open(STATS_FILE, "r") as f:
        return json.load(f)
