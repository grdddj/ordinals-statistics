from __future__ import annotations

import json
from collections import defaultdict

from common import STATS_FILE, InscriptionDict


def get_data() -> dict[str, InscriptionDict]:
    return json.loads(STATS_FILE.read_text())


def content_types() -> dict[str, int]:
    data = get_data()
    content_types: dict[str, int] = defaultdict(int)
    for item in data.values():
        content_types[item["content_type"]] += 1
    return content_types


def biggest_sizes(limit: int) -> list[InscriptionDict]:
    data = get_data()
    res = sorted(data.values(), key=lambda x: x["content_length"], reverse=True)
    return res[:limit]


def total_content_size() -> int:
    # TODO: count for the txsize and for the prev tx size
    data = get_data()
    return sum([item["content_length"] for item in data.values()])


if __name__ == "__main__":
    # print(biggest_sizes(10))
    # print(total_content_size())

    types = content_types()
    for k, v in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"{k}: {v}")
