import calendar
import logging
import time
from datetime import date, datetime
from typing import List, Tuple

from project.us_daily.config import Config
from project.us_daily.storage import (
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


def fetch_ticker_aggs(client, ticker: str, config: Config) -> dict:
    months = generate_months(config.start_date, current_month())
    failures = []

    for month in months:
        file_path = get_month_file_path(config.data_dir, ticker, month)

        if file_exists(file_path) and not is_current_month(month):
            logger.debug(f"  {ticker} {month}: exists, skipping")
            continue

        start_date, end_date = get_month_bounds(month)
        aggs = None
        last_error = None

        for attempt in range(1, config.max_retries + 1):
            try:
                aggs_iter = client.list_aggs(
                    ticker,
                    1,
                    "day",
                    from_=start_date,
                    to=end_date,
                    adjusted=True,
                    sort="asc",
                )
                aggs = list(aggs_iter)
                break
            except Exception as e:
                last_error = e
                logger.warning(
                    f"  {ticker} {month}: attempt {attempt}/{config.max_retries} failed: {e}"
                )
                if attempt < config.max_retries:
                    time.sleep(config.request_interval)

        if aggs is None:
            failures.append(
                {
                    "ticker": ticker,
                    "month": month,
                    "error": str(last_error),
                }
            )
            logger.error(f"  {ticker} {month}: all retries failed, skipping")
            continue

        data = {
            "ticker": ticker,
            "month": month,
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
            "data": [
                {
                    "open": a.open,
                    "high": a.high,
                    "low": a.low,
                    "close": a.close,
                    "volume": a.volume,
                    "vwap": a.vwap,
                    "timestamp": a.timestamp,
                    "transactions": a.transactions,
                }
                for a in aggs
            ],
        }
        save_json(file_path, data)
        logger.info(f"  {ticker} {month}: fetched {len(aggs)} bars")
        time.sleep(config.request_interval)

    return {"failures": failures}
