from file_db import ByteData, get_session

session = get_session()

# Define a query to retrieve all records from the byte_data table
query = session.query(ByteData)

# Execute the query and retrieve all records
records = query.all()

# Loop through the records and print the data
for record in records:
    print(record.id, record.data)
