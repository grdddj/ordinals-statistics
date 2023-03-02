from common import load_stats_json
from data_db import InscriptionModel, get_session


def write_all_ordinal_data() -> None:
    # Go through all .dat files in ORD_DATA_DIR and write them to the database
    # the key is the file_name without .dat and the value is the file contents
    session = get_session()
    counter = 0
    records = []
    stats_dict = load_stats_json()
    for ordinal in stats_dict.values():
        counter += 1
        new_record = InscriptionModel(
            id=ordinal["index"],
            tx_id=ordinal["tx_id"],
            minted_address=ordinal["minted_address"],
            content_type=ordinal["content_type"],
            content_hash=ordinal["content_hash"],
            timestamp=ordinal["timestamp"],
            content_length=ordinal["content_length"],
            genesis_fee=ordinal["genesis_fee"],
            genesis_height=ordinal["genesis_height"],
            output_value=ordinal["output_value"],
            sat_index=ordinal["sat_index"],
        )
        records.append(new_record)
        if counter % 1000 == 0:
            print(counter)
            session.bulk_save_objects(records)
            session.commit()
            records = []

    session.bulk_save_objects(records)
    session.commit()

    session.close()


if __name__ == "__main__":
    write_all_ordinal_data()
