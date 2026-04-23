# Provider Dependencies Resolution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resolve all `from src.*` imports in `provider/` by creating private internal modules (`_config.py`, `_data/`), making provider fully self-contained.

**Architecture:** Create `src/provider/_config.py` (slim Config singleton + `normalize_report_language`), `src/provider/_data/` (stock mapping copied from reference repo). Then replace all `from src.*` imports with `from provider._*` imports across 6 fetcher files.

**Tech Stack:** Python 3.9+, dataclasses, os.environ

**Design Doc:** `.claude/plans/20250423-provider-deps-design.md`

---

### Task 1: Create `_data/stock_mapping.py`

**Files:**
- Create: `src/provider/_data/__init__.py`
- Create: `src/provider/_data/stock_mapping.py`

- [ ] **Step 1: Create `_data/` directory**

```bash
mkdir -p src/provider/_data
```

- [ ] **Step 2: Create `_data/__init__.py`**

Write `src/provider/_data/__init__.py`:

```python
# -*- coding: utf-8 -*-
from provider._data.stock_mapping import STOCK_NAME_MAP

__all__ = ["STOCK_NAME_MAP"]
```

- [ ] **Step 3: Create `_data/stock_mapping.py`**

Write `src/provider/_data/stock_mapping.py` — copy the complete file from reference repo (https://github.com/ZhuLinsen/daily_stock_analysis/blob/main/src/data/stock_mapping.py). This file has no external imports. It contains:
- `STOCK_NAME_MAP` dict (~90 entries: A-shares, US stocks, HK stocks)
- `is_meaningful_stock_name(name, stock_code)` function

```python
# -*- coding: utf-8 -*-
from __future__ import annotations

"""
===================================
股票代码与名称映射
===================================

Shared stock code -> name mapping, used by analyzer, data_provider, and name_to_code_resolver.
"""

# Stock code -> name mapping (common stocks)
STOCK_NAME_MAP = {
    # === A-shares ===
    "600519": "贵州茅台",
    "000001": "平安银行",
    "300750": "宁德时代",
    "002594": "比亚迪",
    "600036": "招商银行",
    "601318": "中国平安",
    "000858": "五粮液",
    "600276": "恒瑞医药",
    "601012": "隆基绿能",
    "002475": "立讯精密",
    "300059": "东方财富",
    "002415": "海康威视",
    "600900": "长江电力",
    "601166": "兴业银行",
    "600028": "中国石化",
    "600030": "中信证券",
    "600031": "三一重工",
    "600050": "中国联通",
    "600104": "上汽集团",
    "600111": "北方稀土",
    "600150": "中国船舶",
    "600309": "万华化学",
    "600406": "国电南瑞",
    "600690": "海尔智家",
    "600760": "中航沈飞",
    "600809": "山西汾酒",
    "600887": "伊利股份",
    "600930": "华电新能",
    "601088": "中国神华",
    "601127": "赛力斯",
    "601211": "国泰海通",
    "601225": "陕西煤业",
    "601288": "农业银行",
    "601328": "交通银行",
    "601398": "工商银行",
    "601601": "中国太保",
    "601628": "中国人寿",
    "601658": "邮储银行",
    "601668": "中国建筑",
    "601728": "中国电信",
    "601816": "京沪高铁",
    "601857": "中国石油",
    "601888": "中国中免",
    "601899": "紫金矿业",
    "601919": "中远海控",
    "601985": "中国核电",
    "601988": "中国银行",
    "603019": "中科曙光",
    "603259": "药明康德",
    "603501": "豪威集团",
    "603993": "洛阳钼业",
    "688008": "澜起科技",
    "688012": "中微公司",
    "688041": "海光信息",
    "688111": "金山办公",
    "688256": "寒武纪",
    "688981": "中芯国际",
    # === US stocks ===
    "AAPL": "苹果",
    "TSLA": "特斯拉",
    "MSFT": "微软",
    "GOOGL": "谷歌A",
    "GOOG": "谷歌C",
    "AMZN": "亚马逊",
    "NVDA": "英伟达",
    "META": "Meta",
    "AMD": "AMD",
    "INTC": "英特尔",
    "BABA": "阿里巴巴",
    "PDD": "拼多多",
    "JD": "京东",
    "BIDU": "百度",
    "NIO": "蔚来",
    "XPEV": "小鹏汽车",
    "LI": "理想汽车",
    "COIN": "Coinbase",
    "MSTR": "MicroStrategy",
    # === HK stocks (5-digit) ===
    "00700": "腾讯控股",
    "03690": "美团",
    "01810": "小米集团",
    "09988": "阿里巴巴",
    "09618": "京东集团",
    "09888": "百度集团",
    "01024": "快手",
    "00981": "中芯国际",
    "02015": "理想汽车",
    "09868": "小鹏汽车",
    "00005": "汇丰控股",
    "01299": "友邦保险",
    "00941": "中国移动",
    "00883": "中国海洋石油",
}


def is_meaningful_stock_name(name: str | None, stock_code: str) -> bool:
    """Return whether a stock name is useful for display or caching."""
    if not name:
        return False

    normalized_name = str(name).strip()
    if not normalized_name:
        return False

    normalized_code = (stock_code or "").strip().upper()
    if normalized_name.upper() == normalized_code:
        return False

    if normalized_name.startswith("股票"):
        return False

    placeholder_values = {
        "N/A",
        "NA",
        "NONE",
        "NULL",
        "--",
        "-",
        "UNKNOWN",
        "TICKER",
    }
    if normalized_name.upper() in placeholder_values:
        return False

    return True
```

- [ ] **Step 4: Commit**

```bash
git add src/provider/_data/
git commit -m "feat: add provider/_data/stock_mapping module"
```

---

### Task 2: Create `_data/stock_index_loader.py`

**Files:**
- Create: `src/provider/_data/stock_index_loader.py`

- [ ] **Step 1: Create `_data/stock_index_loader.py`**

Write `src/provider/_data/stock_index_loader.py` — copy from reference repo (https://github.com/ZhuLinsen/daily_stock_analysis/blob/main/src/data/stock_index_loader.py) with ONE import change on line 10:

```python
# Change from:
from src.data.stock_mapping import is_meaningful_stock_name
# To:
from provider._data.stock_mapping import is_meaningful_stock_name
```

Full file content:

```python
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import logging
from pathlib import Path
from threading import RLock
from typing import Dict, Iterable

from provider._data.stock_mapping import is_meaningful_stock_name

logger = logging.getLogger(__name__)

_STOCK_INDEX_FILENAME = "stocks.index.json"
_STOCK_INDEX_CACHE: Dict[str, str] | None = None
_STOCK_INDEX_CACHE_LOCK = RLock()


def get_stock_index_candidate_paths() -> tuple[Path, ...]:
    """Return the supported locations for the generated stock index."""
    repo_root = Path(__file__).resolve().parents[2]
    return (
        repo_root / "apps" / "dsa-web" / "public" / _STOCK_INDEX_FILENAME,
        repo_root / "static" / _STOCK_INDEX_FILENAME,
    )


def _add_lookup_key(keys: set[str], value: str) -> None:
    candidate = str(value or "").strip()
    if not candidate:
        return
    keys.add(candidate)
    keys.add(candidate.upper())


def _build_lookup_keys(canonical_code: str, display_code: str) -> Iterable[str]:
    keys: set[str] = set()
    _add_lookup_key(keys, canonical_code)
    _add_lookup_key(keys, display_code)

    canonical_upper = str(canonical_code or "").strip().upper()
    display_upper = str(display_code or "").strip().upper()

    if "." in canonical_upper:
        base, suffix = canonical_upper.rsplit(".", 1)
        if suffix in {"SH", "SZ", "SS", "BJ"} and base.isdigit():
            _add_lookup_key(keys, base)
        elif suffix == "HK" and base.isdigit() and 1 <= len(base) <= 5:
            digits = base.zfill(5)
            _add_lookup_key(keys, digits)
            _add_lookup_key(keys, f"HK{digits}")

    for candidate in (canonical_upper, display_upper):
        if candidate.startswith("HK"):
            digits = candidate[2:]
            if digits.isdigit() and 1 <= len(digits) <= 5:
                digits = digits.zfill(5)
                _add_lookup_key(keys, digits)
                _add_lookup_key(keys, f"HK{digits}")

    return keys


def _load_stock_index_file(index_path: Path) -> Dict[str, str]:
    with index_path.open("r", encoding="utf-8") as fh:
        raw_items = json.load(fh)

    if not isinstance(raw_items, list):
        raise ValueError(
            f"Unexpected {_STOCK_INDEX_FILENAME} payload type: {type(raw_items).__name__}"
        )

    stock_name_map: Dict[str, str] = {}
    for item in raw_items:
        if not isinstance(item, list) or len(item) < 3:
            continue

        canonical_code, display_code, name_zh = item[0], item[1], item[2]
        if not is_meaningful_stock_name(name_zh, str(display_code or canonical_code or "")):
            continue

        for key in _build_lookup_keys(str(canonical_code or ""), str(display_code or "")):
            stock_name_map[key] = str(name_zh).strip()

    return stock_name_map


def get_stock_name_index_map() -> Dict[str, str]:
    """Lazily load and cache the generated stock-name index."""
    global _STOCK_INDEX_CACHE

    if _STOCK_INDEX_CACHE is not None:
        return _STOCK_INDEX_CACHE

    with _STOCK_INDEX_CACHE_LOCK:
        if _STOCK_INDEX_CACHE is not None:
            return _STOCK_INDEX_CACHE

        for candidate_path in get_stock_index_candidate_paths():
            if not candidate_path.is_file():
                continue

            try:
                _STOCK_INDEX_CACHE = _load_stock_index_file(candidate_path)
                logger.debug(
                    "[股票名称] 已加载前端股票索引映射: %s (%d 条)",
                    candidate_path,
                    len(_STOCK_INDEX_CACHE),
                )
                return _STOCK_INDEX_CACHE
            except (OSError, TypeError, ValueError) as exc:
                logger.debug("[股票名称] 读取股票索引失败 %s: %s", candidate_path, exc)

        _STOCK_INDEX_CACHE = {}
        return _STOCK_INDEX_CACHE


def get_index_stock_name(stock_code: str) -> str | None:
    """Resolve a stock name from the generated frontend stock index."""
    code = str(stock_code or "").strip()
    if not code:
        return None

    stock_name_map = get_stock_name_index_map()
    for key in _build_lookup_keys(code, code):
        name = stock_name_map.get(key)
        if is_meaningful_stock_name(name, code):
            return name

    return None


def _clear_stock_index_cache_for_tests() -> None:
    global _STOCK_INDEX_CACHE
    with _STOCK_INDEX_CACHE_LOCK:
        _STOCK_INDEX_CACHE = None
```

- [ ] **Step 2: Commit**

```bash
git add src/provider/_data/stock_index_loader.py
git commit -m "feat: add provider/_data/stock_index_loader module"
```

---

### Task 3: Create `_config.py`

**Files:**
- Create: `src/provider/_config.py`

- [ ] **Step 1: Create `_config.py`**

Write `src/provider/_config.py`:

```python
# -*- coding: utf-8 -*-
"""
Slim configuration singleton for provider module.

Reads configuration from environment variables. Only includes attributes
actually used by provider fetchers.
"""

import os
from dataclasses import dataclass
from threading import Lock
from typing import Optional


# ---------------------------------------------------------------------------
# normalize_report_language  (extracted from src/report_language.py)
# ---------------------------------------------------------------------------

SUPPORTED_REPORT_LANGUAGES = ("zh", "en")

_REPORT_LANGUAGE_ALIASES = {
    "zh-cn": "zh", "zh_cn": "zh", "zh-hans": "zh", "zh_hans": "zh",
    "zh-tw": "zh", "zh_tw": "zh", "cn": "zh", "chinese": "zh",
    "english": "en", "en-us": "en", "en_us": "en", "en-gb": "en", "en_gb": "en",
}


def normalize_report_language(value: Optional[str], default: str = "zh") -> str:
    """Normalize report language to a supported short code."""
    candidate = (value or default).strip().lower().replace(" ", "_")
    candidate = _REPORT_LANGUAGE_ALIASES.get(candidate, candidate)
    return candidate if candidate in SUPPORTED_REPORT_LANGUAGES else default


# ---------------------------------------------------------------------------
# Config singleton
# ---------------------------------------------------------------------------

@dataclass
class Config:
    # Tushare
    tushare_token: str = ""
    # Longbridge
    longbridge_app_key: str = ""
    longbridge_app_secret: str = ""
    longbridge_access_token: str = ""
    # TickFlow
    tickflow_api_key: str = ""
    # Feature toggles
    enable_eastmoney_patch: bool = True
    enable_realtime_quote: bool = True
    enable_chip_distribution: bool = True
    enable_fundamental_pipeline: bool = True
    prefetch_realtime_quotes: bool = True
    # Realtime source priority
    realtime_source_priority: str = "tencent,akshare,efinance"
    # Fundamental pipeline
    fundamental_fetch_timeout_seconds: float = 30.0
    fundamental_stage_timeout_seconds: float = 60.0
    fundamental_cache_ttl_seconds: int = 3600
    fundamental_cache_max_entries: int = 256
    fundamental_retry_max: int = 2


_instance: Optional[Config] = None
_lock = Lock()


def _env_bool(key: str, default: str = "true") -> bool:
    return os.environ.get(key, default).lower() != "false"


def get_config() -> Config:
    """Return the global Config singleton, creating it on first call."""
    global _instance
    if _instance is not None:
        return _instance
    with _lock:
        if _instance is not None:
            return _instance
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
            realtime_source_priority=os.environ.get(
                "REALTIME_SOURCE_PRIORITY", "tencent,akshare,efinance"
            ),
            fundamental_fetch_timeout_seconds=float(
                os.environ.get("FUNDAMENTAL_FETCH_TIMEOUT_SECONDS", "30")
            ),
            fundamental_stage_timeout_seconds=float(
                os.environ.get("FUNDAMENTAL_STAGE_TIMEOUT_SECONDS", "60")
            ),
            fundamental_cache_ttl_seconds=int(
                os.environ.get("FUNDAMENTAL_CACHE_TTL_SECONDS", "3600")
            ),
            fundamental_cache_max_entries=int(
                os.environ.get("FUNDAMENTAL_CACHE_MAX_ENTRIES", "256")
            ),
            fundamental_retry_max=int(
                os.environ.get("FUNDAMENTAL_RETRY_MAX", "2")
            ),
        )
        return _instance
```

- [ ] **Step 2: Commit**

```bash
git add src/provider/_config.py
git commit -m "feat: add provider/_config module with slim Config singleton"
```

---

### Task 4: Update imports in `base.py`

**Files:**
- Modify: `src/provider/base.py`

- [ ] **Step 1: Replace top-level imports (lines 27-28)**

In `src/provider/base.py`, replace:

```python
from src.data.stock_index_loader import get_index_stock_name
from src.data.stock_mapping import STOCK_NAME_MAP, is_meaningful_stock_name
```

with:

```python
from provider._data.stock_index_loader import get_index_stock_name
from provider._data.stock_mapping import STOCK_NAME_MAP, is_meaningful_stock_name
```

- [ ] **Step 2: Replace all lazy `from src.config import get_config` (9 occurrences)**

Global replace in `src/provider/base.py`:

```python
# from
from src.config import get_config
# to
from provider._config import get_config
```

This appears at lines 564, 1066, 1151, 1400, 1751, 1973, 2270, 2334, 2384.

- [ ] **Step 3: Verify no remaining `from src.` in base.py**

```bash
grep "from src\." src/provider/base.py
```

Expected: no output.

- [ ] **Step 4: Commit**

```bash
git add src/provider/base.py
git commit -m "refactor: update base.py imports from src.* to provider._*"
```

---

### Task 5: Update imports in fetcher files

**Files:**
- Modify: `src/provider/efinance_fetcher.py` (line 55)
- Modify: `src/provider/akshare_fetcher.py` (line 45)
- Modify: `src/provider/tushare_fetcher.py` (line 36)
- Modify: `src/provider/yfinance_fetcher.py` (lines 40-42)
- Modify: `src/provider/longbridge_fetcher.py` (lines 165, 293, 326)

- [ ] **Step 1: Fix `efinance_fetcher.py`**

In `src/provider/efinance_fetcher.py`, line 55, replace:

```python
from src.config import get_config
```

with:

```python
from provider._config import get_config
```

- [ ] **Step 2: Fix `akshare_fetcher.py`**

In `src/provider/akshare_fetcher.py`, line 45, replace:

```python
from src.config import get_config
```

with:

```python
from provider._config import get_config
```

- [ ] **Step 3: Fix `tushare_fetcher.py`**

In `src/provider/tushare_fetcher.py`, line 36, replace:

```python
from src.config import get_config
```

with:

```python
from provider._config import get_config
```

- [ ] **Step 4: Fix `yfinance_fetcher.py`**

In `src/provider/yfinance_fetcher.py`, lines 39-42, replace:

```python
# 可选导入本地股票映射补丁，若缺失则使用空字典兜底
try:
    from src.data.stock_mapping import STOCK_NAME_MAP, is_meaningful_stock_name
except (ImportError, ModuleNotFoundError):
```

with:

```python
# 可选导入本地股票映射补丁，若缺失则使用空字典兜底
try:
    from provider._data.stock_mapping import STOCK_NAME_MAP, is_meaningful_stock_name
except (ImportError, ModuleNotFoundError):
```

- [ ] **Step 5: Fix `longbridge_fetcher.py`**

Three lazy imports inside try blocks. Replace each occurrence:

Line 165:
```python
# from
from src.report_language import normalize_report_language
# to
from provider._config import normalize_report_language
```

Line 293:
```python
# from
from src.config import get_config
# to
from provider._config import get_config
```

Line 326:
```python
# from
from src.config import get_config
# to
from provider._config import get_config
```

- [ ] **Step 6: Verify no remaining `from src.` in any provider file**

```bash
grep -r "from src\." src/provider/
```

Expected: no output.

- [ ] **Step 7: Commit**

```bash
git add src/provider/efinance_fetcher.py src/provider/akshare_fetcher.py src/provider/tushare_fetcher.py src/provider/yfinance_fetcher.py src/provider/longbridge_fetcher.py
git commit -m "refactor: update fetcher imports from src.* to provider._*"
```

---

### Task 6: Verify provider imports work

- [ ] **Step 1: Test that _config imports cleanly**

```bash
python -c "from provider._config import get_config, normalize_report_language; c = get_config(); print(f'Config OK: tushare_token={c.tushare_token!r}'); print(f'Lang: {normalize_report_language(\"chinese\")}')"
```

Expected:
```
Config OK: tushare_token=''
Lang: zh
```

- [ ] **Step 2: Test that _data imports cleanly**

```bash
python -c "from provider._data.stock_mapping import STOCK_NAME_MAP, is_meaningful_stock_name; print(f'Mapping OK: {len(STOCK_NAME_MAP)} entries'); print(f'茅台: {is_meaningful_stock_name(\"贵州茅台\", \"600519\")}')"
```

Expected:
```
Mapping OK: 90 entries
茅台: True
```

```bash
python -c "from provider._data.stock_index_loader import get_index_stock_name; print(f'Index loader OK: {get_index_stock_name(\"600519\")}')"
```

Expected: `Index loader OK: None` (no index file present, graceful fallback)

- [ ] **Step 3: Test that provider.__init__ imports without error**

```bash
python -c "from provider import DataFetcherManager; print('provider OK')"
```

Expected: `provider OK` (may show warnings about missing optional deps like efinance/akshare, but no ImportError)

- [ ] **Step 4: If any failures, fix and commit**

Address any remaining import errors discovered in steps 1-3.
