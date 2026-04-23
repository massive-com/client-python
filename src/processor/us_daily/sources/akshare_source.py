import logging
from typing import Dict, Optional

import pandas as pd

from processor.us_daily.sources.base import BaseSource, STANDARD_COLUMNS

logger = logging.getLogger("us_daily")

try:
    import akshare as ak
except ImportError:  # pragma: no cover
    ak = None  # type: ignore[assignment]

# 中文列名 → 英文列名映射
_COLUMN_MAPPING = {
    "日期": "date",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount",
    "涨跌幅": "pct_chg",
    "振幅": "amplitude",
    "涨跌额": "change",
    "换手率": "turnover_rate",
}


class AkshareSource(BaseSource):
    name = "akshare"

    def __init__(self, request_interval: float = 2.0):
        self.request_interval = request_interval
        self._us_code_map: Optional[Dict[str, str]] = None

    def _to_us_em_symbol(self, ticker: str) -> Optional[str]:
        """将纯 ticker 转换为东财格式（如 AAPL → 105.AAPL）"""
        ticker = ticker.strip().upper()

        if self._us_code_map is None:
            try:
                spot_df = ak.stock_us_spot_em()
                self._us_code_map = {}
                if spot_df is not None and not spot_df.empty and "代码" in spot_df.columns:
                    for _, row in spot_df.iterrows():
                        full_code = str(row["代码"])
                        parts = full_code.split(".", 1)
                        if len(parts) == 2:
                            self._us_code_map[parts[1].upper()] = full_code
                logger.debug(f"[akshare] US code map built: {len(self._us_code_map)} entries")
            except Exception as e:
                logger.warning(f"[akshare] stock_us_spot_em failed: {e}")
                self._us_code_map = {}
                return None

        return self._us_code_map.get(ticker)

    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        if ak is None:
            raise ImportError("akshare is not installed")

        symbol = ticker.strip().upper()
        logger.debug(f"[akshare] fetching {symbol} {start_date}~{end_date}")

        # 策略 1: stock_us_hist（东财接口，字段最全）
        em_symbol = self._to_us_em_symbol(symbol)
        if em_symbol is not None:
            try:
                df = ak.stock_us_hist(
                    symbol=em_symbol,
                    period="daily",
                    start_date=start_date.replace("-", ""),
                    end_date=end_date.replace("-", ""),
                    adjust="qfq",
                )
                if df is not None and not df.empty:
                    # 中文列名转英文
                    df = df.rename(columns=_COLUMN_MAPPING)
                    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
                    logger.debug(f"[akshare] stock_us_hist success: {len(df)} rows")
                    return df.reset_index(drop=True)
            except Exception as e:
                logger.warning(f"[akshare] stock_us_hist failed for {symbol}: {e}")

        # 策略 2: stock_us_daily 回退
        try:
            df = ak.stock_us_daily(symbol=symbol, adjust="qfq")

            if df is None or df.empty:
                return pd.DataFrame(columns=STANDARD_COLUMNS)

            df["date"] = pd.to_datetime(df["date"])
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            df = df[(df["date"] >= start_dt) & (df["date"] <= end_dt)]

            if df.empty:
                return pd.DataFrame(columns=STANDARD_COLUMNS)

            df["date"] = df["date"].dt.strftime("%Y-%m-%d")
            return df.reset_index(drop=True)
        except Exception as e:
            logger.warning(f"[akshare] stock_us_daily also failed for {symbol}: {e}")
            return pd.DataFrame(columns=STANDARD_COLUMNS)
