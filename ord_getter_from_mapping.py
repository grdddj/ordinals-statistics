import json
import logging
import threading
import time
from pathlib import Path

import requests

HERE = Path(__file__).parent

log_file_path = HERE / "ord_getter.log"
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

no_of_threads = 5

folder = HERE / "ordinals"
MAP_FILE = HERE / "ordinals_stats" / "ord_id_to_tx_id.json"

URL = "https://ordinals.com/inscription/{}i0"

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
)
request_headers = {"User-Agent": user_agent}


def fetch_html(tx_id: str) -> Path:
    url = URL.format(tx_id)
    print("url", url)
    r = requests.get(url, headers=request_headers)

    path = folder / f"{tx_id}.html"
    with open(path, "w") as f:
        f.write(r.text)

    return path


def is_already_there(tx_id: str) -> bool:
    return (folder / f"{tx_id}.html").exists()


logging.info("Starting ord_getter_from_mapping.py")

ALL_TXIDS_TO_GET = []

mapping_content: dict[str, str] = json.loads(MAP_FILE.read_text())

for ord_id, tx_id in mapping_content.items():
    if len(tx_id) == 66 and tx_id.endswith("i0"):
        tx_id = tx_id[:-2]
    assert len(tx_id) == 64
    if not is_already_there(tx_id):
        ALL_TXIDS_TO_GET.append(tx_id)

logging.info(
    f"About to get {len(ALL_TXIDS_TO_GET)} websites from {len(mapping_content)} ordinals"
)

all_ids_iter = iter(ALL_TXIDS_TO_GET)


def get_website():
    while True:
        try:
            tx_id = next(all_ids_iter)
        except StopIteration:
            break

        try:
            fetch_html(tx_id)
        except Exception as e:
            logging.error(f"Error with {tx_id}: {e}")


if __name__ == "__main__":
    for _ in range(no_of_threads):
        new_thread = threading.Thread(target=get_website)
        new_thread.start()
        time.sleep(0.2)
