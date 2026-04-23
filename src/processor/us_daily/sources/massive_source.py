import logging
from datetime import datetime, timezone

import pandas as pd

from processor.us_daily.sources.base import BaseSource, STANDARD_COLUMNS

logger = logging.getLogger("us_daily")


class MassiveSource(BaseSource):
    name = "massive"

    def __init__(self, client, request_interval: float = 12.0):
        self.client = client
        self.request_interval = request_interval

    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        logger.debug(f"[massive] fetching {ticker} {start_date}~{end_date}")

        aggs = list(
            self.client.list_aggs(
                ticker, 1, "day",
                from_=start_date, to=end_date,
                adjusted=True, sort="asc",
            )
        )

        if not aggs:
            return pd.DataFrame(columns=STANDARD_COLUMNS)

        rows = []
        for a in aggs:
            dt = datetime.fromtimestamp(a.timestamp / 1000, tz=timezone.utc)
            rows.append({
                "date": dt.strftime("%Y-%m-%d"),
                "open": a.open,
                "high": a.high,
                "low": a.low,
                "close": a.close,
                "volume": a.volume,
            })

        df = pd.DataFrame(rows, columns=STANDARD_COLUMNS)
        return df
