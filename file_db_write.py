from common import ORD_DATA_DIR
from file_db import ByteData, get_session


def trial_write() -> None:
    session = get_session()

    # Define the byte data to be stored
    byte_data = b"This is a test byte data"

    # Create a new record for the byte data in the database
    new_record = ByteData(id="test", data=byte_data)
    session.add(new_record)
    session.commit()

    # Close the session
    session.close()


def write_all_ordinal_data() -> None:
    # Go through all .dat files in ORD_DATA_DIR and write them to the database
    # the key is the file_name without .dat and the value is the file contents
    session = get_session()
    counter = 0
    records = []
    for file in ORD_DATA_DIR.iterdir():
        counter += 1
        if file.suffix == ".dat":
            byte_data = file.read_bytes()
            new_record = ByteData(id=file.stem, data=byte_data)
            records.append(new_record)
        if counter % 100 == 0:
            print(counter)
            session.bulk_save_objects(records)
            session.commit()
            records = []

    session.bulk_save_objects(records)
    session.commit()

    session.close()


if __name__ == "__main__":
    # trial_write()
    write_all_ordinal_data()
