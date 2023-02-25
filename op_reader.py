from pathlib import Path

files = Path(".").glob("op_return_*.txt")

prefixes = [
    "CC",
    "OUT:",
    "=:BNB.BNB:",
    "=:ETH.ETH:",
    "REFUND:",
    "ADD:BTC",
    "SWAPTX:",
    "MIGRATE:",
    "YGGDRASIL-:",
    "SWAP:",
    "Procertif:",
    "nip5:Tzikin:",
    "BERNSTEIN 2.0 REG",
    "ion:",
    "DC-L5:",
    "omni",
]

whole_words = [
    "bumpfee",
    "consolidate",
    "aggregate",
    "Bitzlato",
    "Samaneh067",
]


def should_ignore(val: str) -> bool:
    for prefix in prefixes:
        if val.startswith(prefix):
            return True

    for word in whole_words:
        if val == word:
            return True

    if val[1] == ":" or val.endswith(":0"):
        return True

    # dfab5e1b90ed151dbc214356ec33fdf9181ef59613a46de0d0ced9800844c8b0
    if len(val) == 64:
        try:
            int(val, 16)
            return True
        except:
            pass

    # 0xdfab5e1b90ed151dbc214356ec33fdf9181ef59613a46de0d0ced9800844c8b0
    if len(val) == 66 and val.startswith("0x"):
        try:
            int(val[2:], 16)
            return True
        except:
            pass

    # 1xhoGPb8eqfd2ZtKxwJjsBtUu1F23FUSUmeDFcV
    if val[0].isdigit() and 38 <= len(val) <= 42 and " " not in val:
        return True

    # 0x70Ea4A37F26f3763555b32b5E3b6E7c50cbA13D2:1
    if val.startswith("0x") and " " not in val:
        return True

    return False


texts = []

for file in files:
    for line in file.open():
        if "OP_RETURN" in line:
            value = line.split("OP_RETURN")[1].strip()
            try:
                val = bytes.fromhex(value).decode("utf-8")
                if should_ignore(val):
                    # raise Exception("ignore")
                    # print(val)
                    continue
                else:
                    pass
                    texts.append(val)
                    # print(val)
            except:
                # print("value", value)
                pass


with open("op_return.txt", "w", encoding="utf8") as f:
    for text in sorted(texts):
        f.write(text + "\n")
