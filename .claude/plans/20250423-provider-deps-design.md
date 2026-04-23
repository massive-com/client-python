# Provider Dependencies Resolution Design

**Date:** 2025-04-23
**Scope:** Resolve `from src.*` imports in `provider/` by creating private internal modules

---

## 1. Goal

`provider/` 模块依赖 3 个来自外部项目 (daily_stock_analysis) 的模块：`src.config`、`src.data`、`src.report_language`。将这些依赖内化为 `provider/` 的私有模块，使 provider 完全自包含。

## 2. Reference Repository

https://github.com/ZhuLinsen/daily_stock_analysis — 原始项目，provider 模块从该项目中提取。

## 3. New Files

### 3.1 `src/provider/_config.py` (~60 行)

精简的 Config 单例，仅包含 provider 实际使用的 15 个属性，从环境变量读取：

```python
import os
from dataclasses import dataclass
from threading import Lock

SUPPORTED_REPORT_LANGUAGES = ("zh", "en")
_REPORT_LANGUAGE_ALIASES = {
    "zh-cn": "zh", "zh_cn": "zh", "zh-hans": "zh", "zh_hans": "zh",
    "zh-tw": "zh", "zh_tw": "zh", "cn": "zh", "chinese": "zh",
    "english": "en", "en-us": "en", "en_us": "en", "en-gb": "en", "en_gb": "en",
}

def normalize_report_language(value, default="zh"):
    candidate = (value or default).strip().lower().replace(" ", "_")
    candidate = _REPORT_LANGUAGE_ALIASES.get(candidate, candidate)
    return candidate if candidate in SUPPORTED_REPORT_LANGUAGES else default

@dataclass
class Config:
    tushare_token: str = ""
    longbridge_app_key: str = ""
    longbridge_app_secret: str = ""
    longbridge_access_token: str = ""
    tickflow_api_key: str = ""
    enable_eastmoney_patch: bool = True
    enable_realtime_quote: bool = True
    enable_chip_distribution: bool = True
    enable_fundamental_pipeline: bool = True
    prefetch_realtime_quotes: bool = True
    realtime_source_priority: str = "tencent,akshare,efinance"
    fundamental_fetch_timeout_seconds: float = 30.0
    fundamental_stage_timeout_seconds: float = 60.0
    fundamental_cache_ttl_seconds: int = 3600
    fundamental_cache_max_entries: int = 256
    fundamental_retry_max: int = 2

_instance = None
_lock = Lock()

def get_config() -> Config:
    global _instance
    if _instance is not None:
        return _instance
    with _lock:
        if _instance is not None:
            return _instance
        def _env_bool(key, default="true"):
            return os.environ.get(key, default).lower() != "false"
        _instance = Config(
            tushare_token=os.environ.get("TUSHARE_TOKEN", ""),
            longbridge_app_key=os.environ.get("LONGBRIDGE_APP_KEY", ""),
            longbridge_app_secret=os.environ.get("LONGBRIDGE_APP_SECRET", ""),
            longbridge_access_token=os.environ.get("LONGBRIDGE_ACCESS_TOKEN", ""),
            tickflow_api_key=os.environ.get("TICKFLOW_API_KEY", ""),
            enable_eastmoney_patch=_env_bool("ENABLE_EASTMONEY_PATCH"),
            enable_realtime_quote=_env_bool("ENABLE_REALTIME_QUOTE"),
            enable_chip_distribution=_env_bool("ENABLE_CHIP_DISTRIBUTION"),
            enable_fundamental_pipeline=_env_bool("ENABLE_FUNDAMENTAL_PIPELINE"),
            prefetch_realtime_quotes=_env_bool("PREFETCH_REALTIME_QUOTES"),
            realtime_source_priority=os.environ.get("REALTIME_SOURCE_PRIORITY", "tencent,akshare,efinance"),
            fundamental_fetch_timeout_seconds=float(os.environ.get("FUNDAMENTAL_FETCH_TIMEOUT_SECONDS", "30")),
            fundamental_stage_timeout_seconds=float(os.environ.get("FUNDAMENTAL_STAGE_TIMEOUT_SECONDS", "60")),
            fundamental_cache_ttl_seconds=int(os.environ.get("FUNDAMENTAL_CACHE_TTL_SECONDS", "3600")),
            fundamental_cache_max_entries=int(os.environ.get("FUNDAMENTAL_CACHE_MAX_ENTRIES", "256")),
            fundamental_retry_max=int(os.environ.get("FUNDAMENTAL_RETRY_MAX", "2")),
        )
        return _instance
```

### 3.2 `src/provider/_data/stock_mapping.py`

从参考仓库 `src/data/stock_mapping.py` 完整复制。包含：
- `STOCK_NAME_MAP` — 股票代码→名称映射字典（A 股、美股、港股）
- `is_meaningful_stock_name(name, stock_code)` — 判断股票名是否有效

### 3.3 `src/provider/_data/stock_index_loader.py`

从参考仓库 `src/data/stock_index_loader.py` 完整复制，仅改一处 import：
```python
# from
from src.data.stock_mapping import is_meaningful_stock_name
# to
from provider._data.stock_mapping import is_meaningful_stock_name
```

### 3.4 `src/provider/_data/__init__.py`

```python
from provider._data.stock_mapping import STOCK_NAME_MAP

__all__ = ["STOCK_NAME_MAP"]
```

## 4. Import Path Changes (~20 处)

所有变更均为 `from src.*` → `from provider._*` 的机械替换：

| 文件 | 原 import | 新 import |
|------|-----------|-----------|
| `base.py` (line 27) | `from src.data.stock_index_loader import get_index_stock_name` | `from provider._data.stock_index_loader import get_index_stock_name` |
| `base.py` (line 28) | `from src.data.stock_mapping import STOCK_NAME_MAP, is_meaningful_stock_name` | `from provider._data.stock_mapping import STOCK_NAME_MAP, is_meaningful_stock_name` |
| `base.py` (9 处 lazy) | `from src.config import get_config` | `from provider._config import get_config` |
| `efinance_fetcher.py` | `from src.config import get_config` | `from provider._config import get_config` |
| `akshare_fetcher.py` | `from src.config import get_config` | `from provider._config import get_config` |
| `tushare_fetcher.py` | `from src.config import get_config` | `from provider._config import get_config` |
| `yfinance_fetcher.py` | `from src.data.stock_mapping import ...` | `from provider._data.stock_mapping import ...` |
| `longbridge_fetcher.py` | `from src.report_language import normalize_report_language` | `from provider._config import normalize_report_language` |
| `longbridge_fetcher.py` | `from src.config import get_config` | `from provider._config import get_config` |

## 5. Not In Scope

- `.env` 文件加载（只读 `os.environ`）
- Config 验证逻辑（`ConfigIssue` 系统）
- `report_language.py` 的其他函数
- provider 功能性测试（当前无测试，不新增）
- `__init__.py` 的 import 清理
