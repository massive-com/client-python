import unittest
import json
import os
import tempfile


class TestConfig(unittest.TestCase):
    def test_default_config(self):
        from processor.us_daily.config import Config

        config = Config()
        self.assertEqual(config.refresh_tickers, False)
        self.assertEqual(config.start_date, "2026-01")
        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.exchanges, ["nasdaq", "nyse", "arca"])
        self.assertEqual(config.data_source_priority, ["akshare", "yfinance", "massive"])
        self.assertEqual(config.akshare_interval, 2.0)
        self.assertEqual(config.yfinance_interval, 1.0)
        self.assertEqual(config.massive_interval, 12.0)
        self.assertEqual(config.list_dir, "data/us_list")
        self.assertEqual(config.daily_dir, "data/us_daily")

    def test_load_config_from_file(self):
        from processor.us_daily.config import load_config

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({
                "refresh_tickers": True,
                "akshare_interval": 3.0,
                "exchanges": ["nasdaq"],
            }, f)
            tmp_path = f.name

        try:
            config = load_config(tmp_path)
            self.assertEqual(config.refresh_tickers, True)
            self.assertEqual(config.akshare_interval, 3.0)
            self.assertEqual(config.exchanges, ["nasdaq"])
            # defaults preserved for unspecified fields
            self.assertEqual(config.start_date, "2026-01")
            self.assertEqual(config.massive_interval, 12.0)
        finally:
            os.unlink(tmp_path)

    def test_load_config_missing_file_uses_defaults(self):
        from processor.us_daily.config import load_config

        config = load_config("/nonexistent/path/config.json")
        self.assertEqual(config.refresh_tickers, False)
        self.assertEqual(config.data_source_priority, ["akshare", "yfinance", "massive"])


if __name__ == "__main__":
    unittest.main()
