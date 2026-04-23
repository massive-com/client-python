import unittest
from unittest.mock import patch, MagicMock
import pandas as pd


class TestAkshareSource(unittest.TestCase):

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

    def _make_spot_em_df(self):
        return pd.DataFrame({
            "代码": ["105.AAPL", "106.BAC"],
            "名称": ["苹果", "美国银行"],
        })

    def test_fetch_daily_uses_stock_us_hist_primary(self):
        """优先使用 stock_us_hist"""
        from processor.us_daily.sources.akshare_source import AkshareSource

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_spot_em.return_value = self._make_spot_em_df()
            mock_ak.stock_us_hist.return_value = self._make_us_hist_df()
            source = AkshareSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2024-01-01", "2024-01-31")

        mock_ak.stock_us_hist.assert_called_once()
        mock_ak.stock_us_daily.assert_not_called()
        self.assertEqual(len(result), 2)

    def test_fetch_daily_returns_all_fields(self):
        """返回所有字段，不仅限于 STANDARD_COLUMNS"""
        from processor.us_daily.sources.akshare_source import AkshareSource

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_spot_em.return_value = self._make_spot_em_df()
            mock_ak.stock_us_hist.return_value = self._make_us_hist_df()
            source = AkshareSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2024-01-01", "2024-01-31")

        for col in ["date", "open", "high", "low", "close", "volume"]:
            self.assertIn(col, result.columns)
        for col in ["amount", "pct_chg", "amplitude", "change", "turnover_rate"]:
            self.assertIn(col, result.columns)

    def test_fetch_daily_fallback_to_stock_us_daily(self):
        """stock_us_hist 失败时回退到 stock_us_daily"""
        from processor.us_daily.sources.akshare_source import AkshareSource

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_spot_em.return_value = self._make_spot_em_df()
            mock_ak.stock_us_hist.side_effect = Exception("API error")
            mock_ak.stock_us_daily.return_value = self._make_us_daily_df()
            source = AkshareSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2024-01-01", "2024-01-31")

        self.assertEqual(len(result), 2)
        mock_ak.stock_us_daily.assert_called_once()

    def test_fetch_daily_fallback_filters_by_date(self):
        """回退到 stock_us_daily 时正确过滤日期"""
        from processor.us_daily.sources.akshare_source import AkshareSource

        daily_df = pd.DataFrame({
            "date": pd.to_datetime(["2023-12-31", "2024-01-02", "2024-02-01"]),
            "open": [70.0, 74.06, 80.0],
            "high": [71.0, 75.15, 81.0],
            "low": [69.0, 73.80, 79.0],
            "close": [70.5, 74.36, 80.5],
            "volume": [100000, 108872000, 90000],
        })

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_spot_em.return_value = self._make_spot_em_df()
            mock_ak.stock_us_hist.side_effect = Exception("fail")
            mock_ak.stock_us_daily.return_value = daily_df
            source = AkshareSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2024-01-01", "2024-01-31")

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["date"], "2024-01-02")

    def test_fetch_daily_returns_empty_on_no_data(self):
        """无数据时返回空 DataFrame"""
        from processor.us_daily.sources.akshare_source import AkshareSource

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_spot_em.return_value = self._make_spot_em_df()
            mock_ak.stock_us_hist.return_value = pd.DataFrame()
            mock_ak.stock_us_daily.return_value = pd.DataFrame()
            source = AkshareSource(request_interval=0.0)
            result = source.fetch_daily("AAPL", "2024-01-01", "2024-01-31")

        self.assertTrue(result.empty)

    def test_fetch_daily_case_insensitive_ticker(self):
        """ticker 输入不区分大小写"""
        from processor.us_daily.sources.akshare_source import AkshareSource

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_spot_em.return_value = self._make_spot_em_df()
            mock_ak.stock_us_hist.return_value = self._make_us_hist_df()
            source = AkshareSource(request_interval=0.0)
            result = source.fetch_daily("aapl", "2024-01-01", "2024-01-31")

        self.assertEqual(len(result), 2)

    def test_code_map_cached(self):
        """stock_us_spot_em 只调用一次，第二次使用缓存"""
        from processor.us_daily.sources.akshare_source import AkshareSource

        with patch("processor.us_daily.sources.akshare_source.ak") as mock_ak:
            mock_ak.stock_us_spot_em.return_value = self._make_spot_em_df()
            mock_ak.stock_us_hist.return_value = self._make_us_hist_df()
            source = AkshareSource(request_interval=0.0)
            source.fetch_daily("AAPL", "2024-01-01", "2024-01-31")
            source.fetch_daily("AAPL", "2024-02-01", "2024-02-28")

        self.assertEqual(mock_ak.stock_us_spot_em.call_count, 1)


if __name__ == "__main__":
    unittest.main()
