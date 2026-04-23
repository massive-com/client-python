import logging
from datetime import date, datetime
from typing import List

from processor.us_daily.config import Config
from processor.us_daily.sources.manager import FetchError
from processor.us_daily.storage import (
    get_year_file_path,
    file_exists,
    save_json,
)

logger = logging.getLogger("us_daily")


def generate_years(start_year: int, end_year: int) -> List[int]:
    return list(range(start_year, end_year + 1))


def get_year_bounds(year: int) -> tuple:
    return f"{year}-01-01", f"{year}-12-31"


def is_current_year(year: int) -> bool:
    return year == date.today().year


def fetch_ticker_aggs(source_manager, ticker: str, config: Config) -> dict:
    """Fetch yearly OHLCV data for a ticker using SourceManager.

    Args:
        source_manager: SourceManager instance with failover sources.
        ticker: Stock ticker symbol (e.g. "AAPL").
        config: Config with daily_data_dir, start_year, max_retries.

    Returns:
        Dict with "failures" list of failed years.
    """
    years = generate_years(config.start_year, date.today().year)
    failures = []

    for year in years:
        file_path = get_year_file_path(config.daily_data_dir, ticker, year)

        if file_exists(file_path) and not is_current_year(year):
            logger.debug(f"  {ticker} {year}: exists, skipping")
            continue

        start_date, end_date = get_year_bounds(year)

        try:
            df, source_name = source_manager.fetch_daily(ticker, start_date, end_date)
        except FetchError as e:
            failures.append({
                "ticker": ticker,
                "year": year,
                "error": str(e),
            })
            logger.error(f"  {ticker} {year}: {e}")
            continue

        data = {
            "ticker": ticker,
            "year": year,
            "source": source_name,
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
            "data": df.to_dict(orient="records"),
        }
        save_json(file_path, data)
        logger.info(f"  {ticker} {year}: fetched {len(df)} bars from {source_name}")

    return {"failures": failures}
