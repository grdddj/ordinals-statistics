import json
import logging
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

HERE = Path(__file__).parent

log_file_path = HERE / "stats.log"
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)


@dataclass
class Inscription:
    tx_id: str
    link_ordinals: str
    link_memspace: str
    address: str
    index: int
    content_type: str
    timestamp: str
    content_length: int
    genesis_fee: int
    genesis_height: int
    output_value: int
    sat_index: int


HERE = Path(__file__).parent

folder = HERE / "ordinals"
stats = HERE / "ordinals_stats"

STAT_FILE = stats / "stats.json"


def parse_data(file: Path) -> Inscription:
    html_content = file.read_text()
    soup = BeautifulSoup(html_content, "html.parser")

    inscription_index = soup.findAll("h1")[0].text
    index_num = int(inscription_index.split(" ")[1])
    tx_id = file.stem

    keys_and_values: list[str] = []
    for i in soup.find("dl"):  # type: ignore
        content = i.text.strip()  # type: ignore
        if content:
            keys_and_values.append(content)

    # creat a dict - loop through keys_and_values, first item is key, second is value, etc.
    # then use the dict to create the Inscription object
    kv_dict = {}
    for i in range(0, len(keys_and_values), 2):
        kv_dict[keys_and_values[i]] = keys_and_values[i + 1]

    return Inscription(
        tx_id=tx_id,
        link_ordinals=f"https://ordinals.com/inscription/{tx_id}i0",
        link_memspace=f"https://mempool.space/tx/{tx_id}",
        address=kv_dict.get("address", ""),
        index=index_num,
        timestamp=kv_dict.get("timestamp", ""),
        content_type=kv_dict.get("content type", ""),
        content_length=int(kv_dict.get("content length", "0").split(" ")[0]),
        genesis_fee=int(kv_dict.get("genesis fee", "0")),
        genesis_height=int(kv_dict.get("genesis height", "0")),
        output_value=int(kv_dict.get("output value", "0")),
        sat_index=int(kv_dict.get("sat", "0")),
    )


def analyze() -> None:
    total = 0
    negatives = 0

    ORDINALS: dict[int, dict[Any, Any]] = {}

    files = folder.glob("*.html")
    for file in files:
        total += 1
        file_size = file.stat().st_size
        if file_size < 500:
            negatives += 1
        else:
            # pass
            data = parse_data(file)
            ORDINALS[data.index] = asdict(data)

        if total % 100 == 0:
            logging.info(f"total: {total}")
            logging.info(f"negatives: {negatives}")

    with open(STAT_FILE, "w") as stats:
        json.dump(ORDINALS, stats, indent=4, sort_keys=True)

    print("total", total)
    print("negatives", negatives)


if __name__ == "__main__":
    trial = len(sys.argv) > 1

    if trial:
        data = parse_data(HERE / "trial.html")
        print("data", data)
    else:
        analyze()
