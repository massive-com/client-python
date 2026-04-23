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
