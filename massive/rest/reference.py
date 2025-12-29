from .base import BaseClient
from typing import Optional, Any, Dict, List, Union, Iterator
from .models import (
    MarketHoliday,
    MarketStatus,
    Ticker,
    TickerChangeResults,
    TickerDetails,
    TickerNews,
    RelatedCompany,
    TickerTypes,
    Sort,
    Order,
    AssetClass,
    Locale,
    Split,
    StockSplit,
    Dividend,
    StockDividend,
    DividendType,
    Frequency,
    Condition,
    DataType,
    SIP,
    Exchange,
    OptionsContract,
    ShortInterest,
    ShortVolume,
    RiskFactor,
    RiskFactorTaxonomy,
)
from urllib3 import HTTPResponse
from datetime import date

from .models.request import RequestOptionBuilder


class MarketsClient(BaseClient):
    def get_market_holidays(
        self, params: Optional[Dict[str, Any]] = None, raw: bool = False
    ) -> Union[List[MarketHoliday], HTTPResponse]:
        """
        Get upcoming market holidays and their open/close times.

        :param params: Any additional query params.
        :param raw: Return HTTPResponse object instead of results object.
        :return: List of market holidays.
        """
        url = "/v1/marketstatus/upcoming"

        return self._get(
            path=url,
            params=params,
            deserializer=MarketHoliday.from_dict,
            raw=raw,
            result_key="",
        )

    def get_market_status(
        self, params: Optional[Dict[str, Any]] = None, raw: bool = False
    ) -> Union[MarketStatus, HTTPResponse]:
        """
        Get the current trading status of the exchanges and overall financial markets.

        :param params: Any additional query params.
        :param raw: Return HTTPResponse object instead of results object.
        :return: Market status.
        """
        url = "/v1/marketstatus/now"

        return self._get(
            path=url, params=params, deserializer=MarketStatus.from_dict, raw=raw
        )


