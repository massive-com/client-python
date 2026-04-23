from .base import BaseClient
from typing import Optional, Any, Dict, List, Union, Iterator
from .models import (
    TickerSnapshot,
    Direction,
    OptionContractSnapshot,
    SnapshotMarketType,
    SnapshotTickerFullBook,
    UniversalSnapshot,
    IndicesSnapshot,
    Sort,
    Order,
)
from urllib3 import HTTPResponse

from .models.request import RequestOptionBuilder


def get_locale(market_type: Union[SnapshotMarketType, str]):
    if market_type == SnapshotMarketType.STOCKS.value:
        return "us"

    return "global"


class SnapshotClient(BaseClient):
    def list_universal_snapshots(
        self,
        type: Optional[Union[str, SnapshotMarketType]] = None,
        ticker_any_of: Optional[List[str]] = None,
        order: Optional[Union[str, Order]] = None,
        limit: Optional[int] = 10,
        sort: Optional[Union[str, Sort]] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[UniversalSnapshot], HTTPResponse]:
        """
        Get snapshots for assets of all types
        - https://massive.com/docs/stocks/get_v3_snapshot
        - https://massive.com/docs/options/get_v3_snapshot
        - https://massive.com/docs/indices/get_v3_snapshot
        - https://massive.com/docs/forex/get_v3_snapshot
        - https://massive.com/docs/crypto/get_v3_snapshot

        :param type: the type of the asset
        :param ticker_any_of: Comma-separated list of tickers, up to a maximum of 250. If no tickers are passed then all
        :param order: The order to sort the results on. Default is asc (ascending).
        :param limit: Limit the size of the response per-page, default is 10 and max is 250.
        :param sort: The field to sort the results on. Default is ticker. If the search query parameter is present, sort is ignored and results are ordered by relevance.
        results will be returned in a paginated manner. Warning: The maximum number of characters allowed in a URL
        are subject to your technology stack.
        :param ticker_lt search for tickers less than
        :param ticker_lte search for tickers less than or equal to
        :param ticker_gt search for tickers greater than
        :param ticker_gte search for tickers greater than or equal to
        :param raw: returns the raw HTTP response if true, else the response is deserialized into a structured object
        :param options: request options
        :return: list of Snapshots
        """
        url = f"/v3/snapshot"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_universal_snapshots, locals()),
            result_key="results",
            deserializer=UniversalSnapshot.from_dict,
            raw=raw,
            options=options,
        )

    def get_snapshot_all(
        self,
        market_type: Union[str, SnapshotMarketType],
        tickers: Optional[Union[str, List[str]]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        include_otc: Optional[bool] = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[TickerSnapshot], HTTPResponse]:
        """
        Get the most up-to-date market data for all traded stock symbols.

        Note: Snapshot data is cleared at 12am EST and gets populated as data is received from the exchanges. This can happen as early as 4am EST.

        :param market_type: Which market to get a snapshot of.
        :param tickers: A comma separated list of tickers to get snapshots for.
        :param include_otc: Include OTC securities in the response. Default is false (don't include OTC securities).
        :return: List of Snapshots
        """
        locale = get_locale(market_type)
        url = f"/v2/snapshot/locale/{locale}/markets/{market_type}/tickers"
        if type(tickers) is list:
            tickers = ",".join(tickers)
        return self._get(
            path=url,
            params=self._get_params(self.get_snapshot_all, locals()),
            deserializer=TickerSnapshot.from_dict,
            raw=raw,
            result_key="tickers",
            options=options,
        )

    def get_snapshot_direction(
        self,
        market_type: Union[str, SnapshotMarketType],
        direction: Union[str, Direction],
        params: Optional[Dict[str, Any]] = None,
        include_otc: Optional[bool] = False,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[TickerSnapshot], HTTPResponse]:
        """
        Get the most up-to-date market data for the current top 20 gainers or losers of the day in the stocks/equities markets.

        Top gainers are those tickers whose price has increased by the highest percentage since the previous day's close. Top losers are those tickers whose price has decreased by the highest percentage since the previous day's close.

        Note: Snapshot data is cleared at 12am EST and gets populated as data is received from the exchanges.

        :param market_type: Which market to get a snapshot of.
        :param direction: The direction ("gainers" or "losers")
        :param include_otc: Include OTC securities in the response. Default is false (don't include OTC securities).
        :return: List of Snapshots
        """
        locale = get_locale(market_type)
        url = f"/v2/snapshot/locale/{locale}/markets/{market_type}/{direction}"
        return self._get(
            path=url,
            params=self._get_params(self.get_snapshot_direction, locals()),
            result_key="tickers",
            deserializer=TickerSnapshot.from_dict,
            raw=raw,
            options=options,
        )

    def get_snapshot_ticker(
        self,
        market_type: Union[str, SnapshotMarketType],
        ticker: str,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[TickerSnapshot, HTTPResponse]:
        """
        Get the most up-to-date market data for all traded stock symbols.

        Note: Snapshot data is cleared at 12am EST and gets populated as data is received from the exchanges. This can happen as early as 4am EST.

        :param market_type: Which market to get a snapshot of.
        :param ticker: The ticker symbol.
        :return: List of Snapshots
        """
        locale = get_locale(market_type)
        url = f"/v2/snapshot/locale/{locale}/markets/{market_type}/tickers/{ticker}"
        return self._get(
            path=url,
            params=self._get_params(self.get_snapshot_ticker, locals()),
            result_key="ticker",
            deserializer=TickerSnapshot.from_dict,
            raw=raw,
            options=options,
        )

    def get_snapshot_option(
        self,
        underlying_asset: str,
        option_contract: str,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[OptionContractSnapshot, HTTPResponse]:
        """
        Get the snapshot of an option contract for a stock equity.

        :param underlying_asset: The underlying ticker symbol of the option contract.
        :param option_contract: The option contract identifier.
        :return: List of Snapshots
        """
        url = f"/v3/snapshot/options/{underlying_asset}/{option_contract}"
        return self._get(
            path=url,
            params=self._get_params(self.get_snapshot_option, locals()),
            result_key="results",
            deserializer=OptionContractSnapshot.from_dict,
            raw=raw,
            options=options,
        )

    def list_snapshot_options_chain(
        self,
        underlying_asset: str,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[OptionContractSnapshot], HTTPResponse]:
        """
        Get the snapshot of all options contracts for an underlying ticker.

        :param underlying_asset: The underlying ticker symbol of the option contract.
        :return: List of Snapshots
        """
        url = f"/v3/snapshot/options/{underlying_asset}"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_snapshot_options_chain, locals()),
            result_key="results",
            deserializer=OptionContractSnapshot.from_dict,
            raw=raw,
            options=options,
        )

    def get_snapshot_crypto_book(
        self,
        ticker: str,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[SnapshotTickerFullBook, HTTPResponse]:
        """
        Get the current level 2 book of a single ticker. This is the combined book from all of the exchanges.

        Note: Snapshot data is cleared at 12am EST and gets populated as data is received from the exchanges.

        :param ticker: The ticker symbol.
        :return: List of Snapshots
        """
        url = f"/v2/snapshot/locale/global/markets/crypto/tickers/{ticker}/book"
        return self._get(
            path=url,
            params=self._get_params(self.get_snapshot_crypto_book, locals()),
            result_key="data",
            deserializer=SnapshotTickerFullBook.from_dict,
            raw=raw,
            options=options,
        )

    def get_snapshot_indices(
        self,
        ticker_any_of: Optional[Union[str, List[str]]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[IndicesSnapshot], HTTPResponse]:
        url = f"/v3/snapshot/indices"

        return self._get(
            path=url,
            params=self._get_params(self.get_snapshot_indices, locals()),
            deserializer=IndicesSnapshot.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )
