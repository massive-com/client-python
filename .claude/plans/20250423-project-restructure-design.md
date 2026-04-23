# Project Restructure Design

**Date:** 2025-04-23
**Scope:** One-shot restructure — directory migration, pyproject.toml rewrite, import fixup, cleanup

---

## 1. Goal

将项目从 Poetry-based 结构重构为标准 `src/` layout + PEP 621，同时重命名 `data_provider` → `processor`，并将 `provider/` 的第三方依赖正规化写入 `pyproject.toml`。

## 2. Target Directory Structure

```
massive-com/
├── src/
│   ├── massive/          # SDK 客户端（REST + WebSocket）
│   │   ├── __init__.py
│   │   ├── rest/
│   │   ├── websocket/
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── modelclass.py
│   ├── provider/         # 多数据源获取层
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── realtime_types.py
│   │   ├── us_index_mapping.py
│   │   ├── fundamental_adapter.py
│   │   ├── efinance_fetcher.py
│   │   ├── akshare_fetcher.py
│   │   ├── tushare_fetcher.py
│   │   ├── pytdx_fetcher.py
│   │   ├── baostock_fetcher.py
│   │   ├── yfinance_fetcher.py
│   │   ├── longbridge_fetcher.py
│   │   └── tickflow_fetcher.py
│   └── processor/        # 原 data_provider，重命名
│       ├── __init__.py
│       └── us_daily/
│           ├── __init__.py
│           ├── __main__.py
│           ├── config.py
│           ├── config.json
│           ├── storage.py
│           ├── ticker_filter.py
│           └── agg_fetcher.py
├── tests/
│   ├── test_rest/        # 原顶层 test_rest/
│   ├── test_websocket/   # 原顶层 test_websocket/
│   └── test_us_daily/    # 原 tests/test_us_daily/
├── examples/             # 不动
├── docs/                 # 不动
├── data/                 # 不动
├── logs/                 # 不动
├── pyproject.toml        # 重写
└── README.md
```

## 3. pyproject.toml

从 `[tool.poetry]` 迁移到 PEP 621 + setuptools：

```toml
[project]
name = "massive"
version = "0.0.0"
description = "Official Massive (formerly Polygon.io) REST and Websocket client."
requires-python = ">=3.9"
license = {text = "MIT"}

dependencies = [
    "urllib3>=1.26.9",
    "websockets>=14.0",
    "certifi>=2022.5.18,<2027.0.0",
    "pandas",
]

[project.optional-dependencies]
efinance = ["efinance"]
akshare = ["akshare"]
tushare = ["tushare"]
pytdx = ["pytdx"]
baostock = ["baostock"]
yfinance = ["yfinance"]
longbridge = ["longbridge-openapi"]
all = [
    "efinance",
    "akshare",
    "tushare",
    "pytdx",
    "baostock",
    "yfinance",
    "longbridge-openapi",
]
dev = [
    "black>=24.8.0",
    "mypy>=1.19",
    "types-urllib3>=1.26.25",
    "types-certifi>=2021.10.8",
    "types-setuptools>=81.0.0",
    "pook>=2.1.4",
    "orjson>=3.11.5",
    "pytest",
]
docs = [
    "Sphinx>=7.4.7",
    "sphinx-rtd-theme>=3.1.0",
    "sphinx-autodoc-typehints>=2.3.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.black]
line-length = 88

[tool.mypy]
python_version = "3.9"
```

## 4. Import Path Changes

### 4.1 `data_provider` → `processor`（~36 处）

**源码文件（3 个）：**
- `src/processor/us_daily/__main__.py`
- `src/processor/us_daily/ticker_filter.py`
- `src/processor/us_daily/agg_fetcher.py`

**测试文件（4 个）：**
- `tests/test_us_daily/test_agg_fetcher.py`（含 `patch()` 路径）
- `tests/test_us_daily/test_config.py`
- `tests/test_us_daily/test_storage.py`
- `tests/test_us_daily/test_ticker_filter.py`（含 `patch()` 路径）

全部执行 `data_provider` → `processor` 全局替换。

### 4.2 `massive` 包（0 处变更）

内部使用相对 import，搬入 `src/massive/` 后路径自动生效。两处绝对 import（`indicators.py`、`summaries.py`）配合 `pythonpath = ["src"]` 仍然有效。

### 4.3 `provider` 包（0 处变更）

当前无任何文件 import `provider`。

### 4.4 测试文件（0 处变更）

`test_rest/`、`test_websocket/` 中的 `from massive import ...` 路径不变，配合 `pythonpath = ["src"]` 生效。

## 5. config.py 路径修复

`processor/us_daily/config.py` 的 `load_config()` 默认参数从硬编码路径改为基于 `__file__` 的相对定位：

```python
def load_config(config_path: str = None) -> Config:
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
    ...
```

`data_dir = "data/us_daily"` 保持不变（相对于项目根目录）。

## 6. CLAUDE.md 更新

- 去掉 Poetry/Makefile 命令
- 新命令：`pip install -e ".[all,dev]"`、`pytest`、`black src/ tests/`、`mypy src/`
- 补充 `src/` layout、`provider/`、`processor/` 架构说明
- `python -m processor.us_daily` 作为 processor 运行入口

## 7. Delete & Cleanup

| 操作 | 目标 |
|------|------|
| 删除 | `Makefile`、`poetry.lock` |
| 保留不动 | `.massive/`、`docs/`、`examples/`、`data/`、`logs/`、`README.md` |

## 8. Not In Scope

- `provider/` 内部重组织（保持扁平结构不变）
- `processor/` 功能扩展（仅重命名占位）
- examples 路径更新（`from massive import` 不变）
- 测试框架迁移（保留 unittest，增加 pytest 支持）