class TickersClient(BaseClient):
    def list_tickers(
        self,
        ticker: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        type: Optional[str] = None,
        market: Optional[str] = None,
        exchange: Optional[str] = None,
        cusip: Optional[int] = None,
        cik: Optional[int] = None,
        date: Optional[str] = None,
        active: Optional[bool] = None,
        search: Optional[str] = None,
        limit: Optional[int] = 10,
        sort: Optional[Union[str, Sort]] = "ticker",
        order: Optional[Union[str, Order]] = "asc",
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[Ticker], HTTPResponse]:
        """
        Query all ticker symbols which are supported by Massive.com. This API currently includes Stocks/Equities, Indices, Forex, and Crypto.

        :param ticker: Specify a ticker symbol. Defaults to empty string which queries all tickers.
        :param ticker_lt: Ticker less than.
        :param ticker_lte: Ticker less than or equal to.
        :param ticker_gt: Ticker greater than.
        :param ticker_gte: Ticker greater than or equal to.
        :param type: Specify the type of the tickers. Find the types that we support via our Ticker Types API. Defaults to empty string which queries all types.
        :param market: Filter by market type. By default all markets are included.
        :param exchange: Specify the assets primary exchange Market Identifier Code (MIC) according to ISO 10383. Defaults to empty string which queries all exchanges.
        :param cusip: Specify the CUSIP code of the asset you want to search for. Find more information about CUSIP codes at their website. Defaults to empty string which queries all CUSIPs.
        :param cik: Specify the CIK of the asset you want to search for. Find more information about CIK codes at their website. Defaults to empty string which queries all CIKs.
        :param date: Specify a point in time to retrieve tickers available on that date. Defaults to the most recent available date.
        :param search: Search for terms within the ticker and/or company name.
        :param active: Specify if the tickers returned should be actively traded on the queried date. Default is true.
        :param limit: Limit the size of the response per-page, default is 100 and max is 1000.
        :param sort: The field to sort the results on. Default is ticker. If the search query parameter is present, sort is ignored and results are ordered by relevance.
        :param order: The order to sort the results on. Default is asc (ascending).
        :param params: Any additional query params.
        :param raw: Return raw object instead of results object.
        :return: List of tickers.
        """
        url = "/v3/reference/tickers"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_tickers, locals()),
            raw=raw,
            deserializer=Ticker.from_dict,
            options=options,
        )

    def get_ticker_details(
        self,
        ticker: Optional[str] = None,
        date: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[TickerDetails, HTTPResponse]:
        """
        Get a single ticker supported by Massive.com. This response will have detailed information about the ticker and the company behind it.

        :param ticker: The ticker symbol of the asset.
        :param date: Specify a point in time to get information about the ticker available on that date. When retrieving information from SEC filings, we compare this date with the period of report date on the SEC filing.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Ticker Details V3
        """
        url = f"/v3/reference/tickers/{ticker}"

        return self._get(
            path=url,
            params=self._get_params(self.get_ticker_details, locals()),
            deserializer=TickerDetails.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )

    def get_ticker_events(
        self,
        ticker: str,
        types: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[TickerChangeResults, HTTPResponse]:
        """
        Get event history of ticker given particular point in time.
        :param ticker: The ticker symbol of the asset.
        :param params: Additional query parameters
        :param raw: Return raw object instead of results object.
        :return: Ticker Event VX
        """
        url = f"/vX/reference/tickers/{ticker}/events"

        return self._get(
            path=url,
            params=self._get_params(self.get_ticker_events, locals()),
            deserializer=TickerChangeResults.from_dict,
            result_key="results",
            raw=raw,
            options=options,
        )

    def list_ticker_news(
        self,
        ticker: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        published_utc: Optional[str] = None,
        published_utc_lt: Optional[str] = None,
        published_utc_lte: Optional[str] = None,
        published_utc_gt: Optional[str] = None,
        published_utc_gte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[TickerNews], HTTPResponse]:
        """
        Get the most recent news articles relating to a stock ticker symbol, including a summary of the article and a link to the original source.

        :param ticker: Return results that contain this ticker.
        :param published_utc: Return results published on, before, or after this date.
        :param limit: Limit the number of results returned per-page, default is 10 and max is 1000.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params.
        :param raw: Return raw object instead of results object.
        :return: Ticker News.
        """
        url = "/v2/reference/news"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_ticker_news, locals()),
            raw=raw,
            deserializer=TickerNews.from_dict,
            options=options,
        )

    def get_ticker_types(
        self,
        asset_class: Optional[Union[str, AssetClass]] = None,
        locale: Optional[Union[str, Locale]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[TickerTypes], HTTPResponse]:
        """
        List all ticker types that Massive.com has.

        :param asset_class: Filter by asset class.
        :param locale: Filter by locale.
        :param params: Any additional query params.
        :param raw: Return raw object instead of results object.
        :return: Ticker Types.
        """
        url = "/v3/reference/tickers/types"

        return self._get(
            path=url,
            params=self._get_params(self.get_ticker_types, locals()),
            deserializer=TickerTypes.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )

    def get_related_companies(
        self,
        ticker: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[RelatedCompany, HTTPResponse]:
        """
        Get a list of tickers related to the queried ticker based on News and Returns data.

        :param ticker: The ticker symbol to search.
        :param params: Any additional query params.
        :param raw: Return raw object instead of results object.
        :return: Related Companies.
        """
        url = f"/v1/related-companies/{ticker}"

        return self._get(
            path=url,
            params=self._get_params(self.get_related_companies, locals()),
            deserializer=RelatedCompany.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )


class SplitsClient(BaseClient):
    def list_splits(
        self,
        ticker: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        execution_date: Optional[Union[str, date]] = None,
        execution_date_lt: Optional[Union[str, date]] = None,
        execution_date_lte: Optional[Union[str, date]] = None,
        execution_date_gt: Optional[Union[str, date]] = None,
        execution_date_gte: Optional[Union[str, date]] = None,
        reverse_split: Optional[bool] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[Split], HTTPResponse]:
        """
        Get a list of historical stock splits, including the ticker symbol, the execution date, and the factors of the split ratio.

        :param ticker: Return the stock splits that contain this ticker.
        :param ticker_lt: Ticker less than.
        :param ticker_lte: Ticker less than or equal to.
        :param ticker_gt: Ticker greater than.
        :param ticker_gte: Ticker greater than or equal to.
        :param execution_date: Query by execution date with the format YYYY-MM-DD.
        :param execution_date_lt: Execution date less than.
        :param execution_date_lte: Execution date less than or equal to.
        :param execution_date_gt: Execution date greater than.
        :param execution_date_gte: Execution date greater than or equal to.
        :param reverse_split: Query for reverse stock splits. A split ratio where split_from is greater than split_to represents a reverse split. By default this filter is not used.
        :param limit: Limit the number of results returned per-page, default is 10 and max is 1000.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params.
        :param raw: Return raw object instead of results object.
        :return: List of splits.
        """
        url = "/v3/reference/splits"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_splits, locals()),
            raw=raw,
            deserializer=Split.from_dict,
            options=options,
        )


