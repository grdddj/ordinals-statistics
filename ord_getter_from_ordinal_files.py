import threading
import time
from pathlib import Path

import requests

HERE = Path(__file__).parent

no_of_threads = 5

folder = HERE / "ordinals"

files = HERE.glob("ordinal*.txt")

URL = "https://ordinals.com/inscription/{}i0"

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
)
request_headers = {"User-Agent": user_agent}


def fetch_html(tx_id: str) -> None:
    r = requests.get(URL.format(tx_id), headers=request_headers)

    with open(folder / f"{tx_id}.html", "w") as f:
        f.write(r.text)


def is_already_there(tx_id: str) -> bool:
    return (folder / f"{tx_id}.html").exists()


all_tx_ids: list[list[str]] = []

for file in files:
    file_ids = []
    for line in file.open():
        if "----------" in line:
            continue
        tx_id = line.strip()
        if not is_already_there(tx_id):
            file_ids.append(tx_id)
    all_tx_ids.append(file_ids)


ALL_TXIDS = []

longest = len(max(all_tx_ids, key=len))
for i in range(longest):
    for tx_ids in all_tx_ids:
        try:
            ALL_TXIDS.append(tx_ids[i])
        except IndexError:
            pass

all_ids_iter = iter(ALL_TXIDS)


def get_website():
    while True:
        try:
            tx_id = next(all_ids_iter)
            fetch_html(tx_id)
        except StopIteration:
            break


if __name__ == "__main__":
    for _ in range(no_of_threads):
        new_thread = threading.Thread(target=get_website)
        new_thread.start()
        time.sleep(0.2)
