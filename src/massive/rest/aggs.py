from .base import BaseClient
from typing import Optional, Any, Dict, List, Union, Iterator
from .models import Agg, GroupedDailyAgg, DailyOpenCloseAgg, PreviousCloseAgg, Sort
from urllib3 import HTTPResponse
from datetime import datetime, date

from .models.request import RequestOptionBuilder


class AggsClient(BaseClient):
    def list_aggs(
        self,
        ticker: str,
        multiplier: int,
        timespan: str,
        # "from" is a keyword in python https://www.w3schools.com/python/python_ref_keywords.asp
        from_: Union[str, int, datetime, date],
        to: Union[str, int, datetime, date],
        adjusted: Optional[bool] = None,
        sort: Optional[Union[str, Sort]] = None,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[Agg], HTTPResponse]:
        """
        List aggregate bars for a ticker over a given date range in custom time window sizes.

        :param ticker: The ticker symbol.
        :param multiplier: The size of the timespan multiplier.
        :param timespan: The size of the time window.
        :param from_: The start of the aggregate time window as YYYY-MM-DD, a date, Unix MS Timestamp, or a datetime.
        :param to: The end of the aggregate time window as YYYY-MM-DD, a date, Unix MS Timestamp, or a datetime.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. asc will return results in ascending order (oldest at the top), desc will return results in descending order (newest at the top).The end of the aggregate time window.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and Default 5000. Read more about how limit is used to calculate aggregate results in our article on Aggregate Data API Improvements.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Iterator of aggregates
        """
        if isinstance(from_, datetime):
            from_ = int(from_.timestamp() * self.time_mult("millis"))

        if isinstance(to, datetime):
            to = int(to.timestamp() * self.time_mult("millis"))
        url = f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_}/{to}"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_aggs, locals()),
            raw=raw,
            deserializer=Agg.from_dict,
            options=options,
        )

    def get_aggs(
        self,
        ticker: str,
        multiplier: int,
        timespan: str,
        # "from" is a keyword in python https://www.w3schools.com/python/python_ref_keywords.asp
        from_: Union[str, int, datetime, date],
        to: Union[str, int, datetime, date],
        adjusted: Optional[bool] = None,
        sort: Optional[Union[str, Sort]] = None,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[Agg], HTTPResponse]:
        """
        Get aggregate bars for a ticker over a given date range in custom time window sizes.

        :param ticker: The ticker symbol.
        :param multiplier: The size of the timespan multiplier.
        :param timespan: The size of the time window.
        :param from_: The start of the aggregate time window as YYYY-MM-DD, a date, Unix MS Timestamp, or a datetime.
        :param to: The end of the aggregate time window as YYYY-MM-DD, a date, Unix MS Timestamp, or a datetime.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.
        :param sort: Sort the results by timestamp. asc will return results in ascending order (oldest at the top), desc will return results in descending order (newest at the top).The end of the aggregate time window.
        :param limit: Limits the number of base aggregates queried to create the aggregate results. Max 50000 and Default 5000. Read more about how limit is used to calculate aggregate results in our article on Aggregate Data API Improvements.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: List of aggregates
        """
        if isinstance(from_, datetime):
            from_ = int(from_.timestamp() * self.time_mult("millis"))

        if isinstance(to, datetime):
            to = int(to.timestamp() * self.time_mult("millis"))
        url = f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_}/{to}"

        return self._get(
            path=url,
            params=self._get_params(self.get_aggs, locals()),
            result_key="results",
            deserializer=Agg.from_dict,
            raw=raw,
            options=options,
        )

    # TODO: next breaking change release move "market_type" to be 2nd mandatory
    # param
    def get_grouped_daily_aggs(
        self,
        date: Union[str, date],
        adjusted: Optional[bool] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        locale: str = "us",
        market_type: str = "stocks",
        include_otc: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[GroupedDailyAgg], HTTPResponse]:
        """
        Get the daily open, high, low, and close (OHLC) for the entire market.

        :param date: The beginning date for the aggregate window.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: List of grouped daily aggregates
        """
        url = f"/v2/aggs/grouped/locale/{locale}/market/{market_type}/{date}"

        return self._get(
            path=url,
            params=self._get_params(self.get_grouped_daily_aggs, locals()),
            result_key="results",
            deserializer=GroupedDailyAgg.from_dict,
            raw=raw,
            options=options,
        )

    def get_daily_open_close_agg(
        self,
        ticker: str,
        date: Union[str, date],
        adjusted: Optional[bool] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[DailyOpenCloseAgg, HTTPResponse]:
        """
        Get the open, close and afterhours prices of a stock symbol on a certain date.

        :param ticker: The exchange symbol that this item is traded under.
        :param date: The beginning date for the aggregate window.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Daily open close aggregate
        """
        url = f"/v1/open-close/{ticker}/{date}"

        return self._get(
            path=url,
            params=self._get_params(self.get_daily_open_close_agg, locals()),
            deserializer=DailyOpenCloseAgg.from_dict,
            raw=raw,
            options=options,
        )

    def get_previous_close_agg(
        self,
        ticker: str,
        adjusted: Optional[bool] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[PreviousCloseAgg, HTTPResponse]:
        """
        Get the previous day's open, high, low, and close (OHLC) for the specified stock ticker.

        :param ticker: The ticker symbol of the stock/equity.
        :param adjusted: Whether or not the results are adjusted for splits. By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Previous close aggregate
        """
        url = f"/v2/aggs/ticker/{ticker}/prev"

        return self._get(
            path=url,
            params=self._get_params(self.get_previous_close_agg, locals()),
            result_key="results",
            deserializer=PreviousCloseAgg.from_dict,
            raw=raw,
            options=options,
        )
