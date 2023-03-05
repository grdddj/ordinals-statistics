import json

from common import STATS_FILE, STATS_FOLDER, InscriptionDict

FIXED_FILE = STATS_FOLDER / "stats_fixes2.json"

HASH_FILE = STATS_FOLDER / "all_hashes.txt"

FIXED: dict[int, InscriptionDict] = {}

with open(STATS_FILE, "r") as f:
    ORDINALS: dict[str, InscriptionDict] = json.load(f)

with open(HASH_FILE, "r") as f:
    HASHES: dict[str, str] = {}
    for line in f:
        line = line.strip()
        tx_id, hash = line.split(" :")
        HASHES[tx_id] = hash


# for ord_id, inscription in ORDINALS.items():
#     inscription.pop("link_memspace", None)  # type: ignore
#     inscription.pop("link_ordinals", None)  # type: ignore
#     FIXED[int(ord_id)] = inscription

for ord_id, inscription in ORDINALS.items():
    tx_id = inscription["tx_id"]
    inscription["content_hash"] = HASHES.get(tx_id, "")
    FIXED[int(ord_id)] = inscription


with open(FIXED_FILE, "w") as f:
    json.dump(FIXED, f, indent=4, sort_keys=True)


# STATS_FILE = STATS_FOLDER / "stats.json"
# FIXED_FILE = STATS_FOLDER / "stats_fixes.json"

# FIXED: dict[str, Inscription] = {}

# with open(STATS_FILE, "r") as f:
#     ORDINALS: dict[str, Inscription] = json.load(f)

# for ord_id, inscription in ORDINALS.items():
#     if len(ord_id) < 7:
#         FIXED[ord_id] = inscription
#     else:
#         ord_id = str(inscription["index"])
#         FIXED[ord_id] = inscription

# with open(FIXED_FILE, "w") as f:
#     json.dump(FIXED, f, indent=4, sort_keys=True)
