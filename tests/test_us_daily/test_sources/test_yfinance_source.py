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
