import json

from common import MAPPING_FILE
from data_db import InscriptionModel, get_session
from db_update_inscriptions import fill_new_inscription
from logger import logging


def fill_all_missing_inscriptions() -> None:
    logging.info("fill_all_missing_inscriptions started")
    with open(MAPPING_FILE, "r") as f:
        MAPPING: dict[str, str] = json.load(f)

    session = get_session()

    all_ord_ids_from_db = set(el[0] for el in session.query(InscriptionModel.id).all())

    missing_ord_ids = set(int(key) for key in MAPPING.keys()) - all_ord_ids_from_db

    logging.info(f"There are {len(missing_ord_ids)} missing ord IDs")

    failed_to_add: list[str] = []
    for ord_id in missing_ord_ids:
        if ord_id not in MAPPING:
            logging.error(f"ERROR: {ord_id} not in MAPPING")
            continue
        tx_id = MAPPING[ord_id]
        res = fill_new_inscription(ord_id, tx_id)
        if res:
            logging.info(f"Ordinal {ord_id} added")
        else:
            logging.warning(f"Failed to add {ord_id} - {tx_id}")
            failed_to_add.append(ord_id)

    logging.info(failed_to_add)
    logging.info(f"Unable to add {len(failed_to_add)}")
    logging.info("fill_all_missing_inscriptions started")


if __name__ == "__main__":
    fill_all_missing_inscriptions()
