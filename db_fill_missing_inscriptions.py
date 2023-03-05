import json

from common import MAPPING_FILE
from data_db import InscriptionModel, get_session
from db_update_inscriptions import fill_new_inscription

with open(MAPPING_FILE, "r") as f:
    MAPPING = json.load(f)

session = get_session()

missing: list[int] = []
for key, value in MAPPING.items():
    if session.get(InscriptionModel, int(key)) is None:
        print(f"Ordinal {key} not found")
        missing.append(int(key))

print(f"Missing: {missing}")

for miss in missing:
    fill_new_inscription(miss, MAPPING[str(miss)])
