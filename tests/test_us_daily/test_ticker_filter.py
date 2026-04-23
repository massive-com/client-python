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
        from data_provider.us_daily.ticker_filter import filter_top_tickers
        from data_provider.us_daily.config import Config

        config = Config(market_cap_min=5e9, request_interval=0)

        client = MagicMock()
        # list_tickers returns different tickers per exchange
        client.list_tickers.return_value = iter(
            [
                self._make_ticker("AAPL", "XNAS"),
                self._make_ticker("TINY", "XNAS"),
            ]
        )

        # get_ticker_details: AAPL has large cap, TINY does not
        def mock_details(ticker):
            if ticker == "AAPL":
                return self._make_details("AAPL", "Apple Inc.", 3e12, "XNAS")
            elif ticker == "TINY":
                return self._make_details("TINY", "Tiny Corp", 1e9, "XNAS")

        client.get_ticker_details.side_effect = mock_details

        with patch("data_provider.us_daily.ticker_filter.EXCHANGES", ["XNAS"]):
            with patch("data_provider.us_daily.ticker_filter.time.sleep"):
                result = filter_top_tickers(client, config)

        tickers = [t["ticker"] for t in result]
        self.assertIn("AAPL", tickers)
        self.assertNotIn("TINY", tickers)

    def test_filter_top_tickers_includes_required_fields(self):
        from data_provider.us_daily.ticker_filter import filter_top_tickers
        from data_provider.us_daily.config import Config

        config = Config(market_cap_min=5e9, request_interval=0)

        client = MagicMock()
        client.list_tickers.return_value = iter(
            [
                self._make_ticker("MSFT", "XNYS"),
            ]
        )
        client.get_ticker_details.return_value = self._make_details(
            "MSFT", "Microsoft Corporation", 2.8e12, "XNYS"
        )

        with patch("data_provider.us_daily.ticker_filter.EXCHANGES", ["XNYS"]):
            with patch("data_provider.us_daily.ticker_filter.time.sleep"):
                result = filter_top_tickers(client, config)

        self.assertEqual(len(result), 1)
        entry = result[0]
        self.assertEqual(entry["ticker"], "MSFT")
        self.assertEqual(entry["name"], "Microsoft Corporation")
        self.assertEqual(entry["market_cap"], 2.8e12)
        self.assertEqual(entry["exchange"], "XNYS")

    def test_filter_skips_ticker_on_details_error(self):
        from data_provider.us_daily.ticker_filter import filter_top_tickers
        from data_provider.us_daily.config import Config

        config = Config(market_cap_min=5e9, request_interval=0)

        client = MagicMock()
        client.list_tickers.return_value = iter(
            [
                self._make_ticker("FAIL", "XNAS"),
                self._make_ticker("AAPL", "XNAS"),
            ]
        )

        def mock_details(ticker):
            if ticker == "FAIL":
                raise Exception("API error")
            return self._make_details("AAPL", "Apple Inc.", 3e12, "XNAS")

        client.get_ticker_details.side_effect = mock_details

        with patch("data_provider.us_daily.ticker_filter.EXCHANGES", ["XNAS"]):
            with patch("data_provider.us_daily.ticker_filter.time.sleep"):
                result = filter_top_tickers(client, config)

        tickers = [t["ticker"] for t in result]
        self.assertIn("AAPL", tickers)
        self.assertNotIn("FAIL", tickers)


if __name__ == "__main__":
    unittest.main()
