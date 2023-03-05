import json

from common import MAPPING_FILE, MISSING_FILE, STATS_FILE, InscriptionDict

with open(STATS_FILE, "r") as f:
    ORDINALS: dict[str, InscriptionDict] = json.load(f)

with open(MAPPING_FILE, "r") as f:
    MAPPING: dict[str, str] = json.load(f)

amount = len(ORDINALS)

missing: list[tuple[str, str]] = []

for i in range(1, amount + 1):
    if str(i) not in ORDINALS:
        print(f"Missing {i} : {MAPPING[str(i)]}")
        missing.append((str(i), MAPPING[str(i)]))

with open(MISSING_FILE, "w") as f:
    for item in missing:
        f.write(f"{item[0]} : {item[1]}" + "\n")
