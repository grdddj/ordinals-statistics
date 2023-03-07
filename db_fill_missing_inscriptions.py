import json

from common import MAPPING_FILE
from data_db import InscriptionModel, get_session
from db_update_inscriptions import fill_new_inscription


def fill_all_missing_inscriptions() -> None:
    with open(MAPPING_FILE, "r") as f:
        MAPPING: dict[str, str] = json.load(f)

    session = get_session()

    all_ord_ids_from_db = set(session.query(InscriptionModel.id).all())

    for ord_id, tx_id in reversed(MAPPING.items()):
        ord_id = int(ord_id)
        if ord_id not in all_ord_ids_from_db:
            res = fill_new_inscription(ord_id, tx_id)
            if res:
                print(f"Ordinal {ord_id} added")
            else:
                print(f"Failed to add {ord_id} - {tx_id}")


if __name__ == "__main__":
    fill_all_missing_inscriptions()
