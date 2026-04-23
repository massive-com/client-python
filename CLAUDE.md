# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Official Python client library for the Massive (formerly Polygon.io) REST and WebSocket APIs. Provides market data access for stocks, options, forex, crypto, and more. Published as the `massive` package on PyPI.

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
