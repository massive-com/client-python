from typing import Optional, Any, Dict, List, Union, Iterator
from urllib3 import HTTPResponse
from datetime import datetime, date

from .base import BaseClient
from .models.benzinga import (
    BenzingaAnalystInsight,
    BenzingaAnalyst,
    BenzingaConsensusRating,
    BenzingaEarning,
    BenzingaFirm,
    BenzingaGuidance,
    BenzingaNews,
    BenzingaRating,
    BenzingaBullsBearsSay,
)
from .models.common import Sort
from .models.request import RequestOptionBuilder


class BenzingaClient(BaseClient):
    """
    Client for the Benzinga REST Endpoints
    (aligned with the paths from /benzinga/v1/...)
    """

    def list_benzinga_analyst_insights(
        self,
        date: Optional[Union[str, date]] = None,
        date_any_of: Optional[str] = None,
        date_gt: Optional[Union[str, date]] = None,
        date_gte: Optional[Union[str, date]] = None,
        date_lt: Optional[Union[str, date]] = None,
        date_lte: Optional[Union[str, date]] = None,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        last_updated: Optional[str] = None,
        last_updated_any_of: Optional[str] = None,
        last_updated_gt: Optional[str] = None,
        last_updated_gte: Optional[str] = None,
        last_updated_lt: Optional[str] = None,
        last_updated_lte: Optional[str] = None,
        firm: Optional[str] = None,
        firm_any_of: Optional[str] = None,
        firm_gt: Optional[str] = None,
        firm_gte: Optional[str] = None,
        firm_lt: Optional[str] = None,
        firm_lte: Optional[str] = None,
        rating_action: Optional[str] = None,
        rating_action_any_of: Optional[str] = None,
        rating_action_gt: Optional[str] = None,
        rating_action_gte: Optional[str] = None,
        rating_action_lt: Optional[str] = None,
        rating_action_lte: Optional[str] = None,
        benzinga_firm_id: Optional[str] = None,
        benzinga_firm_id_any_of: Optional[str] = None,
        benzinga_firm_id_gt: Optional[str] = None,
        benzinga_firm_id_gte: Optional[str] = None,
        benzinga_firm_id_lt: Optional[str] = None,
        benzinga_firm_id_lte: Optional[str] = None,
        benzinga_rating_id: Optional[str] = None,
        benzinga_rating_id_any_of: Optional[str] = None,
        benzinga_rating_id_gt: Optional[str] = None,
        benzinga_rating_id_gte: Optional[str] = None,
        benzinga_rating_id_lt: Optional[str] = None,
        benzinga_rating_id_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaAnalystInsight], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v1/analyst-insights
        """
        url = "/benzinga/v1/analyst-insights"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_analyst_insights, locals()),
            raw=raw,
            deserializer=BenzingaAnalystInsight.from_dict,
            options=options,
        )

    def list_benzinga_analysts(
        self,
        benzinga_id: Optional[str] = None,
        benzinga_id_any_of: Optional[str] = None,
        benzinga_id_gt: Optional[str] = None,
        benzinga_id_gte: Optional[str] = None,
        benzinga_id_lt: Optional[str] = None,
        benzinga_id_lte: Optional[str] = None,
        benzinga_firm_id: Optional[str] = None,
        benzinga_firm_id_any_of: Optional[str] = None,
        benzinga_firm_id_gt: Optional[str] = None,
        benzinga_firm_id_gte: Optional[str] = None,
        benzinga_firm_id_lt: Optional[str] = None,
        benzinga_firm_id_lte: Optional[str] = None,
        firm_name: Optional[str] = None,
        firm_name_any_of: Optional[str] = None,
        firm_name_gt: Optional[str] = None,
        firm_name_gte: Optional[str] = None,
        firm_name_lt: Optional[str] = None,
        firm_name_lte: Optional[str] = None,
        full_name: Optional[str] = None,
        full_name_any_of: Optional[str] = None,
        full_name_gt: Optional[str] = None,
        full_name_gte: Optional[str] = None,
        full_name_lt: Optional[str] = None,
        full_name_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaAnalyst], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v1/analysts
        """
        url = "/benzinga/v1/analysts"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_analysts, locals()),
            raw=raw,
            deserializer=BenzingaAnalyst.from_dict,
            options=options,
        )

    def list_benzinga_consensus_ratings(
        self,
        ticker: str,
        date: Optional[Union[str, date]] = None,
        date_gt: Optional[Union[str, date]] = None,
        date_gte: Optional[Union[str, date]] = None,
        date_lt: Optional[Union[str, date]] = None,
        date_lte: Optional[Union[str, date]] = None,
        limit: Optional[int] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaConsensusRating], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v1/consensus-ratings/{ticker}
        """
        url = f"/benzinga/v1/consensus-ratings/{ticker}"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_consensus_ratings, locals()),
            raw=raw,
            deserializer=BenzingaConsensusRating.from_dict,
            options=options,
        )

    def list_benzinga_earnings(
        self,
        date: Optional[Union[str, date]] = None,
        date_any_of: Optional[str] = None,
        date_gt: Optional[Union[str, date]] = None,
        date_gte: Optional[Union[str, date]] = None,
        date_lt: Optional[Union[str, date]] = None,
        date_lte: Optional[Union[str, date]] = None,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        importance: Optional[int] = None,
        importance_any_of: Optional[str] = None,
        importance_gt: Optional[int] = None,
        importance_gte: Optional[int] = None,
        importance_lt: Optional[int] = None,
        importance_lte: Optional[int] = None,
        last_updated: Optional[str] = None,
        last_updated_any_of: Optional[str] = None,
        last_updated_gt: Optional[str] = None,
        last_updated_gte: Optional[str] = None,
        last_updated_lt: Optional[str] = None,
        last_updated_lte: Optional[str] = None,
        date_status: Optional[str] = None,
        date_status_any_of: Optional[str] = None,
        date_status_gt: Optional[str] = None,
        date_status_gte: Optional[str] = None,
        date_status_lt: Optional[str] = None,
        date_status_lte: Optional[str] = None,
        eps_surprise_percent: Optional[float] = None,
        eps_surprise_percent_any_of: Optional[str] = None,
        eps_surprise_percent_gt: Optional[float] = None,
        eps_surprise_percent_gte: Optional[float] = None,
        eps_surprise_percent_lt: Optional[float] = None,
        eps_surprise_percent_lte: Optional[float] = None,
        revenue_surprise_percent: Optional[float] = None,
        revenue_surprise_percent_any_of: Optional[str] = None,
        revenue_surprise_percent_gt: Optional[float] = None,
        revenue_surprise_percent_gte: Optional[float] = None,
        revenue_surprise_percent_lt: Optional[float] = None,
        revenue_surprise_percent_lte: Optional[float] = None,
        fiscal_year: Optional[int] = None,
        fiscal_year_any_of: Optional[str] = None,
        fiscal_year_gt: Optional[int] = None,
        fiscal_year_gte: Optional[int] = None,
        fiscal_year_lt: Optional[int] = None,
        fiscal_year_lte: Optional[int] = None,
        fiscal_period: Optional[str] = None,
        fiscal_period_any_of: Optional[str] = None,
        fiscal_period_gt: Optional[str] = None,
        fiscal_period_gte: Optional[str] = None,
        fiscal_period_lt: Optional[str] = None,
        fiscal_period_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaEarning], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v1/earnings
        """
        url = "/benzinga/v1/earnings"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_earnings, locals()),
            raw=raw,
            deserializer=BenzingaEarning.from_dict,
            options=options,
        )

    def list_benzinga_firms(
        self,
        benzinga_id: Optional[str] = None,
        benzinga_id_any_of: Optional[str] = None,
        benzinga_id_gt: Optional[str] = None,
        benzinga_id_gte: Optional[str] = None,
        benzinga_id_lt: Optional[str] = None,
        benzinga_id_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaFirm], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v1/firms
        """
        url = "/benzinga/v1/firms"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_firms, locals()),
            raw=raw,
            deserializer=BenzingaFirm.from_dict,
            options=options,
        )

    def list_benzinga_guidance(
        self,
        date: Optional[Union[str, date]] = None,
        date_any_of: Optional[str] = None,
        date_gt: Optional[Union[str, date]] = None,
        date_gte: Optional[Union[str, date]] = None,
        date_lt: Optional[Union[str, date]] = None,
        date_lte: Optional[Union[str, date]] = None,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        positioning: Optional[str] = None,
        positioning_any_of: Optional[str] = None,
        positioning_gt: Optional[str] = None,
        positioning_gte: Optional[str] = None,
        positioning_lt: Optional[str] = None,
        positioning_lte: Optional[str] = None,
        importance: Optional[int] = None,
        importance_any_of: Optional[str] = None,
        importance_gt: Optional[int] = None,
        importance_gte: Optional[int] = None,
        importance_lt: Optional[int] = None,
        importance_lte: Optional[int] = None,
        last_updated: Optional[str] = None,
        last_updated_any_of: Optional[str] = None,
        last_updated_gt: Optional[str] = None,
        last_updated_gte: Optional[str] = None,
        last_updated_lt: Optional[str] = None,
        last_updated_lte: Optional[str] = None,
        fiscal_year: Optional[int] = None,
        fiscal_year_any_of: Optional[str] = None,
        fiscal_year_gt: Optional[int] = None,
        fiscal_year_gte: Optional[int] = None,
        fiscal_year_lt: Optional[int] = None,
        fiscal_year_lte: Optional[int] = None,
        fiscal_period: Optional[str] = None,
        fiscal_period_any_of: Optional[str] = None,
        fiscal_period_gt: Optional[str] = None,
        fiscal_period_gte: Optional[str] = None,
        fiscal_period_lt: Optional[str] = None,
        fiscal_period_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaGuidance], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v1/guidance
        """
        url = "/benzinga/v1/guidance"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_guidance, locals()),
            raw=raw,
            deserializer=BenzingaGuidance.from_dict,
            options=options,
        )

    def list_benzinga_news(
        self,
        published: Optional[str] = None,
        published_any_of: Optional[str] = None,
        published_gt: Optional[str] = None,
        published_gte: Optional[str] = None,
        published_lt: Optional[str] = None,
        published_lte: Optional[str] = None,
        last_updated: Optional[str] = None,
        last_updated_any_of: Optional[str] = None,
        last_updated_gt: Optional[str] = None,
        last_updated_gte: Optional[str] = None,
        last_updated_lt: Optional[str] = None,
        last_updated_lte: Optional[str] = None,
        tickers: Optional[str] = None,
        tickers_all_of: Optional[str] = None,
        tickers_any_of: Optional[str] = None,
        channels: Optional[str] = None,
        channels_all_of: Optional[str] = None,
        channels_any_of: Optional[str] = None,
        tags: Optional[str] = None,
        tags_all_of: Optional[str] = None,
        tags_any_of: Optional[str] = None,
        author: Optional[str] = None,
        author_any_of: Optional[str] = None,
        author_gt: Optional[str] = None,
        author_gte: Optional[str] = None,
        author_lt: Optional[str] = None,
        author_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaNews], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v1/news
        """
        url = "/benzinga/v1/news"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_news, locals()),
            raw=raw,
            deserializer=BenzingaNews.from_dict,
            options=options,
        )

    def list_benzinga_news_v2(
        self,
        published: Optional[str] = None,
        published_gt: Optional[str] = None,
        published_gte: Optional[str] = None,
        published_lt: Optional[str] = None,
        published_lte: Optional[str] = None,
        channels: Optional[str] = None,
        channels_all_of: Optional[str] = None,
        channels_any_of: Optional[str] = None,
        tags: Optional[str] = None,
        tags_all_of: Optional[str] = None,
        tags_any_of: Optional[str] = None,
        author: Optional[str] = None,
        author_any_of: Optional[str] = None,
        author_gt: Optional[str] = None,
        author_gte: Optional[str] = None,
        author_lt: Optional[str] = None,
        author_lte: Optional[str] = None,
        stocks: Optional[str] = None,
        stocks_all_of: Optional[str] = None,
        stocks_any_of: Optional[str] = None,
        tickers: Optional[str] = None,
        tickers_all_of: Optional[str] = None,
        tickers_any_of: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaNews], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v2/news
        """
        url = "/benzinga/v2/news"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_news_v2, locals()),
            raw=raw,
            deserializer=BenzingaNews.from_dict,
            options=options,
        )

    def list_benzinga_ratings(
        self,
        date: Optional[Union[str, date]] = None,
        date_any_of: Optional[str] = None,
        date_gt: Optional[Union[str, date]] = None,
        date_gte: Optional[Union[str, date]] = None,
        date_lt: Optional[Union[str, date]] = None,
        date_lte: Optional[Union[str, date]] = None,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        importance: Optional[int] = None,
        importance_any_of: Optional[str] = None,
        importance_gt: Optional[int] = None,
        importance_gte: Optional[int] = None,
        importance_lt: Optional[int] = None,
        importance_lte: Optional[int] = None,
        last_updated: Optional[str] = None,
        last_updated_any_of: Optional[str] = None,
        last_updated_gt: Optional[str] = None,
        last_updated_gte: Optional[str] = None,
        last_updated_lt: Optional[str] = None,
        last_updated_lte: Optional[str] = None,
        rating_action: Optional[str] = None,
        rating_action_any_of: Optional[str] = None,
        rating_action_gt: Optional[str] = None,
        rating_action_gte: Optional[str] = None,
        rating_action_lt: Optional[str] = None,
        rating_action_lte: Optional[str] = None,
        price_target_action: Optional[str] = None,
        price_target_action_any_of: Optional[str] = None,
        price_target_action_gt: Optional[str] = None,
        price_target_action_gte: Optional[str] = None,
        price_target_action_lt: Optional[str] = None,
        price_target_action_lte: Optional[str] = None,
        benzinga_id: Optional[str] = None,
        benzinga_id_any_of: Optional[str] = None,
        benzinga_id_gt: Optional[str] = None,
        benzinga_id_gte: Optional[str] = None,
        benzinga_id_lt: Optional[str] = None,
        benzinga_id_lte: Optional[str] = None,
        benzinga_analyst_id: Optional[str] = None,
        benzinga_analyst_id_any_of: Optional[str] = None,
        benzinga_analyst_id_gt: Optional[str] = None,
        benzinga_analyst_id_gte: Optional[str] = None,
        benzinga_analyst_id_lt: Optional[str] = None,
        benzinga_analyst_id_lte: Optional[str] = None,
        benzinga_firm_id: Optional[str] = None,
        benzinga_firm_id_any_of: Optional[str] = None,
        benzinga_firm_id_gt: Optional[str] = None,
        benzinga_firm_id_gte: Optional[str] = None,
        benzinga_firm_id_lt: Optional[str] = None,
        benzinga_firm_id_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[Union[str, Sort]] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaRating], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v1/ratings
        """
        url = "/benzinga/v1/ratings"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_ratings, locals()),
            raw=raw,
            deserializer=BenzingaRating.from_dict,
            options=options,
        )


    def list_benzinga_bulls_bears_say(
        self,
        ticker: Optional[str] = None,
        ticker_any_of: Optional[str] = None,
        ticker_gt: Optional[str] = None,
        ticker_gte: Optional[str] = None,
        ticker_lt: Optional[str] = None,
        ticker_lte: Optional[str] = None,
        benzinga_id: Optional[str] = None,
        benzinga_id_any_of: Optional[str] = None,
        benzinga_id_gt: Optional[str] = None,
        benzinga_id_gte: Optional[str] = None,
        benzinga_id_lt: Optional[str] = None,
        benzinga_id_lte: Optional[str] = None,
        last_updated: Optional[str] = None,
        last_updated_gt: Optional[str] = None,
        last_updated_gte: Optional[str] = None,
        last_updated_lt: Optional[str] = None,
        last_updated_lte: Optional[str] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Union[Iterator[BenzingaBullsBearsSay], HTTPResponse]:
        """
        Endpoint: GET /benzinga/v1/bulls-bears-say

        A comprehensive database of analyst bull and bear case summaries for publicly traded companies, providing concise summaries of both bullish and bearish investment arguments to help investors see both sides of the story before making investment decisions.
        """
        url = "/benzinga/v1/bulls-bears-say"
        return self._paginate(
            path=url,
            params=self._get_params(self.list_benzinga_bulls_bears_say, locals()),
            raw=raw,
            deserializer=BenzingaBullsBearsSay.from_dict,
            options=options,
        )
