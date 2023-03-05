import sqlite3

db_file = "/mnt/bitcoin2/ord_data/ord_data.db"

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

table_name = "inscriptions"
table_name = "inscriptions_collections"

query = f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';"
cursor.execute(query)

result = cursor.fetchone()
print(result[0])

conn.close()
