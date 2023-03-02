import json

from common import MAPPING_FILE, STATS_FOLDER

chunks_file = STATS_FOLDER / "chunks.txt"

mapping: dict[int, str] = {}

with open(chunks_file, "r") as f:
    for line in f:
        data = json.loads(line)
        for item in data:
            tx_id = item["id"]
            if len(tx_id) == 66 and tx_id.endswith("i0"):
                tx_id = tx_id[:-2]
            mapping[item["num"]] = tx_id

with open(MAPPING_FILE, "w") as f:
    json.dump(mapping, f, indent=4, sort_keys=True)
