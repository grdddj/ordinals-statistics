import json
from collections import defaultdict
from pathlib import Path
from typing import TypedDict

HERE = Path(__file__).parent

STATS_FILE = HERE / "ordinals_stats" / "stats.json"


# TODO: create a speed experiment comparing TypedDict vs @dataclass
# TODO: load the data into sqlite3 and compare it with JSON file and in-python dict
class Inscription(TypedDict):
    index: int
    tx_id: str
    minted_address: str
    content_type: str
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
    # TODO: add content_hash (or the hash of the whole witness element)
    # TODO: add collection name, if any


def get_data() -> dict[str, Inscription]:
    return json.loads(STATS_FILE.read_text())


def content_types() -> dict[str, int]:
    data = get_data()
    content_types: dict[str, int] = defaultdict(int)
    for item in data.values():
        content_types[item["content_type"]] += 1
    return content_types


def biggest_sizes(limit: int) -> list[Inscription]:
    data = get_data()
    res = sorted(data.values(), key=lambda x: x["content_length"], reverse=True)
    return res[:limit]


def total_content_size() -> int:
    # TODO: count for the txsize and for the prev tx size
    data = get_data()
    return sum([item["content_length"] for item in data.values()])


if __name__ == "__main__":
    print(biggest_sizes(10))
