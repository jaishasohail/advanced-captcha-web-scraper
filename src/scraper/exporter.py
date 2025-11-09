from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, List, Dict

from utils.logger import get_logger

logger = get_logger(__name__)


class DataExporter:
    """
    Handles exporting scraped items to JSON and CSV.
    """

    def __init__(self, output_dir: Path) -> None:
    self.output_dir = output_dir
    self.output_dir.mkdir(parents=True, exist_ok=True)

    def to_json(self, items: Iterable[Dict], filename: str = "scraped_data.json") -> Path:
    data: List[Dict] = list(items)
    path = self.output_dir / filename
    path.write_text(json.dumps(
        data, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.debug("Wrote %d records to %s", len(data), path)
    return path

    def to_csv(self, items: Iterable[Dict], filename: str = "scraped_data.csv") -> Path:
    data: List[Dict] = list(items)
    if not data:
    path = self.output_dir / filename
    path.write_text("", encoding="utf-8")
    logger.debug("No data to write; created empty CSV at %s", path)
    return path

    path = self.output_dir / filename
    fieldnames = sorted({k for item in data for k in item.keys()})

    with path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
    writer.writerow(row)

    logger.debug("Wrote %d records to %s", len(data), path)
    return path
