import json

from common import MAPPING_FILE
from ord_scraper import get_last_ordinal_index, get_specific_indexes


def fill_whatever_is_missing() -> None:
    with open(MAPPING_FILE, "r") as f:
        str_mapping: dict[str, str] = json.load(f)

    mapping = {int(k): v for k, v in str_mapping.items()}

    # max_num = max(mapping.keys())
    max_num = get_last_ordinal_index()
    print("max_num", max_num)

    missing: list[int] = []
    for i in range(max_num + 1):
        # one ID - 169689 - is not available
        if i not in mapping and i != 169689:
            missing.append(i)

    # print("missing", missing)
    print("missing", len(missing))

    if not missing:
        return

    new_data = get_specific_indexes(missing)
    print("new_data", len(new_data))

    if not new_data:
        return

    mapping.update(new_data)

    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    fill_whatever_is_missing()
