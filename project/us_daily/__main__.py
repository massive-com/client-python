import logging
import os
import sys
from datetime import datetime

from massive import RESTClient

from project.us_daily.config import load_config
from project.us_daily.storage import (
    get_tickers_file_path,
    file_exists,
    save_json,
    load_json,
)
from project.us_daily.ticker_filter import filter_top_tickers
from project.us_daily.agg_fetcher import fetch_ticker_aggs


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("us_daily")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler("logs/us_daily.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def main():
    logger = setup_logging()
    config = load_config()

    logger.info("=== US Daily Data Fetcher Started ===")
    logger.info(f"Config: {config}")

    client = RESTClient()

    # Step 1: Get ticker list
    tickers_path = get_tickers_file_path(config.data_dir)
    if config.refresh_tickers or not file_exists(tickers_path):
        logger.info("Filtering top tickers from API...")
        tickers = filter_top_tickers(client, config)
        save_json(tickers_path, {
            "updated_at": datetime.now().strftime("%Y-%m-%d"),
            "market_cap_min": config.market_cap_min,
            "tickers": tickers,
        })
        logger.info(f"Saved {len(tickers)} tickers to {tickers_path}")
    else:
        data = load_json(tickers_path)
        tickers = data["tickers"]
        logger.info(
            f"Loaded {len(tickers)} tickers from {tickers_path} "
            f"(updated: {data.get('updated_at', 'unknown')})"
        )

    # Step 2: Fetch agg data for each ticker
    all_failures = []
    total = len(tickers)
    for i, ticker_info in enumerate(tickers):
        ticker = ticker_info["ticker"]
        logger.info(f"[{i + 1}/{total}] Processing {ticker}")
        result = fetch_ticker_aggs(client, ticker, config)
        if result["failures"]:
            all_failures.extend(result["failures"])

    # Step 3: Summary
    logger.info("=== Summary ===")
    logger.info(f"Total tickers: {total}")
    if all_failures:
        logger.warning(f"Failed months: {len(all_failures)}")
        for f in all_failures:
            logger.warning(f"  - {f['ticker']} {f['month']}: {f['error']}")
    else:
        logger.info("All data fetched successfully")
    logger.info("=== Done ===")


if __name__ == "__main__":
    main()
