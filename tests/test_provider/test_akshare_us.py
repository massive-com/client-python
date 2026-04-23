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


class TestFetchUsData(unittest.TestCase):
    """测试美股数据获取及回退逻辑"""

    def _make_fetcher(self):
        with patch("provider.akshare_fetcher.get_config") as mock_cfg:
            mock_cfg.return_value.enable_eastmoney_patch = False
            from provider.akshare_fetcher import AkshareFetcher
            return AkshareFetcher(sleep_min=0, sleep_max=0)

    def _make_us_hist_df(self):
        """stock_us_hist 返回的中文列名 DataFrame"""
        return pd.DataFrame({
            "日期": ["2024-01-02", "2024-01-03"],
            "开盘": [185.0, 186.0],
            "收盘": [186.5, 185.5],
            "最高": [187.0, 187.5],
            "最低": [184.0, 184.5],
            "成交量": [50000000, 48000000],
            "成交额": [9300000000, 8900000000],
            "振幅": [1.62, 1.61],
            "涨跌幅": [0.81, -0.54],
            "涨跌额": [1.5, -1.0],
            "换手率": [0.32, 0.31],
        })

    def _make_us_daily_df(self):
        """stock_us_daily 返回的英文列名 DataFrame"""
        return pd.DataFrame({
            "date": pd.to_datetime(["2024-01-02", "2024-01-03"]),
            "open": [185.0, 186.0],
            "high": [187.0, 187.5],
            "low": [184.0, 184.5],
            "close": [186.5, 185.5],
            "volume": [50000000, 48000000],
        })

    def test_fetch_us_data_primary_success(self):
        """stock_us_hist 成功时直接返回"""
        fetcher = self._make_fetcher()
        fetcher._us_code_map = {"AAPL": "105.AAPL"}

        with patch("akshare.stock_us_hist", return_value=self._make_us_hist_df()) as mock_hist, \
             patch("akshare.stock_us_daily") as mock_daily:
            df = fetcher._fetch_us_data("AAPL", "2024-01-01", "2024-01-31")

        self.assertEqual(len(df), 2)
        mock_hist.assert_called_once()
        mock_daily.assert_not_called()

    def test_fetch_us_data_fallback_to_daily(self):
        """stock_us_hist 失败时回退到 stock_us_daily"""
        fetcher = self._make_fetcher()
        fetcher._us_code_map = {"AAPL": "105.AAPL"}

        with patch("akshare.stock_us_hist", side_effect=Exception("API error")), \
             patch("akshare.stock_us_daily", return_value=self._make_us_daily_df()):
            df = fetcher._fetch_us_data("AAPL", "2024-01-01", "2024-01-31")

        self.assertEqual(len(df), 2)

    def test_fetch_us_data_fallback_when_no_em_symbol(self):
        """无法获取东财代码时直接回退到 stock_us_daily"""
        fetcher = self._make_fetcher()
        fetcher._us_code_map = {}  # AAPL not in map

        with patch("akshare.stock_us_hist") as mock_hist, \
             patch("akshare.stock_us_daily", return_value=self._make_us_daily_df()):
            df = fetcher._fetch_us_data("AAPL", "2024-01-01", "2024-01-31")

        self.assertEqual(len(df), 2)
        mock_hist.assert_not_called()

    def test_fetch_us_data_all_fail_raises(self):
        """两个源都失败时抛出 DataFetchError"""
        from provider.base import DataFetchError
        fetcher = self._make_fetcher()
        fetcher._us_code_map = {"AAPL": "105.AAPL"}

        with patch("akshare.stock_us_hist", side_effect=Exception("hist error")), \
             patch("akshare.stock_us_daily", side_effect=Exception("daily error")):
            with self.assertRaises(DataFetchError):
                fetcher._fetch_us_data("AAPL", "2024-01-01", "2024-01-31")

    def test_fetch_us_data_daily_filters_by_date(self):
        """回退到 stock_us_daily 时按日期范围过滤"""
        fetcher = self._make_fetcher()
        fetcher._us_code_map = {}

        daily_df = pd.DataFrame({
            "date": pd.to_datetime(["2023-12-29", "2024-01-02", "2024-02-01"]),
            "open": [180.0, 185.0, 190.0],
            "high": [181.0, 187.0, 191.0],
            "low": [179.0, 184.0, 189.0],
            "close": [180.5, 186.5, 190.5],
            "volume": [40000000, 50000000, 45000000],
        })

        with patch("akshare.stock_us_daily", return_value=daily_df):
            df = fetcher._fetch_us_data("AAPL", "2024-01-01", "2024-01-31")

        self.assertEqual(len(df), 1)


