from typing import Optional, Any, Dict, List, Union, Iterator
from urllib3 import HTTPResponse
from datetime import datetime, date

from .base import BaseClient
from .models.futures import (
    FuturesAgg,
    FuturesContract,
    FuturesProduct,
    FuturesQuote,
    FuturesTrade,
    FuturesSchedule,
    FuturesMarketStatus,
    FuturesSnapshot,
    FuturesExchange,
)
from .models.common import Sort
from .models.request import RequestOptionBuilder


class FuturesClient(BaseClient):
    """
    Client for the Futures REST Endpoints
    (aligned with the paths from /futures/vX/...)
    """

    def list_futures_aggregates(
        self,
        ticker: str,
        resolution: Optional[str] = None,
        window_start: Optional[str] = None,
        window_start_lt: Optional[str] = None,
        window_start_lte: Optional[str] = None,
        window_start_gt: Optional[str] = None,
        window_start_gte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FuturesAgg], HTTPResponse]:
        """
        Endpoint: GET /futures/vX/aggs/{ticker}

        Get aggregates for a futures contract in a given time range.
        This endpoint returns data that includes:
        - open, close, high, low
        - volume, dollar_volume, etc.
        If `next_url` is present, it will be paginated.
        """
        url = f"/futures/vX/aggs/{ticker}"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_futures_aggregates, locals()),
            raw=raw,
            deserializer=FuturesAgg.from_dict,
            options=options,
        )

    def list_futures_contracts(
        self,
        date: Optional[str] = None,
        date_gt: Optional[str] = None,
        date_gte: Optional[str] = None,
        date_lt: Optional[str] = None,
        date_lte: Optional[str] = None,
        product_code: Optional[str] = None,
        product_code_any_of: Optional[str] = None,
        product_code_gt: Optional[str] = None,
        product_code_gte: Optional[str] = None,
        product_code_lt: Optional[str] = None,
        product_code_lte: Optional[str] = None,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        active: Optional[bool] = None,
        type: Optional[str] = None,
        type_any_of: Optional[str] = None,
        first_trade_date: Optional[str] = None,
        first_trade_date_gt: Optional[str] = None,
        first_trade_date_gte: Optional[str] = None,
        first_trade_date_lt: Optional[str] = None,
        first_trade_date_lte: Optional[str] = None,
        last_trade_date: Optional[str] = None,
        last_trade_date_gt: Optional[str] = None,
        last_trade_date_gte: Optional[str] = None,
        last_trade_date_lt: Optional[str] = None,
        last_trade_date_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FuturesContract], HTTPResponse]:
        """
        Endpoint: GET /futures/vX/contracts

        The Contracts endpoint returns a paginated list of futures contracts.
        """
        url = "/futures/vX/contracts"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_futures_contracts, locals()),
            raw=raw,
            deserializer=FuturesContract.from_dict,
            options=options,
        )

    def list_futures_products(
        self,
        name: Optional[str] = None,
        name_any_of: Optional[str] = None,
        name_gt: Optional[str] = None,
        name_gte: Optional[str] = None,
        name_lt: Optional[str] = None,
        name_lte: Optional[str] = None,
        product_code: Optional[str] = None,
        product_code_any_of: Optional[str] = None,
        product_code_gt: Optional[str] = None,
        product_code_gte: Optional[str] = None,
        product_code_lt: Optional[str] = None,
        product_code_lte: Optional[str] = None,
        date: Optional[str] = None,
        date_gt: Optional[str] = None,
        date_gte: Optional[str] = None,
        date_lt: Optional[str] = None,
        date_lte: Optional[str] = None,
        trading_venue: Optional[str] = None,
        trading_venue_any_of: Optional[str] = None,
        trading_venue_gt: Optional[str] = None,
        trading_venue_gte: Optional[str] = None,
        trading_venue_lt: Optional[str] = None,
        trading_venue_lte: Optional[str] = None,
        sector: Optional[str] = None,
        sector_any_of: Optional[str] = None,
        sub_sector: Optional[str] = None,
        sub_sector_any_of: Optional[str] = None,
        asset_class: Optional[str] = None,
        asset_class_any_of: Optional[str] = None,
        asset_sub_class: Optional[str] = None,
        asset_sub_class_any_of: Optional[str] = None,
        type: Optional[str] = None,
        type_any_of: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FuturesProduct], HTTPResponse]:
        """
        Endpoint: GET /futures/vX/products

        Returns a list of futures products (including combos).
        """
        url = "/futures/vX/products"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_futures_products, locals()),
            raw=raw,
            deserializer=FuturesProduct.from_dict,
            options=options,
        )

    def list_futures_quotes(
        self,
        ticker: str,
        timestamp: Optional[str] = None,
        timestamp_lt: Optional[str] = None,
        timestamp_lte: Optional[str] = None,
        timestamp_gt: Optional[str] = None,
        timestamp_gte: Optional[str] = None,
        session_end_date: Optional[str] = None,
        session_end_date_lt: Optional[str] = None,
        session_end_date_lte: Optional[str] = None,
        session_end_date_gt: Optional[str] = None,
        session_end_date_gte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FuturesQuote], HTTPResponse]:
        """
        Endpoint: GET /futures/vX/quotes/{ticker}

        Get quotes for a contract in a given time range (paginated).
        """
        url = f"/futures/vX/quotes/{ticker}"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_futures_quotes, locals()),
            raw=raw,
            deserializer=FuturesQuote.from_dict,
            options=options,
        )

    def list_futures_trades(
        self,
        ticker: str,
        timestamp: Optional[str] = None,
        timestamp_lt: Optional[str] = None,
        timestamp_lte: Optional[str] = None,
        timestamp_gt: Optional[str] = None,
        timestamp_gte: Optional[str] = None,
        session_end_date: Optional[str] = None,
        session_end_date_lt: Optional[str] = None,
        session_end_date_lte: Optional[str] = None,
        session_end_date_gt: Optional[str] = None,
        session_end_date_gte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FuturesTrade], HTTPResponse]:
        """
        Endpoint: GET /futures/vX/trades/{ticker}

        Get trades for a contract in a given time range (paginated).
        """
        url = f"/futures/vX/trades/{ticker}"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_futures_trades, locals()),
            raw=raw,
            deserializer=FuturesTrade.from_dict,
            options=options,
        )

    def list_futures_schedules(
        self,
        product_code: Optional[str] = None,
        product_code_any_of: Optional[str] = None,
        product_code_gt: Optional[str] = None,
        product_code_gte: Optional[str] = None,
        product_code_lt: Optional[str] = None,
        product_code_lte: Optional[str] = None,
        session_end_date: Optional[str] = None,
        session_end_date_any_of: Optional[str] = None,
        session_end_date_gt: Optional[str] = None,
        session_end_date_gte: Optional[str] = None,
        session_end_date_lt: Optional[str] = None,
        session_end_date_lte: Optional[str] = None,
        trading_venue: Optional[str] = None,
        trading_venue_any_of: Optional[str] = None,
        trading_venue_gt: Optional[str] = None,
        trading_venue_gte: Optional[str] = None,
        trading_venue_lt: Optional[str] = None,
        trading_venue_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FuturesSchedule], HTTPResponse]:
        """
        Endpoint: GET /futures/vX/schedules

        Returns a list of trading schedules for multiple futures products on a specific date.
        If `next_url` is present, this is paginated.
        """
        url = "/futures/vX/schedules"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_futures_schedules, locals()),
            raw=raw,
            deserializer=FuturesSchedule.from_dict,
            options=options,
        )

    def list_futures_market_statuses(
        self,
        product_code: Optional[str] = None,
        product_code_any_of: Optional[str] = None,
        product_code_gt: Optional[str] = None,
        product_code_gte: Optional[str] = None,
        product_code_lt: Optional[str] = None,
        product_code_lte: Optional[str] = None,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FuturesMarketStatus], HTTPResponse]:
        url = "/futures/vX/market-status"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_futures_market_statuses, locals()),
            raw=raw,
            deserializer=FuturesMarketStatus.from_dict,
            options=options,
        )

    def get_futures_snapshot(
        self,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        product_code: Optional[str] = None,
        product_code_any_of: Optional[str] = None,
        product_code_gt: Optional[str] = None,
        product_code_gte: Optional[str] = None,
        product_code_lt: Optional[str] = None,
        product_code_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FuturesSnapshot], HTTPResponse]:
        url = "/futures/vX/snapshot"
        return self._paginate(
            path=url,
            params=self._get_params(self.get_futures_snapshot, locals()),
            raw=raw,
            deserializer=FuturesSnapshot.from_dict,
            options=options,
        )

    def list_futures_exchanges(
        self,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FuturesExchange], HTTPResponse]:
        """
        Endpoint: GET /futures/vX/exchanges

        US futures exchanges and trading venues including major derivatives exchanges (CME, CBOT, NYMEX, COMEX) and other futures market infrastructure for commodity, financial, and other derivative contract trading.
        """
        url = "/futures/vX/exchanges"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_futures_exchanges, locals()),
            raw=raw,
            deserializer=FuturesExchange.from_dict,
            options=options,
        )
