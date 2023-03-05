import json
import logging
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from ord_stats import STATS_FILE, InscriptionDict

HERE = Path(__file__).parent

log_file_path = HERE / "stats.log"
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

HERE = Path(__file__).parent

html_file_foler = HERE / "ordinals"


def parse_data(file: Path) -> InscriptionDict:
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

    # create a dict - loop through keys_and_values, first item is key, second is value, etc.
    # then use the dict to create the Inscription object
    kv_dict = {}
    for i in range(0, len(keys_and_values), 2):
        kv_dict[keys_and_values[i]] = keys_and_values[i + 1]

    return InscriptionDict(
        index=index_num,
        tx_id=tx_id,
        minted_address=kv_dict.get("address", ""),
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

    already_have = set()
    if STATS_FILE.exists():
        with open(STATS_FILE, "r") as f:
            ORDINALS: dict[str, InscriptionDict] = json.load(f)
            for val in ORDINALS.values():
                already_have.add(val["tx_id"])
    else:
        ORDINALS = {}

    logging.info(f"Already have {len(already_have)}")

    files = html_file_foler.glob("*.html")
    for file in files:
        total += 1
        file_size = file.stat().st_size
        if file_size < 500:
            negatives += 1
        else:
            tx_id = file.stem
            if tx_id not in already_have:
                try:
                    data = parse_data(file)
                    ORDINALS[str(data["index"])] = data
                except Exception as e:
                    logging.error(f"error with {file} - {e}")

        if total % 1000 == 0:
            logging.info(f"total: {total}")
            logging.info(f"negatives: {negatives}")

    with open(STATS_FILE, "w") as f:
        json.dump(ORDINALS, f, indent=4, sort_keys=True)

    print("total", total)
    print("negatives", negatives)


if __name__ == "__main__":
    trial = len(sys.argv) > 1

    if trial:
        data = parse_data(HERE / "trial.html")
        print("data", data)
    else:
        analyze()
        logging.info("finished")
