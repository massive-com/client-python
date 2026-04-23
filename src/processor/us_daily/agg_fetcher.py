import calendar
import logging
from datetime import date, datetime
from typing import List, Tuple

from processor.us_daily.config import Config
from processor.us_daily.sources.manager import FetchError
from processor.us_daily.storage import (
    get_month_file_path,
    file_exists,
    save_json,
)

logger = logging.getLogger("us_daily")


def generate_months(start: str, end: str) -> List[str]:
    start_year, start_month = int(start[:4]), int(start[5:7])
    end_year, end_month = int(end[:4]), int(end[5:7])

    months = []
    year, month = start_year, start_month
    while (year, month) <= (end_year, end_month):
        months.append(f"{year:04d}-{month:02d}")
        month += 1
        if month > 12:
            month = 1
            year += 1
    return months


def get_month_bounds(month: str) -> Tuple[str, str]:
    year, mon = int(month[:4]), int(month[5:7])
    last_day = calendar.monthrange(year, mon)[1]
    return f"{year:04d}-{mon:02d}-01", f"{year:04d}-{mon:02d}-{last_day:02d}"


def is_current_month(month: str) -> bool:
    today = date.today()
    return month == f"{today.year:04d}-{today.month:02d}"


def current_month() -> str:
    today = date.today()
    return f"{today.year:04d}-{today.month:02d}"


def fetch_ticker_aggs(source_manager, ticker: str, config: Config) -> dict:
    """Fetch monthly OHLCV data for a ticker using SourceManager.

    Args:
        source_manager: SourceManager instance with failover sources.
        ticker: Stock ticker symbol (e.g. "AAPL").
        config: Config with daily_data_dir, start_date, max_retries.

    Returns:
        Dict with "failures" list of failed months.
    """
    months = generate_months(config.start_date, current_month())
    failures = []

    for month in months:
        file_path = get_month_file_path(config.daily_data_dir, ticker, month)

        if file_exists(file_path) and not is_current_month(month):
            logger.debug(f"  {ticker} {month}: exists, skipping")
            continue

        start_date, end_date = get_month_bounds(month)

        try:
            df, source_name = source_manager.fetch_daily(ticker, start_date, end_date)
        except FetchError as e:
            failures.append({
                "ticker": ticker,
                "month": month,
                "error": str(e),
            })
            logger.error(f"  {ticker} {month}: {e}")
            continue

        data = {
            "ticker": ticker,
            "month": month,
            "source": source_name,
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
            "data": df.to_dict(orient="records"),
        }
        save_json(file_path, data)
        logger.info(f"  {ticker} {month}: fetched {len(df)} bars from {source_name}")

    return {"failures": failures}
