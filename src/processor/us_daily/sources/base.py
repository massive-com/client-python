from abc import ABC, abstractmethod

import pandas as pd

STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


class BaseSource(ABC):
    name: str
    request_interval: float

    @abstractmethod
    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch daily OHLCV data for a US stock ticker.

        Returns a DataFrame with columns matching STANDARD_COLUMNS.
        Raises on unrecoverable errors. Returns empty DataFrame if no data.
        """
        ...
