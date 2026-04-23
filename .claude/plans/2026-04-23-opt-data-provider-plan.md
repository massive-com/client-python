# US Data Provider Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor `processor/us_daily` to support full stock listing by exchange (no market-cap filter) and multi-source daily data fetching with akshare > yfinance > massive failover.

**Architecture:** New `sources/` sub-package with `BaseSource` abstract class, three implementations (AkshareSource, YfinanceSource, MassiveSource), and a `SourceManager` for priority-based failover. `ticker_lister.py` replaces `ticker_filter.py` for full-exchange listing. Config updated with per-source intervals and source priority.

**Tech Stack:** Python 3.9+, dataclasses, akshare, yfinance, massive REST client, pandas

**Design Doc:** `.claude/plans/2026-04-23-opt-data-provider-design.md`

---

### Task 1: Update Config

**Files:**
- Modify: `src/processor/us_daily/config.py`
- Modify: `tests/test_us_daily/test_config.py`

- [ ] **Step 1: Write failing tests for new Config fields**

In `tests/test_us_daily/test_config.py`, replace the `TestConfig` class with:

```python
class TestConfig(unittest.TestCase):
    def test_default_config(self):
        from processor.us_daily.config import Config

        config = Config()
        self.assertEqual(config.refresh_tickers, False)
        self.assertEqual(config.start_date, "2026-01")
        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.exchanges, ["nasdaq", "nyse", "arca"])
        self.assertEqual(config.data_source_priority, ["akshare", "yfinance", "massive"])
        self.assertEqual(config.akshare_interval, 2.0)
        self.assertEqual(config.yfinance_interval, 1.0)
        self.assertEqual(config.massive_interval, 12.0)
        self.assertEqual(config.list_dir, "data/us_list")
        self.assertEqual(config.daily_dir, "data/us_daily")

    def test_load_config_from_file(self):
        from processor.us_daily.config import load_config

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({
                "refresh_tickers": True,
                "akshare_interval": 3.0,
                "exchanges": ["nasdaq"],
            }, f)
            tmp_path = f.name

        try:
            config = load_config(tmp_path)
            self.assertEqual(config.refresh_tickers, True)
            self.assertEqual(config.akshare_interval, 3.0)
            self.assertEqual(config.exchanges, ["nasdaq"])
            # defaults preserved for unspecified fields
            self.assertEqual(config.start_date, "2026-01")
            self.assertEqual(config.massive_interval, 12.0)
        finally:
            os.unlink(tmp_path)

    def test_load_config_missing_file_uses_defaults(self):
        from processor.us_daily.config import load_config

        config = load_config("/nonexistent/path/config.json")
        self.assertEqual(config.refresh_tickers, False)
        self.assertEqual(config.data_source_priority, ["akshare", "yfinance", "massive"])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_us_daily/test_config.py -v`
Expected: FAIL — `Config` does not have `exchanges`, `data_source_priority`, etc.

- [ ] **Step 3: Update Config dataclass**

Replace `src/processor/us_daily/config.py` with:

```python
import json
import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    refresh_tickers: bool = False
    exchanges: List[str] = field(default_factory=lambda: ["nasdaq", "nyse", "arca"])
    start_date: str = "2026-01"
    data_source_priority: List[str] = field(
        default_factory=lambda: ["akshare", "yfinance", "massive"]
    )
    akshare_interval: float = 2.0
    yfinance_interval: float = 1.0
    massive_interval: float = 12.0
    list_dir: str = "data/us_list"
    daily_dir: str = "data/us_daily"
    max_retries: int = 3


def load_config(config_path: str = None) -> Config:
    config = Config()
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            data = json.load(f)
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
    return config
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_us_daily/test_config.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/processor/us_daily/config.py tests/test_us_daily/test_config.py
git commit -m "refactor: update us_daily Config with multi-source fields"
```

---

### Task 2: Update Storage helpers

**Files:**
- Modify: `src/processor/us_daily/storage.py`
- Modify: `tests/test_us_daily/test_storage.py`

- [ ] **Step 1: Write failing tests for new storage helpers**

Add new test methods to `TestStorage` in `tests/test_us_daily/test_storage.py`:

```python
    def test_get_list_file_path(self):
        from processor.us_daily.storage import get_list_file_path

        result = get_list_file_path("data/us_list", "nasdaq")
        self.assertEqual(result, "data/us_list/nasdaq.json")

    def test_get_month_file_path_daily_dir(self):
        from processor.us_daily.storage import get_month_file_path

        result = get_month_file_path("data/us_daily", "AAPL", "2020-01")
        self.assertEqual(result, "data/us_daily/AAPL/2020-01.json")
```

