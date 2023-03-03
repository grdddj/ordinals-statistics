import json
from pathlib import Path

HERE = Path(__file__).parent

timestamp_file = HERE / "block_timestamps.json"


def block_height_at_timestamp(timestamp: int) -> int:
    with open(timestamp_file, "r") as f:
        data = json.load(f)
    for block, block_timestamp in data:
        if block_timestamp > timestamp:
            return block - 1
    return 0
