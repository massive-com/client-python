import logging

import pandas as pd

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    yf = None  # type: ignore[assignment]

from processor.us_daily.sources.base import BaseSource, STANDARD_COLUMNS

logger = logging.getLogger("us_daily")


class YfinanceSource(BaseSource):
    name = "yfinance"

    def __init__(self, request_interval: float = 1.0):
        self.request_interval = request_interval

    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        symbol = ticker.strip().upper()
        logger.debug(f"[yfinance] fetching {symbol} {start_date}~{end_date}")

        t = yf.Ticker(symbol)
        df = t.history(start=start_date, end=end_date)

        if df is None or df.empty:
            return pd.DataFrame(columns=STANDARD_COLUMNS)

        df.index.name = "Date"
        df = df.reset_index()
        df = df.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        })

        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df = df[STANDARD_COLUMNS].reset_index(drop=True)
        return df
