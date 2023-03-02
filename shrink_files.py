from pathlib import Path

DATA_DIR = Path("/mnt/bitcoin2/trial")

hash_files = DATA_DIR.glob("*.data")


def shrink_file(file: Path) -> None:
    file_size = file.stat().st_size
    print("file_size", file_size)
    with open(file, "r+") as f:
        f.seek(file_size)
        f.truncate()
    # with open(file, "w") as f:
    #     f.write(data[:100])


file = DATA_DIR / "ffff.dat"
shrink_file(file)

# for file in hash_files:
#     shrink_file(file)
