import unittest
from unittest.mock import MagicMock, patch, call
import os
import tempfile
import shutil
import json
from datetime import date


class TestGenerateYears(unittest.TestCase):
    def test_generate_years_basic(self):
        from processor.us_daily.agg_fetcher import generate_years

        result = generate_years(2024, 2026)
        self.assertEqual(result, [2024, 2025, 2026])

    def test_generate_years_single(self):
        from processor.us_daily.agg_fetcher import generate_years

        result = generate_years(2024, 2024)
        self.assertEqual(result, [2024])


class TestYearBounds(unittest.TestCase):
    def test_year_bounds(self):
        from processor.us_daily.agg_fetcher import get_year_bounds

        start, end = get_year_bounds(2024)
        self.assertEqual(start, "2024-01-01")
        self.assertEqual(end, "2024-12-31")


class TestIsCurrentYear(unittest.TestCase):
    @patch("processor.us_daily.agg_fetcher.date")
    def test_is_current_year_true(self, mock_date):
        from processor.us_daily.agg_fetcher import is_current_year

        mock_date.today.return_value = date(2026, 4, 22)
        self.assertTrue(is_current_year(2026))

    @patch("processor.us_daily.agg_fetcher.date")
    def test_is_current_year_false(self, mock_date):
        from processor.us_daily.agg_fetcher import is_current_year

        mock_date.today.return_value = date(2026, 4, 22)
        self.assertFalse(is_current_year(2025))


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

    def test_skips_existing_historical_year(self):
        from processor.us_daily.agg_fetcher import fetch_ticker_aggs
        from processor.us_daily.config import Config

        config = Config(start_year=2024, daily_data_dir=self.test_dir)

        ticker_dir = os.path.join(self.test_dir, "AAPL")
        os.makedirs(ticker_dir)
        with open(os.path.join(ticker_dir, "2024.json"), "w") as f:
            json.dump({"ticker": "AAPL", "year": 2024, "data": []}, f)

        manager = self._make_manager()

        with patch(
            "processor.us_daily.agg_fetcher.generate_years", return_value=[2024]
        ):
            with patch(
                "processor.us_daily.agg_fetcher.is_current_year", return_value=False
            ):
                result = fetch_ticker_aggs(manager, "AAPL", config)

        manager.fetch_daily.assert_not_called()
        self.assertEqual(result["failures"], [])

    def test_fetches_missing_year(self):
        from processor.us_daily.agg_fetcher import fetch_ticker_aggs
        from processor.us_daily.config import Config
        import pandas as pd

        config = Config(start_year=2024, daily_data_dir=self.test_dir)

        df = pd.DataFrame({
            "date": ["2024-01-02"],
            "open": [74.06],
            "high": [75.15],
            "low": [73.80],
            "close": [74.36],
            "volume": [108872000],
        })
        manager = self._make_manager(df=df, source_name="akshare")

        with patch(
            "processor.us_daily.agg_fetcher.generate_years", return_value=[2024]
        ):
            with patch(
                "processor.us_daily.agg_fetcher.is_current_year", return_value=False
            ):
                result = fetch_ticker_aggs(manager, "AAPL", config)

        file_path = os.path.join(self.test_dir, "AAPL", "2024.json")
        self.assertTrue(os.path.exists(file_path))

        with open(file_path) as f:
            data = json.load(f)
        self.assertEqual(data["ticker"], "AAPL")
        self.assertEqual(data["year"], 2024)
        self.assertEqual(data["source"], "akshare")
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["close"], 74.36)
        self.assertEqual(result["failures"], [])

    def test_refreshes_current_year(self):
        from processor.us_daily.agg_fetcher import fetch_ticker_aggs
        from processor.us_daily.config import Config
        import pandas as pd

        config = Config(start_year=2026, daily_data_dir=self.test_dir)

        ticker_dir = os.path.join(self.test_dir, "AAPL")
        os.makedirs(ticker_dir)
        with open(os.path.join(ticker_dir, "2026.json"), "w") as f:
            json.dump({"ticker": "AAPL", "year": 2026, "data": []}, f)

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
            "processor.us_daily.agg_fetcher.generate_years", return_value=[2026]
        ):
            with patch(
                "processor.us_daily.agg_fetcher.is_current_year", return_value=True
            ):
                result = fetch_ticker_aggs(manager, "AAPL", config)

        manager.fetch_daily.assert_called_once()
        self.assertEqual(result["failures"], [])

    def test_records_failure_when_all_sources_fail(self):
        from processor.us_daily.agg_fetcher import fetch_ticker_aggs
        from processor.us_daily.config import Config
        from processor.us_daily.sources.manager import FetchError

        config = Config(start_year=2024, daily_data_dir=self.test_dir, max_retries=2)

        manager = self._make_manager(
            error=FetchError("All sources failed for AAPL")
        )

        with patch(
            "processor.us_daily.agg_fetcher.generate_years", return_value=[2024]
        ):
            with patch(
                "processor.us_daily.agg_fetcher.is_current_year", return_value=False
            ):
                result = fetch_ticker_aggs(manager, "AAPL", config)

        self.assertEqual(len(result["failures"]), 1)
        self.assertEqual(result["failures"][0]["ticker"], "AAPL")
        self.assertEqual(result["failures"][0]["year"], 2024)


if __name__ == "__main__":
    unittest.main()
