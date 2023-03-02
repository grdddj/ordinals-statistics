from common import HASH_FILE, ORD_DATA_DIR

hashes: dict[str, str] = {}

for file in ORD_DATA_DIR.glob("*.hash"):
    with open(file, "r") as f:
        hashes[file.stem] = f.read().strip()

with open(HASH_FILE, "w") as f:
    for tx_id, hash in hashes.items():
        f.write(f"{tx_id} : {hash}" + "\n")
