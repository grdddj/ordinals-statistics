from pathlib import Path

HERE = Path(__file__).parent

folder = HERE / "ordinals"

files = folder.glob("*.html")

total = 0
negatives = 0

for file in files:
    total += 1
    file_size = file.stat().st_size
    if file_size < 500:
        negatives += 1
print("total", total)
print("negatives", negatives)