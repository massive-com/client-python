from typing import Optional, Any, Dict, List, Union, Iterator
from urllib3 import HTTPResponse
from datetime import datetime, date

from .base import BaseClient
from .models.etf_global import (
    EtfGlobalAnalytics,
    EtfGlobalConstituent,
    EtfGlobalFundFlow,
    EtfGlobalProfile,
    EtfGlobalTaxonomy,
)
from .models.common import Sort
from .models.request import RequestOptionBuilder


class EtfGlobalClient(BaseClient):
    """
    Client for the ETF Global REST Endpoints
    (aligned with the paths from /etf-global/v1/...)
    """

    def get_etf_global_analytics(
        self,
        composite_ticker: Optional[str] = None,
        composite_ticker_any_of: Optional[str] = None,
        composite_ticker_gt: Optional[str] = None,
        composite_ticker_gte: Optional[str] = None,
        composite_ticker_lt: Optional[str] = None,
        composite_ticker_lte: Optional[str] = None,
        processed_date: Optional[Union[str, date]] = None,
        processed_date_gt: Optional[Union[str, date]] = None,
        processed_date_gte: Optional[Union[str, date]] = None,
        processed_date_lt: Optional[Union[str, date]] = None,
        processed_date_lte: Optional[Union[str, date]] = None,
        effective_date: Optional[Union[str, date]] = None,
        effective_date_gt: Optional[Union[str, date]] = None,
        effective_date_gte: Optional[Union[str, date]] = None,
        effective_date_lt: Optional[Union[str, date]] = None,
        effective_date_lte: Optional[Union[str, date]] = None,
        risk_total_score: Optional[float] = None,
        risk_total_score_gt: Optional[float] = None,
        risk_total_score_gte: Optional[float] = None,
        risk_total_score_lt: Optional[float] = None,
        risk_total_score_lte: Optional[float] = None,
        reward_score: Optional[float] = None,
        reward_score_gt: Optional[float] = None,
        reward_score_gte: Optional[float] = None,
        reward_score_lt: Optional[float] = None,
        reward_score_lte: Optional[float] = None,
        quant_total_score: Optional[float] = None,
        quant_total_score_gt: Optional[float] = None,
        quant_total_score_gte: Optional[float] = None,
        quant_total_score_lt: Optional[float] = None,
        quant_total_score_lte: Optional[float] = None,
        quant_grade: Optional[str] = None,
        quant_grade_any_of: Optional[str] = None,
        quant_grade_gt: Optional[str] = None,
        quant_grade_gte: Optional[str] = None,
        quant_grade_lt: Optional[str] = None,
        quant_grade_lte: Optional[str] = None,
        quant_composite_technical: Optional[float] = None,
        quant_composite_technical_gt: Optional[float] = None,
        quant_composite_technical_gte: Optional[float] = None,
        quant_composite_technical_lt: Optional[float] = None,
        quant_composite_technical_lte: Optional[float] = None,
        quant_composite_sentiment: Optional[float] = None,
        quant_composite_sentiment_gt: Optional[float] = None,
        quant_composite_sentiment_gte: Optional[float] = None,
        quant_composite_sentiment_lt: Optional[float] = None,
        quant_composite_sentiment_lte: Optional[float] = None,
        quant_composite_behavioral: Optional[float] = None,
        quant_composite_behavioral_gt: Optional[float] = None,
        quant_composite_behavioral_gte: Optional[float] = None,
        quant_composite_behavioral_lt: Optional[float] = None,
        quant_composite_behavioral_lte: Optional[float] = None,
        quant_composite_fundamental: Optional[float] = None,
        quant_composite_fundamental_gt: Optional[float] = None,
        quant_composite_fundamental_gte: Optional[float] = None,
        quant_composite_fundamental_lt: Optional[float] = None,
        quant_composite_fundamental_lte: Optional[float] = None,
        quant_composite_global: Optional[float] = None,
        quant_composite_global_gt: Optional[float] = None,
        quant_composite_global_gte: Optional[float] = None,
        quant_composite_global_lt: Optional[float] = None,
        quant_composite_global_lte: Optional[float] = None,
        quant_composite_quality: Optional[float] = None,
        quant_composite_quality_gt: Optional[float] = None,
        quant_composite_quality_gte: Optional[float] = None,
        quant_composite_quality_lt: Optional[float] = None,
        quant_composite_quality_lte: Optional[float] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[EtfGlobalAnalytics], HTTPResponse]:
        """
        Endpoint: GET /etf-global/v1/analytics
        """
        url = "/etf-global/v1/analytics"
        return self._paginate(
            path=url,
            params=self._get_params(self.get_etf_global_analytics, locals()),
            raw=raw,
            deserializer=EtfGlobalAnalytics.from_dict,
            options=options,
        )

    def get_etf_global_constituents(
        self,
        composite_ticker: Optional[str] = None,
        composite_ticker_any_of: Optional[str] = None,
        composite_ticker_gt: Optional[str] = None,
        composite_ticker_gte: Optional[str] = None,
        composite_ticker_lt: Optional[str] = None,
        composite_ticker_lte: Optional[str] = None,
        constituent_ticker: Optional[str] = None,
        constituent_ticker_any_of: Optional[str] = None,
        constituent_ticker_gt: Optional[str] = None,
        constituent_ticker_gte: Optional[str] = None,
        constituent_ticker_lt: Optional[str] = None,
        constituent_ticker_lte: Optional[str] = None,
        effective_date: Optional[Union[str, date]] = None,
        effective_date_gt: Optional[Union[str, date]] = None,
        effective_date_gte: Optional[Union[str, date]] = None,
        effective_date_lt: Optional[Union[str, date]] = None,
        effective_date_lte: Optional[Union[str, date]] = None,
        processed_date: Optional[Union[str, date]] = None,
        processed_date_gt: Optional[Union[str, date]] = None,
        processed_date_gte: Optional[Union[str, date]] = None,
        processed_date_lt: Optional[Union[str, date]] = None,
        processed_date_lte: Optional[Union[str, date]] = None,
        us_code: Optional[str] = None,
        us_code_any_of: Optional[str] = None,
        us_code_gt: Optional[str] = None,
        us_code_gte: Optional[str] = None,
        us_code_lt: Optional[str] = None,
        us_code_lte: Optional[str] = None,
        isin: Optional[str] = None,
        isin_any_of: Optional[str] = None,
        isin_gt: Optional[str] = None,
        isin_gte: Optional[str] = None,
        isin_lt: Optional[str] = None,
        isin_lte: Optional[str] = None,
        figi: Optional[str] = None,
        figi_any_of: Optional[str] = None,
        figi_gt: Optional[str] = None,
        figi_gte: Optional[str] = None,
        figi_lt: Optional[str] = None,
        figi_lte: Optional[str] = None,
        sedol: Optional[str] = None,
        sedol_any_of: Optional[str] = None,
        sedol_gt: Optional[str] = None,
        sedol_gte: Optional[str] = None,
        sedol_lt: Optional[str] = None,
        sedol_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[EtfGlobalConstituent], HTTPResponse]:
        """
        Endpoint: GET /etf-global/v1/constituents
        """
        url = "/etf-global/v1/constituents"
        return self._paginate(
            path=url,
            params=self._get_params(self.get_etf_global_constituents, locals()),
            raw=raw,
            deserializer=EtfGlobalConstituent.from_dict,
            options=options,
        )

    def get_etf_global_fund_flows(
        self,
        processed_date: Optional[Union[str, date]] = None,
        processed_date_gt: Optional[Union[str, date]] = None,
        processed_date_gte: Optional[Union[str, date]] = None,
        processed_date_lt: Optional[Union[str, date]] = None,
        processed_date_lte: Optional[Union[str, date]] = None,
        effective_date: Optional[Union[str, date]] = None,
        effective_date_gt: Optional[Union[str, date]] = None,
        effective_date_gte: Optional[Union[str, date]] = None,
        effective_date_lt: Optional[Union[str, date]] = None,
        effective_date_lte: Optional[Union[str, date]] = None,
        composite_ticker: Optional[str] = None,
        composite_ticker_any_of: Optional[str] = None,
        composite_ticker_gt: Optional[str] = None,
        composite_ticker_gte: Optional[str] = None,
        composite_ticker_lt: Optional[str] = None,
        composite_ticker_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[EtfGlobalFundFlow], HTTPResponse]:
        """
        Endpoint: GET /etf-global/v1/fund-flows
        """
        url = "/etf-global/v1/fund-flows"
        return self._paginate(
            path=url,
            params=self._get_params(self.get_etf_global_fund_flows, locals()),
            raw=raw,
            deserializer=EtfGlobalFundFlow.from_dict,
            options=options,
        )

    def get_etf_global_profiles(
        self,
        processed_date: Optional[Union[str, date]] = None,
        processed_date_gt: Optional[Union[str, date]] = None,
        processed_date_gte: Optional[Union[str, date]] = None,
        processed_date_lt: Optional[Union[str, date]] = None,
        processed_date_lte: Optional[Union[str, date]] = None,
        effective_date: Optional[Union[str, date]] = None,
        effective_date_gt: Optional[Union[str, date]] = None,
        effective_date_gte: Optional[Union[str, date]] = None,
        effective_date_lt: Optional[Union[str, date]] = None,
        effective_date_lte: Optional[Union[str, date]] = None,
        composite_ticker: Optional[str] = None,
        composite_ticker_any_of: Optional[str] = None,
        composite_ticker_gt: Optional[str] = None,
        composite_ticker_gte: Optional[str] = None,
        composite_ticker_lt: Optional[str] = None,
        composite_ticker_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[EtfGlobalProfile], HTTPResponse]:
        """
        Endpoint: GET /etf-global/v1/profiles
        """
        url = "/etf-global/v1/profiles"
        return self._paginate(
            path=url,
            params=self._get_params(self.get_etf_global_profiles, locals()),
            raw=raw,
            deserializer=EtfGlobalProfile.from_dict,
            options=options,
        )

    def get_etf_global_taxonomies(
        self,
        processed_date: Optional[Union[str, date]] = None,
        processed_date_gt: Optional[Union[str, date]] = None,
        processed_date_gte: Optional[Union[str, date]] = None,
        processed_date_lt: Optional[Union[str, date]] = None,
        processed_date_lte: Optional[Union[str, date]] = None,
        effective_date: Optional[Union[str, date]] = None,
        effective_date_gt: Optional[Union[str, date]] = None,
        effective_date_gte: Optional[Union[str, date]] = None,
        effective_date_lt: Optional[Union[str, date]] = None,
        effective_date_lte: Optional[Union[str, date]] = None,
        composite_ticker: Optional[str] = None,
        composite_ticker_any_of: Optional[str] = None,
        composite_ticker_gt: Optional[str] = None,
        composite_ticker_gte: Optional[str] = None,
        composite_ticker_lt: Optional[str] = None,
        composite_ticker_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[EtfGlobalTaxonomy], HTTPResponse]:
        """
        Endpoint: GET /etf-global/v1/taxonomies
        """
        url = "/etf-global/v1/taxonomies"
        return self._paginate(
            path=url,
            params=self._get_params(self.get_etf_global_taxonomies, locals()),
            raw=raw,
            deserializer=EtfGlobalTaxonomy.from_dict,
            options=options,
        )
