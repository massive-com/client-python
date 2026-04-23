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
