import json
import sys

from sqlalchemy.exc import IntegrityError

from common import MAPPING_FILE, OrdinalTx, rpc_connection
from db_data import InscriptionModel
from db_data import get_session as db_data_session
from db_files import ByteData
from db_files import get_session as file_db_session
from logger import logging


def fill_new_inscription(id: int, tx_id: str) -> bool:
    inscr = create_new_inscription(id, tx_id)
    if not inscr:
        return False

    data_session = db_data_session()
    try:
        data_session.add(inscr)
        data_session.commit()
    except IntegrityError as e:
        logging.error(f"IntegrityError Data: {tx_id} - {e}")
        data_session.rollback()
        return False
    finally:
        data_session.close()

    return True


def create_new_inscription(id: int, tx_id: str) -> InscriptionModel | None:
    conn = rpc_connection()
    tx = OrdinalTx.from_tx_id(tx_id, conn)

    inscription = tx.get_inscription(conn)

    if not inscription:
        return None

    tx_fee = tx.fee(conn)
    output_value = tx.vout[0].value
    minted_address = tx.vout[0].address

    # Save payload to db
    file_session = file_db_session()
    try:
        new_record = ByteData(id=tx_id, data=inscription.payload)
        file_session.add(new_record)
        file_session.commit()
    except IntegrityError as e:
        logging.error(f"IntegrityError File: {tx_id} - {e}")
        file_session.rollback()
    finally:
        file_session.close()

    return InscriptionModel(
        id=id,
        tx_id=tx_id,
        minted_address=minted_address,
        content_type=inscription.content_type,
        content_length=inscription.content_length,
        content_hash=inscription.content_hash,
        timestamp=tx.block.timestamp,
        datetime=tx.block.datetime(),
        genesis_fee=tx_fee,
        genesis_height=tx.block.block_height,
        output_value=output_value,
        sat_index=0,
    )


def fill_all_missing_inscriptions() -> None:
    with open(MAPPING_FILE, "r") as f:
        str_mapping: dict[str, str] = json.load(f)

    mapping = {int(k): v for k, v in str_mapping.items()}

    session = db_data_session()

    all_ord_ids_from_db = set(el[0] for el in session.query(InscriptionModel.id).all())

    missing_ord_ids = set(mapping.keys()) - all_ord_ids_from_db

    logging.info(f"There are {len(missing_ord_ids)} missing ord IDs")

    failed_to_add: list[str] = []
    for ord_id in missing_ord_ids:
        if ord_id not in mapping:
            logging.error(f"ERROR: {ord_id} not in mapping")
            continue
        tx_id = mapping[ord_id]
        res = fill_new_inscription(ord_id, tx_id)
        if res:
            logging.info(f"Ordinal {ord_id} added")
        else:
            logging.warning(f"Failed to add {ord_id} - {tx_id}")
            failed_to_add.append(ord_id)

    logging.info(failed_to_add)
    logging.info(f"Unable to add {len(failed_to_add)}")


if __name__ == "__main__":
    logging.info("started fill_all_missing_inscriptions")
    try:
        fill_all_missing_inscriptions()
    except Exception as e:
        logging.exception(f"Unexpected error in fill_all_missing_inscriptions - {e}")
        print("ERROR")
        sys.exit(1)
    logging.info("ending fill_all_missing_inscriptions")
