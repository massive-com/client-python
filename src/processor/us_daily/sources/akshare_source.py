import logging

import pandas as pd

from processor.us_daily.sources.base import BaseSource, STANDARD_COLUMNS

logger = logging.getLogger("us_daily")

try:
    import akshare as ak
except ImportError:  # pragma: no cover
    ak = None  # type: ignore[assignment]


class AkshareSource(BaseSource):
    name = "akshare"

    def __init__(self, request_interval: float = 2.0):
        self.request_interval = request_interval

    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        if ak is None:
            raise ImportError("akshare is not installed")

        symbol = ticker.strip().upper()
        logger.debug(f"[akshare] fetching {symbol} {start_date}~{end_date}")

        df = ak.stock_us_daily(symbol=symbol, adjust="qfq")

        if df is None or df.empty:
            return pd.DataFrame(columns=STANDARD_COLUMNS)

        df["date"] = pd.to_datetime(df["date"])
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        df = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]

        if df.empty:
            return pd.DataFrame(columns=STANDARD_COLUMNS)

        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        df = df[STANDARD_COLUMNS].reset_index(drop=True)
        return df
