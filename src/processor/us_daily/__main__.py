import logging
import os
import sys

from massive import RESTClient

from processor.us_daily.config import load_config
from processor.us_daily.ticker_lister import list_tickers_for_exchange, EXCHANGES
from processor.us_daily.agg_fetcher import fetch_ticker_aggs
from processor.us_daily.sources.akshare_source import AkshareSource
from processor.us_daily.sources.yfinance_source import YfinanceSource
from processor.us_daily.sources.massive_source import MassiveSource
from processor.us_daily.sources.manager import SourceManager
from processor.us_daily.storage import get_list_file_path, load_json, file_exists


SOURCE_CLASSES = {
    "akshare": AkshareSource,
    "yfinance": YfinanceSource,
    "massive": MassiveSource,
}


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


def build_source_manager(config, client) -> SourceManager:
    """Build SourceManager from config priority list."""
    interval_map = {
        "akshare": config.akshare_interval,
        "yfinance": config.yfinance_interval,
        "massive": config.massive_interval,
    }
    sources = []
    for name in config.data_source_priority:
        cls = SOURCE_CLASSES.get(name)
        if cls is None:
            continue
        if name == "massive":
            sources.append(cls(client=client, request_interval=interval_map[name]))
        else:
            sources.append(cls(request_interval=interval_map[name]))
    return SourceManager(sources)


def load_all_tickers(config) -> list:
    """Load tickers from all exchange files in list_dir."""
    all_tickers = []
    seen = set()
    for exchange_name in config.exchanges:
        file_path = get_list_file_path(config.list_dir, exchange_name)
        if not file_exists(file_path):
            continue
        data = load_json(file_path)
        for t in data.get("tickers", []):
            ticker = t["ticker"]
            if ticker not in seen:
                seen.add(ticker)
                all_tickers.append(t)
    return all_tickers


def main():
    logger = setup_logging()
    config = load_config()

    logger.info("=== US Daily Data Fetcher Started ===")
    logger.info(f"Config: {config}")

    client = RESTClient()

    # Step 1: Fetch ticker lists per exchange
    if config.refresh_tickers or any(
        not file_exists(get_list_file_path(config.list_dir, ex))
        for ex in config.exchanges
    ):
        for exchange_name in config.exchanges:
            if exchange_name not in EXCHANGES:
                logger.warning(f"Unknown exchange: {exchange_name}, skipping")
                continue
            logger.info(f"Fetching ticker list for {exchange_name}...")
            list_tickers_for_exchange(client, exchange_name, config)

    # Load all tickers
    tickers = load_all_tickers(config)
    logger.info(f"Total tickers loaded: {len(tickers)}")

    # Step 2: Fetch daily data
    source_manager = build_source_manager(config, client)

    all_failures = []
    total = len(tickers)
    for i, ticker_info in enumerate(tickers):
        ticker = ticker_info["ticker"]
        logger.info(f"[{i + 1}/{total}] Processing {ticker}")
        result = fetch_ticker_aggs(source_manager, ticker, config)
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
