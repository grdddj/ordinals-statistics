from pathlib import Path

from common import rpc_connection

HERE = Path(__file__).parent

timestamp_file = HERE / "timestamps.txt"

conn = rpc_connection()

block_height = conn.getblockcount()
print(f"block_height: {block_height:_}")

timestamps: list[tuple[int, int]] = []
for i in range(0, block_height):
    block_hash = conn.getblockhash(i)
    block = conn.getblock(block_hash)
    timestamp = block["time"]
    timestamps.append((i, timestamp))
    if i % 1000 == 0:
        print(f"i: {i:_}")
        with open(timestamp_file, "a") as f:
            for block, timestamp in timestamps:
                f.write(f"{block} {timestamp}\n")
        timestamps = []

with open(timestamp_file, "a") as f:
    for block, timestamp in timestamps:
        f.write(f"{block} {timestamp}\n")
