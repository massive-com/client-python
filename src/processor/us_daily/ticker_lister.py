import logging
import time
from datetime import date
from typing import Dict, List

from processor.us_daily.config import Config
from processor.us_daily.storage import save_json, load_json, file_exists

logger = logging.getLogger("us_daily")

TICKERS_FILE = "tickers.json"


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


def _get_tickers_file(config: Config) -> str:
    import os
    return os.path.join(config.list_data_dir, TICKERS_FILE)


def _file_age_days(file_path: str) -> float:
    import os
    return (time.time() - os.path.getmtime(file_path)) / 86400


def list_all_tickers(client, config: Config) -> List[dict]:
    """Fetch all US stock tickers and save to file.

    Supports resume: if the output file already exists, previously fetched
    tickers are kept and only missing ones are fetched.
    """
    file_path = _get_tickers_file(config)

    # Return cached data if file is <= 7 days old
    if file_exists(file_path) and _file_age_days(file_path) <= 7:
        data = load_json(file_path)
        tickers = data.get("tickers", [])
        logger.info(f"Using cached tickers ({len(tickers)} tickers, file <= 7 days old)")
        return tickers

    # Load existing tickers for resume
    existing_tickers: Dict[str, dict] = {}
    if file_exists(file_path):
        data = load_json(file_path)
        for t in data.get("tickers", []):
            existing_tickers[t["ticker"]] = t
        logger.info(
            f"Resuming: {len(existing_tickers)} tickers already fetched"
        )

    # Get full ticker list from API (all US stocks, no exchange filter)
    logger.info("Listing all US stock tickers")
    try:
        ticker_objs = list(
            client.list_tickers(
                market="stocks", active=True, limit=1000
            )
        )
    except Exception as e:
        logger.error(f"Failed to list tickers: {e}")
        return list(existing_tickers.values())

    time.sleep(config.massive_interval)
    logger.info(f"Found {len(ticker_objs)} tickers")

    # Fetch details for new tickers only
    new_count = 0
    for i, ticker_obj in enumerate(ticker_objs):
        # if new_count >= 6:
        #     break

        ticker_str = ticker_obj.ticker
        if ticker_str in existing_tickers:
            continue

        try:
            details = client.get_ticker_details(ticker_str)
            entry = _details_to_dict(details)
            existing_tickers[ticker_str] = entry
            new_count += 1
            logger.info(
                f"[{i + 1}/{len(ticker_objs)}] {ticker_str}: OK"
            )
        except Exception as e:
            logger.warning(
                f"[{i + 1}/{len(ticker_objs)}] {ticker_str}: {e}"
            )

        time.sleep(config.massive_interval)

        # Flush to disk every 100 new details to avoid losing progress
        if new_count > 0 and new_count % 20 == 0:
            tickers_list = list(existing_tickers.values())
            save_json(file_path, {
                "updated_at": date.today().strftime("%Y-%m-%d"),
                "count": len(tickers_list),
                "tickers": tickers_list,
            })
            logger.info(
                f"Checkpoint: saved {len(tickers_list)} tickers to {file_path}"
            )

    # Final save
    tickers_list = list(existing_tickers.values())
    save_json(file_path, {
        "updated_at": date.today().strftime("%Y-%m-%d"),
        "count": len(tickers_list),
        "tickers": tickers_list,
    })

    logger.info(f"Saved {len(tickers_list)} tickers to {file_path}")
    return tickers_list