class DividendsClient(BaseClient):
    def list_dividends(
        self,
        ticker: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ex_dividend_date: Optional[Union[str, date]] = None,
        ex_dividend_date_lt: Optional[Union[str, date]] = None,
        ex_dividend_date_lte: Optional[Union[str, date]] = None,
        ex_dividend_date_gt: Optional[Union[str, date]] = None,
        ex_dividend_date_gte: Optional[Union[str, date]] = None,
        record_date: Optional[Union[str, date]] = None,
        record_date_lt: Optional[Union[str, date]] = None,
        record_date_lte: Optional[Union[str, date]] = None,
        record_date_gt: Optional[Union[str, date]] = None,
        record_date_gte: Optional[Union[str, date]] = None,
        declaration_date: Optional[Union[str, date]] = None,
        declaration_date_lt: Optional[Union[str, date]] = None,
        declaration_date_lte: Optional[Union[str, date]] = None,
        declaration_date_gt: Optional[Union[str, date]] = None,
        declaration_date_gte: Optional[Union[str, date]] = None,
        pay_date: Optional[Union[str, date]] = None,
        pay_date_lt: Optional[Union[str, date]] = None,
        pay_date_lte: Optional[Union[str, date]] = None,
        pay_date_gt: Optional[Union[str, date]] = None,
        pay_date_gte: Optional[Union[str, date]] = None,
        frequency: Optional[Union[int, Frequency]] = None,
        cash_amount: Optional[float] = None,
        cash_amount_lt: Optional[float] = None,
        cash_amount_lte: Optional[float] = None,
        cash_amount_gt: Optional[float] = None,
        cash_amount_gte: Optional[float] = None,
        dividend_type: Optional[Union[str, DividendType]] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[Dividend], HTTPResponse]:
        """
        Get a list of historical cash dividends, including the ticker symbol, declaration date, ex-dividend date, record date, pay date, frequency, and amount.

        :param ticker: Return the dividends that contain this ticker.
        :param ticker_lt: Ticker less than.
        :param ticker_lte: Ticker less than or equal to.
        :param ticker_gt: Ticker greater than.
        :param ticker_gte: Ticker greater than or equal to.
        :param ex_dividend_date: Query by ex-dividend date with the format YYYY-MM-DD.
        :param ex_dividend_date_lt: Ex-dividend date less than.
        :param ex_dividend_date_lte: Ex-dividend date less than or equal to.
        :param ex_dividend_date_gt: Ex-dividend date greater than.
        :param ex_dividend_date_gte: Ex-dividend date greater than or equal to.
        :param record_date: Query by record date with the format YYYY-MM-DD.
        :param record_date_lt: Record date less than.
        :param record_date_lte: Record date less than or equal to.
        :param record_date_gt: Record date greater than.
        :param record_date_gte: Record date greater than or equal to.
        :param declaration_date: Query by declaration date with the format YYYY-MM-DD.
        :param declaration_date_lt: Declaration date less than.
        :param declaration_date_lte: Declaration date less than or equal to.
        :param declaration_date_gt: Declaration date greater than.
        :param declaration_date_gte: Declaration date greater than or equal to.
        :param pay_date: Query by pay date with the format YYYY-MM-DD.
        :param pay_date_lt: Pay date less than.
        :param pay_date_lte: Pay date less than or equal to.
        :param pay_date_gt: Pay date greater than.
        :param pay_date_gte: Pay date greater than or equal to.
        :param frequency: Query by the number of times per year the dividend is paid out. Possible values are 0 (one-time), 1 (annually), 2 (bi-annually), 4 (quarterly), and 12 (monthly).
        :param cash_amount: Query by the cash amount of the dividend.
        :param dividend_type: Query by the type of dividend. Dividends that have been paid and/or are expected to be paid on consistent schedules are denoted as CD. Special Cash dividends that have been paid that are infrequent or unusual, and/or can not be expected to occur in the future are denoted as SC.
        :param limit: Limit the number of results returned per-page, default is 10 and max is 1000.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params.
        :param raw: Return raw object instead of results object.
        :return: List of dividends.
        """
        url = "/v3/reference/dividends"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_dividends, locals()),
            raw=raw,
            deserializer=Dividend.from_dict,
            options=options,
        )


