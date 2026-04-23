# Project Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure the project from Poetry-based layout to standard `src/` layout with PEP 621, rename `data_provider` to `processor`, and normalize dependencies in `pyproject.toml`.

**Architecture:** Move `massive/`, `provider/`, `data_provider/` into `src/` (renaming `data_provider` to `processor`). Move `test_rest/` and `test_websocket/` into `tests/`. Rewrite `pyproject.toml` from `[tool.poetry]` to PEP 621 + setuptools. Fix all `data_provider` → `processor` imports. Delete `Makefile` and `poetry.lock`.

**Tech Stack:** Python 3.9+, setuptools, pytest

**Design Doc:** `.claude/plans/20250423-project-restructure-design.md`

---

### Task 1: Create `src/` directory and move packages

**Files:**
- Create: `src/` directory
- Move: `massive/` → `src/massive/`
- Move: `provider/` → `src/provider/`
- Move: `data_provider/` → `src/processor/` (rename)

- [ ] **Step 1: Create src directory**

```bash
mkdir -p src
```

- [ ] **Step 2: Move massive/ into src/**

```bash
git mv massive src/massive
```

- [ ] **Step 3: Move provider/ into src/**

```bash
git mv provider src/provider
```

- [ ] **Step 4: Move data_provider/ to src/processor/ (rename)**

```bash
git mv data_provider src/processor
```

- [ ] **Step 5: Verify directory structure**

```bash
ls src/
```

Expected: `massive  processor  provider`

```bash
ls src/processor/us_daily/
```

Expected: `__init__.py  __main__.py  agg_fetcher.py  config.json  config.py  storage.py  ticker_filter.py`

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor: move massive, provider, data_provider into src/ layout

Rename data_provider to processor."
```

---

### Task 2: Move test directories into tests/

**Files:**
- Move: `test_rest/` → `tests/test_rest/`
- Move: `test_websocket/` → `tests/test_websocket/`
- Keep: `tests/test_us_daily/` (already in place)

- [ ] **Step 1: Move test_rest/ into tests/**

```bash
git mv test_rest tests/test_rest
```

- [ ] **Step 2: Move test_websocket/ into tests/**

```bash
git mv test_websocket tests/test_websocket
```

- [ ] **Step 3: Verify structure**

```bash
ls tests/
```

Expected: `__init__.py  test_rest  test_us_daily  test_websocket`

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "refactor: move test_rest and test_websocket into tests/"
```

---

### Task 3: Fix `data_provider` → `processor` imports in source files

**Files:**
- Modify: `src/processor/us_daily/__main__.py` (lines 8-16)
- Modify: `src/processor/us_daily/ticker_filter.py` (line 5)
- Modify: `src/processor/us_daily/agg_fetcher.py` (lines 7-12)

- [ ] **Step 1: Fix imports in `__main__.py`**

In `src/processor/us_daily/__main__.py`, replace all `data_provider` with `processor`:

```python
# Line 8-16: change from
from data_provider.us_daily.config import load_config
from data_provider.us_daily.storage import (
    get_tickers_file_path,
    file_exists,
    save_json,
    load_json,
)
from data_provider.us_daily.ticker_filter import filter_top_tickers
from data_provider.us_daily.agg_fetcher import fetch_ticker_aggs

# to
from processor.us_daily.config import load_config
from processor.us_daily.storage import (
    get_tickers_file_path,
    file_exists,
    save_json,
    load_json,
)
from processor.us_daily.ticker_filter import filter_top_tickers
from processor.us_daily.agg_fetcher import fetch_ticker_aggs
```

- [ ] **Step 2: Fix imports in `ticker_filter.py`**

In `src/processor/us_daily/ticker_filter.py`, line 5:

```python
# change from
from data_provider.us_daily.config import Config

# to
from processor.us_daily.config import Config
```

- [ ] **Step 3: Fix imports in `agg_fetcher.py`**

In `src/processor/us_daily/agg_fetcher.py`, lines 7-12:

```python
# change from
from data_provider.us_daily.config import Config
from data_provider.us_daily.storage import (
    get_month_file_path,
    file_exists,
    save_json,
)

# to
from processor.us_daily.config import Config
from processor.us_daily.storage import (
    get_month_file_path,
    file_exists,
    save_json,
)
```

- [ ] **Step 4: Commit**

```bash
git add src/processor/
git commit -m "refactor: update data_provider imports to processor in source files"
```

---

### Task 4: Fix `data_provider` → `processor` imports in test files

**Files:**
- Modify: `tests/test_us_daily/test_agg_fetcher.py` (all `data_provider` refs including `patch()` paths)
- Modify: `tests/test_us_daily/test_config.py` (all `data_provider` refs)
- Modify: `tests/test_us_daily/test_storage.py` (all `data_provider` refs)
- Modify: `tests/test_us_daily/test_ticker_filter.py` (all `data_provider` refs including `patch()` paths)

- [ ] **Step 1: Fix `test_agg_fetcher.py`**

Global replace `data_provider` → `processor` in `tests/test_us_daily/test_agg_fetcher.py`. This covers:
- `from data_provider.us_daily.agg_fetcher import ...` (lines 12, 18, 25, 32, 39, 46, 56, 63, 77, 107, 151, 193)
- `from data_provider.us_daily.config import Config` (lines 78, 108, 152, 194)
- `patch("data_provider.us_daily.agg_fetcher....)` (lines 54, 61, 95, 98, 100, 131, 134, 136, 181, 184, 186, 208, 211, 213)

All become `processor.us_daily.*`.

- [ ] **Step 2: Fix `test_config.py`**

Global replace `data_provider` → `processor` in `tests/test_us_daily/test_config.py`. This covers:
- `from data_provider.us_daily.config import Config` (line 9)
- `from data_provider.us_daily.config import load_config` (lines 20, 37)

- [ ] **Step 3: Fix `test_storage.py`**

Global replace `data_provider` → `processor` in `tests/test_us_daily/test_storage.py`. This covers:
- `from data_provider.us_daily.storage import ...` (lines 16, 22, 28, 37, 44)

- [ ] **Step 4: Fix `test_ticker_filter.py`**

Global replace `data_provider` → `processor` in `tests/test_us_daily/test_ticker_filter.py`. This covers:
- `from data_provider.us_daily.ticker_filter import filter_top_tickers` (lines 22, 54)
- `from data_provider.us_daily.config import Config` (lines 23, 56)
- `patch("data_provider.us_daily.ticker_filter.EXCHANGES", ...)` (lines 45, 69, 101)
- `patch("data_provider.us_daily.ticker_filter.time.sleep")` (lines 46, 70, 102)

- [ ] **Step 5: Commit**

```bash
git add tests/test_us_daily/
git commit -m "refactor: update data_provider imports to processor in test files"
```

---

### Task 5: Fix `config.py` path to use `__file__`-relative lookup

**Files:**
- Modify: `src/processor/us_daily/config.py` (line 16)

- [ ] **Step 1: Update `load_config` default path**

In `src/processor/us_daily/config.py`, change:

```python
# from
def load_config(config_path: str = "data_provider/us_daily/config.json") -> Config:
    config = Config()
    if os.path.exists(config_path):

# to
def load_config(config_path: str = None) -> Config:
    config = Config()
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
```

- [ ] **Step 2: Commit**

```bash
git add src/processor/us_daily/config.py
git commit -m "fix: use __file__-relative path for config.json lookup"
```

---

### Task 6: Rewrite `pyproject.toml`

**Files:**
- Modify: `pyproject.toml` (full rewrite)

- [ ] **Step 1: Replace pyproject.toml content**

Replace the entire `pyproject.toml` with:

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

- [ ] **Step 2: Commit**

```bash
git add pyproject.toml
git commit -m "refactor: rewrite pyproject.toml from Poetry to PEP 621 + setuptools"
```

---

### Task 7: Delete Makefile and poetry.lock

**Files:**
- Delete: `Makefile`
- Delete: `poetry.lock`

- [ ] **Step 1: Delete Makefile**

```bash
git rm Makefile
```

- [ ] **Step 2: Delete poetry.lock**

```bash
git rm poetry.lock
```

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove Makefile and poetry.lock"
```

---

### Task 8: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update Development Commands section**

Replace the Development Commands section with:

````markdown
## Development Commands

```bash
# Install dependencies (core + all data sources + dev tools)
pip install -e ".[all,dev]"

# Run all tests
pytest

# Run specific test directory
pytest tests/test_rest/
pytest tests/test_websocket/
pytest tests/test_us_daily/

# Run a single test file
pytest tests/test_rest/test_aggs.py

# Run a single test method
pytest tests/test_rest/test_aggs.py::TestAggs::test_list_aggs

# Code formatting (auto-fix)
black src/ tests/ examples/

# Static type checking
mypy src/

# Run US daily data processor
python -m processor.us_daily

# Regenerate REST API spec from OpenAPI
python .massive/rest.py

# Update WebSocket API spec
curl https://api.massive.com/specs/websocket.json > .massive/websocket.json
```
````

- [ ] **Step 2: Update Architecture section**

Replace the Architecture section with:

````markdown
## Architecture

### Project Layout

Standard `src/` layout with three top-level packages:

- `src/massive/` — REST and WebSocket SDK client library
- `src/provider/` — Multi-source data fetcher layer with automatic failover
- `src/processor/` — Data collection and processing pipelines

### Client Structure

`RESTClient` (in `massive/rest/__init__.py`) uses multiple inheritance to compose domain-specific client mixins (AggsClient, TradesClient, QuotesClient, etc.) on top of `BaseClient` (`massive/rest/base.py`). Each mixin lives in its own file under `massive/rest/` and handles one API domain.

`WebSocketClient` (`massive/websocket/__init__.py`) is a standalone async client using the `websockets` library with auto-reconnect support.

### Provider Layer

`DataFetcherManager` (in `provider/base.py`) orchestrates multiple data source fetchers (efinance, akshare, tushare, pytdx, baostock, yfinance, longbridge) with automatic priority-based failover. Each fetcher extends `BaseFetcher` and implements source-specific data retrieval.

### Processor

`processor/us_daily/` fetches US stock daily OHLCV data via the Massive REST API. Run with `python -m processor.us_daily`.

### Models

- REST models: `massive/rest/models/` — one file per domain, using the custom `@modelclass` decorator (from `massive/modelclass.py`) which wraps `@dataclass` with flexible init that accepts positional or keyword args.
- WebSocket models: `massive/websocket/models/`

### API Spec Codegen

`.massive/rest.py` generates REST client code from `.massive/rest.json` (OpenAPI spec). `.massive/websocket.json` is the WebSocket spec.

### Tests

- `tests/test_rest/` — uses `pook` for HTTP mocking, with mock responses in `tests/test_rest/mocks/`
- `tests/test_websocket/` — has its own mock WebSocket server in `mock_server.py`
- `tests/test_us_daily/` — unit tests for the US daily processor
- Test base classes: `tests/test_rest/base.py` and `tests/test_websocket/base_ws.py`

### Key Conventions

- API key via `MASSIVE_API_KEY` env var or constructor parameter
- Base URL: `https://api.massive.com`
- Auth header: `Authorization: Bearer <key>`
- Python 3.9+ required
- Formatting: `black`; type checking: `mypy`
````

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md for new project structure"
```

---

### Task 9: Verify everything works

- [ ] **Step 1: Install in editable mode**

```bash
pip install -e ".[dev]"
```

Expected: Installs successfully with no errors.

- [ ] **Step 2: Run us_daily tests**

```bash
pytest tests/test_us_daily/ -v
```

Expected: All tests pass. Specifically:
- `test_config.py` — 3 tests pass
- `test_storage.py` — 5 tests pass
- `test_agg_fetcher.py` — 8 tests pass (4 classes)
- `test_ticker_filter.py` — 3 tests pass

- [ ] **Step 3: Run REST tests**

```bash
pytest tests/test_rest/ -v
```

Expected: All tests pass.

- [ ] **Step 4: Run WebSocket tests**

```bash
pytest tests/test_websocket/ -v
```

Expected: All tests pass.

- [ ] **Step 5: Verify import works**

```bash
python -c "from massive import RESTClient; print('massive OK')"
python -c "from processor.us_daily.config import Config; print('processor OK')"
python -c "from provider.base import DataFetcherManager; print('provider OK')"
```

Expected: All three print their "OK" message.

- [ ] **Step 6: If any failures, fix and commit**

Address any import errors or test failures discovered in steps 1-5, then commit fixes.