class TestFetchRawDataUsStock(unittest.TestCase):
    """测试 _fetch_raw_data 的美股分支路由"""

    def _make_fetcher(self):
        with patch("provider.akshare_fetcher.get_config") as mock_cfg:
            mock_cfg.return_value.enable_eastmoney_patch = False
            from provider.akshare_fetcher import AkshareFetcher
            return AkshareFetcher(sleep_min=0, sleep_max=0)

    def test_us_code_routes_to_fetch_us_data(self):
        """美股代码应路由到 _fetch_us_data 而非抛异常"""
        fetcher = self._make_fetcher()
        fetcher._us_code_map = {"AAPL": "105.AAPL"}

        us_hist_df = pd.DataFrame({
            "日期": ["2024-01-02"],
            "开盘": [185.0],
            "收盘": [186.5],
            "最高": [187.0],
            "最低": [184.0],
            "成交量": [50000000],
            "成交额": [9300000000],
            "振幅": [1.62],
            "涨跌幅": [0.81],
            "涨跌额": [1.5],
            "换手率": [0.32],
        })

        with patch("akshare.stock_us_hist", return_value=us_hist_df):
            df = fetcher._fetch_raw_data("AAPL", "2024-01-01", "2024-01-31")

        self.assertFalse(df.empty)


class TestNormalizeDataUsStock(unittest.TestCase):
    """测试 _normalize_data 对美股数据的扩展字段保留"""

    def _make_fetcher(self):
        with patch("provider.akshare_fetcher.get_config") as mock_cfg:
            mock_cfg.return_value.enable_eastmoney_patch = False
            from provider.akshare_fetcher import AkshareFetcher
            return AkshareFetcher(sleep_min=0, sleep_max=0)

    def test_us_stock_keeps_all_fields(self):
        """美股数据应保留所有映射后的字段"""
        fetcher = self._make_fetcher()

        raw_df = pd.DataFrame({
            "日期": ["2024-01-02"],
            "开盘": [185.0],
            "收盘": [186.5],
            "最高": [187.0],
            "最低": [184.0],
            "成交量": [50000000],
            "成交额": [9300000000],
            "振幅": [1.62],
            "涨跌幅": [0.81],
            "涨跌额": [1.5],
            "换手率": [0.32],
        })

        result = fetcher._normalize_data(raw_df, "AAPL")

        # 标准字段
        self.assertIn("date", result.columns)
        self.assertIn("open", result.columns)
        self.assertIn("close", result.columns)
        self.assertIn("volume", result.columns)
        self.assertIn("amount", result.columns)
        self.assertIn("pct_chg", result.columns)
        # 美股扩展字段
        self.assertIn("amplitude", result.columns)
        self.assertIn("change", result.columns)
        self.assertIn("turnover_rate", result.columns)
        # code 字段
        self.assertIn("code", result.columns)
        self.assertEqual(result.iloc[0]["code"], "AAPL")

    def test_a_stock_still_filters_columns(self):
        """A 股数据仍然只保留 STANDARD_COLUMNS"""
        fetcher = self._make_fetcher()

        raw_df = pd.DataFrame({
            "日期": ["2024-01-02"],
            "开盘": [10.0],
            "收盘": [10.5],
            "最高": [11.0],
            "最低": [9.5],
            "成交量": [1000000],
            "成交额": [10500000],
            "振幅": [15.0],
            "涨跌幅": [5.0],
            "涨跌额": [0.5],
            "换手率": [1.2],
        })

        result = fetcher._normalize_data(raw_df, "600519")

        # A 股不应包含扩展字段
        self.assertNotIn("amplitude", result.columns)
        self.assertNotIn("change", result.columns)
        self.assertNotIn("turnover_rate", result.columns)


if __name__ == "__main__":
    unittest.main()
