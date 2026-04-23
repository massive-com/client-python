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
