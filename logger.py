import logging
from pathlib import Path

HERE = Path(__file__).parent

log_file_path = HERE / "common.log"
logging.basicConfig(
    filename=log_file_path,
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)
