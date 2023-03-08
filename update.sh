set -e

cd "$(dirname "$0")"

python3.11 ord_mapping_update.py
python3.11 db_update.py
python3.11 html_report.py
bash deploy.sh