- [ ] **Step 2: Run tests to verify new test fails**

Run: `pytest tests/test_us_daily/test_storage.py::TestStorage::test_get_list_file_path -v`
Expected: FAIL — `get_list_file_path` does not exist.

- [ ] **Step 3: Add get_list_file_path to storage.py**

In `src/processor/us_daily/storage.py`, add after the `get_tickers_file_path` function:

```python
def get_list_file_path(list_dir: str, exchange: str) -> str:
    return os.path.join(list_dir, f"{exchange}.json")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_us_daily/test_storage.py -v`
Expected: All tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/processor/us_daily/storage.py tests/test_us_daily/test_storage.py
git commit -m "feat: add get_list_file_path to storage helpers"
```

---

### Task 3: Create BaseSource and SourceManager

**Files:**
- Create: `src/processor/us_daily/sources/__init__.py`
- Create: `src/processor/us_daily/sources/base.py`
- Create: `src/processor/us_daily/sources/manager.py`
- Create: `tests/test_us_daily/test_sources/__init__.py`
- Create: `tests/test_us_daily/test_sources/test_manager.py`

- [ ] **Step 1: Write failing tests for SourceManager**

Create `tests/test_us_daily/test_sources/__init__.py` (empty file).

Create `tests/test_us_daily/test_sources/test_manager.py`:

```python
import unittest
from unittest.mock import MagicMock, patch
import pandas as pd


