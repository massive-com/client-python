from typing import Optional, Any, Dict, List, Union, Iterator
from urllib3 import HTTPResponse
from datetime import datetime, date

from .base import BaseClient
from .models.economy import (
    FedInflation,
    TreasuryYield,
    FedInflationExpectations,
    FedLaborMarket,
    EUMerchantAggregate,
    EUMerchantHierarchy,
)
from .models.common import Sort, Order
from .models.request import RequestOptionBuilder


class EconomyClient(BaseClient):
    """
    Client for the Fed REST Endpoints
    (aligned with the paths from /fed/v1/...)
    """

    def list_treasury_yields(
        self,
        date: Optional[str] = None,
        date_any_of: Optional[str] = None,
        date_gt: Optional[str] = None,
        date_gte: Optional[str] = None,
        date_lt: Optional[str] = None,
        date_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[TreasuryYield], HTTPResponse]:
        """
        Retrieve treasury yield data.

        :param date: Calendar date of the yield observation (YYYY-MM-DD).
        :param date_any_of: Filter equal to any of the values.
        :param date_gt: Filter for dates greater than the provided date.
        :param date_gte: Filter for dates greater than or equal to the provided date.
        :param date_lt: Filter for dates less than the provided date.
        :param date_lte: Filter for dates less than or equal to the provided date.
        :param limit: Limit the number of results returned. Default 100, max 50000.
        :param sort: Field to sort by (e.g., "date"). Default "date".
        :param order: Order results based on the sort field ("asc" or "desc"). Default "desc".
        :param params: Additional query parameters.
        :param raw: Return raw HTTPResponse object if True, else return List[TreasuryYield].
        :param options: RequestOptionBuilder for additional headers or params.
        :return: A list of TreasuryYield objects or HTTPResponse if raw=True.
        """
        url = "/fed/v1/treasury-yields"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_treasury_yields, locals()),
            deserializer=TreasuryYield.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )

    def list_inflation(
        self,
        date: Optional[Union[str, date]] = None,
        date_any_of: Optional[str] = None,
        date_gt: Optional[Union[str, date]] = None,
        date_gte: Optional[Union[str, date]] = None,
        date_lt: Optional[Union[str, date]] = None,
        date_lte: Optional[Union[str, date]] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FedInflation], HTTPResponse]:
        """
        Endpoint: GET /fed/v1/inflation
        """
        url = "/fed/v1/inflation"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_inflation, locals()),
            raw=raw,
            deserializer=FedInflation.from_dict,
            options=options,
        )

    def list_inflation_expectations(
        self,
        date: Optional[Union[str, date]] = None,
        date_any_of: Optional[str] = None,
        date_gt: Optional[Union[str, date]] = None,
        date_gte: Optional[Union[str, date]] = None,
        date_lt: Optional[Union[str, date]] = None,
        date_lte: Optional[Union[str, date]] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FedInflationExpectations], HTTPResponse]:
        """
        A table tracking inflation expectations from both market-based and economic model perspectives across different time horizons.

        :param date: Calendar date of the observation (YYYY-MM-DD).
        :param date_any_of: Filter equal to any of the values. Multiple values can be specified by using a comma separated list.
        :param date_gt: Filter greater than the value.
        :param date_gte: Filter greater than or equal to the value.
        :param date_lt: Filter less than the value.
        :param date_lte: Filter less than or equal to the value.
        :param limit: Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'.
        :param sort: A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'date' if not specified. The sort order defaults to 'asc' if not specified.
        :param params: Additional query parameters.
        :param raw: Return raw HTTPResponse object if True, else return Iterator[FedInflationExpectations].
        :param options: RequestOptionBuilder for additional headers or params.
        :return: An iterator of FedInflationExpectations objects or HTTPResponse if raw=True.
        """
        url = "/fed/v1/inflation-expectations"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_inflation_expectations, locals()),
            deserializer=FedInflationExpectations.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )

    def list_labor_market_indicators(
        self,
        date: Optional[str] = None,
        date_any_of: Optional[str] = None,
        date_gt: Optional[str] = None,
        date_gte: Optional[str] = None,
        date_lt: Optional[str] = None,
        date_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[FedLaborMarket], HTTPResponse]:
        """
        Labor market indicators from the Federal Reserve, including unemployment rate, labor force participation, average hourly earnings, and job openings data.

        :param date: Calendar date of the observation (YYYY-MM-DD).
        :param date_any_of: Filter equal to any of the values. Multiple values can be specified by using a comma separated list.
        :param date_gt: Filter greater than the value.
        :param date_gte: Filter greater than or equal to the value.
        :param date_lt: Filter less than the value.
        :param date_lte: Filter less than or equal to the value.
        :param limit: Limit the maximum number of results returned. Defaults to '100' if not specified. The maximum allowed limit is '50000'.
        :param sort: A comma separated list of sort columns. For each column, append '.asc' or '.desc' to specify the sort direction. The sort column defaults to 'date' if not specified. The sort order defaults to 'asc' if not specified.
        :param params: Additional query parameters.
        :param raw: Return raw HTTPResponse object if True, else return Iterator[FedLaborMarket].
        :param options: RequestOptionBuilder for additional headers or params.
        :return: An iterator of FedLaborMarket objects or HTTPResponse if raw=True.
        """
        url = "/fed/v1/labor-market"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_labor_market_indicators, locals()),
            deserializer=FedLaborMarket.from_dict,
            raw=raw,
            options=options,
        )

    def list_eu_merchant_aggregates(
        self,
        transaction_date: Optional[Union[str, date]] = None,
        transaction_date_gt: Optional[Union[str, date]] = None,
        transaction_date_gte: Optional[Union[str, date]] = None,
        transaction_date_lt: Optional[Union[str, date]] = None,
        transaction_date_lte: Optional[Union[str, date]] = None,
        name: Optional[str] = None,
        name_any_of: Optional[str] = None,
        name_gt: Optional[str] = None,
        name_gte: Optional[str] = None,
        name_lt: Optional[str] = None,
        name_lte: Optional[str] = None,
        user_country: Optional[str] = None,
        user_country_any_of: Optional[str] = None,
        channel: Optional[str] = None,
        channel_any_of: Optional[str] = None,
        consumer_type: Optional[str] = None,
        consumer_type_any_of: Optional[str] = None,
        parent_name: Optional[str] = None,
        parent_name_any_of: Optional[str] = None,
        parent_name_gt: Optional[str] = None,
        parent_name_gte: Optional[str] = None,
        parent_name_lt: Optional[str] = None,
        parent_name_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[EUMerchantAggregate], HTTPResponse]:
        """
        Aggregated consumer transactions from European credit card panels (UK, DE, FR, IT, ES, AT).
        Each row represents daily credit card, debit card, or open banking transactions
        (7-day lag from transaction date) at a tagged merchant or payment processor.

        Includes ticker (Bloomberg) and industry mapping for ~250 US public companies.
        User counts provided across 8- and 28-day windows for normalization.
        """
        url = "/consumer-spending/eu/v1/merchant-aggregates"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_eu_merchant_aggregates, locals()),
            deserializer=EUMerchantAggregate.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )

    def list_eu_merchant_hierarchy(
        self,
        lookup_name: Optional[str] = None,
        lookup_name_any_of: Optional[str] = None,
        lookup_name_gt: Optional[str] = None,
        lookup_name_gte: Optional[str] = None,
        lookup_name_lt: Optional[str] = None,
        lookup_name_lte: Optional[str] = None,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        listing_status: Optional[str] = None,
        listing_status_any_of: Optional[str] = None,
        active_from: Optional[Union[str, date]] = None,
        active_from_gt: Optional[Union[str, date]] = None,
        active_from_gte: Optional[Union[str, date]] = None,
        active_from_lt: Optional[Union[str, date]] = None,
        active_from_lte: Optional[Union[str, date]] = None,
        active_to: Optional[Union[str, date]] = None,
        active_to_gt: Optional[Union[str, date]] = None,
        active_to_gte: Optional[Union[str, date]] = None,
        active_to_lt: Optional[Union[str, date]] = None,
        active_to_lte: Optional[Union[str, date]] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[EUMerchantHierarchy], HTTPResponse]:
        """
        Reference data mapping merchants to parent companies, tickers, sectors,
        and industries across Fable's European consumer transaction panel.

        Use lookup_name + active_from/active_to to join with merchant-aggregates
        for point-in-time queries.
        """
        url = "/consumer-spending/eu/v1/merchant-hierarchy"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_eu_merchant_hierarchy, locals()),
            deserializer=EUMerchantHierarchy.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )
