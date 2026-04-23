import unittest
import json
import os
import tempfile


class TestConfig(unittest.TestCase):
    def test_default_config(self):
        from processor.us_daily.config import Config

        config = Config()
        self.assertEqual(config.refresh_tickers, False)
        self.assertEqual(config.market_cap_min, 5e9)
        self.assertEqual(config.start_date, "2026-01")
        self.assertEqual(config.request_interval, 12)
        self.assertEqual(config.data_dir, "data/us_daily")
        self.assertEqual(config.max_retries, 3)

    def test_load_config_from_file(self):
        from processor.us_daily.config import load_config

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"refresh_tickers": True, "market_cap_min": 1e10}, f)
            tmp_path = f.name

        try:
            config = load_config(tmp_path)
            self.assertEqual(config.refresh_tickers, True)
            self.assertEqual(config.market_cap_min, 1e10)
            # defaults preserved for unspecified fields
            self.assertEqual(config.start_date, "2026-01")
            self.assertEqual(config.request_interval, 12)
        finally:
            os.unlink(tmp_path)

    def test_load_config_missing_file_uses_defaults(self):
        from processor.us_daily.config import load_config

        config = load_config("/nonexistent/path/config.json")
        self.assertEqual(config.refresh_tickers, False)
        self.assertEqual(config.market_cap_min, 5e9)


if __name__ == "__main__":
    unittest.main()
