.. _snapshot_header:

Snapshot
=================================

=================================
Get snapshots for all asset types
=================================

- `Stocks snapshot all tickers`_
- `Options snapshot all tickers`_
- `Forex snapshot all tickers`_
- `Crypto snapshot all tickers`_

.. automethod:: massive.RESTClient.list_universal_snapshots

=================================
Get all snapshots
=================================

- `Stocks snapshot all tickers (deprecated)`_
- `Forex snapshot all tickers (deprecated)`_
- `Crypto snapshot all tickers (deprecated)`_

.. automethod:: massive.RESTClient.get_snapshot_all

=================================
Get gainers/losers snapshot
=================================

- `Stocks snapshot gainers/losers`_
- `Forex snapshot gainers/losers`_
- `Crypto snapshot gainers/losers`_

.. automethod:: massive.RESTClient.get_snapshot_direction

=================================
Get ticker snapshot
=================================

- `Stocks snapshot ticker`_
- `Forex snapshot ticker`_
- `Crypto snapshot ticker`_

.. automethod:: massive.RESTClient.get_snapshot_ticker

=================================
Get options snapshot
=================================

- `Options snapshot option contract`_

.. automethod:: massive.RESTClient.get_snapshot_option

=================================
Get crypto L2 book snapshot
=================================

- `Crypto snapshot ticker full book (L2)`_

.. automethod:: massive.RESTClient.get_snapshot_crypto_book

=================================
Get indices snapshot
=================================

- `Indices snapshot`_

.. automethod:: massive.RESTClient.list_snapshot_indices

.. automethod:: massive.RESTClient.get_snapshot_indices

.. _Stocks snapshot all tickers: https://massive.com/docs/stocks/get_v3_snapshot
.. _Options snapshot all tickers: https://massive.com/docs/options/get_v3_snapshot
.. _Forex snapshot all tickers: https://massive.com/docs/forex/get_v3_snapshot
.. _Crypto snapshot all tickers:: https://massive.com/docs/crypto/get_v3_snapshot
.. _Stocks snapshot all tickers (deprecated): https://massive.com/docs/stocks/get_v2_snapshot_locale_us_markets_stocks_tickers
.. _Options snapshot all tickers (deprecated): https://massive.com/docs/options/get_v2_snapshot_locale_us_markets_stocks_tickers
.. _Forex snapshot all tickers (deprecated): https://massive.com/docs/forex/get_v2_snapshot_locale_global_markets_forex_tickers
.. _Crypto snapshot all tickers (deprecated):: https://massive.com/docs/crypto/get_v2_snapshot_locale_global_markets_crypto_tickers
.. _Stocks snapshot gainers/losers: https://massive.com/docs/stocks/get_v2_snapshot_locale_us_markets_stocks__direction
.. _Forex snapshot gainers/losers: https://massive.com/docs/forex/get_v2_snapshot_locale_global_markets_forex__direction
.. _Crypto snapshot gainers/losers: https://massive.com/docs/crypto/get_v2_snapshot_locale_global_markets_crypto__direction
.. _Stocks snapshot ticker: https://massive.com/docs/stocks/get_v2_snapshot_locale_us_markets_stocks_tickers__stocksticker
.. _Forex snapshot ticker: https://massive.com/docs/forex/get_v2_snapshot_locale_global_markets_forex_tickers__ticker
.. _Crypto snapshot ticker: https://massive.com/docs/crypto/get_v2_snapshot_locale_global_markets_crypto_tickers__ticker
.. _Options snapshot option contract: https://massive.com/docs/options/get_v3_snapshot_options__underlyingasset___optioncontract
.. _Crypto snapshot ticker full book (L2): https://massive.com/docs/crypto/get_v2_snapshot_locale_global_markets_crypto_tickers__ticker__book
.. _Indices snapshot: https://massive.com/docs/indices/get_v3_snapshot_indices