class TestSourceManager(unittest.TestCase):
    def _make_source(self, name, data=None, error=None):
        """Create a mock source that returns data or raises error."""
        from processor.us_daily.sources.base import BaseSource

        source = MagicMock(spec=BaseSource)
        source.name = name
        source.request_interval = 0.0
        if error:
            source.fetch_daily.side_effect = error
        elif data is not None:
            source.fetch_daily.return_value = data
        else:
            source.fetch_daily.return_value = pd.DataFrame()
        return source

    def test_returns_first_successful_source(self):
        from processor.us_daily.sources.manager import SourceManager

        df = pd.DataFrame({"date": ["2020-01-02"], "close": [100.0]})
        s1 = self._make_source("source1", data=df)
        s2 = self._make_source("source2", data=df)

        manager = SourceManager([s1, s2])
        with patch("processor.us_daily.sources.manager.time.sleep"):
            result_df, source_name = manager.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertEqual(source_name, "source1")
        s1.fetch_daily.assert_called_once_with("AAPL", "2020-01-01", "2020-01-31")
        s2.fetch_daily.assert_not_called()

    def test_falls_back_on_failure(self):
        from processor.us_daily.sources.manager import SourceManager

        df = pd.DataFrame({"date": ["2020-01-02"], "close": [100.0]})
        s1 = self._make_source("source1", error=Exception("API down"))
        s2 = self._make_source("source2", data=df)

        manager = SourceManager([s1, s2])
        with patch("processor.us_daily.sources.manager.time.sleep"):
            result_df, source_name = manager.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertEqual(source_name, "source2")

    def test_falls_back_on_empty_dataframe(self):
        from processor.us_daily.sources.manager import SourceManager

        empty_df = pd.DataFrame()
        good_df = pd.DataFrame({"date": ["2020-01-02"], "close": [100.0]})
        s1 = self._make_source("source1", data=empty_df)
        s2 = self._make_source("source2", data=good_df)

        manager = SourceManager([s1, s2])
        with patch("processor.us_daily.sources.manager.time.sleep"):
            result_df, source_name = manager.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertEqual(source_name, "source2")

    def test_raises_when_all_fail(self):
        from processor.us_daily.sources.manager import SourceManager, FetchError

        s1 = self._make_source("source1", error=Exception("fail1"))
        s2 = self._make_source("source2", error=Exception("fail2"))

        manager = SourceManager([s1, s2])
        with patch("processor.us_daily.sources.manager.time.sleep"):
            with self.assertRaises(FetchError):
                manager.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

    def test_sleeps_after_successful_fetch(self):
        from processor.us_daily.sources.manager import SourceManager

        df = pd.DataFrame({"date": ["2020-01-02"], "close": [100.0]})
        s1 = self._make_source("source1", data=df)
        s1.request_interval = 5.0

        manager = SourceManager([s1])
        with patch("processor.us_daily.sources.manager.time.sleep") as mock_sleep:
            manager.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        mock_sleep.assert_called_once_with(5.0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_us_daily/test_sources/test_manager.py -v`
Expected: FAIL — modules do not exist.

- [ ] **Step 3: Create sources package with BaseSource**

Create `src/processor/us_daily/sources/__init__.py`:

```python
from processor.us_daily.sources.manager import SourceManager, FetchError

__all__ = ["SourceManager", "FetchError"]
```

Create `src/processor/us_daily/sources/base.py`:

```python
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
```

- [ ] **Step 4: Create SourceManager**

Create `src/processor/us_daily/sources/manager.py`:

```python
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
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_us_daily/test_sources/test_manager.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 6: Commit**

```bash
git add src/processor/us_daily/sources/ tests/test_us_daily/test_sources/
git commit -m "feat: add BaseSource interface and SourceManager with failover"
```

---

### Task 4: Implement AkshareSource

**Files:**
- Create: `src/processor/us_daily/sources/akshare_source.py`
- Create: `tests/test_us_daily/test_sources/test_akshare_source.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_us_daily/test_sources/test_akshare_source.py`:

```python
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd


class TestAkshareSource(unittest.TestCase):
    def test_fetch_daily_returns_standard_columns(self):
        from processor.us_daily.sources.akshare_source import AkshareSource
        from processor.us_daily.sources.base import STANDARD_COLUMNS

        raw_df = pd.DataFrame({
            "date": pd.to_datetime(["2020-01-02", "2020-01-03"]),
            "open": [74.06, 75.0],
            "high": [75.15, 76.0],
            "low": [73.80, 74.5],
            "close": [74.36, 75.5],
            "volume": [108872000, 98000000],
        })

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_daily.return_value = raw_df
            source = AkshareSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertListEqual(list(result.columns), STANDARD_COLUMNS)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.iloc[0]["close"], 74.36)

    def test_fetch_daily_filters_by_date(self):
        from processor.us_daily.sources.akshare_source import AkshareSource

        raw_df = pd.DataFrame({
            "date": pd.to_datetime(["2019-12-31", "2020-01-02", "2020-02-01"]),
            "open": [70.0, 74.06, 80.0],
            "high": [71.0, 75.15, 81.0],
            "low": [69.0, 73.80, 79.0],
            "close": [70.5, 74.36, 80.5],
            "volume": [100000, 108872000, 90000],
        })

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_daily.return_value = raw_df
            source = AkshareSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["date"], "2020-01-02")

    def test_fetch_daily_calls_with_correct_symbol(self):
        from processor.us_daily.sources.akshare_source import AkshareSource

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_daily.return_value = pd.DataFrame()
            source = AkshareSource(request_interval=0.0)
            source.fetch_daily("aapl", "2020-01-01", "2020-01-31")

        mock_ak.stock_us_daily.assert_called_once_with(symbol="AAPL", adjust="qfq")

    def test_fetch_daily_returns_empty_on_no_data(self):
        from processor.us_daily.sources.akshare_source import AkshareSource

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_daily.return_value = pd.DataFrame()
            source = AkshareSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_us_daily/test_sources/test_akshare_source.py -v`
Expected: FAIL — module does not exist.

- [ ] **Step 3: Implement AkshareSource**

Create `src/processor/us_daily/sources/akshare_source.py`:

```python
import logging

import pandas as pd

from processor.us_daily.sources.base import BaseSource, STANDARD_COLUMNS

logger = logging.getLogger("us_daily")


class AkshareSource(BaseSource):
    name = "akshare"

    def __init__(self, request_interval: float = 2.0):
        self.request_interval = request_interval

    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        import akshare as ak

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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_us_daily/test_sources/test_akshare_source.py -v`
Expected: All 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/processor/us_daily/sources/akshare_source.py tests/test_us_daily/test_sources/test_akshare_source.py
git commit -m "feat: add AkshareSource for US daily data"
```

---

### Task 5: Implement YfinanceSource

**Files:**
- Create: `src/processor/us_daily/sources/yfinance_source.py`
- Create: `tests/test_us_daily/test_sources/test_yfinance_source.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_us_daily/test_sources/test_yfinance_source.py`:

```python
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd


class TestYfinanceSource(unittest.TestCase):
    def test_fetch_daily_returns_standard_columns(self):
        from processor.us_daily.sources.yfinance_source import YfinanceSource
        from processor.us_daily.sources.base import STANDARD_COLUMNS

        raw_df = pd.DataFrame(
            {
                "Open": [74.06, 75.0],
                "High": [75.15, 76.0],
                "Low": [73.80, 74.5],
                "Close": [74.36, 75.5],
                "Volume": [108872000, 98000000],
            },
            index=pd.to_datetime(["2020-01-02", "2020-01-03"]),
        )

        with patch("processor.us_daily.sources.yfinance_source.yf") as mock_yf:
            mock_ticker = MagicMock()
            mock_ticker.history.return_value = raw_df
            mock_yf.Ticker.return_value = mock_ticker
            source = YfinanceSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertListEqual(list(result.columns), STANDARD_COLUMNS)
        self.assertEqual(len(result), 2)
        self.assertEqual(result.iloc[0]["close"], 74.36)

    def test_fetch_daily_passes_correct_params(self):
        from processor.us_daily.sources.yfinance_source import YfinanceSource

        with patch("processor.us_daily.sources.yfinance_source.yf") as mock_yf:
            mock_ticker = MagicMock()
            mock_ticker.history.return_value = pd.DataFrame()
            mock_yf.Ticker.return_value = mock_ticker
            source = YfinanceSource(request_interval=0.0)
            source.fetch_daily("aapl", "2020-01-01", "2020-01-31")

        mock_yf.Ticker.assert_called_once_with("AAPL")
        mock_ticker.history.assert_called_once_with(start="2020-01-01", end="2020-01-31")

    def test_fetch_daily_returns_empty_on_no_data(self):
        from processor.us_daily.sources.yfinance_source import YfinanceSource

        with patch("processor.us_daily.sources.yfinance_source.yf") as mock_yf:
            mock_ticker = MagicMock()
            mock_ticker.history.return_value = pd.DataFrame()
            mock_yf.Ticker.return_value = mock_ticker
            source = YfinanceSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_us_daily/test_sources/test_yfinance_source.py -v`
Expected: FAIL — module does not exist.

- [ ] **Step 3: Implement YfinanceSource**

Create `src/processor/us_daily/sources/yfinance_source.py`:

```python
import logging

import pandas as pd

from processor.us_daily.sources.base import BaseSource, STANDARD_COLUMNS

logger = logging.getLogger("us_daily")


class YfinanceSource(BaseSource):
    name = "yfinance"

    def __init__(self, request_interval: float = 1.0):
        self.request_interval = request_interval

    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        import yfinance as yf

        symbol = ticker.strip().upper()
        logger.debug(f"[yfinance] fetching {symbol} {start_date}~{end_date}")

        t = yf.Ticker(symbol)
        df = t.history(start=start_date, end=end_date)

        if df is None or df.empty:
            return pd.DataFrame(columns=STANDARD_COLUMNS)

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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_us_daily/test_sources/test_yfinance_source.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/processor/us_daily/sources/yfinance_source.py tests/test_us_daily/test_sources/test_yfinance_source.py
git commit -m "feat: add YfinanceSource for US daily data"
```

---

### Task 6: Implement MassiveSource

**Files:**
- Create: `src/processor/us_daily/sources/massive_source.py`
- Create: `tests/test_us_daily/test_sources/test_massive_source.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_us_daily/test_sources/test_massive_source.py`:

```python
import unittest
from unittest.mock import MagicMock
import pandas as pd


class TestMassiveSource(unittest.TestCase):
    def test_fetch_daily_returns_standard_columns(self):
        from processor.us_daily.sources.massive_source import MassiveSource
        from processor.us_daily.sources.base import STANDARD_COLUMNS

        agg1 = MagicMock()
        agg1.open = 74.06
        agg1.high = 75.15
        agg1.low = 73.80
        agg1.close = 74.36
        agg1.volume = 108872000
        agg1.timestamp = 1577944800000  # 2020-01-02 UTC

        client = MagicMock()
        client.list_aggs.return_value = iter([agg1])

        source = MassiveSource(client=client, request_interval=0.0)
        result = source.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertListEqual(list(result.columns), STANDARD_COLUMNS)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["close"], 74.36)
        self.assertEqual(result.iloc[0]["date"], "2020-01-02")

    def test_fetch_daily_calls_client_correctly(self):
        from processor.us_daily.sources.massive_source import MassiveSource

        client = MagicMock()
        client.list_aggs.return_value = iter([])

        source = MassiveSource(client=client, request_interval=0.0)
        source.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        client.list_aggs.assert_called_once_with(
            "AAPL", 1, "day",
            from_="2020-01-01", to="2020-01-31",
            adjusted=True, sort="asc",
        )

    def test_fetch_daily_returns_empty_on_no_data(self):
        from processor.us_daily.sources.massive_source import MassiveSource

        client = MagicMock()
        client.list_aggs.return_value = iter([])

        source = MassiveSource(client=client, request_interval=0.0)
        result = source.fetch_daily("AAPL", "2020-01-01", "2020-01-31")

        self.assertTrue(result.empty)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_us_daily/test_sources/test_massive_source.py -v`
Expected: FAIL — module does not exist.

- [ ] **Step 3: Implement MassiveSource**

Create `src/processor/us_daily/sources/massive_source.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_us_daily/test_sources/test_massive_source.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/processor/us_daily/sources/massive_source.py tests/test_us_daily/test_sources/test_massive_source.py
git commit -m "feat: add MassiveSource for US daily data"
```

---

### Task 7: Create ticker_lister.py

**Files:**
- Create: `src/processor/us_daily/ticker_lister.py`
- Create: `tests/test_us_daily/test_ticker_lister.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_us_daily/test_ticker_lister.py`:

```python
import unittest
from unittest.mock import MagicMock, patch, call
import os
import tempfile
import shutil
import json


