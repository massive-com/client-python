# US Data Provider 优化设计

**Date:** 2026-04-23
**Scope:** 重构 `processor/us_daily`，升级股票列表获取和天级数据获取逻辑

---

## 1. 目标

将 `processor/us_daily` 升级为两部分：

1. **股票列表获取** — 按交易所（NASDAQ, NYSE, ARCA）全量获取所有上市股票及 TickerDetails 全部字段，不做市值过滤，固定使用 massive API
2. **天级数据获取** — 支持 akshare > yfinance > massive 三数据源优先级 failover，归一化到统一列存储，每个数据源独立配置请求间隔

## 2. 架构

### 2.1 目录结构

```
processor/us_daily/
├── __init__.py
├── __main__.py          # 入口，编排两步流程
├── config.py            # 配置（数据源优先级、各源间隔等）
├── storage.py           # 文件 I/O
├── ticker_lister.py     # 新文件，替代 ticker_filter.py
├── sources/             # 新目录：数据源抽象 + 实现
│   ├── __init__.py      # 导出 SourceManager
│   ├── base.py          # BaseSource 接口
│   ├── manager.py       # SourceManager（failover 编排）
│   ├── akshare_source.py
│   ├── yfinance_source.py
│   └── massive_source.py
└── agg_fetcher.py       # 改造：调用 SourceManager
```

### 2.2 数据流

1. `__main__.py` 加载 config → 初始化 `RESTClient` + `SourceManager`
2. Step 1：`ticker_lister.py` 用 `RESTClient` 从 massive API 按交易所获取全量股票 + TickerDetails，存到 `./data/us_list/`
3. Step 2：`agg_fetcher.py` 遍历股票列表，按月调用 `SourceManager.fetch_daily()` 获取天级数据，归一化后存到 `./data/us_daily/<ticker>/<YYYY-MM>.json`

## 3. 数据源抽象与 Failover

### 3.1 BaseSource 接口

```python
class BaseSource(ABC):
    name: str                    # "akshare" / "yfinance" / "massive"
    request_interval: float      # 从 config 读取，每次请求后 sleep

    @abstractmethod
    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """返回归一化后的 DataFrame，列为 STANDARD_COLUMNS"""
        ...
```

### 3.2 STANDARD_COLUMNS

```python
STANDARD_COLUMNS = ["date", "open", "high", "low", "close", "volume"]
```

只保留所有数据源都能提供的 6 列。

### 3.3 SourceManager

```python
class SourceManager:
    def __init__(self, sources: List[BaseSource]):
        self.sources = sources  # 已按优先级排序

    def fetch_daily(self, ticker: str, start_date: str, end_date: str) -> Tuple[pd.DataFrame, str]:
        """依次尝试各 source，返回 (df, source_name)，全部失败则抛异常"""
        for source in self.sources:
            try:
                df = source.fetch_daily(ticker, start_date, end_date)
                if not df.empty:
                    time.sleep(source.request_interval)
                    return df, source.name
            except Exception as e:
                logger.warning(f"{source.name} failed for {ticker}: {e}")
                continue
        raise FetchError(f"All sources failed for {ticker}")
```

### 3.4 三个实现

| Source | 库调用 | ticker 转换 | 请求间隔默认值 |
|--------|--------|------------|--------------|
| AkshareSource | `ak.stock_us_daily(symbol=ticker)` | 直接用 ticker | 2s |
| YfinanceSource | `yf.download(ticker, start, end)` | 直接用 ticker | 1s |
| MassiveSource | `client.list_aggs(ticker, ...)` | 直接用 ticker | 12s |

## 4. 股票列表获取（ticker_lister.py）

### 4.1 交易所映射

```python
EXCHANGES = {
    "nasdaq": "XNAS",
    "nyse": "XNYS",
    "arca": "ARCX",
}
```

### 4.2 流程

1. 遍历配置的交易所列表（默认全部三个）
2. 对每个交易所调用 `client.list_tickers(market="stocks", exchange=ex, active=True, limit=1000)` 获取所有 ticker
3. 对每个 ticker 调用 `client.get_ticker_details(ticker)` 获取完整详情
4. 每次请求后 sleep `config.massive_interval`（12s）
5. 按交易所分别存储
6. 支持断点续传：如果交易所文件已存在，加载其中已有的 tickers 列表作为已完成集合，只对不在集合中的 ticker 调用 `get_ticker_details`，完成后覆盖写入整个文件

### 4.3 存储结构

```
data/us_list/
├── nasdaq.json
├── nyse.json
└── arca.json
```

文件格式：

```json
{
    "updated_at": "2026-04-23",
    "exchange": "XNAS",
    "count": 3500,
    "tickers": [
        {
            "ticker": "AAPL",
            "name": "Apple Inc",
            "market_cap": 3.2e12,
            "description": "...",
            "sic_code": "3571",
            "total_employees": 164000,
            "list_date": "1980-12-12",
            "share_class_shares_outstanding": 15500000000
        }
    ]
}
```

## 5. 天级数据获取与存储（agg_fetcher.py）

### 5.1 流程

1. 从 `./data/us_list/` 加载股票列表（合并所有交易所）
2. 对每个 ticker，生成月份列表（`config.start_date` 到当前月）
3. 对每个月份：
   - 文件已存在且不是当前月 → 跳过
   - 文件已存在且是当前月 → 重新获取
   - 文件不存在 → 获取
4. 调用 `source_manager.fetch_daily(ticker, month_start, month_end)`
5. 归一化后存储

### 5.2 存储格式

```json
{
    "ticker": "AAPL",
    "month": "2026-04",
    "source": "akshare",
    "fetched_at": "2026-04-23T10:30:45",
    "data": [
        {
            "date": "2026-04-01",
            "open": 150.5,
            "high": 152.1,
            "low": 150.0,
            "close": 151.8,
            "volume": 45000000
        }
    ]
}
```

### 5.3 错误处理

所有数据源都失败时，记录到 failures 列表，继续处理下一个 ticker，最后汇总输出失败报告。

## 6. 配置（config.py）

```python
@dataclass
class Config:
    # --- 股票列表 ---
    refresh_tickers: bool = False
    exchanges: List[str] = field(default_factory=lambda: ["nasdaq", "nyse", "arca"])

    # --- 天级数据 ---
    start_date: str = "2026-01"
    data_source_priority: List[str] = field(default_factory=lambda: ["akshare", "yfinance", "massive"])

    # --- 各数据源请求间隔（秒）---
    akshare_interval: float = 2.0
    yfinance_interval: float = 1.0
    massive_interval: float = 12.0

    # --- 路径 ---
    list_dir: str = "data/us_list"
    daily_dir: str = "data/us_daily"

    # --- 重试 ---
    max_retries: int = 3
```

删除的配置项：`market_cap_min`（不再做市值过滤）。

## 7. 旧文件处理

- **删除：** `ticker_filter.py` — 被 `ticker_lister.py` 替代
- **改造：** `__main__.py`、`agg_fetcher.py`、`config.py`、`storage.py`
- **新增：** `ticker_lister.py`、`sources/` 目录及其下 6 个文件
