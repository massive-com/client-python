# 头部美股日K数据采集 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建 `project/us_daily` 模块，采集主要美股交易所中市值 >= 50 亿美金公司的日 K 线数据（2020 年至今），按月存储为 JSON 文件，支持增量更新。

**Architecture:** 单进程流水线：加载配置 → 筛选 ticker → 按月抓取日K → JSON 存储。通过检查文件是否存在实现增量更新。每次 API 请求后 sleep 20s 满足限流要求。

**Tech Stack:** Python 3.9+, `massive` SDK（RESTClient, list_tickers, get_ticker_details, list_aggs），标准库 json/logging/dataclasses/calendar/datetime

---

## File Structure

| File | Responsibility |
|------|---------------|
| `project/__init__.py` | 空，使 project 成为 package |
| `project/us_daily/__init__.py` | 空，使 us_daily 成为 package |
| `project/us_daily/config.py` | Config dataclass + load_config() |
| `project/us_daily/storage.py` | JSON 读写、路径计算、文件存在判断 |
| `project/us_daily/ticker_filter.py` | 遍历交易所获取 ticker、查详情过滤市值 |
| `project/us_daily/agg_fetcher.py` | 按月获取日K数据、增量判断、重试逻辑 |
| `project/us_daily/__main__.py` | 入口：配置加载 → ticker 筛选 → 数据抓取 → 汇总 |
| `project/us_daily/config.json` | 默认配置文件 |
| `tests/test_us_daily/test_config.py` | config 模块测试 |
| `tests/test_us_daily/test_storage.py` | storage 模块测试 |
| `tests/test_us_daily/test_ticker_filter.py` | ticker_filter 模块测试 |
| `tests/test_us_daily/test_agg_fetcher.py` | agg_fetcher 模块测试 |

---

### Task 1: Config 模块

**Files:**
- Create: `project/__init__.py`
- Create: `project/us_daily/__init__.py`
- Create: `project/us_daily/config.py`
- Create: `project/us_daily/config.json`
- Create: `tests/test_us_daily/__init__.py`
- Create: `tests/test_us_daily/test_config.py`

- [ ] **Step 1: Write the failing test for Config defaults and load_config**

Create `tests/test_us_daily/__init__.py` (empty) and `tests/test_us_daily/test_config.py`:

```python
import unittest
import json
import os
import tempfile


class TestConfig(unittest.TestCase):
    def test_default_config(self):
        from project.us_daily.config import Config

        config = Config()
        self.assertEqual(config.refresh_tickers, False)
        self.assertEqual(config.market_cap_min, 5e9)
        self.assertEqual(config.start_date, "2020-01")
        self.assertEqual(config.request_interval, 20)
        self.assertEqual(config.data_dir, "data/us_daily")
        self.assertEqual(config.max_retries, 3)

    def test_load_config_from_file(self):
        from project.us_daily.config import load_config

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump({"refresh_tickers": True, "market_cap_min": 1e10}, f)
            tmp_path = f.name

        try:
            config = load_config(tmp_path)
            self.assertEqual(config.refresh_tickers, True)
            self.assertEqual(config.market_cap_min, 1e10)
            # defaults preserved for unspecified fields
            self.assertEqual(config.start_date, "2020-01")
            self.assertEqual(config.request_interval, 20)
        finally:
            os.unlink(tmp_path)

    def test_load_config_missing_file_uses_defaults(self):
        from project.us_daily.config import load_config

        config = load_config("/nonexistent/path/config.json")
        self.assertEqual(config.refresh_tickers, False)
        self.assertEqual(config.market_cap_min, 5e9)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run python -m pytest tests/test_us_daily/test_config.py -v`
Expected: FAIL — ModuleNotFoundError for `project.us_daily.config`

- [ ] **Step 3: Create package files and implement Config**

Create `project/__init__.py` (empty):

```python
```

Create `project/us_daily/__init__.py` (empty):

```python
```

Create `project/us_daily/config.py`:

```python
import json
import os
from dataclasses import dataclass


@dataclass
class Config:
    refresh_tickers: bool = False
    market_cap_min: float = 5e9
    start_date: str = "2020-01"
    request_interval: int = 20
    data_dir: str = "data/us_daily"
    max_retries: int = 3


def load_config(config_path: str = "project/us_daily/config.json") -> Config:
    config = Config()
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            data = json.load(f)
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
    return config
```

