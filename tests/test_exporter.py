from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure src/ is importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from scraper.exporter import DataExporter  # noqa: E402


def test_exporter_writes_json_and_csv(tmp_path: Path):
    items = [
        {
            "product_id": "A1",
            "product_name": "Item 1",
            "price": "$10.00",
            "availability": "In Stock",
        },
        {
            "product_id": "A2",
            "product_name": "Item 2",
            "price": "$20.00",
            "availability": "Out of Stock",
        },
    ]

    exporter = DataExporter(output_dir=tmp_path)
    json_path = exporter.to_json(items)
    csv_path = exporter.to_csv(items)

    assert json_path.exists()
    assert csv_path.exists()

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert len(data) == 2
    assert data[0]["product_id"] == "A1"

    csv_content = csv_path.read_text(encoding="utf-8").strip().splitlines()
    # header + 2 rows
    assert len(csv_content) == 3
