from utils.logger import get_logger
from config import settings
from scraper.exporter import DataExporter
from scraper.spider import AdvancedSpider
import argparse
import sys
from pathlib import Path

# Ensure src/ subpackages can be imported when running from project root
CURRENT_DIR = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_DIR.parents[2]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))


logger = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Advanced Captcha Web Scraper - Bitbash Demo"
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "csv", "both"],
        default="both",
        help="Output format for scraped data.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=settings.MAX_PAGES,
        help="Maximum number of pages to scrape.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Enable headless browser mode (if Selenium is used).",
    )
    parser.add_argument(
        "--use-proxies",
        action="store_true",
        help="Enable rotating proxies during scraping.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logger.info("Starting Advanced Captcha Web Scraper")

    spider = AdvancedSpider(
        target_urls=settings.TARGET_URLS,
        max_pages=args.max_pages,
        headless=args.headless,
        use_proxies=args.use_proxies,
    )

    try:
    items = spider.run()
    logger.info("Scraping finished. Parsed %d items.", len(items))
    except Exception as exc:  # noqa: BLE001
    logger.exception("Fatal error while running spider: %s", exc)
    sys.exit(1)

    exporter = DataExporter(output_dir=settings.OUTPUT_DIR)

    if args.output_format in ("json", "both"):
    json_path = exporter.to_json(items)
    logger.info("Exported JSON data to %s", json_path)

    if args.output_format in ("csv", "both"):
    csv_path = exporter.to_csv(items)
    logger.info("Exported CSV data to %s", csv_path)

    logger.info("Done.")


if __name__ == "__main__":
    main()
