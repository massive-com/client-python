import logging
import time
from datetime import date
from typing import Dict, List

from processor.us_daily.config import Config
from processor.us_daily.storage import get_list_file_path, save_json, load_json, file_exists

logger = logging.getLogger("us_daily")

EXCHANGES: Dict[str, str] = {
    "nasdaq": "XNAS",
    "nyse": "XNYS",
    "arca": "ARCX",
}


def _details_to_dict(details) -> dict:
    """Convert a TickerDetails object to a plain dict, dropping None values."""
    result = {}
    for key, value in vars(details).items():
        if key.startswith("_"):
            continue
        if value is None:
            continue
        if hasattr(value, "__dict__") and not isinstance(value, (str, int, float, bool)):
            value = {k: v for k, v in vars(value).items() if not k.startswith("_") and v is not None}
        result[key] = value
    return result


def list_tickers_for_exchange(client, exchange_name: str, config: Config) -> List[dict]:
    """Fetch all tickers for an exchange and save to file.

    Supports resume: if the output file already exists, previously fetched
    tickers are kept and only missing ones are fetched.
    """
    exchange_code = EXCHANGES[exchange_name]
    file_path = get_list_file_path(config.list_dir, exchange_name)

    # Load existing tickers for resume
    existing_tickers: Dict[str, dict] = {}
    if file_exists(file_path):
        data = load_json(file_path)
        for t in data.get("tickers", []):
            existing_tickers[t["ticker"]] = t
        logger.info(
            f"[{exchange_name}] Resuming: {len(existing_tickers)} tickers already fetched"
        )

    # Get full ticker list from API
    logger.info(f"[{exchange_name}] Listing tickers for {exchange_code}")
    try:
        ticker_objs = list(
            client.list_tickers(
                market="stocks", exchange=exchange_code, active=True, limit=1000
            )
        )
    except Exception as e:
        logger.error(f"[{exchange_name}] Failed to list tickers: {e}")
        return list(existing_tickers.values())

    time.sleep(config.massive_interval)
    logger.info(f"[{exchange_name}] Found {len(ticker_objs)} tickers")

    # Fetch details for new tickers only
    for i, ticker_obj in enumerate(ticker_objs):
        ticker_str = ticker_obj.ticker
        if ticker_str in existing_tickers:
            continue

        try:
            details = client.get_ticker_details(ticker_str)
            entry = _details_to_dict(details)
            existing_tickers[ticker_str] = entry
            logger.info(
                f"[{exchange_name}] [{i + 1}/{len(ticker_objs)}] {ticker_str}: OK"
            )
        except Exception as e:
            logger.warning(
                f"[{exchange_name}] [{i + 1}/{len(ticker_objs)}] {ticker_str}: {e}"
            )

        time.sleep(config.massive_interval)

    # Save result
    tickers_list = list(existing_tickers.values())
    save_json(file_path, {
        "updated_at": date.today().strftime("%Y-%m-%d"),
        "exchange": exchange_code,
        "count": len(tickers_list),
        "tickers": tickers_list,
    })

    logger.info(f"[{exchange_name}] Saved {len(tickers_list)} tickers to {file_path}")
    return tickers_list
