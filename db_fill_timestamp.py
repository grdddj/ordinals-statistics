from datetime import datetime
from data_db import get_session, InscriptionModel

# Get a session object
session = get_session()

# Define a function to convert a datetime string to a Unix timestamp
def datetime_to_timestamp(dt_str: str) -> int:
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S %Z")
    return int(dt.timestamp())


for entry in session.query(InscriptionModel):
    entry.timestamp = datetime_to_timestamp(entry.datetime)

# Commit the changes to the database
session.commit()

# Close the session
session.close()