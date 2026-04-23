import logging
import os
import sys

from massive import RESTClient

from processor.us_daily.config import load_config
from processor.us_daily.ticker_lister import list_all_tickers, _get_tickers_file
from processor.us_daily.agg_fetcher import fetch_ticker_aggs
from processor.us_daily.sources.akshare_source import AkshareSource
from processor.us_daily.sources.yfinance_source import YfinanceSource
from processor.us_daily.sources.massive_source import MassiveSource
from processor.us_daily.sources.manager import SourceManager
from processor.us_daily.storage import load_json, file_exists


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
    """Load tickers from the tickers file."""
    file_path = _get_tickers_file(config)
    if not file_exists(file_path):
        return []
    data = load_json(file_path)
    return data.get("tickers", [])


def main():
    logger = setup_logging()
    config = load_config()

    logger.info("=== US Daily Data Fetcher Started ===")
    logger.info(f"Config: {config}")

    client = RESTClient()

    # Step 1: Fetch ticker list
    tickers_file = _get_tickers_file(config)
    if config.refresh_tickers or not file_exists(tickers_file):
        logger.info("Fetching ticker list...")
        list_all_tickers(client, config)

    # Load all tickers
    tickers = load_all_tickers(config)
    logger.info(f"Total tickers loaded: {len(tickers)}")

    # Step 2: Fetch daily data
    source_manager = build_source_manager(config, client)

    # Filter tickers by market cap
    if config.market_cap_min > 0:
        filtered = []
        for t in tickers:
            market_cap = t.get("market_cap")
            if market_cap is not None and market_cap >= config.market_cap_min:
                filtered.append(t)
            elif market_cap is None:
                logger.debug(
                    f"Skipping {t['ticker']}: market_cap is None"
                )
            else:
                logger.debug(
                    f"Skipping {t['ticker']}: market_cap={market_cap:.0f} < {config.market_cap_min:.0f}"
                )
        logger.info(
            f"Filtered by market_cap >= {config.market_cap_min:.0f}: {len(filtered)}/{len(tickers)} tickers"
        )
        tickers = filtered

    all_failures = []
    all_bars = 0
    total = len(tickers)
    for i, ticker_info in enumerate(tickers):
        ticker = ticker_info["ticker"]
        logger.info(f"[{i + 1}/{total}] Processing {ticker}")
        result = fetch_ticker_aggs(source_manager, ticker, config)
        all_bars += result["total_bars"]
        if result["failures"]:
            all_failures.extend(result["failures"])

    # Step 3: Summary
    logger.info("=== Summary ===")
    logger.info(f"Total tickers: {total}, total bars fetched: {all_bars}")
    if all_failures:
        logger.warning(f"Failed years: {len(all_failures)}")
        for f in all_failures:
            logger.warning(f"  - {f['ticker']} {f['year']}: {f['error']}")
    else:
        logger.info("All data fetched successfully")
    logger.info("=== Done ===")


if __name__ == "__main__":
    main()
