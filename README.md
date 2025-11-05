# Massive (formerly Polygon.io) Python Client - WebSocket & RESTful APIs

Welcome to the official Python client library for the [Massive](https://massive.com/) REST and WebSocket API. To get started, please see the [Getting Started](https://massive.com/docs/stocks/getting-started) section in our documentation, view the [examples](./examples/) directory for code snippets.

**Note:** Polygon.io has rebranded as [Massive.com](https://massive.com) on Oct 30, 2025. Existing API keys, accounts, and integrations continue to work exactly as before. The only change in this SDK is that it now defaults to the new API base at `api.massive.com`, while `api.polygon.io` remains supported for an extended period.

For details, see our [rebrand announcement blog post](https://massive.com/blog/polygon-is-now-massive/) or open an issue / contact [support@massive.com](mailto:support@massive.com) if you have questions.

## Prerequisites

Before installing the Massive Python client, ensure your environment has Python 3.9 or higher.

## Install

Please use pip to install or update to the latest stable version.
```
pip install -U massive
```

## Getting started

To get started, please see the [Getting Started](https://massive.com/docs/stocks/getting-started) section in our docs, view the [examples](./examples) directory for code snippets.

The free tier of our API comes with usage limitations, potentially leading to rate limit errors if these are exceeded. For uninterrupted access and to support larger data requirements, we recommend reviewing our [subscription plans](https://massive.com/pricing), which are tailored for a wide range of needs from development to high-demand applications. Refer to our pricing page for detailed information on limits and features to ensure a seamless experience, especially for real-time data processing.

## REST API Client
Import the RESTClient.
```python
from massive import RESTClient
```
Create a new client with your [API key](https://massive.com/dashboard/api-keys)
```python
client = RESTClient(api_key="<API_KEY>")
```
### Using the Client
Request data using client methods.
```python
ticker = "AAPL"

# List Aggregates (Bars)
aggs = []
for a in client.list_aggs(ticker=ticker, multiplier=1, timespan="minute", from_="2023-01-01", to="2023-06-13", limit=50000):
    aggs.append(a)

print(aggs)

# Get Last Trade
trade = client.get_last_trade(ticker=ticker)
print(trade)

# List Trades
trades = client.list_trades(ticker=ticker, timestamp="2022-01-04")
for trade in trades:
    print(trade)

# Get Last Quote
quote = client.get_last_quote(ticker=ticker)
print(quote)

# List Quotes
quotes = client.list_quotes(ticker=ticker, timestamp="2022-01-04")
for quote in quotes:
    print(quote)
```

### Pagination Behavior

By default, the client paginates results for endpoints like `list_trades` and `list_quotes` behind the scenes for you. Understanding how pagination interacts with the `limit` parameter is key.

#### Default (Pagination Enabled)

Pagination is enabled by default (`pagination=True`):

* `limit` controls the page size, not the total number of results.
* The client automatically fetches all pages, yielding results until none remain.

Here's an example:

```python
client = RESTClient(api_key="<API_KEY>")
trades = [t for t in client.list_trades(ticker="TSLA", limit=100)]
```

This fetches all TSLA trades, 100 per page.

#### Disabling Pagination

To return a fixed number of results and stop, disable pagination:

```python
client = RESTClient(api_key="<API_KEY>", pagination=False)
trades = [t for t in client.list_trades(ticker="TSLA", limit=100)]
```

This returns at most 100 total trades, no additional pages.

### Performance Tip

If you're fetching large datasets, always use the maximum supported limit for the API endpoint. This reduces the number of API calls and improves overall performance.

### Additional Filter Parameters

Many of the APIs in this client library support the use of additional filter parameters to refine your queries. Please refer to the specific API documentation for details on which filter parameters are supported for each endpoint. These filters can be applied using the following operators:

- `.gt`: greater than
- `.gte`: greater than or equal to
- `.lt`: less than
- `.lte`: less than or equal to

Here's a sample code snippet that demonstrates how to use these filter parameters when requesting an Options Chain using the `list_snapshot_options_chain` method. In this example, the filter parameters ensure that the returned options chain data will only include options with an expiration date that is greater than or equal to "2024-03-16" and a strike price that falls between 29 and 30 (inclusive).

```python
options_chain = []
for o in client.list_snapshot_options_chain(
    "HCP",
    params={
        "expiration_date.gte": "2024-03-16",
        "strike_price.gte": 29,
        "strike_price.lte": 30,
    },
):
    options_chain.append(o)

print(options_chain)
print(len(options_chain))
```

Also, please refer to the API documentation to get a full understanding of how the API works and the supported arguments. All required arguments are annotated with red asterisks " * " and argument examples are set.

## Debugging with RESTClient

Sometimes you may find it useful to see the actual request and response details while working with the API. The `RESTClient` allows for this through its `trace=True` option.

### How to Enable Debug Mode

You can activate the debug mode as follows:

```python
client = RESTClient(trace=True, verbose=True)
```

### What Does Debug Mode Do?

When debug mode is enabled, the client will print out useful debugging information for each API request. You need to enable `verbose=True` too so that you log the trace or already have your own logger configured. This includes: the request URL, the headers sent in the request, and the headers received in the response.

### Example Output

For instance, if you made a request for `TSLA` data for the date `2023-08-01`, you would see debug output similar to the following:

```
Request URL: https://api.massive.com/v2/aggs/ticker/TSLA/range/1/minute/2023-08-01/2023-08-01?limit=50000
Request Headers: {'Authorization': 'Bearer REDACTED', 'Accept-Encoding': 'gzip', 'User-Agent': 'Massive.com PythonClient/1.12.4'}
Response Headers: {'Server': 'nginx/1.19.2', 'Date': 'Tue, 05 Sep 2023 23:07:02 GMT', 'Content-Type': 'application/json', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Content-Encoding': 'gzip', 'Vary': 'Accept-Encoding', 'X-Request-Id': '727c82feed3790b44084c3f4cae1d7d4', 'Strict-Transport-Security': 'max-age=15724800; includeSubDomains'}
```

This can be an invaluable tool for debugging issues or understanding how the client interacts with the API.

## WebSocket Client 

Import classes
```python
from massive import WebSocketClient
from massive.websocket.models import WebSocketMessage
from typing import List
```
### Using the client
Create a new client with your [API key](https://massive.com/dashboard/api-keys) and subscription options.
```python
# Note: Multiple subscriptions can be added to the array 
# For example, if you want to subscribe to AAPL and META,
# you can do so by adding "T.META" to the subscriptions array. ["T.AAPL", "T.META"]
# If you want to subscribe to all tickers, place an asterisk in place of the symbol. ["T.*"]
ws = WebSocketClient(api_key=<API_KEY>, subscriptions=["T.AAPL"])
```
Create a handler function and run the WebSocket.
```python
def handle_msg(msg: List[WebSocketMessage]):
    for m in msg:
        print(m)

ws.run(handle_msg=handle_msg)
```
Check out more detailed examples [here](https://github.com/massive-com/client-python/tree/master/examples/websocket).

## Contributing

If you found a bug or have an idea for a new feature, please first discuss it with us by
[submitting a new issue](https://github.com/massive-com/client-python/issues/new/choose).
We will respond to issues within at most 3 weeks.
We're also open to volunteers if you want to submit a PR for any open issues but
please discuss it with us beforehand. PRs that aren't linked to an existing issue or
discussed with us ahead of time will generally be declined.

### Development

If you plan to contribute by developing new features then you will need to install certain dependencies.

#### Poetry

Poetry is a packaging and dependency manager for Python.
Installation instructions can be found [on their website](https://python-poetry.org/docs/#installation).
Once installed run `poetry install` to install the required dependencies. This step should be run after incorporating new upstream changes.

#### Makefile

Our Makefile has the common operations needed when developing on this repo. Running tests and linting can both be
run through our Makefile. Just run `make help` to see the list of available commands.

If you're using `pyenv` to manage active Python versions then you might need to launch a Poetry shell before running
Make commands in order to actually use your chosen Python version. This is because Poetry uses the system Python version
by default.

```shell
poetry shell # start shell
poetry install # install deps

make test # run your make commands
```

## Release planning
This client will attempt to follow the release cadence of our API.
When endpoints are deprecated and newer versions are added, the client will
maintain two methods in a backwards compatible way
(e.g. `list_trades` and `list_trades_v4(...)`).
When deprecated endpoints are removed from the API, we'll rename the versioned
method (e.g. `list_trades_v4(...)` -> `list_trades(...)`), remove the old method,
and release a new major version of the client.

The goal is to give users ample time to upgrade to newer versions of our API
_before_ we bump the major version of the client, and in general, we'll try to
bundle breaking changes like this to avoid frequent major version bumps.

Exceptions to this are:

- Methods under `client.vx`. These are expiremental.
- Methods that start with `_*`. We use these internally.
- Type annotations. We may modify these based on our JSON responses.
- We may add model fields.
