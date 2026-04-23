import logging
import time
from typing import List, Tuple

import pandas as pd

from processor.us_daily.sources.base import BaseSource

logger = logging.getLogger("us_daily")


class FetchError(Exception):
    """Raised when all data sources fail."""
    pass


class SourceManager:
    def __init__(self, sources: List[BaseSource]):
        self.sources = sources

    def fetch_daily(
        self, ticker: str, start_date: str, end_date: str
    ) -> Tuple[pd.DataFrame, str]:
        """Try each source in priority order. Return (df, source_name).

        Raises FetchError if all sources fail or return empty data.
        """
        errors = []
        for source in self.sources:
            try:
                df = source.fetch_daily(ticker, start_date, end_date)
                if df is not None and not df.empty:
                    time.sleep(source.request_interval)
                    return df, source.name
                else:
                    logger.debug(
                        f"{source.name} returned empty data for {ticker}"
                    )
            except Exception as e:
                logger.warning(f"{source.name} failed for {ticker}: {e}")
                errors.append(f"{source.name}: {e}")
                continue
        raise FetchError(
            f"All sources failed for {ticker}: {'; '.join(errors)}"
        )
