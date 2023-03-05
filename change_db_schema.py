import sqlite3

db_file = "/mnt/bitcoin2/ord_data/ord_data.db"

conn = sqlite3.connect(db_file)

# Define the SQL script to add the column
sql_script = """
ALTER TABLE inscriptions
ADD COLUMN unix_timestamp INTEGER NOT NULL DEFAULT 0;
"""
sql_script = """
ALTER TABLE inscriptions
RENAME COLUMN timestamp TO datetime;
"""
sql_script = """
ALTER TABLE inscriptions
RENAME COLUMN unix_timestamp TO timestamp;
"""
sql_script = """
ALTER TABLE inscriptions
ADD COLUMN name_from_collection TEXT;
"""
sql_script = """
ALTER TABLE inscriptions
ADD COLUMN collection_id TEXT REFERENCES inscriptions_collections(name);
"""
sql_script = "DROP TABLE IF EXISTS alembic_version;"
sql_script = "DROP TABLE IF EXISTS inscriptions_collections;"

# Execute the SQL script
with conn:
    conn.execute(sql_script)

# Close the database connection
conn.close()
