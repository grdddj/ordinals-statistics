import json
from pathlib import Path

HERE = Path(__file__).parent

no_of_threads = 5

folder = HERE / "ordinals_stats"
chunks_file = folder / "chunks.txt"
MAPPING_FILE = folder / "ord_id_to_tx_id.json"

mapping: dict[int, str] = {}

with open(chunks_file, "r") as f:
    for line in f:
        data = json.loads(line)
        for item in data:
            mapping[item["num"]] = item["id"]
        # break

with open(MAPPING_FILE, "w") as f:
    json.dump(mapping, f, indent=4, sort_keys=True)
