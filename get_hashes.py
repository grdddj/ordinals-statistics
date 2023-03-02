import hashlib

from common import ORD_DATA_DIR


def find_hashes() -> None:
    hashes: dict[str, str] = {}
    for file in ORD_DATA_DIR.iterdir():
        if file.suffix == ".dat":
            byte_data = file.read_bytes()
            hash = hashlib.md5(byte_data).hexdigest()
            hashes[file.stem] = hash

    with open("all_hashes.txt", "w") as f:
        for key, value in hashes.items():
            f.write(f"{key} :{value}" + "\n")


if __name__ == "__main__":
    find_hashes()
