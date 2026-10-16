# AGENTS.md

Guidelines for AI coding agents working on the Massive Python client (`massive` on PyPI).

Unlike the Go, JS, and JVM clients, this SDK is **hand-written**. No code is generated, so changes go directly into `massive/`.

## Essential commands

```bash
poetry install         # Install dependencies (Python 3.10+)
make test              # Run REST and WebSocket tests
make test_rest         # REST tests only
make lint              # black --check + mypy (what CI runs)
poetry run black massive test_* examples   # Format
make rest-spec         # Download the latest OpenAPI spec to .massive/rest.json
```

If you use pyenv, run commands through `poetry run` or a Poetry shell so the right Python is used.

## Layout

- `massive/rest/base.py`: `BaseClient` with the HTTP pool, `_get`, `_paginate`, and `_get_params`.
- `massive/rest/*.py`: one mixin client per domain (`aggs.py`, `trades.py`, `reference.py`, `futures.py`, `financials.py`, ...). `massive/rest/__init__.py` combines them into `RESTClient`.
- `massive/rest/models/`: response models, one file per domain.
- `massive/websocket/`: WebSocket client and message models.
- `massive/modelclass.py`: the `@modelclass` decorator used by every model.
- `test_rest/`, `test_websocket/`: unittest suites. REST tests serve JSON fixtures from `test_rest/mocks/` using `pook`.
- `examples/`: runnable scripts (`rest/`, `websocket/`, `launchpad/`, `tools/`).
- `docs/`: Sphinx docs, published on ReadTheDocs.
- `.massive/`: a reference snapshot of the OpenAPI spec. Nothing in the code or tests reads it, and it may be out of date. Run `make rest-spec` before relying on it, or read https://api.massive.com/openapi directly.

## Adding a REST endpoint

The OpenAPI spec at https://api.massive.com/openapi is the source of truth for paths, parameters, and response fields.

1. **Model.** Add a class to the matching file in `massive/rest/models/`:
   ```python
   @modelclass
   class Disclosure:
       "Docstring describing the object."
       accession_number: Optional[str] = None

       @staticmethod
       def from_dict(d):
           return Disclosure(accession_number=d.get("accession_number"))
   ```
   Every field is `Optional[...] = None`. Read keys with `d.get(...)`, and build nested objects with `Sub.from_dict(d["x"]) if "x" in d else None`.
2. **Export.** Most model files are star-exported from `massive/rest/models/__init__.py`. If the file you used isn't (e.g. `benzinga`, `economy`, `etf_global`, `tmx`), import the model directly in the client module.
3. **Client method.** Add it to the matching domain client in `massive/rest/`:
   - List endpoints are named `list_<...>`, return `Union[Iterator[Model], HTTPResponse]`, and call `self._paginate(path=..., params=self._get_params(self.<method>, locals()), result_key="results", deserializer=Model.from_dict, raw=raw, options=options)`.
   - Single-object endpoints are named `get_<...>` and call `self._get(...)`.
   - Every query param is a keyword argument defaulting to `None`. Write range filters as `x_gt`, `x_gte`, `x_lt`, `x_lte`, `x_any_of`; `_get_params` turns them into `x.gt` and so on.
   - Always end the signature with `params: Optional[Dict[str, Any]] = None, raw: bool = False, options: Optional[RequestOptionBuilder] = None`.
4. **New domain only.** Create a `BaseClient` subclass and add it to `RESTClient`'s bases in `massive/rest/__init__.py`.
5. **Tests, examples, docs.** For core endpoints, add a fixture under `test_rest/mocks/<url path>.json`, a test in `test_rest/test_<domain>.py`, an example in `examples/rest/`, and an `automethod` entry in `docs/source/*.rst`.
6. Run `make lint` and `make test`.

## Conventions

- Keep Python 3.10 compatibility, and match the existing style: `typing.Optional`, `Union`, `List`, `Dict`, not `X | Y`.
- Format with black (defaults). Code must pass mypy.
- Don't break public APIs. When an endpoint gets a new version, keep the old method and add a versioned one (e.g. `list_trades_v4`). Adding model fields is always fine. `client.vx` is experimental.
- API keys come from the `MASSIVE_API_KEY` env var. Never hardcode a key in code, tests, or examples.
- Tests must not call the live API. Use the `test_rest/mocks/` fixtures.

## Pull requests

- Open or link an issue first. PRs not tied to an issue are generally declined.
- Releases come from `v*` tags on `master` (see `.github/workflows/release.yml`). Don't change the version in `pyproject.toml`; it's set from the tag.
