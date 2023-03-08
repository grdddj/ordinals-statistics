import requests

URL = "https://turbo.ordinalswallet.com/inscriptions?offset={}"

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
)
request_headers = {"User-Agent": user_agent}


def get_last_ordinal_index() -> int:
    offset = 0
    r = requests.get(URL.format(offset), headers=request_headers)
    data = r.json()
    max_num = 0
    for item in data:
        max_num = max(max_num, item["num"])
    return max_num


def get_specific_indexes(indexes: list[int]) -> dict[int, str]:
    last_index = get_last_ordinal_index()
    result: dict[int, str] = {}

    # get all offsets
    all_offsets = set()
    for index in indexes:
        offset = last_index - index
        # bring it down to the whole hundred
        offset = offset - (offset % 100)
        all_offsets.add(offset)

    # fetch all offsets
    index_set = set(indexes)
    for offset in all_offsets:
        r = requests.get(URL.format(offset), headers=request_headers)
        data = r.json()
        for item in data:
            num = item["num"]
            if num in index_set:
                tx_id = item["id"]
                if len(tx_id) == 66 and tx_id.endswith("i0"):
                    tx_id = tx_id[:-2]
                result[num] = tx_id

    return result
