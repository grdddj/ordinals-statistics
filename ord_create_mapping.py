import json

from common import MAPPING_FILE, STATS_FOLDER

chunks_file = STATS_FOLDER / "chunks.txt"


def get_new_data() -> dict[int, str]:
    new_data: dict[int, str] = {}
    with open(chunks_file, "r") as f:
        for line in f:
            data = json.loads(line)
            for item in data:
                tx_id = item["id"]
                if len(tx_id) == 66 and tx_id.endswith("i0"):
                    tx_id = tx_id[:-2]
                new_data[item["num"]] = tx_id
    return new_data


if __name__ == "__main__":
    with open(MAPPING_FILE, "r") as f:
        str_mapping: dict[str, str] = json.load(f)

    mapping = {int(k): v for k, v in str_mapping.items()}

    new_data = get_new_data()
    mapping.update(new_data)

    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=4, sort_keys=True)
