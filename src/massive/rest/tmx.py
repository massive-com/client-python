from typing import Optional, Any, Dict, List, Union, Iterator
from urllib3 import HTTPResponse
from datetime import datetime, date

from .base import BaseClient
from .models.tmx import (
    TmxCorporateEvent,
)
from .models.common import Sort
from .models.request import RequestOptionBuilder


class TmxClient(BaseClient):
    """
    Client for the TMX REST Endpoints
    (aligned with the paths from /tmx/v1/...)
    """

    def list_tmx_corporate_events(
        self,
        date: Optional[Union[str, date]] = None,
        date_any_of: Optional[str] = None,
        date_gt: Optional[Union[str, date]] = None,
        date_gte: Optional[Union[str, date]] = None,
        date_lt: Optional[Union[str, date]] = None,
        date_lte: Optional[Union[str, date]] = None,
        type: Optional[str] = None,
        type_any_of: Optional[str] = None,
        type_gt: Optional[str] = None,
        type_gte: Optional[str] = None,
        type_lt: Optional[str] = None,
        type_lte: Optional[str] = None,
        status: Optional[str] = None,
        status_any_of: Optional[str] = None,
        status_gt: Optional[str] = None,
        status_gte: Optional[str] = None,
        status_lt: Optional[str] = None,
        status_lte: Optional[str] = None,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        isin: Optional[str] = None,
        isin_any_of: Optional[str] = None,
        isin_gt: Optional[str] = None,
        isin_gte: Optional[str] = None,
        isin_lt: Optional[str] = None,
        isin_lte: Optional[str] = None,
        trading_venue: Optional[str] = None,
        trading_venue_any_of: Optional[str] = None,
        trading_venue_gt: Optional[str] = None,
        trading_venue_gte: Optional[str] = None,
        trading_venue_lt: Optional[str] = None,
        trading_venue_lte: Optional[str] = None,
        tmx_company_id: Optional[int] = None,
        tmx_company_id_any_of: Optional[str] = None,
        tmx_company_id_gt: Optional[int] = None,
        tmx_company_id_gte: Optional[int] = None,
        tmx_company_id_lt: Optional[int] = None,
        tmx_company_id_lte: Optional[int] = None,
        tmx_record_id: Optional[str] = None,
        tmx_record_id_any_of: Optional[str] = None,
        tmx_record_id_gt: Optional[str] = None,
        tmx_record_id_gte: Optional[str] = None,
        tmx_record_id_lt: Optional[str] = None,
        tmx_record_id_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[TmxCorporateEvent], HTTPResponse]:
        """
        Endpoint: GET /tmx/v1/corporate-events
        """
        url = "/tmx/v1/corporate-events"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_tmx_corporate_events, locals()),
            raw=raw,
            deserializer=TmxCorporateEvent.from_dict,
            options=options,
        )
