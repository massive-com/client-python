from .base import BaseClient
from typing import Optional, Any, Dict, Union, Iterator
from .models import Trade, LastTrade, CryptoTrade, Sort, Order
from urllib3 import HTTPResponse
from datetime import datetime, date

from .models.request import RequestOptionBuilder


class TradesClient(BaseClient):
    def list_trades(
        self,
        ticker: str,
        timestamp: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lte: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gte: Optional[Union[str, int, datetime, date]] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[Trade], HTTPResponse]:
        """
        Get trades for a ticker symbol in a given time range.

        :param ticker: The ticker symbol.
        :param timestamp: Either a date with the format YYYY-MM-DD or a nanosecond timestamp.
        :param timestamp_lt: Timestamp less than
        :param timestamp_lte: Timestamp less than or equal to
        :param timestamp_gt: Timestamp greater than
        :param timestamp_gte: Timestamp greater than or equal to
        :param limit: Limits the number of base aggregates queried per-page to create the aggregate results. Max 50000 and Default 5000. Read more about how limit is used to calculate aggregate results in our article on Aggregate Data API Improvements.
        :param sort: Sort the results by timestamp. asc will return results in ascending order (oldest at the top), desc will return results in descending order (newest at the top).The end of the aggregate time window.
        :param order: Order results based on the sort field
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Iterator of trades
        """
        url = f"/v3/trades/{ticker}"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_trades, locals()),
            raw=raw,
            deserializer=Trade.from_dict,
            options=options,
        )

    def get_last_trade(
        self,
        ticker: str,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[LastTrade, HTTPResponse]:
        """
        Get the most recent trade for a ticker.

        :param ticker: The ticker symbol of the asset
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Last trade
        """
        url = f"/v2/last/trade/{ticker}"

        return self._get(
            path=url,
            params=self._get_params(self.get_last_trade, locals()),
            result_key="results",
            deserializer=LastTrade.from_dict,
            raw=raw,
            options=options,
        )

    def get_last_crypto_trade(
        self,
        from_: str,
        to: str,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[CryptoTrade, HTTPResponse]:
        """
        Get the last trade tick for a cryptocurrency pair.

        :param from_: The "from" symbol of the pair.
        :param to: The "to" symbol of the pair.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Last crypto trade
        """
        url = f"/v1/last/crypto/{from_}/{to}"

        return self._get(
            path=url,
            params=self._get_params(self.get_last_crypto_trade, locals()),
            result_key="last",
            deserializer=CryptoTrade.from_dict,
            raw=raw,
            options=options,
        )
