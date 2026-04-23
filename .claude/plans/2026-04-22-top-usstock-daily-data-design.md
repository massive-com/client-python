# 头部美股日K数据采集 — 设计文档

## 概述

构建一个数据采集模块，获取纳斯达克、纽交所、NYSE Arca 交易所中市值 >= 50亿美金的头部公司，按月采集自 2020 年以来的日 K 线数据，支持增量更新。

## 模块结构

```
project/us_daily/
├── __init__.py
├── __main__.py        # 入口：加载配置 → 筛选 ticker → 逐个抓取
├── config.py          # Config dataclass + 默认值 + 配置文件加载
├── ticker_filter.py   # 调用 list_tickers + get_ticker_details 筛选头部公司
├── agg_fetcher.py     # 按月调用 list_aggs，含增量判断和重试逻辑
└── storage.py         # JSON 文件读写，路径管理

data/us_daily/
├── top_tickers.json   # 筛选出的头部公司列表
└── {TICKER}/          # 每个 ticker 一个目录
    ├── 2020-01.json
    ├── 2020-02.json
    └── ...

logs/
└── us_daily.log       # 运行日志
```

## 执行流程

```
1. 加载配置（project/us_daily/config.json）
2. 初始化 RESTClient
3. 是否刷新 ticker 列表？
   ├── refresh_tickers=true 或 top_tickers.json 不存在 → 调用 API 筛选 → 写入 top_tickers.json
   └── refresh_tickers=false 且文件存在 → 读取 top_tickers.json
4. 遍历每个 ticker：
   4.1 创建 ticker 目录（如不存在）
   4.2 生成 start_date 到当前月的月份列表
   4.3 对每个月份：
       - 文件已存在 且 不是当前月 → 跳过
       - 文件已存在 且 是当前月 → 重新请求并覆盖
       - 文件不存在 → 请求并写入
       - 每次 API 请求后 sleep request_interval 秒
5. 输出汇总（完成数、失败数及详情）
```

## 配置模块

### Config dataclass

```python
@dataclass
class Config:
    refresh_tickers: bool = False       # 是否刷新头部公司列表
    market_cap_min: float = 5e9         # 市值阈值（美元）
    start_date: str = "2020-01"         # 数据起始年月
    request_interval: int = 20          # API 请求间隔（秒）
    data_dir: str = "data/us_daily"     # 数据存储路径
    max_retries: int = 3                # 请求失败重试次数
```

### 配置文件

路径：`project/us_daily/config.json`，不存在则使用默认值。

```json
{
  "refresh_tickers": true,
  "market_cap_min": 5000000000,
  "start_date": "2020-01",
  "request_interval": 20,
  "data_dir": "data/us_daily",
  "max_retries": 3
}
```

## Ticker 筛选模块

### ticker_filter.py

**流程：**

1. 调用 `client.list_tickers(market="stocks", exchange=exchange, active=True, limit=1000)` 遍历三个交易所：
   - `XNAS`（纳斯达克）
   - `XNYS`（纽约证券交易所）
   - `ARCX`（NYSE Arca）
2. 对每个 ticker 调用 `client.get_ticker_details(ticker)` 获取 `market_cap`
3. 过滤 `market_cap >= config.market_cap_min`
4. 每次 API 请求后 sleep `config.request_interval` 秒
5. 结果写入 `data/us_daily/top_tickers.json`

### top_tickers.json 格式

```json
{
  "updated_at": "2026-04-22",
  "market_cap_min": 5000000000,
  "tickers": [
    {"ticker": "AAPL", "name": "Apple Inc.", "market_cap": 3200000000000, "exchange": "XNAS"},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "market_cap": 2800000000000, "exchange": "XNAS"}
  ]
}
```

## 数据抓取模块

### agg_fetcher.py

**核心逻辑：**

```python
def fetch_ticker_aggs(client, ticker, config):
    months = generate_months(config.start_date, current_month())
    for month in months:
        file_path = get_month_file_path(config.data_dir, ticker, month)

        # 增量判断
        if file_exists(file_path) and not is_current_month(month):
            continue  # 历史月份已有数据，跳过

        # 请求数据（带重试）
        aggs = fetch_with_retry(client, ticker, month, config.max_retries)

        # 写入文件
        save_month_data(file_path, aggs)

        sleep(config.request_interval)
```

**月份范围：** `generate_months("2020-01", "2026-04")` → `["2020-01", "2020-02", ..., "2026-04"]`

**API 调用：** `client.list_aggs(ticker, 1, "day", from_=月初, to=月末, adjusted=True, sort="asc")`

**重试逻辑：** 最多 `max_retries` 次，每次重试前 sleep `request_interval`。仍然失败则记录日志，跳过该月份继续。

### 月数据文件格式

`data/us_daily/{TICKER}/{YYYY-MM}.json`：

```json
{
  "ticker": "AAPL",
  "month": "2020-01",
  "fetched_at": "2026-04-22T10:30:00",
  "data": [
    {
      "open": 74.06,
      "high": 75.15,
      "low": 73.80,
      "close": 74.36,
      "volume": 108872000,
      "vwap": 74.53,
      "timestamp": 1577854800000,
      "transactions": 480012
    }
  ]
}
```

## 存储模块

### storage.py

**核心函数：**

- `get_tickers_file_path(data_dir)` → `data/us_daily/top_tickers.json`
- `get_month_file_path(data_dir, ticker, month)` → `data/us_daily/AAPL/2020-01.json`
- `save_json(path, data)` — 写入 JSON，自动创建父目录
- `load_json(path)` — 读取 JSON
- `file_exists(path)` — 判断文件是否存在

## 入口模块

### __main__.py

```python
def main():
    # 1. 加载配置
    config = load_config()

    # 2. 初始化日志（输出到 logs/us_daily.log + stdout）
    setup_logging()

    # 3. 初始化 REST 客户端
    client = RESTClient()

    # 4. 获取 ticker 列表
    if config.refresh_tickers or not tickers_file_exists(config):
        tickers = filter_top_tickers(client, config)
        save_tickers(config, tickers)
    else:
        tickers = load_tickers(config)

    # 5. 逐个抓取日K数据
    failed = []
    for i, ticker_info in enumerate(tickers):
        logger.info(f"[{i+1}/{len(tickers)}] 开始处理 {ticker_info['ticker']}")
        result = fetch_ticker_aggs(client, ticker_info["ticker"], config)
        if result.failures:
            failed.extend(result.failures)

    # 6. 输出汇总
    logger.info(f"完成：{len(tickers)} 只股票")
    if failed:
        logger.warning(f"失败：{len(failed)} 个月份")
        for f in failed:
            logger.warning(f"  - {f['ticker']} {f['month']}: {f['error']}")
```

**运行方式：** `python -m project.us_daily`

## 日志

- 使用 Python `logging` 模块
- 同时输出到 `logs/us_daily.log` 和 stdout
- 格式：`2026-04-22 10:30:00 [INFO] [3/150] AAPL - 2020-01 fetched`
- 包含进度信息，便于监控长时间运行

## 限流

- 每次 API 请求后 sleep `config.request_interval` 秒（默认 20s）
- 适用于 list_tickers 分页、get_ticker_details、list_aggs 所有请求
