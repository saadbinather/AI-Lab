"""Extract saved PNG outputs from notebooks into assets/generated.

This utility uses only outputs already stored in the notebooks; it does not
invent metrics or rerun experiments requiring external datasets.
"""
from pathlib import Path
import base64
import json
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)

for old in OUT.glob("*.png"):
    old.unlink()

count = 0
for notebook in sorted((ROOT / "notebooks").rglob("*.ipynb")):
    slug = re.sub(r"[^a-z0-9]+", "_", notebook.stem.lower()).strip("_")
    data = json.loads(notebook.read_text(encoding="utf-8"))
    index = 0
    for cell in data.get("cells", []):
        for output in cell.get("outputs", []):
            image = output.get("data", {}).get("image/png")
            if not image:
                continue
            if isinstance(image, list):
                image = "".join(image)
            target = OUT / f"{slug}_output_{index:02d}.png"
            target.write_bytes(base64.b64decode(image))
            index += 1
            count += 1
print(f"Extracted {count} saved PNG outputs into {OUT.relative_to(ROOT)}")
