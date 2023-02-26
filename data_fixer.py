import json
from pathlib import Path
from typing import Any

from ord_stats import Inscription

HERE = Path(__file__).parent

STATS_FILE = HERE / "ordinals_stats" / "stats_fixes.json"
FIXED_FILE = HERE / "ordinals_stats" / "stats_fixes2.json"

FIXED: dict[int, Inscription] = {}

with open(STATS_FILE, "r") as f:
    ORDINALS: dict[str, Inscription] = json.load(f)

with open(FIXED_FILE, "w") as f:
    json.dump(FIXED, f, indent=4, sort_keys=True)


for ord_id, inscription in ORDINALS.items():
    inscription.pop("link_memspace", None)  # type: ignore
    inscription.pop("link_ordinals", None)  # type: ignore
    FIXED[int(ord_id)] = inscription

with open(FIXED_FILE, "w") as f:
    json.dump(FIXED, f, indent=4, sort_keys=True)


# STATS_FILE = HERE / "ordinals_stats" / "stats.json"
# FIXED_FILE = HERE / "ordinals_stats" / "stats_fixes.json"

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
