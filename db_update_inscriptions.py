from sqlalchemy.exc import IntegrityError

from common import OrdinalTx, logging, rpc_connection
from data_db import InscriptionModel
from data_db import get_session as data_db_session
from file_db import ByteData
from file_db import get_session as file_db_session


def fill_new_inscription(id: int, tx_id: str) -> bool:
    inscr = create_new_inscription(id, tx_id)
    if not inscr:
        return False

    data_session = data_db_session()
    try:
        data_session.add(inscr)
        data_session.commit()
    except IntegrityError as e:
        logging.info(f"IntegrityError Data: {tx_id} - {e}")
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
    data_session = file_db_session()
    try:
        new_record = ByteData(id=tx_id, data=inscription.payload)
        data_session.add(new_record)
        data_session.commit()
    except IntegrityError as e:
        logging.info(f"IntegrityError File: {tx_id} - {e}")
        data_session.rollback()
    finally:
        data_session.close()

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