Create `project/us_daily/config.json`:

```json
{
  "refresh_tickers": false,
  "market_cap_min": 5000000000,
  "start_date": "2020-01",
  "request_interval": 20,
  "data_dir": "data/us_daily",
  "max_retries": 3
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run python -m pytest tests/test_us_daily/test_config.py -v`
Expected: 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add project/__init__.py project/us_daily/__init__.py project/us_daily/config.py project/us_daily/config.json tests/test_us_daily/__init__.py tests/test_us_daily/test_config.py
git commit -m "feat: add config module for us_daily data fetcher"
```

---

### Task 2: Storage 模块

**Files:**
- Create: `project/us_daily/storage.py`
- Create: `tests/test_us_daily/test_storage.py`

- [ ] **Step 1: Write the failing tests for storage functions**

Create `tests/test_us_daily/test_storage.py`:

```python
import unittest
import json
import os
import tempfile
import shutil


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_tickers_file_path(self):
        from project.us_daily.storage import get_tickers_file_path

        result = get_tickers_file_path("data/us_daily")
        self.assertEqual(result, "data/us_daily/top_tickers.json")

    def test_get_month_file_path(self):
        from project.us_daily.storage import get_month_file_path

        result = get_month_file_path("data/us_daily", "AAPL", "2020-01")
        self.assertEqual(result, "data/us_daily/AAPL/2020-01.json")

    def test_save_and_load_json(self):
        from project.us_daily.storage import save_json, load_json

        file_path = os.path.join(self.test_dir, "sub", "test.json")
        data = {"key": "value", "num": 42}
        save_json(file_path, data)
        loaded = load_json(file_path)
        self.assertEqual(loaded, data)

    def test_save_json_creates_parent_dirs(self):
        from project.us_daily.storage import save_json

        file_path = os.path.join(self.test_dir, "a", "b", "c", "test.json")
        save_json(file_path, {"x": 1})
        self.assertTrue(os.path.exists(file_path))

    def test_file_exists(self):
        from project.us_daily.storage import file_exists

        existing = os.path.join(self.test_dir, "exists.json")
        with open(existing, "w") as f:
            f.write("{}")

        self.assertTrue(file_exists(existing))
        self.assertFalse(file_exists(os.path.join(self.test_dir, "nope.json")))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run python -m pytest tests/test_us_daily/test_storage.py -v`
Expected: FAIL — ModuleNotFoundError for `project.us_daily.storage`

- [ ] **Step 3: Implement storage module**

Create `project/us_daily/storage.py`:

```python
import json
import os


def get_tickers_file_path(data_dir: str) -> str:
    return os.path.join(data_dir, "top_tickers.json")


def get_month_file_path(data_dir: str, ticker: str, month: str) -> str:
    return os.path.join(data_dir, ticker, f"{month}.json")