class ConditionsClient(BaseClient):
    def list_conditions(
        self,
        asset_class: Optional[Union[str, AssetClass]] = None,
        data_type: Optional[Union[str, DataType]] = None,
        id: Optional[int] = None,
        sip: Optional[Union[str, SIP]] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[Condition], HTTPResponse]:
        """
        List all conditions that Massive.com uses.

        :param asset_class: Filter for conditions within a given asset class.
        :param data_type: Data types that this condition applies to.
        :param id: Filter for conditions with a given ID.
        :param sip: Filter by SIP. If the condition contains a mapping for that SIP, the condition will be returned.
        :param limit: Limit the number of results returned per-page, default is 10 and max is 1000.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params.
        :param raw: Return raw object instead of results object.
        :return: List of conditions.
        """
        url = "/v3/reference/conditions"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_conditions, locals()),
            raw=raw,
            deserializer=Condition.from_dict,
            options=options,
        )


class ExchangesClient(BaseClient):
    def get_exchanges(
        self,
        asset_class: Optional[Union[str, AssetClass]] = None,
        locale: Optional[Union[str, Locale]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[Exchange], HTTPResponse]:
        """
        List all exchanges that Massive.com knows about.

        :param asset_class: Filter by asset class.
        :param locale: Filter by locale.
        :param params: Any additional query params.
        :param raw: Return HTTPResponse object instead of results object.
        :return: List of exchanges.
        """
        url = "/v3/reference/exchanges"

        return self._get(
            path=url,
            params=self._get_params(self.get_exchanges, locals()),
            deserializer=Exchange.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )


class ContractsClient(BaseClient):
    def get_options_contract(
        self,
        ticker: str,
        as_of: Optional[Union[str, date]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[OptionsContract, HTTPResponse]:
        """
        Get the most recent trade for a ticker.

        :param ticker: The ticker symbol of the asset
        :param as_of: Specify a point in time for the contract as of this date with format YYYY-MM-DD.
        :param params: Any additional query params.
        :param raw: Return raw object instead of results object.
        :return: Last trade.
        """
        url = f"/v3/reference/options/contracts/{ticker}"

        return self._get(
            path=url,
            params=self._get_params(self.get_options_contract, locals()),
            result_key="results",
            deserializer=OptionsContract.from_dict,
            raw=raw,
            options=options,
        )

    def list_options_contracts(
        self,
        underlying_ticker: Optional[str] = None,
        underlying_ticker_lt: Optional[str] = None,
        underlying_ticker_lte: Optional[str] = None,
        underlying_ticker_gt: Optional[str] = None,
        underlying_ticker_gte: Optional[str] = None,
        contract_type: Optional[str] = None,
        expiration_date: Optional[Union[str, date]] = None,
        expiration_date_lt: Optional[Union[str, date]] = None,
        expiration_date_lte: Optional[Union[str, date]] = None,
        expiration_date_gt: Optional[Union[str, date]] = None,
        expiration_date_gte: Optional[Union[str, date]] = None,
        as_of: Optional[Union[str, date]] = None,
        strike_price: Optional[float] = None,
        strike_price_lt: Optional[float] = None,
        strike_price_lte: Optional[float] = None,
        strike_price_gt: Optional[float] = None,
        strike_price_gte: Optional[float] = None,
        expired: Optional[bool] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[OptionsContract], HTTPResponse]:
        """
        List historical options contracts.

        :param underlying_ticker: Query for contracts relating to an underlying stock ticker.
        :param contract_type: Query by the type of contract.
        :param expiration_date: Query by contract expiration with date format YYYY-MM-DD.
        :param as_of: Specify a point in time for contracts as of this date with format YYYY-MM-DD.
        :param strike_price: Query by strike price of a contract.
        :param expired: Query for expired contracts.
        :param limit: Limit the number of results returned per-page, default is 10 and max is 1000.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params.
        :param raw: Return raw object instead of results object
        :return: List of options contracts.
        """
        url = "/v3/reference/options/contracts"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_options_contracts, locals()),
            raw=raw,
            deserializer=OptionsContract.from_dict,
            options=options,
        )

    def list_short_interest(
        self,
        ticker: Optional[str] = None,
        days_to_cover: Optional[str] = None,
        days_to_cover_lt: Optional[str] = None,
        days_to_cover_lte: Optional[str] = None,
        days_to_cover_gt: Optional[str] = None,
        days_to_cover_gte: Optional[str] = None,
        settlement_date: Optional[str] = None,
        settlement_date_lt: Optional[str] = None,
        settlement_date_lte: Optional[str] = None,
        settlement_date_gt: Optional[str] = None,
        settlement_date_gte: Optional[str] = None,
        avg_daily_volume: Optional[str] = None,
        avg_daily_volume_lt: Optional[str] = None,
        avg_daily_volume_lte: Optional[str] = None,
        avg_daily_volume_gt: Optional[str] = None,
        avg_daily_volume_gte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[ShortInterest], HTTPResponse]:
        """
        Retrieve short interest data for stocks.

        :param ticker: Filter by the primary ticker symbol.
        :param days_to_cover: Filter by the days to cover value.
        :param days_to_cover_lt: Filter for days to cover dates less than the provided date.
        :param days_to_cover_lte: Filter for days to cover dates less than or equal to the provided date.
        :param days_to_cover_gt: Filter for days to cover dates greater than the provided date.
        :param days_to_cover_gte: Filter for days to cover dates greater than or equal to the provided date.
        :param settlement_date: Filter by settlement date (YYYY-MM-DD).
        :param settlement_date_lt: Filter for settlement dates less than the provided date.
        :param settlement_date_lte: Filter for settlement dates less than or equal to the provided date.
        :param settlement_date_gt: Filter for settlement dates greater than the provided date.
        :param settlement_date_gte: Filter for settlement dates greater than or equal to the provided date.
        :param avg_daily_volume: Filter by average daily volume.
        :param avg_daily_volume_lt: Filter for average daily volume dates less than the provided date.
        :param avg_daily_volume_lte: Filter for average daily volume dates less than or equal to the provided date.
        :param avg_daily_volume_gt: Filter for average daily volume dates greater than the provided date.
        :param avg_daily_volume_gte: Filter for average daily volume dates greater than or equal to the provided date.
        :param limit: Limit the number of results returned. Default 10, max 50000.
        :param sort: Field to sort by (e.g., "ticker").
        :param order: Order results based on the sort field ("asc" or "desc"). Default "desc".
        :param params: Additional query parameters.
        :param raw: Return raw HTTPResponse object if True, else return List[ShortInterest].
        :param options: RequestOptionBuilder for additional headers or params.
        :return: A list of ShortInterest objects or HTTPResponse if raw=True.
        """
        url = "/stocks/v1/short-interest"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_short_interest, locals()),
            deserializer=ShortInterest.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )

    def list_short_volume(
        self,
        ticker: Optional[str] = None,
        date: Optional[str] = None,
        date_lt: Optional[str] = None,
        date_lte: Optional[str] = None,
        date_gt: Optional[str] = None,
        date_gte: Optional[str] = None,
        short_volume_ratio: Optional[str] = None,
        short_volume_ratio_lt: Optional[str] = None,
        short_volume_ratio_lte: Optional[str] = None,
        short_volume_ratio_gt: Optional[str] = None,
        short_volume_ratio_gte: Optional[str] = None,
        total_volume: Optional[str] = None,
        total_volume_lt: Optional[str] = None,
        total_volume_lte: Optional[str] = None,
        total_volume_gt: Optional[str] = None,
        total_volume_gte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[ShortVolume], HTTPResponse]:
        """
        Retrieve short volume data for stocks.

        :param ticker: Filter by the primary ticker symbol.
        :param date: Filter by the date of trade activity (YYYY-MM-DD).
        :param date_lt: Filter for dates less than the provided date.
        :param date_lte: Filter for dates less than or equal to the provided date.
        :param date_gt: Filter for dates greater than the provided date.
        :param date_gte: Filter for dates greater than or equal to the provided date.
        :param short_volume_ratio: Filter by short volume ratio.
        :param short_volume_ratio_lt: Filter for short volume ratio less than the provided date.
        :param short_volume_ratio_lte: Filter for short volume ratio less than or equal to the provided date.
        :param short_volume_ratio_gt: Filter for short volume ratio greater than the provided date.
        :param short_volume_ratio_gte: Filter for short volume ratio greater than or equal to the provided date.
        :param total_volume: Filter by total volume.
        :param total_volume_lt: Filter for total volume less than the provided date.
        :param total_volume_lte: Filter for total volume less than or equal to the provided date.
        :param total_volume_gt: Filter for total volume greater than the provided date.
        :param total_volume_gte: Filter for total volume greater than or equal to the provided date.
        :param limit: Limit the number of results returned. Default 10, max 50000.
        :param sort: Field to sort by (e.g., "ticker").
        :param order: Order results based on the sort field ("asc" or "desc"). Default "desc".
        :param params: Additional query parameters.
        :param raw: Return raw HTTPResponse object if True, else return List[ShortVolume].
        :param options: RequestOptionBuilder for additional headers or params.
        :return: A list of ShortVolume objects or HTTPResponse if raw=True.
        """
        url = "/stocks/v1/short-volume"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_short_volume, locals()),
            deserializer=ShortVolume.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )

    # Add these functions to financials.py in the FinancialsClient class

    def list_stocks_splits(
        self,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        execution_date: Optional[Union[str, date]] = None,
        execution_date_gt: Optional[Union[str, date]] = None,
        execution_date_gte: Optional[Union[str, date]] = None,
        execution_date_lt: Optional[Union[str, date]] = None,
        execution_date_lte: Optional[Union[str, date]] = None,
        adjustment_type: Optional[str] = None,
        adjustment_type_any_of: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[StockSplit], HTTPResponse]:
        """
        Endpoint: GET /stocks/v1/splits
        """
        url = "/stocks/v1/splits"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_stocks_splits, locals()),
            raw=raw,
            deserializer=StockSplit.from_dict,
            options=options,
        )

    def list_stocks_dividends(
        self,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        ex_dividend_date: Optional[Union[str, date]] = None,
        ex_dividend_date_gt: Optional[Union[str, date]] = None,
        ex_dividend_date_gte: Optional[Union[str, date]] = None,
        ex_dividend_date_lt: Optional[Union[str, date]] = None,
        ex_dividend_date_lte: Optional[Union[str, date]] = None,
        frequency: Optional[int] = None,
        frequency_gt: Optional[int] = None,
        frequency_gte: Optional[int] = None,
        frequency_lt: Optional[int] = None,
        frequency_lte: Optional[int] = None,
        distribution_type: Optional[str] = None,
        distribution_type_any_of: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[StockDividend], HTTPResponse]:
        """
        Endpoint: GET /stocks/v1/dividends
        """
        url = "/stocks/v1/dividends"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_stocks_dividends, locals()),
            raw=raw,
            deserializer=StockDividend.from_dict,
            options=options,
        )

    def list_stocks_filings_risk_factors(
        self,
        filing_date: Optional[Union[str, date]] = None,
        filing_date_any_of: Optional[str] = None,
        filing_date_gt: Optional[Union[str, date]] = None,
        filing_date_gte: Optional[Union[str, date]] = None,
        filing_date_lt: Optional[Union[str, date]] = None,
        filing_date_lte: Optional[Union[str, date]] = None,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        cik: Optional[str] = None,
        cik_any_of: Optional[str] = None,
        cik_gt: Optional[str] = None,
        cik_gte: Optional[str] = None,
        cik_lt: Optional[str] = None,
        cik_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[RiskFactor], HTTPResponse]:
        """
        Endpoint: GET /stocks/filings/vX/risk-factors
        """
        url = "/stocks/filings/vX/risk-factors"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_stocks_filings_risk_factors, locals()),
            raw=raw,
            deserializer=RiskFactor.from_dict,
            options=options,
        )

    def list_stocks_taxonomies_risk_factors(
        self,
        taxonomy: Optional[float] = None,
        taxonomy_gt: Optional[float] = None,
        taxonomy_gte: Optional[float] = None,
        taxonomy_lt: Optional[float] = None,
        taxonomy_lte: Optional[float] = None,
        primary_category: Optional[str] = None,
        primary_category_any_of: Optional[str] = None,
        primary_category_gt: Optional[str] = None,
        primary_category_gte: Optional[str] = None,
        primary_category_lt: Optional[str] = None,
        primary_category_lte: Optional[str] = None,
        secondary_category: Optional[str] = None,
        secondary_category_any_of: Optional[str] = None,
        secondary_category_gt: Optional[str] = None,
        secondary_category_gte: Optional[str] = None,
        secondary_category_lt: Optional[str] = None,
        secondary_category_lte: Optional[str] = None,
        tertiary_category: Optional[str] = None,
        tertiary_category_any_of: Optional[str] = None,
        tertiary_category_gt: Optional[str] = None,
        tertiary_category_gte: Optional[str] = None,
        tertiary_category_lt: Optional[str] = None,
        tertiary_category_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[RiskFactorTaxonomy], HTTPResponse]:
        """
        Endpoint: GET /stocks/taxonomies/vX/risk-factors
        """
        url = "/stocks/taxonomies/vX/risk-factors"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_stocks_taxonomies_risk_factors, locals()),
            raw=raw,
            deserializer=RiskFactorTaxonomy.from_dict,
            options=options,
        )
