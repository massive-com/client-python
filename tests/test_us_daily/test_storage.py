import unittest
import json
import os
import tempfile
import shutil


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_tickers_file_path(self):
        from processor.us_daily.storage import get_tickers_file_path

        result = get_tickers_file_path("data/us_daily")
        self.assertEqual(result, "data/us_daily/top_tickers.json")

    def test_get_month_file_path(self):
        from processor.us_daily.storage import get_month_file_path

        result = get_month_file_path("data/us_daily", "AAPL", "2020-01")
        self.assertEqual(result, "data/us_daily/AAPL/2020-01.json")

    def test_save_and_load_json(self):
        from processor.us_daily.storage import save_json, load_json

        file_path = os.path.join(self.test_dir, "sub", "test.json")
        data = {"key": "value", "num": 42}
        save_json(file_path, data)
        loaded = load_json(file_path)
        self.assertEqual(loaded, data)

    def test_save_json_creates_parent_dirs(self):
        from processor.us_daily.storage import save_json

        file_path = os.path.join(self.test_dir, "a", "b", "c", "test.json")
        save_json(file_path, {"x": 1})
        self.assertTrue(os.path.exists(file_path))

    def test_file_exists(self):
        from processor.us_daily.storage import file_exists

        existing = os.path.join(self.test_dir, "exists.json")
        with open(existing, "w") as f:
            f.write("{}")

        self.assertTrue(file_exists(existing))
        self.assertFalse(file_exists(os.path.join(self.test_dir, "nope.json")))


if __name__ == "__main__":
    unittest.main()
