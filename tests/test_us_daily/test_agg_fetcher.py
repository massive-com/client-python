import unittest
from unittest.mock import MagicMock, patch, call
import os
import tempfile
import shutil
import json
from datetime import date


class TestGenerateMonths(unittest.TestCase):
    def test_generate_months_basic(self):
        from processor.us_daily.agg_fetcher import generate_months

        result = generate_months("2020-01", "2020-04")
        self.assertEqual(result, ["2020-01", "2020-02", "2020-03", "2020-04"])

    def test_generate_months_cross_year(self):
        from processor.us_daily.agg_fetcher import generate_months

        result = generate_months("2023-11", "2024-02")
        self.assertEqual(result, ["2023-11", "2023-12", "2024-01", "2024-02"])

    def test_generate_months_single(self):
        from processor.us_daily.agg_fetcher import generate_months

        result = generate_months("2024-06", "2024-06")
        self.assertEqual(result, ["2024-06"])


class TestMonthBounds(unittest.TestCase):
    def test_month_bounds_january(self):
        from processor.us_daily.agg_fetcher import get_month_bounds

        start, end = get_month_bounds("2020-01")
        self.assertEqual(start, "2020-01-01")
        self.assertEqual(end, "2020-01-31")

    def test_month_bounds_february_leap(self):
        from processor.us_daily.agg_fetcher import get_month_bounds

        start, end = get_month_bounds("2024-02")
        self.assertEqual(start, "2024-02-01")
        self.assertEqual(end, "2024-02-29")

    def test_month_bounds_february_non_leap(self):
        from processor.us_daily.agg_fetcher import get_month_bounds

        start, end = get_month_bounds("2023-02")
        self.assertEqual(start, "2023-02-01")
        self.assertEqual(end, "2023-02-28")


class TestIsCurrentMonth(unittest.TestCase):
    @patch("processor.us_daily.agg_fetcher.date")
    def test_is_current_month_true(self, mock_date):
        from processor.us_daily.agg_fetcher import is_current_month

        mock_date.today.return_value = date(2026, 4, 22)
        self.assertTrue(is_current_month("2026-04"))

    @patch("processor.us_daily.agg_fetcher.date")
    def test_is_current_month_false(self, mock_date):
        from processor.us_daily.agg_fetcher import is_current_month

        mock_date.today.return_value = date(2026, 4, 22)
        self.assertFalse(is_current_month("2026-03"))


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


if __name__ == "__main__":
    unittest.main()
