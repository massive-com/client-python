import unittest
from unittest.mock import patch, MagicMock
import pandas as pd


class TestToUsEmSymbol(unittest.TestCase):
    """测试美股东财代码格式转换"""

    def _make_fetcher(self):
        with patch("provider.akshare_fetcher.get_config") as mock_cfg:
            mock_cfg.return_value.enable_eastmoney_patch = False
            from provider.akshare_fetcher import AkshareFetcher
            return AkshareFetcher(sleep_min=0, sleep_max=0)

    def test_cache_hit(self):
        """缓存命中时直接返回，不调用 stock_us_spot_em"""
        fetcher = self._make_fetcher()
        fetcher._us_code_map = {"AAPL": "105.AAPL", "TSLA": "105.TSLA"}

        with patch("akshare.stock_us_spot_em") as mock_spot:
            result = fetcher._to_us_em_symbol("AAPL")

        self.assertEqual(result, "105.AAPL")
        mock_spot.assert_not_called()

    def test_cache_miss_builds_map(self):
        """缓存为空时调用 stock_us_spot_em 构建映射"""
        fetcher = self._make_fetcher()

        spot_df = pd.DataFrame({
            "代码": ["105.AAPL", "106.BAC", "105.TSLA"],
            "名称": ["苹果", "美国银行", "特斯拉"],
        })

        with patch("akshare.stock_us_spot_em", return_value=spot_df):
            result = fetcher._to_us_em_symbol("AAPL")

        self.assertEqual(result, "105.AAPL")
        self.assertEqual(fetcher._us_code_map["TSLA"], "105.TSLA")

    def test_ticker_not_found_returns_none(self):
        """ticker 不在映射表中返回 None"""
        fetcher = self._make_fetcher()
        fetcher._us_code_map = {"AAPL": "105.AAPL"}

        result = fetcher._to_us_em_symbol("UNKNOWN")
        self.assertIsNone(result)

    def test_spot_em_failure_returns_none(self):
        """stock_us_spot_em 调用失败返回 None"""
        fetcher = self._make_fetcher()

        with patch("akshare.stock_us_spot_em", side_effect=Exception("network error")):
            result = fetcher._to_us_em_symbol("AAPL")

        self.assertIsNone(result)

    def test_case_insensitive_input(self):
        """输入 ticker 不区分大小写"""
        fetcher = self._make_fetcher()
        fetcher._us_code_map = {"AAPL": "105.AAPL"}

        result = fetcher._to_us_em_symbol("aapl")
        self.assertEqual(result, "105.AAPL")


if __name__ == "__main__":
    unittest.main()
