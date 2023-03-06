import json

from common import MAPPING_FILE
from data_db import InscriptionModel, get_session
from db_update_inscriptions import fill_new_inscription


def fill_all_missing_inscriptions() -> None:
    with open(MAPPING_FILE, "r") as f:
        MAPPING: dict[str, str] = json.load(f)

    session = get_session()

    for ord_id, tx_id in MAPPING.items():
        ord_id = int(ord_id)
        if session.get(InscriptionModel, ord_id) is None:
            print(f"Ordinal {ord_id} not found")
            fill_new_inscription(ord_id, tx_id)


if __name__ == "__main__":
    fill_all_missing_inscriptions()
