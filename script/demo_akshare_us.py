#!/usr/bin/env python3
"""AKShare 东财美股数据获取 Demo。

1. 通过 stock_us_spot_em 获取所有美股代码 -> ./data/demo_list/us_stocks.json
2. 通过 stock_us_hist 获取每只股票 2026 年日线数据 -> ./data/demo_stock/{TICKER}/{TICKER}_2026.json
"""

import json
import logging
import sys
import time
from pathlib import Path
from typing import Optional

import pandas as pd

try:
    import akshare as ak
except ImportError:
    print("错误: akshare 未安装。请运行: pip install akshare", file=sys.stderr)
    sys.exit(1)

from processor.us_daily.sources.akshare_source import AkshareSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("demo_akshare_us")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DEMO_LIST_DIR = DATA_DIR / "demo_list"
DEMO_STOCK_DIR = DATA_DIR / "demo_stock"
YEAR = 2026
MAX_RETRIES = 3
RETRY_BACKOFFS = [2, 4, 8]  # seconds


def fetch_us_stock_list(output_dir: Path) -> list[dict]:
    """通过 stock_us_spot_em 获取所有美股代码列表。

    Returns:
        股票列表 [{"ticker": "AAPL", "name": "苹果", "em_code": "105.AAPL"}, ...]
    """
    logger.info("获取美股代码列表...")
    try:
        df = ak.stock_us_spot_em()
    except Exception as e:
        logger.error(f"获取美股列表失败: {e}")
        sys.exit(1)

    if df is None or df.empty:
        logger.error("美股列表为空")
        sys.exit(1)

    if "代码" not in df.columns:
        logger.error("美股列表缺少 '代码' 列")
        sys.exit(1)

    stocks = []
    code_col = "代码"
    name_col = "名称" if "名称" in df.columns else None

    for _, row in df.iterrows():
        if pd.isna(row[code_col]):
            continue
        full_code = str(row[code_col])
        parts = full_code.split(".", 1)
        ticker = parts[1].upper() if len(parts) == 2 else full_code.upper()
        name = str(row[name_col]) if name_col and pd.notna(row[name_col]) else ""
        stocks.append({"ticker": ticker, "name": name, "em_code": full_code})

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "us_stocks.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)

    logger.info(f"美股列表已保存: {output_file} ({len(stocks)} 只)")
    return stocks


def fetch_daily_for_stock(
    source: AkshareSource,
    ticker: str,
    year: int,
) -> Optional[pd.DataFrame]:
    """获取单只股票指定年份的日线数据（含重试）。

    Returns:
        DataFrame 或 None（失败时）
    """
    start = f"{year}0101"
    end = f"{year}1231"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            df = source.fetch_daily(ticker, start, end)
            if df is not None and not df.empty:
                return df
            logger.warning(f"[{ticker}] 返回空数据 (attempt {attempt}/{MAX_RETRIES})")
        except Exception as e:
            logger.warning(f"[{ticker}] 获取失败 (attempt {attempt}/{MAX_RETRIES}): {e}")

        if attempt < MAX_RETRIES:
            backoff = RETRY_BACKOFFS[attempt - 1]
            logger.debug(f"[{ticker}] 等待 {backoff}s 后重试...")
            time.sleep(backoff)

    logger.error(f"[{ticker}] 重试 {MAX_RETRIES} 次后仍失败，跳过")
    return None


def save_summary(
    output_dir: Path,
    total: int,
    success: int,
    failed: int,
    failed_tickers: list[str],
) -> None:
    """保存抓取摘要到 JSON 文件。"""
    summary = {
        "total": total,
        "success": success,
        "failed": failed,
        "failed_tickers": failed_tickers,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_file = output_dir / "fetch_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    logger.info(f"摘要已保存: {summary_file}")


def main(dry_run: bool = False) -> None:
    if dry_run:
        logger.info("--dry-run 模式：仅获取股票列表，不抓取数据")
    else:
        logger.info("开始获取美股数据 demo")

    stocks = fetch_us_stock_list(DEMO_LIST_DIR)
    logger.info(f"共 {len(stocks)} 只美股")

    if dry_run:
        logger.info("--dry-run 完成")
        return

    source = AkshareSource()
    success = 0
    failed = 0
    failed_tickers: list[str] = []

    for i, stock in enumerate(stocks):
        ticker = stock["ticker"]
        logger.info(f"[{i+1}/{len(stocks)}] 获取 {ticker} ({stock['name']})...")

        df = fetch_daily_for_stock(source, ticker, YEAR)
        if df is not None:
            stock_dir = DEMO_STOCK_DIR / ticker
            stock_dir.mkdir(parents=True, exist_ok=True)
            output_file = stock_dir / f"{ticker}_{YEAR}.json"
            df.to_json(output_file, orient="records", force_ascii=False, indent=2)
            logger.info(f"[{i+1}/{len(stocks)}] {ticker}: {len(df)} 行 -> {output_file}")
            success += 1
        else:
            failed += 1
            failed_tickers.append(ticker)

    save_summary(DEMO_STOCK_DIR, len(stocks), success, failed, failed_tickers)
    logger.info(f"完成: 成功 {success}, 失败 {failed}")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    main(dry_run=dry_run)
