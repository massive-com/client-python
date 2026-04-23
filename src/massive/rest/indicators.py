from massive.rest.models.common import SeriesType
from massive.rest.models.indicators import (
    SMAIndicatorResults,
    EMAIndicatorResults,
    RSIIndicatorResults,
    MACDIndicatorResults,
)
from .base import BaseClient
from typing import Optional, Any, Dict, List, Union
from .models import Order
from urllib3 import HTTPResponse
from datetime import datetime, date

from .models.request import RequestOptionBuilder


class IndicatorsClient(BaseClient):
    def get_sma(
        self,
        ticker: str,
        timestamp: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lte: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gte: Optional[Union[str, int, datetime, date]] = None,
        timespan: Optional[str] = None,
        window: Optional[int] = None,
        adjusted: Optional[bool] = None,
        expand_underlying: Optional[bool] = None,
        order: Optional[Union[str, Order]] = None,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        series_type: Optional[Union[str, SeriesType]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[SMAIndicatorResults, HTTPResponse]:
        """
        Get SMA values for a given ticker over a given range with the specified parameters

        :param ticker: The ticker symbol
        :param timespan: The size of the underlying aggregate time window
        :param window: The window size used to calculate the simple moving average. i.e. a window size of 10 with daily
             aggregates would result in a 10-day moving average
        :param timestamp: Either a date with the format YYYY-MM-DD or a millisecond timestamp.
        :param timestamp_lt: Timestamp less than
        :param timestamp_lte: Timestamp less than or equal to
        :param timestamp_gt: Timestamp greater than
        :param timestamp_gte: Timestamp greater than or equal to
        :param adjusted: Whether the underlying aggregates are adjusted for splits. By default, the aggregates used to
             calculate this indicator are adjusted. Set this as false to get results that are NOT adjusted for splits
        :param expand_underlying: Whether to include the aggregates used to calculate this indicator in the response
        :param order: Sort the results by timestamp. asc will return results in ascending order (oldest at the top),
         desc will return results in descending order (newest at the top).The end of the aggregate time window
        :param limit: Limit the number of results returned, default is 10 and max is 5000
        :param params: Any additional query params
        :param series_type: The price in the aggregate which will be used to calculate the simple moving average
         i.e. 'close' will result in using close prices to calculate the simple moving average
        :param raw: Return raw object instead of results object
        :return: SingleIndicatorResults
        """

        url = f"/v1/indicators/sma/{ticker}"

        return self._get(
            path=url,
            params=self._get_params(self.get_sma, locals()),
            result_key="results",
            deserializer=SMAIndicatorResults.from_dict,
            raw=raw,
            options=options,
        )

    def get_ema(
        self,
        ticker: str,
        timestamp: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lte: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gte: Optional[Union[str, int, datetime, date]] = None,
        timespan: Optional[str] = None,
        window: Optional[int] = None,
        adjusted: Optional[bool] = None,
        expand_underlying: Optional[bool] = None,
        order: Optional[Union[str, Order]] = None,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        series_type: Optional[Union[str, SeriesType]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[EMAIndicatorResults, HTTPResponse]:
        """
        Get EMA values for a given ticker over a given range with the specified parameters

        :param ticker: The ticker symbol
        :param timespan: The size of the underlying aggregate time window
        :param window: The window size used to calculate the exponential moving average. i.e. a window size of 10 with daily
             aggregates would result in a 10-day moving average
        :param timestamp: Either a date with the format YYYY-MM-DD or a millisecond timestamp.
        :param timestamp_lt: Timestamp less than
        :param timestamp_lte: Timestamp less than or equal to
        :param timestamp_gt: Timestamp greater than
        :param timestamp_gte: Timestamp greater than or equal to
        :param adjusted: Whether the underlying aggregates are adjusted for splits. By default, the aggregates used to
             calculate this indicator are adjusted. Set this as false to get results that are NOT adjusted for splits
        :param expand_underlying: Whether to include the aggregates used to calculate this indicator in the response
        :param order: Sort the results by timestamp. asc will return results in ascending order (oldest at the top),
         desc will return results in descending order (newest at the top).The end of the aggregate time window
        :param limit: Limit the number of results returned, default is 10 and max is 5000
        :param params: Any additional query params
        :param series_type: The price in the aggregate which will be used to calculate the simple moving average
         i.e. 'close' will result in using close prices to calculate the simple moving average
        :param raw: Return raw object instead of results object
        :return: SingleIndicatorResults
        """

        url = f"/v1/indicators/ema/{ticker}"

        return self._get(
            path=url,
            params=self._get_params(self.get_ema, locals()),
            result_key="results",
            deserializer=EMAIndicatorResults.from_dict,
            raw=raw,
            options=options,
        )

    def get_rsi(
        self,
        ticker: str,
        timestamp: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lte: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gte: Optional[Union[str, int, datetime, date]] = None,
        timespan: Optional[str] = None,
        window: Optional[int] = None,
        adjusted: Optional[bool] = None,
        expand_underlying: Optional[bool] = None,
        order: Optional[Union[str, Order]] = None,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        series_type: Optional[Union[str, SeriesType]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[RSIIndicatorResults, HTTPResponse]:
        """
        Get RSI values for a given ticker over a given range with the specified parameters

        :param ticker: The ticker symbol
        :param timespan: The size of the underlying aggregate time window
        :param window: The window size used to calculate the simple moving average. i.e. a window size of 10 with daily
             aggregates would result in a 10-day moving average
        :param timestamp: Either a date with the format YYYY-MM-DD or a millisecond timestamp.
        :param timestamp_lt: Timestamp less than
        :param timestamp_lte: Timestamp less than or equal to
        :param timestamp_gt: Timestamp greater than
        :param timestamp_gte: Timestamp greater than or equal to
        :param adjusted: Whether the underlying aggregates are adjusted for splits. By default, the aggregates used to
             calculate this indicator are adjusted. Set this as false to get results that are NOT adjusted for splits
        :param expand_underlying: Whether to include the aggregates used to calculate this indicator in the response
        :param order: Sort the results by timestamp. asc will return results in ascending order (oldest at the top),
         desc will return results in descending order (newest at the top).The end of the aggregate time window
        :param limit: Limit the number of results returned, default is 10 and max is 5000
        :param params: Any additional query params
        :param series_type: The price in the aggregate which will be used to calculate the simple moving average
         i.e. 'close' will result in using close prices to calculate the simple moving average
        :param raw: Return raw object instead of results object
        :return: SingleIndicatorResults
        """

        url = f"/v1/indicators/rsi/{ticker}"

        return self._get(
            path=url,
            params=self._get_params(self.get_rsi, locals()),
            result_key="results",
            deserializer=RSIIndicatorResults.from_dict,
            raw=raw,
            options=options,
        )

    def get_macd(
        self,
        ticker: str,
        timestamp: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_lte: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gt: Optional[Union[str, int, datetime, date]] = None,
        timestamp_gte: Optional[Union[str, int, datetime, date]] = None,
        timespan: Optional[str] = None,
        short_window: Optional[int] = None,
        long_window: Optional[int] = None,
        signal_window: Optional[int] = None,
        adjusted: Optional[bool] = None,
        expand_underlying: Optional[bool] = None,
        order: Optional[Union[str, Order]] = None,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        series_type: Optional[Union[str, SeriesType]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[MACDIndicatorResults, HTTPResponse]:
        """
        Get MACD values for a given ticker over a given range with the specified parameters

        :param ticker: The ticker symbol
        :param timespan: The size of the underlying aggregate time window
        :param short_window: The short window size used to calculate the MACD data
        :param long_window: The long window size used to calculate the MACD data
        :param signal_window: The window size used to calculate the MACD signal line
        :param timestamp: Either a date with the format YYYY-MM-DD or a millisecond timestamp.
        :param timestamp_lt: Timestamp less than
        :param timestamp_lte: Timestamp less than or equal to
        :param timestamp_gt: Timestamp greater than
        :param timestamp_gte: Timestamp greater than or equal to
        :param adjusted: Whether the underlying aggregates are adjusted for splits. By default, the aggregates used to
             calculate this indicator are adjusted. Set this as false to get results that are NOT adjusted for splits
        :param expand_underlying: Whether to include the aggregates used to calculate this indicator in the response
        :param order: Sort the results by timestamp. asc will return results in ascending order (oldest at the top),
         desc will return results in descending order (newest at the top).The end of the aggregate time window
        :param limit: Limit the number of results returned, default is 10 and max is 5000
        :param params: Any additional query params
        :param series_type: The price in the aggregate which will be used to calculate the simple moving average
         i.e. 'close' will result in using close prices to calculate the simple moving average
        :param raw: Return raw object instead of results object
        :return: MACDIndicatorResults
        """

        url = f"/v1/indicators/macd/{ticker}"

        return self._get(
            path=url,
            params=self._get_params(self.get_macd, locals()),
            result_key="results",
            deserializer=MACDIndicatorResults.from_dict,
            raw=raw,
            options=options,
        )
