import unittest
from unittest.mock import MagicMock, patch, call
from types import SimpleNamespace
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
        """Create a SimpleNamespace TickerDetails with all fields as attributes."""
        return SimpleNamespace(**kwargs)

    def test_list_tickers_for_exchange(self):
        from processor.us_daily.ticker_lister import list_tickers_for_exchange
        from processor.us_daily.config import Config

        config = Config(list_data_dir=self.test_dir, massive_interval=0)

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

        config = Config(list_data_dir=self.test_dir, massive_interval=0)

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

        config = Config(list_data_dir=self.test_dir, massive_interval=0)

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
