# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Official Python client library for the Massive (formerly Polygon.io) REST and WebSocket APIs. Provides market data access for stocks, options, forex, crypto, and more. Published as the `massive` package on PyPI.

## Development Commands

```bash
# Install dependencies
poetry install

# Run all tests
make test

# Run only REST or WebSocket tests
make test_rest
make test_websocket

# Run a single test file
poetry run python -m unittest test_rest/test_aggs.py

# Run a single test method
poetry run python -m unittest test_rest.test_aggs.TestAggs.test_list_aggs

# Code formatting (auto-fix)
make style

# Static type checking
poetry run mypy massive test_* examples

# Both style + static checks
make lint

# Regenerate REST API spec from OpenAPI
make rest-spec
```

## Architecture

### Client Structure

`RESTClient` (in `massive/rest/__init__.py`) uses multiple inheritance to compose domain-specific client mixins (AggsClient, TradesClient, QuotesClient, etc.) on top of `BaseClient` (`massive/rest/base.py`). Each mixin lives in its own file under `massive/rest/` and handles one API domain.

`WebSocketClient` (`massive/websocket/__init__.py`) is a standalone async client using the `websockets` library with auto-reconnect support.

### Models

- REST models: `massive/rest/models/` — one file per domain, using the custom `@modelclass` decorator (from `massive/modelclass.py`) which wraps `@dataclass` with flexible init that accepts positional or keyword args.
- WebSocket models: `massive/websocket/models/`

### API Spec Codegen

`.massive/rest.py` generates REST client code from `.massive/rest.json` (OpenAPI spec). `.massive/websocket.json` is the WebSocket spec. Use `make rest-spec` / `make ws-spec` to update specs from the API.

### Tests

- `test_rest/` — uses `pook` for HTTP mocking, with mock responses in `test_rest/mocks/`
- `test_websocket/` — has its own mock WebSocket server in `mock_server.py`
- Test base classes: `test_rest/base.py` and `test_websocket/base_ws.py`

### Key Conventions

- API key via `MASSIVE_API_KEY` env var or constructor parameter
- Base URL: `https://api.massive.com`
- Auth header: `Authorization: Bearer <key>`
- Python 3.9+ required
- Formatting: `black`; type checking: `mypy`