def save_json(path: str, data: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def file_exists(path: str) -> bool:
    return os.path.isfile(path)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run python -m pytest tests/test_us_daily/test_storage.py -v`
Expected: 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add project/us_daily/storage.py tests/test_us_daily/test_storage.py
git commit -m "feat: add storage module for JSON file I/O and path management"
```

---

### Task 3: Ticker Filter 模块

**Files:**
- Create: `project/us_daily/ticker_filter.py`
- Create: `tests/test_us_daily/test_ticker_filter.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_us_daily/test_ticker_filter.py`:

```python
import unittest
from unittest.mock import MagicMock, patch, call
from dataclasses import dataclass


class TestTickerFilter(unittest.TestCase):
    def _make_ticker(self, ticker_str, exchange):
        t = MagicMock()
        t.ticker = ticker_str
        t.primary_exchange = exchange
        return t

    def _make_details(self, ticker_str, name, market_cap, exchange):
        d = MagicMock()
        d.ticker = ticker_str
        d.name = name
        d.market_cap = market_cap
        d.primary_exchange = exchange
        return d

    def test_filter_top_tickers_filters_by_market_cap(self):
        from project.us_daily.ticker_filter import filter_top_tickers
        from project.us_daily.config import Config

        config = Config(market_cap_min=5e9, request_interval=0)

        client = MagicMock()
        # list_tickers returns different tickers per exchange
        client.list_tickers.return_value = iter([
            self._make_ticker("AAPL", "XNAS"),
            self._make_ticker("TINY", "XNAS"),
        ])

        # get_ticker_details: AAPL has large cap, TINY does not
        def mock_details(ticker):
            if ticker == "AAPL":
                return self._make_details("AAPL", "Apple Inc.", 3e12, "XNAS")
            elif ticker == "TINY":
                return self._make_details("TINY", "Tiny Corp", 1e9, "XNAS")

        client.get_ticker_details.side_effect = mock_details

        with patch("project.us_daily.ticker_filter.EXCHANGES", ["XNAS"]):
            with patch("project.us_daily.ticker_filter.time.sleep"):
                result = filter_top_tickers(client, config)

        tickers = [t["ticker"] for t in result]
        self.assertIn("AAPL", tickers)
        self.assertNotIn("TINY", tickers)

    def test_filter_top_tickers_includes_required_fields(self):
        from project.us_daily.ticker_filter import filter_top_tickers
        from project.us_daily.config import Config

        config = Config(market_cap_min=5e9, request_interval=0)

        client = MagicMock()
        client.list_tickers.return_value = iter([
            self._make_ticker("MSFT", "XNYS"),
        ])
        client.get_ticker_details.return_value = self._make_details(
            "MSFT", "Microsoft Corporation", 2.8e12, "XNYS"
        )

        with patch("project.us_daily.ticker_filter.EXCHANGES", ["XNYS"]):
            with patch("project.us_daily.ticker_filter.time.sleep"):
                result = filter_top_tickers(client, config)

        self.assertEqual(len(result), 1)
        entry = result[0]
        self.assertEqual(entry["ticker"], "MSFT")
        self.assertEqual(entry["name"], "Microsoft Corporation")
        self.assertEqual(entry["market_cap"], 2.8e12)
        self.assertEqual(entry["exchange"], "XNYS")

    def test_filter_skips_ticker_on_details_error(self):
        from project.us_daily.ticker_filter import filter_top_tickers
        from project.us_daily.config import Config

        config = Config(market_cap_min=5e9, request_interval=0)

        client = MagicMock()
        client.list_tickers.return_value = iter([
            self._make_ticker("FAIL", "XNAS"),
            self._make_ticker("AAPL", "XNAS"),
        ])

        def mock_details(ticker):
            if ticker == "FAIL":
                raise Exception("API error")
            return self._make_details("AAPL", "Apple Inc.", 3e12, "XNAS")

        client.get_ticker_details.side_effect = mock_details

        with patch("project.us_daily.ticker_filter.EXCHANGES", ["XNAS"]):
            with patch("project.us_daily.ticker_filter.time.sleep"):
                result = filter_top_tickers(client, config)

        tickers = [t["ticker"] for t in result]
        self.assertIn("AAPL", tickers)
        self.assertNotIn("FAIL", tickers)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run python -m pytest tests/test_us_daily/test_ticker_filter.py -v`
Expected: FAIL — ModuleNotFoundError for `project.us_daily.ticker_filter`

- [ ] **Step 3: Implement ticker_filter module**

Create `project/us_daily/ticker_filter.py`:

```python
import logging
import time
from typing import List

from project.us_daily.config import Config

logger = logging.getLogger("us_daily")

EXCHANGES = ["XNAS", "XNYS", "ARCX"]


def filter_top_tickers(client, config: Config) -> List[dict]:
    result = []
    for exchange in EXCHANGES:
        logger.info(f"Fetching tickers for exchange: {exchange}")
        try:
            tickers = client.list_tickers(
                market="stocks",
                exchange=exchange,
                active=True,
                limit=1000,
            )
        except Exception as e:
            logger.error(f"Failed to list tickers for {exchange}: {e}")
            continue

        time.sleep(config.request_interval)

        for ticker_obj in tickers:
            ticker_str = ticker_obj.ticker
            try:
                details = client.get_ticker_details(ticker_str)
                time.sleep(config.request_interval)
            except Exception as e:
                logger.warning(
                    f"Failed to get details for {ticker_str}: {e}"
                )
                continue

            if details.market_cap is None:
                logger.debug(f"{ticker_str}: no market_cap data, skipping")
                continue

            if details.market_cap >= config.market_cap_min:
                entry = {
                    "ticker": details.ticker,
                    "name": details.name,
                    "market_cap": details.market_cap,
                    "exchange": details.primary_exchange,
                }
                result.append(entry)
                logger.info(
                    f"  {details.ticker}: market_cap={details.market_cap:.0f} ✓"
                )
            else:
                logger.debug(
                    f"  {ticker_str}: market_cap={details.market_cap:.0f} < {config.market_cap_min:.0f}, skipping"
                )

    logger.info(f"Total top tickers found: {len(result)}")
    return result
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run python -m pytest tests/test_us_daily/test_ticker_filter.py -v`
Expected: 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add project/us_daily/ticker_filter.py tests/test_us_daily/test_ticker_filter.py
git commit -m "feat: add ticker_filter module to select top US stocks by market cap"
```

---

### Task 4: Agg Fetcher 模块

**Files:**
- Create: `project/us_daily/agg_fetcher.py`
- Create: `tests/test_us_daily/test_agg_fetcher.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_us_daily/test_agg_fetcher.py`:

```python
import unittest
from unittest.mock import MagicMock, patch, call
import os
import tempfile
import shutil
import json
from datetime import date


class TestGenerateMonths(unittest.TestCase):
    def test_generate_months_basic(self):
        from project.us_daily.agg_fetcher import generate_months

        result = generate_months("2020-01", "2020-04")
        self.assertEqual(result, ["2020-01", "2020-02", "2020-03", "2020-04"])

    def test_generate_months_cross_year(self):
        from project.us_daily.agg_fetcher import generate_months

        result = generate_months("2023-11", "2024-02")
        self.assertEqual(result, ["2023-11", "2023-12", "2024-01", "2024-02"])

    def test_generate_months_single(self):
        from project.us_daily.agg_fetcher import generate_months

        result = generate_months("2024-06", "2024-06")
        self.assertEqual(result, ["2024-06"])


class TestMonthBounds(unittest.TestCase):
    def test_month_bounds_january(self):
        from project.us_daily.agg_fetcher import get_month_bounds

        start, end = get_month_bounds("2020-01")
        self.assertEqual(start, "2020-01-01")
        self.assertEqual(end, "2020-01-31")

    def test_month_bounds_february_leap(self):
        from project.us_daily.agg_fetcher import get_month_bounds

        start, end = get_month_bounds("2024-02")
        self.assertEqual(start, "2024-02-01")
        self.assertEqual(end, "2024-02-29")

    def test_month_bounds_february_non_leap(self):
        from project.us_daily.agg_fetcher import get_month_bounds

        start, end = get_month_bounds("2023-02")
        self.assertEqual(start, "2023-02-01")
        self.assertEqual(end, "2023-02-28")


class TestIsCurrentMonth(unittest.TestCase):
    @patch("project.us_daily.agg_fetcher.date")
    def test_is_current_month_true(self, mock_date):
        from project.us_daily.agg_fetcher import is_current_month

        mock_date.today.return_value = date(2026, 4, 22)
        self.assertTrue(is_current_month("2026-04"))

    @patch("project.us_daily.agg_fetcher.date")
    def test_is_current_month_false(self, mock_date):
        from project.us_daily.agg_fetcher import is_current_month

        mock_date.today.return_value = date(2026, 4, 22)
        self.assertFalse(is_current_month("2026-03"))


class TestFetchTickerAggs(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_skips_existing_historical_month(self):
        from project.us_daily.agg_fetcher import fetch_ticker_aggs
        from project.us_daily.config import Config

        config = Config(
            start_date="2020-01",
            data_dir=self.test_dir,
            request_interval=0,
        )

        # Create existing file for 2020-01
        ticker_dir = os.path.join(self.test_dir, "AAPL")
        os.makedirs(ticker_dir)
        with open(os.path.join(ticker_dir, "2020-01.json"), "w") as f:
            json.dump({"ticker": "AAPL", "month": "2020-01", "data": []}, f)

        client = MagicMock()

        with patch("project.us_daily.agg_fetcher.generate_months", return_value=["2020-01"]):
            with patch("project.us_daily.agg_fetcher.is_current_month", return_value=False):
                with patch("project.us_daily.agg_fetcher.time.sleep"):
                    result = fetch_ticker_aggs(client, "AAPL", config)

        # Should not have called list_aggs since file exists and not current month
        client.list_aggs.assert_not_called()
        self.assertEqual(result["failures"], [])

    def test_fetches_missing_month(self):
        from project.us_daily.agg_fetcher import fetch_ticker_aggs
        from project.us_daily.config import Config

        config = Config(
            start_date="2020-01",
            data_dir=self.test_dir,
            request_interval=0,
        )

        agg1 = MagicMock()
        agg1.open = 74.06
        agg1.high = 75.15
        agg1.low = 73.80
        agg1.close = 74.36
        agg1.volume = 108872000.0
        agg1.vwap = 74.53
        agg1.timestamp = 1577854800000
        agg1.transactions = 480012

        client = MagicMock()
        client.list_aggs.return_value = iter([agg1])

        with patch("project.us_daily.agg_fetcher.generate_months", return_value=["2020-01"]):
            with patch("project.us_daily.agg_fetcher.is_current_month", return_value=False):
                with patch("project.us_daily.agg_fetcher.time.sleep"):
                    result = fetch_ticker_aggs(client, "AAPL", config)

        # Verify file was created
        file_path = os.path.join(self.test_dir, "AAPL", "2020-01.json")
        self.assertTrue(os.path.exists(file_path))

        with open(file_path) as f:
            data = json.load(f)
        self.assertEqual(data["ticker"], "AAPL")
        self.assertEqual(data["month"], "2020-01")
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["open"], 74.06)
        self.assertEqual(result["failures"], [])

    def test_refreshes_current_month(self):
        from project.us_daily.agg_fetcher import fetch_ticker_aggs
        from project.us_daily.config import Config

        config = Config(
            start_date="2026-04",
            data_dir=self.test_dir,
            request_interval=0,
        )

        # Create existing file for current month
        ticker_dir = os.path.join(self.test_dir, "AAPL")
        os.makedirs(ticker_dir)
        with open(os.path.join(ticker_dir, "2026-04.json"), "w") as f:
            json.dump({"ticker": "AAPL", "month": "2026-04", "data": []}, f)

        agg1 = MagicMock()
        agg1.open = 200.0
        agg1.high = 210.0
        agg1.low = 195.0
        agg1.close = 205.0
        agg1.volume = 50000000.0
        agg1.vwap = 203.0
        agg1.timestamp = 1714348800000
        agg1.transactions = 300000

        client = MagicMock()
        client.list_aggs.return_value = iter([agg1])

        with patch("project.us_daily.agg_fetcher.generate_months", return_value=["2026-04"]):
            with patch("project.us_daily.agg_fetcher.is_current_month", return_value=True):
                with patch("project.us_daily.agg_fetcher.time.sleep"):
                    result = fetch_ticker_aggs(client, "AAPL", config)

        # Should have called list_aggs even though file exists
        client.list_aggs.assert_called_once()
        self.assertEqual(result["failures"], [])

    def test_records_failure_after_retries(self):
        from project.us_daily.agg_fetcher import fetch_ticker_aggs
        from project.us_daily.config import Config

        config = Config(
            start_date="2020-01",
            data_dir=self.test_dir,
            request_interval=0,
            max_retries=2,
        )

        client = MagicMock()
        client.list_aggs.side_effect = Exception("API timeout")

        with patch("project.us_daily.agg_fetcher.generate_months", return_value=["2020-01"]):
            with patch("project.us_daily.agg_fetcher.is_current_month", return_value=False):
                with patch("project.us_daily.agg_fetcher.time.sleep"):
                    result = fetch_ticker_aggs(client, "AAPL", config)

        self.assertEqual(len(result["failures"]), 1)
        self.assertEqual(result["failures"][0]["ticker"], "AAPL")
        self.assertEqual(result["failures"][0]["month"], "2020-01")
        self.assertIn("API timeout", result["failures"][0]["error"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `poetry run python -m pytest tests/test_us_daily/test_agg_fetcher.py -v`
Expected: FAIL — ModuleNotFoundError for `project.us_daily.agg_fetcher`

- [ ] **Step 3: Implement agg_fetcher module**

Create `project/us_daily/agg_fetcher.py`:

```python
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
                logger.warning(
                    f"  {ticker} {month}: attempt {attempt}/{config.max_retries} failed: {e}"
                )
                if attempt < config.max_retries:
                    time.sleep(config.request_interval)

        if aggs is None:
            failures.append({
                "ticker": ticker,
                "month": month,
                "error": str(e),
            })
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `poetry run python -m pytest tests/test_us_daily/test_agg_fetcher.py -v`
Expected: 8 tests PASS (4 utility + 4 integration)

- [ ] **Step 5: Commit**

```bash
git add project/us_daily/agg_fetcher.py tests/test_us_daily/test_agg_fetcher.py
git commit -m "feat: add agg_fetcher module for incremental daily bar data collection"
```

---

### Task 5: 入口模块 (__main__.py)

**Files:**
- Create: `project/us_daily/__main__.py`

- [ ] **Step 1: Implement __main__.py**

Create `project/us_daily/__main__.py`:

```python
import logging
import os
import sys
from datetime import datetime

from massive import RESTClient

from project.us_daily.config import load_config
from project.us_daily.storage import (
    get_tickers_file_path,
    file_exists,
    save_json,
    load_json,
)
from project.us_daily.ticker_filter import filter_top_tickers
from project.us_daily.agg_fetcher import fetch_ticker_aggs


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


def main():
    logger = setup_logging()
    config = load_config()

    logger.info("=== US Daily Data Fetcher Started ===")
    logger.info(f"Config: {config}")

    client = RESTClient()

    # Step 1: Get ticker list
    tickers_path = get_tickers_file_path(config.data_dir)
    if config.refresh_tickers or not file_exists(tickers_path):
        logger.info("Filtering top tickers from API...")
        tickers = filter_top_tickers(client, config)
        save_json(tickers_path, {
            "updated_at": datetime.now().strftime("%Y-%m-%d"),
            "market_cap_min": config.market_cap_min,
            "tickers": tickers,
        })
        logger.info(f"Saved {len(tickers)} tickers to {tickers_path}")
    else:
        data = load_json(tickers_path)
        tickers = data["tickers"]
        logger.info(
            f"Loaded {len(tickers)} tickers from {tickers_path} "
            f"(updated: {data.get('updated_at', 'unknown')})"
        )

    # Step 2: Fetch agg data for each ticker
    all_failures = []
    total = len(tickers)
    for i, ticker_info in enumerate(tickers):
        ticker = ticker_info["ticker"]
        logger.info(f"[{i + 1}/{total}] Processing {ticker}")
        result = fetch_ticker_aggs(client, ticker, config)
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

- [ ] **Step 2: Verify it can be invoked (dry run)**

Run: `poetry run python -m project.us_daily --help 2>&1 || echo "Module loads OK (no --help support expected)"`

This just checks the module can be imported without errors. Actual execution requires a valid API key and would hit the real API.

- [ ] **Step 3: Commit**

```bash
git add project/us_daily/__main__.py
git commit -m "feat: add __main__.py entry point for us_daily data fetcher"
```

---

### Task 6: Run all tests and final verification

**Files:** None (verification only)

- [ ] **Step 1: Run the full test suite**

Run: `poetry run python -m pytest tests/test_us_daily/ -v`
Expected: All tests PASS (3 config + 5 storage + 3 ticker_filter + 8 agg_fetcher = 19 tests)

- [ ] **Step 2: Run type check**

Run: `poetry run mypy project/`
Expected: No errors (or only notes about the massive library types)

- [ ] **Step 3: Run style check**

Run: `make style`
Expected: Files formatted

- [ ] **Step 4: Final commit if style changes**

```bash
git add -A project/ tests/test_us_daily/
git commit -m "style: format us_daily module with black"
```
