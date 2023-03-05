import json
from pathlib import Path

from ord_getter_from_mapping import fetch_html
from ord_stats import InscriptionDict
from ord_stats_getter import parse_data

HERE = Path(__file__).parent

STATS_FILE = HERE / "ordinals_stats" / "stats_fixes2.json"
FIXED_FILE = HERE / "ordinals_stats" / "stats_fixes3.json"

MISSING_FILE = HERE / "missing.txt"

missing_ords: list[tuple[int, str]] = []

with open(MISSING_FILE, "r") as f:
    for line in f:
        split_line = line.split(" : ")
        missing_ords.append((int(split_line[0].strip()), split_line[1].strip()))

# import webbrowser
# url_template = "https://ordinalswallet.com/inscription/{}i0"
# for ord_id, tx_id in missing_ords[:5]:
#     url = url_template.format(tx_id)
#     webbrowser.open(url, new=0, autoraise=True)
# 1/0

FIXED: dict[int, InscriptionDict] = {}

failed: list[str] = []

for ord_id, tx_id in missing_ords:
    print("ord_id, tx_id", ord_id, tx_id)
    try:
        path = fetch_html(tx_id)
        print("path", path)
        inscription = parse_data(path)
        FIXED[ord_id] = inscription
    except Exception as e:
        print(e)
        failed.append(tx_id)

print("failed", failed)

with open(STATS_FILE, "r") as f:
    ORDINALS: dict[str, InscriptionDict] = json.load(f)

for ord_id, inscription in ORDINALS.items():
    FIXED[int(ord_id)] = inscription

with open(FIXED_FILE, "w") as f:
    json.dump(FIXED, f, indent=4, sort_keys=True)
