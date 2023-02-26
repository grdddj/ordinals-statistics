import json
from pathlib import Path

from ord_stats import Inscription

HERE = Path(__file__).parent

MAPPING_FILE = HERE / "ordinals_stats" / "ord_id_to_tx_id.json"
STATS_FILE = HERE / "ordinals_stats" / "stats_fixes3.json"

with open(STATS_FILE, "r") as f:
    ORDINALS: dict[str, Inscription] = json.load(f)

with open(MAPPING_FILE, "r") as f:
    MAPPING: dict[str, str] = json.load(f)

amount = len(ORDINALS)

missing: list[tuple[str, str]] = []

for i in range(1, amount + 1):
    if str(i) not in ORDINALS:
        print(f"Missing {i} : {MAPPING[str(i)]}")
        missing.append((str(i), MAPPING[str(i)]))

with open(HERE / "missing.txt", "w") as f:
    for item in missing:
        f.write(f"{item[0]} : {item[1]}" + "\n")