class TestTickerLister(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _make_ticker(self, ticker_str):
        t = MagicMock()
        t.ticker = ticker_str
        return t

    def _make_details(self, **kwargs):
        """Create a mock TickerDetails with all fields as attributes."""
        d = MagicMock()
        for k, v in kwargs.items():
            setattr(d, k, v)
        # Simulate __dict__ for serialization
        d.__dict__ = kwargs
        return d

    def test_list_tickers_for_exchange(self):
        from processor.us_daily.ticker_lister import list_tickers_for_exchange
        from processor.us_daily.config import Config

        config = Config(list_dir=self.test_dir, massive_interval=0)

        client = MagicMock()
        client.list_tickers.return_value = iter([
            self._make_ticker("AAPL"),
            self._make_ticker("MSFT"),
        ])

        details_aapl = self._make_details(
            ticker="AAPL", name="Apple Inc", market_cap=3e12,
            primary_exchange="XNAS",
        )
        details_msft = self._make_details(
            ticker="MSFT", name="Microsoft", market_cap=2.8e12,
            primary_exchange="XNAS",
        )

        def mock_details(ticker):
            return {"AAPL": details_aapl, "MSFT": details_msft}[ticker]

        client.get_ticker_details.side_effect = mock_details

        with patch("processor.us_daily.ticker_lister.time.sleep"):
            list_tickers_for_exchange(client, "nasdaq", config)

        file_path = os.path.join(self.test_dir, "nasdaq.json")
        self.assertTrue(os.path.exists(file_path))

        with open(file_path) as f:
            data = json.load(f)

        self.assertEqual(data["exchange"], "XNAS")
        self.assertEqual(data["count"], 2)
        tickers = [t["ticker"] for t in data["tickers"]]
        self.assertIn("AAPL", tickers)
        self.assertIn("MSFT", tickers)

    def test_resume_skips_existing_tickers(self):
        from processor.us_daily.ticker_lister import list_tickers_for_exchange
        from processor.us_daily.config import Config

        config = Config(list_dir=self.test_dir, massive_interval=0)

        # Pre-populate file with AAPL already fetched
        file_path = os.path.join(self.test_dir, "nasdaq.json")
        existing_data = {
            "updated_at": "2026-04-22",
            "exchange": "XNAS",
            "count": 1,
            "tickers": [
                {"ticker": "AAPL", "name": "Apple Inc", "market_cap": 3e12},
            ],
        }
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(existing_data, f)

        client = MagicMock()
        client.list_tickers.return_value = iter([
            self._make_ticker("AAPL"),
            self._make_ticker("MSFT"),
        ])

        details_msft = self._make_details(
            ticker="MSFT", name="Microsoft", market_cap=2.8e12,
            primary_exchange="XNAS",
        )
        client.get_ticker_details.return_value = details_msft

        with patch("processor.us_daily.ticker_lister.time.sleep"):
            list_tickers_for_exchange(client, "nasdaq", config)

        # Should only call get_ticker_details for MSFT (AAPL already exists)
        client.get_ticker_details.assert_called_once_with("MSFT")

        with open(file_path) as f:
            data = json.load(f)
        self.assertEqual(data["count"], 2)

    def test_skips_ticker_on_details_error(self):
        from processor.us_daily.ticker_lister import list_tickers_for_exchange
        from processor.us_daily.config import Config

        config = Config(list_dir=self.test_dir, massive_interval=0)

        client = MagicMock()
        client.list_tickers.return_value = iter([
            self._make_ticker("FAIL"),
            self._make_ticker("AAPL"),
        ])

        details_aapl = self._make_details(
            ticker="AAPL", name="Apple Inc", market_cap=3e12,
            primary_exchange="XNAS",
        )

        def mock_details(ticker):
            if ticker == "FAIL":
                raise Exception("API error")
            return details_aapl

        client.get_ticker_details.side_effect = mock_details

        with patch("processor.us_daily.ticker_lister.time.sleep"):
            list_tickers_for_exchange(client, "nasdaq", config)

        file_path = os.path.join(self.test_dir, "nasdaq.json")
        with open(file_path) as f:
            data = json.load(f)

        tickers = [t["ticker"] for t in data["tickers"]]
        self.assertIn("AAPL", tickers)
        self.assertNotIn("FAIL", tickers)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_us_daily/test_ticker_lister.py -v`
Expected: FAIL — module does not exist.

- [ ] **Step 3: Implement ticker_lister.py**

Create `src/processor/us_daily/ticker_lister.py`:

```python
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
        # Handle nested objects with their own __dict__
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_us_daily/test_ticker_lister.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/processor/us_daily/ticker_lister.py tests/test_us_daily/test_ticker_lister.py
git commit -m "feat: add ticker_lister with full exchange listing and resume support"
```

---

### Task 8: Refactor agg_fetcher.py to use SourceManager

**Files:**
- Modify: `src/processor/us_daily/agg_fetcher.py`
- Modify: `tests/test_us_daily/test_agg_fetcher.py`

- [ ] **Step 1: Update tests for new agg_fetcher interface**

Replace `TestFetchTickerAggs` class in `tests/test_us_daily/test_agg_fetcher.py` (keep `TestGenerateMonths`, `TestMonthBounds`, `TestIsCurrentMonth` unchanged):

```python
class TestFetchTickerAggs(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def _make_manager(self, df=None, source_name="akshare", error=None):
        from processor.us_daily.sources.manager import SourceManager

        manager = MagicMock(spec=SourceManager)
        if error:
            manager.fetch_daily.side_effect = error
        else:
            manager.fetch_daily.return_value = (df, source_name)
        return manager

    def test_skips_existing_historical_month(self):
        from processor.us_daily.agg_fetcher import fetch_ticker_aggs
        from processor.us_daily.config import Config

        config = Config(start_date="2020-01", daily_dir=self.test_dir)

        ticker_dir = os.path.join(self.test_dir, "AAPL")
        os.makedirs(ticker_dir)
        with open(os.path.join(ticker_dir, "2020-01.json"), "w") as f:
            json.dump({"ticker": "AAPL", "month": "2020-01", "data": []}, f)

        manager = self._make_manager()

        with patch(
            "processor.us_daily.agg_fetcher.generate_months", return_value=["2020-01"]
        ):
            with patch(
                "processor.us_daily.agg_fetcher.is_current_month", return_value=False
            ):
                result = fetch_ticker_aggs(manager, "AAPL", config)

        manager.fetch_daily.assert_not_called()
        self.assertEqual(result["failures"], [])

    def test_fetches_missing_month(self):
        from processor.us_daily.agg_fetcher import fetch_ticker_aggs
        from processor.us_daily.config import Config
        import pandas as pd

        config = Config(start_date="2020-01", daily_dir=self.test_dir)

        df = pd.DataFrame({
            "date": ["2020-01-02"],
            "open": [74.06],
            "high": [75.15],
            "low": [73.80],
            "close": [74.36],
            "volume": [108872000],
        })
        manager = self._make_manager(df=df, source_name="akshare")

        with patch(
            "processor.us_daily.agg_fetcher.generate_months", return_value=["2020-01"]
        ):
            with patch(
                "processor.us_daily.agg_fetcher.is_current_month", return_value=False
            ):
                result = fetch_ticker_aggs(manager, "AAPL", config)

        file_path = os.path.join(self.test_dir, "AAPL", "2020-01.json")
        self.assertTrue(os.path.exists(file_path))

        with open(file_path) as f:
            data = json.load(f)
        self.assertEqual(data["ticker"], "AAPL")
        self.assertEqual(data["month"], "2020-01")
        self.assertEqual(data["source"], "akshare")
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["close"], 74.36)
        self.assertEqual(result["failures"], [])

    def test_refreshes_current_month(self):
        from processor.us_daily.agg_fetcher import fetch_ticker_aggs
        from processor.us_daily.config import Config
        import pandas as pd

        config = Config(start_date="2026-04", daily_dir=self.test_dir)

        ticker_dir = os.path.join(self.test_dir, "AAPL")
        os.makedirs(ticker_dir)
        with open(os.path.join(ticker_dir, "2026-04.json"), "w") as f:
            json.dump({"ticker": "AAPL", "month": "2026-04", "data": []}, f)

        df = pd.DataFrame({
            "date": ["2026-04-01"],
            "open": [200.0],
            "high": [210.0],
            "low": [195.0],
            "close": [205.0],
            "volume": [50000000],
        })
        manager = self._make_manager(df=df, source_name="yfinance")

        with patch(
            "processor.us_daily.agg_fetcher.generate_months", return_value=["2026-04"]
        ):
            with patch(
                "processor.us_daily.agg_fetcher.is_current_month", return_value=True
            ):
                result = fetch_ticker_aggs(manager, "AAPL", config)

        manager.fetch_daily.assert_called_once()
        self.assertEqual(result["failures"], [])

    def test_records_failure_when_all_sources_fail(self):
        from processor.us_daily.agg_fetcher import fetch_ticker_aggs
        from processor.us_daily.config import Config
        from processor.us_daily.sources.manager import FetchError

        config = Config(start_date="2020-01", daily_dir=self.test_dir, max_retries=2)

        manager = self._make_manager(
            error=FetchError("All sources failed for AAPL")
        )

        with patch(
            "processor.us_daily.agg_fetcher.generate_months", return_value=["2020-01"]
        ):
            with patch(
                "processor.us_daily.agg_fetcher.is_current_month", return_value=False
            ):
                result = fetch_ticker_aggs(manager, "AAPL", config)

        self.assertEqual(len(result["failures"]), 1)
        self.assertEqual(result["failures"][0]["ticker"], "AAPL")
        self.assertEqual(result["failures"][0]["month"], "2020-01")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_us_daily/test_agg_fetcher.py::TestFetchTickerAggs -v`
Expected: FAIL — `fetch_ticker_aggs` still expects `client` as first arg, not `manager`.

- [ ] **Step 3: Rewrite agg_fetcher.py to use SourceManager**

Replace `src/processor/us_daily/agg_fetcher.py` with:

```python
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
        config: Config with daily_dir, start_date, max_retries.

    Returns:
        Dict with "failures" list of failed months.
    """
    months = generate_months(config.start_date, current_month())
    failures = []

    for month in months:
        file_path = get_month_file_path(config.daily_dir, ticker, month)

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
```

- [ ] **Step 4: Run all agg_fetcher tests**

Run: `pytest tests/test_us_daily/test_agg_fetcher.py -v`
Expected: All tests PASS (including `TestGenerateMonths`, `TestMonthBounds`, `TestIsCurrentMonth`, and the updated `TestFetchTickerAggs`).

- [ ] **Step 5: Commit**

```bash
git add src/processor/us_daily/agg_fetcher.py tests/test_us_daily/test_agg_fetcher.py
git commit -m "refactor: update agg_fetcher to use SourceManager with failover"
```

---

### Task 9: Update __main__.py and delete ticker_filter.py

**Files:**
- Modify: `src/processor/us_daily/__main__.py`
- Delete: `src/processor/us_daily/ticker_filter.py`
- Delete: `tests/test_us_daily/test_ticker_filter.py`

- [ ] **Step 1: Rewrite __main__.py**

Replace `src/processor/us_daily/__main__.py` with:

```python
import logging
import os
import sys

from massive import RESTClient

from processor.us_daily.config import load_config
from processor.us_daily.ticker_lister import list_tickers_for_exchange, EXCHANGES
from processor.us_daily.agg_fetcher import fetch_ticker_aggs
from processor.us_daily.sources.akshare_source import AkshareSource
from processor.us_daily.sources.yfinance_source import YfinanceSource
from processor.us_daily.sources.massive_source import MassiveSource
from processor.us_daily.sources.manager import SourceManager
from processor.us_daily.storage import get_list_file_path, load_json, file_exists


SOURCE_CLASSES = {
    "akshare": AkshareSource,
    "yfinance": YfinanceSource,
    "massive": MassiveSource,
}


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("us_daily")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler("logs/us_daily.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def build_source_manager(config, client) -> SourceManager:
    """Build SourceManager from config priority list."""
    interval_map = {
        "akshare": config.akshare_interval,
        "yfinance": config.yfinance_interval,
        "massive": config.massive_interval,
    }
    sources = []
    for name in config.data_source_priority:
        cls = SOURCE_CLASSES.get(name)
        if cls is None:
            continue
        if name == "massive":
            sources.append(cls(client=client, request_interval=interval_map[name]))
        else:
            sources.append(cls(request_interval=interval_map[name]))
    return SourceManager(sources)


def load_all_tickers(config) -> list:
    """Load tickers from all exchange files in list_dir."""
    all_tickers = []
    seen = set()
    for exchange_name in config.exchanges:
        file_path = get_list_file_path(config.list_dir, exchange_name)
        if not file_exists(file_path):
            continue
        data = load_json(file_path)
        for t in data.get("tickers", []):
            ticker = t["ticker"]
            if ticker not in seen:
                seen.add(ticker)
                all_tickers.append(t)
    return all_tickers


def main():
    logger = setup_logging()
    config = load_config()

    logger.info("=== US Daily Data Fetcher Started ===")
    logger.info(f"Config: {config}")

    client = RESTClient()

    # Step 1: Fetch ticker lists per exchange
    if config.refresh_tickers or any(
        not file_exists(get_list_file_path(config.list_dir, ex))
        for ex in config.exchanges
    ):
        for exchange_name in config.exchanges:
            if exchange_name not in EXCHANGES:
                logger.warning(f"Unknown exchange: {exchange_name}, skipping")
                continue
            logger.info(f"Fetching ticker list for {exchange_name}...")
            list_tickers_for_exchange(client, exchange_name, config)

    # Load all tickers
    tickers = load_all_tickers(config)
    logger.info(f"Total tickers loaded: {len(tickers)}")

    # Step 2: Fetch daily data
    source_manager = build_source_manager(config, client)

    all_failures = []
    total = len(tickers)
    for i, ticker_info in enumerate(tickers):
        ticker = ticker_info["ticker"]
        logger.info(f"[{i + 1}/{total}] Processing {ticker}")
        result = fetch_ticker_aggs(source_manager, ticker, config)
        if result["failures"]:
            all_failures.extend(result["failures"])

    # Step 3: Summary
    logger.info("=== Summary ===")
    logger.info(f"Total tickers: {total}")
    if all_failures:
        logger.warning(f"Failed months: {len(all_failures)}")
        for f in all_failures:
            logger.warning(f"  - {f['ticker']} {f['month']}: {f['error']}")
    else:
        logger.info("All data fetched successfully")
    logger.info("=== Done ===")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Delete old ticker_filter.py and its tests**

```bash
git rm src/processor/us_daily/ticker_filter.py
git rm tests/test_us_daily/test_ticker_filter.py
```

- [ ] **Step 3: Run full test suite to verify nothing is broken**

Run: `pytest tests/test_us_daily/ -v`
Expected: All tests PASS. No imports reference `ticker_filter`.

- [ ] **Step 4: Commit**

```bash
git add src/processor/us_daily/__main__.py
git commit -m "refactor: update __main__.py with SourceManager and remove ticker_filter"
```

---

### Task 10: Run full test suite and verify

- [ ] **Step 1: Run all us_daily tests**

```bash
pytest tests/test_us_daily/ -v
```

Expected: All tests PASS.

- [ ] **Step 2: Run import smoke test**

```bash
python -c "
from processor.us_daily.config import Config, load_config
from processor.us_daily.sources import SourceManager, FetchError
from processor.us_daily.sources.base import BaseSource, STANDARD_COLUMNS
from processor.us_daily.sources.akshare_source import AkshareSource
from processor.us_daily.sources.yfinance_source import YfinanceSource
from processor.us_daily.sources.massive_source import MassiveSource
from processor.us_daily.ticker_lister import list_tickers_for_exchange, EXCHANGES
from processor.us_daily.agg_fetcher import fetch_ticker_aggs
print('All imports OK')
print(f'STANDARD_COLUMNS: {STANDARD_COLUMNS}')
print(f'EXCHANGES: {EXCHANGES}')
print(f'Default config: {Config()}')
"
```

Expected: `All imports OK` with correct values printed.

- [ ] **Step 3: Verify no remaining references to deleted code**

```bash
grep -r "ticker_filter\|market_cap_min\|top_tickers\|data_dir\|request_interval" src/processor/us_daily/ --include="*.py"
```

Expected: No references to `ticker_filter`, `market_cap_min`, `top_tickers`, or the old `data_dir`/`request_interval` fields.

- [ ] **Step 4: Commit if any fixups needed**

If any issues found in steps 1-3, fix them and commit:

```bash
git add -A src/processor/us_daily/ tests/test_us_daily/
git commit -m "fix: resolve remaining issues from us_daily refactor"
```
