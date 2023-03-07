from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Self

from typing_extensions import TypedDict

from bitcoin.rpc import RawProxy

HERE = Path(__file__).parent

STATS_FOLDER = HERE / "ordinals_stats"
MAPPING_FILE = STATS_FOLDER / "ord_id_to_tx_id.json"
STATS_FILE = STATS_FOLDER / "stats_ordinals_com.json"

OP_RETURN_DATA_DIR = Path("/mnt/bitcoin2/op_return_data")

ORDINALS_COLLECTIONS_DIR = HERE / "ordinals-collections" / "collections"

# ORD_DATA_DIR = Path("/mnt/bitcoin2/ord_data")
ORD_DATA_DIR = HERE / "ordinals"
HASH_FILE = ORD_DATA_DIR / "all_hashes.txt"

MISSING_FILE = HERE / "missing.txt"

BTC_SATOSHI = 100_000_000

log_file_path = HERE / "common.log"
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)


def rpc_connection() -> RawProxy:
    return RawProxy(service_port=8332, btc_conf_file="mainnet.conf")


def load_stats_json() -> dict[str, InscriptionDict]:
    with open(STATS_FILE, "r") as f:
        return json.load(f)


class InscriptionDict(TypedDict):
    """For the stats JSON file"""

    index: int
    tx_id: str
    minted_address: str
    content_type: str
    content_hash: str
    timestamp: str
    content_length: int
    genesis_fee: int
    genesis_height: int
    output_value: int
    sat_index: int


@dataclass
class InscriptionContent:
    content_type: str
    content_hash: str
    content_length: int
    payload: bytes

    # TODO: add the overall size of transaction
    # TODO: add the overall size of parent transaction
    # TODO: add the current owner - or at least whether it was already sent to other address
    # (bcli gettxout tx_id tx_output_index)
    # TODO: add collection name, if any

    def __repr__(self) -> str:
        return f"InscriptionContent(content_type={self.content_type}, content_hash={self.content_hash}, content_length={self.content_length})"


@dataclass
class BasicBlock:
    block_hash: str
    block_height: int
    timestamp: int

    @classmethod
    def from_block_hash(cls, block_hash: str, conn: RawProxy) -> Self:
        block = conn.getblock(block_hash)
        return cls(
            block_hash=block_hash,
            block_height=block["height"],
            timestamp=block["time"],
        )

    @classmethod
    def from_block_height(cls, block_height: int, conn: RawProxy) -> Self:
        block_hash = conn.getblockhash(block_height)
        block = conn.getblock(block_hash)
        return cls(
            block_hash=block_hash,
            block_height=block_height,
            timestamp=block["time"],
        )

    @classmethod
    def from_tx_id(cls, tx_id: str, conn: RawProxy) -> Self:
        raw_tx = conn.getrawtransaction(tx_id, True)
        block_hash = raw_tx["blockhash"]
        return cls.from_block_hash(block_hash, conn)

    def datetime(self) -> str:
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class Input:
    d: dict

    def __repr__(self) -> str:
        return f"Input(tx_id={self.tx_id}, vout={self.vout})"

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return cls(d)

    @property
    def tx_id(self) -> str:
        return self.d["txid"]

    @property
    def vout(self) -> int:
        return self.d["vout"]

    @property
    def txinwitness(self) -> list[str]:
        return self.d["txinwitness"]

    def value(self, conn: RawProxy) -> int:
        prev_tx = Tx.from_tx_id(self.tx_id, conn)
        return prev_tx.vout[self.vout].value


@dataclass
class Output:
    d: dict

    def __repr__(self) -> str:
        return f"Output(address={self.address}, value={self.value})"

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        return cls(d)

    @property
    def address(self) -> str:
        return self.d.get("scriptPubKey", {}).get("address", "")

    @property
    def value(self) -> int:
        return int(BTC_SATOSHI * self.d["value"])


@dataclass
class Tx:
    tx_id: str
    block: BasicBlock
    vin: list[Input]
    vout: list[Output]

    @classmethod
    def from_tx_id(cls, tx_id: str, conn: RawProxy) -> Self:
        raw_tx = conn.getrawtransaction(tx_id)
        tx = conn.decoderawtransaction(raw_tx)
        return cls(
            tx_id=tx_id,
            block=BasicBlock.from_tx_id(tx_id, conn),
            vin=[Input.from_dict(vin) for vin in tx["vin"]],
            vout=[Output.from_dict(vout) for vout in tx["vout"]],
        )

    def fee(self, conn: RawProxy) -> int:
        return self.total_input(conn) - self.total_output()

    def total_input(self, conn: RawProxy) -> int:
        total_input = 0
        for vin in self.vin:
            input_tx = Tx.from_tx_id(vin.tx_id, conn)
            total_input += input_tx.vout[vin.vout].value
        return total_input

    def total_output(self) -> int:
        return sum([vout.value for vout in self.vout])


@dataclass
class OrdinalTx(Tx):
    def get_inscription(self, conn: RawProxy) -> InscriptionContent | None:
        try:
            witness_script = self.vin[0].txinwitness[1]

            decoded_script = conn.decodescript(witness_script)["asm"]

            script_parts = decoded_script.split(" ")

            assert len(script_parts[0]) == 64, "first part is not 64"
            assert script_parts[-1] == "OP_ENDIF", "no OP_ENDIF"
            assert script_parts[1] == "OP_CHECKSIG", "no OP_CHECKSIG"
            while script_parts[2] != "0" and script_parts[3] != "OP_IF":
                # There could be some additional things, like
                # ['756e69736174', 'aeb98c9e8601', 'OP_2DROP']
                script_parts.pop(2)
            assert script_parts[2] == "0", "no 2"
            assert script_parts[3] == "OP_IF", "no OP_IF"
            assert script_parts[4] == "6582895", "no 6582895"
            assert script_parts[5] == "1", "no 5"

            content_type = script_parts[6]
            content_type_ascii = bytes.fromhex(content_type).decode("ascii")
            assert script_parts[7] == "0", "no 7"

            # cleanup
            if script_parts[-2] == "-2":
                # pop this one
                script_parts.pop(-2)

            data_parts = script_parts[8:-1]
            hex_data = "".join(data_parts)

            content_length = len(hex_data) // 2

            try:
                payload = bytes.fromhex(hex_data)
            except ValueError:
                first_index = len(witness_script) - (content_length * 2) - 2
                data = witness_script[first_index:-2]
                payload = bytes.fromhex(data)

            return InscriptionContent(
                content_length=content_length,
                content_type=content_type_ascii,
                content_hash=hashlib.md5(payload).hexdigest(),
                payload=payload,
            )
        except AssertionError as e:
            logging.error(f"AssertionError {self.tx_id} : {e}")
            return None
        except Exception as e:
            logging.error(f"Exception {self.tx_id} : {e}")
            return None
