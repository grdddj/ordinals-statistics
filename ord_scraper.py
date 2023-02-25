from pathlib import Path

import requests

HERE = Path(__file__).parent

no_of_threads = 5

folder = HERE / "ordinals_stats"
FILE = folder / "chunks.txt"

URL = "https://turbo.ordinalswallet.com/inscriptions?offset={}"

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
)
request_headers = {"User-Agent": user_agent}


def fetch_endpoint(offset: int) -> None:
    r = requests.get(URL.format(offset), headers=request_headers)

    with open(FILE, "a") as f:
        f.write(r.text + "\n")


if __name__ == "__main__":
    for i in range(0, 178000, 100):
        print("i", i)
        fetch_endpoint(i)
