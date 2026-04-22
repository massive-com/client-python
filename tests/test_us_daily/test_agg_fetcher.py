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

        with patch(
            "project.us_daily.agg_fetcher.generate_months", return_value=["2020-01"]
        ):
            with patch(
                "project.us_daily.agg_fetcher.is_current_month", return_value=False
            ):
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

        with patch(
            "project.us_daily.agg_fetcher.generate_months", return_value=["2020-01"]
        ):
            with patch(
                "project.us_daily.agg_fetcher.is_current_month", return_value=False
            ):
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

        with patch(
            "project.us_daily.agg_fetcher.generate_months", return_value=["2026-04"]
        ):
            with patch(
                "project.us_daily.agg_fetcher.is_current_month", return_value=True
            ):
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

        with patch(
            "project.us_daily.agg_fetcher.generate_months", return_value=["2020-01"]
        ):
            with patch(
                "project.us_daily.agg_fetcher.is_current_month", return_value=False
            ):
                with patch("project.us_daily.agg_fetcher.time.sleep"):
                    result = fetch_ticker_aggs(client, "AAPL", config)

        self.assertEqual(len(result["failures"]), 1)
        self.assertEqual(result["failures"][0]["ticker"], "AAPL")
        self.assertEqual(result["failures"][0]["month"], "2020-01")
        self.assertIn("API timeout", result["failures"][0]["error"])


if __name__ == "__main__":
    unittest.main()
