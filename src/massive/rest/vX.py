from .base import BaseClient
from typing import Optional, Any, Dict, List, Union, Iterator
from .models import (
    StockFinancial,
    IPOListing,
    Timeframe,
    Sort,
    Order,
)
from urllib3 import HTTPResponse
from datetime import datetime, date
from .models.request import RequestOptionBuilder


class VXClient(BaseClient):
    def list_stock_financials(
        self,
        ticker: Optional[str] = None,
        cik: Optional[str] = None,
        company_name: Optional[str] = None,
        company_name_search: Optional[str] = None,
        sic: Optional[str] = None,
        filing_date: Optional[Union[str, int, datetime, date]] = None,
        filing_date_lt: Optional[Union[str, int, datetime, date]] = None,
        filing_date_lte: Optional[Union[str, int, datetime, date]] = None,
        filing_date_gt: Optional[Union[str, int, datetime, date]] = None,
        filing_date_gte: Optional[Union[str, int, datetime, date]] = None,
        period_of_report_date: Optional[Union[str, int, datetime, date]] = None,
        period_of_report_date_lt: Optional[Union[str, int, datetime, date]] = None,
        period_of_report_date_lte: Optional[Union[str, int, datetime, date]] = None,
        period_of_report_date_gt: Optional[Union[str, int, datetime, date]] = None,
        period_of_report_date_gte: Optional[Union[str, int, datetime, date]] = None,
        timeframe: Optional[Union[str, Timeframe]] = None,
        include_sources: Optional[bool] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[StockFinancial], HTTPResponse]:
        """
        Get historical financial data for a stock ticker.

        :param ticker: Query by company ticker.
        :param cik: Query by central index key (CIK) Number.
        :param company_name: Query by company name.
        :param company_name_search: Query by company name with partial-match text search.
        :param sic: Query by standard industrial classification (SIC).
        :param filing_date: Query by the date when the filing with financials data was filed in YYYY-MM-DD format.
        :param filing_date_lt: filing_date less than.
        :param filing_date_lte: filing_date less than or equal to.
        :param filing_date_gt: filing_date greater than.
        :param filing_date_gte: filing_date greater than or equal to.
        :param period_of_report_date: The period of report for the period_of_report with financials data in YYYY-MM-DD format.
        :param period_of_report_date_lt: period_of_report_date less than.
        :param period_of_report_date_lte: period_of_report_date less than or equal to.
        :param period_of_report_date_gt: period_of_report_date greater than.
        :param period_of_report_date_gte: period_of_report_date greater than or equal to.
        :param timeframe: Query by timeframe.
        :param include_sources: Whether or not to include the xpath and formula attributes for each financial data point.
        :param limit: Limit the number of results returned per-page, default is 10 and max is 100.
        :param sort: Sort field used for ordering.
        :param order: Order results based on the sort field.
        :param params: Any additional query params
        :param raw: Return raw object instead of results object
        :return: Iterator of financials
        """
        url = "/vX/reference/financials"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_stock_financials, locals()),
            raw=raw,
            deserializer=StockFinancial.from_dict,
            options=options,
        )

    def list_ipos(
        self,
        ticker: Optional[str] = None,
        us_code: Optional[str] = None,
        isin: Optional[str] = None,
        listing_date: Optional[str] = None,
        listing_date_lt: Optional[str] = None,
        listing_date_lte: Optional[str] = None,
        listing_date_gt: Optional[str] = None,
        listing_date_gte: Optional[str] = None,
        ipo_status: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        order: Optional[Union[str, Order]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[List[IPOListing], HTTPResponse]:
        """
        Retrieve upcoming or historical IPOs.

        :param ticker: Filter by a case-sensitive ticker symbol.
        :param us_code: Filter by a US code (unique identifier for a North American financial security).
        :param isin: Filter by an International Securities Identification Number (ISIN).
        :param listing_date: Filter by the listing date (YYYY-MM-DD).
        :param ipo_status: Filter by IPO status (e.g. "new", "pending", "history", etc.).
        :param limit: Limit the number of results per page. Default 10, max 1000.
        :param sort: Field to sort by. Default is "listing_date".
        :param order: Order results based on the sort field ("asc" or "desc"). Default "desc".
        :param params: Additional query params.
        :param raw: Return raw HTTPResponse object if True, else return List[IPOListing].
        :param options: RequestOptionBuilder for additional headers or params.
        :return: A list of IPOListing objects or HTTPResponse if raw=True.
        """
        url = "/vX/reference/ipos"

        return self._paginate(
            path=url,
            params=self._get_params(self.list_ipos, locals()),
            deserializer=IPOListing.from_dict,
            raw=raw,
            result_key="results",
            options=options,
        )
