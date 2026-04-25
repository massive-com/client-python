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


def main(dry_run: bool = False) -> None:
    """入口函数。"""
    if dry_run:
        logger.info("--dry-run 模式：仅获取股票列表，不抓取数据")
    else:
        logger.info("开始获取美股数据 demo")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    main(dry_run=dry_run)
