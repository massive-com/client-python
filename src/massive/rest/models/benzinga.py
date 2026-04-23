from typing import Optional, List
from ...modelclass import modelclass


@modelclass
class BenzingaAnalystInsight:
    benzinga_firm_id: Optional[str] = None
    benzinga_id: Optional[str] = None
    benzinga_rating_id: Optional[str] = None
    company_name: Optional[str] = None
    date: Optional[str] = None
    firm: Optional[str] = None
    insight: Optional[str] = None
    last_updated: Optional[str] = None
    price_target: Optional[float] = None
    rating: Optional[str] = None
    rating_action: Optional[str] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return BenzingaAnalystInsight(
            benzinga_firm_id=d.get("benzinga_firm_id"),
            benzinga_id=d.get("benzinga_id"),
            benzinga_rating_id=d.get("benzinga_rating_id"),
            company_name=d.get("company_name"),
            date=d.get("date"),
            firm=d.get("firm"),
            insight=d.get("insight"),
            last_updated=d.get("last_updated"),
            price_target=d.get("price_target"),
            rating=d.get("rating"),
            rating_action=d.get("rating_action"),
            ticker=d.get("ticker"),
        )


@modelclass
class BenzingaAnalyst:
    benzinga_firm_id: Optional[str] = None
    benzinga_id: Optional[str] = None
    firm_name: Optional[str] = None
    full_name: Optional[str] = None
    last_updated: Optional[str] = None
    overall_avg_return: Optional[float] = None
    overall_avg_return_percentile: Optional[float] = None
    overall_success_rate: Optional[float] = None
    smart_score: Optional[float] = None
    total_ratings: Optional[float] = None
    total_ratings_percentile: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return BenzingaAnalyst(
            benzinga_firm_id=d.get("benzinga_firm_id"),
            benzinga_id=d.get("benzinga_id"),
            firm_name=d.get("firm_name"),
            full_name=d.get("full_name"),
            last_updated=d.get("last_updated"),
            overall_avg_return=d.get("overall_avg_return"),
            overall_avg_return_percentile=d.get("overall_avg_return_percentile"),
            overall_success_rate=d.get("overall_success_rate"),
            smart_score=d.get("smart_score"),
            total_ratings=d.get("total_ratings"),
            total_ratings_percentile=d.get("total_ratings_percentile"),
        )


@modelclass
class BenzingaConsensusRating:
    buy_ratings: Optional[int] = None
    consensus_price_target: Optional[float] = None
    consensus_rating: Optional[str] = None
    consensus_rating_value: Optional[float] = None
    high_price_target: Optional[float] = None
    hold_ratings: Optional[int] = None
    low_price_target: Optional[float] = None
    price_target_contributors: Optional[int] = None
    ratings_contributors: Optional[int] = None
    sell_ratings: Optional[int] = None
    strong_buy_ratings: Optional[int] = None
    strong_sell_ratings: Optional[int] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return BenzingaConsensusRating(
            buy_ratings=d.get("buy_ratings"),
            consensus_price_target=d.get("consensus_price_target"),
            consensus_rating=d.get("consensus_rating"),
            consensus_rating_value=d.get("consensus_rating_value"),
            high_price_target=d.get("high_price_target"),
            hold_ratings=d.get("hold_ratings"),
            low_price_target=d.get("low_price_target"),
            price_target_contributors=d.get("price_target_contributors"),
            ratings_contributors=d.get("ratings_contributors"),
            sell_ratings=d.get("sell_ratings"),
            strong_buy_ratings=d.get("strong_buy_ratings"),
            strong_sell_ratings=d.get("strong_sell_ratings"),
            ticker=d.get("ticker"),
        )


@modelclass
class BenzingaEarning:
    actual_eps: Optional[float] = None
    actual_revenue: Optional[float] = None
    benzinga_id: Optional[str] = None
    company_name: Optional[str] = None
    currency: Optional[str] = None
    date: Optional[str] = None
    date_status: Optional[str] = None
    eps_method: Optional[str] = None
    eps_surprise: Optional[float] = None
    eps_surprise_percent: Optional[float] = None
    estimated_eps: Optional[float] = None
    estimated_revenue: Optional[float] = None
    fiscal_period: Optional[str] = None
    fiscal_year: Optional[int] = None
    importance: Optional[int] = None
    last_updated: Optional[str] = None
    notes: Optional[str] = None
    previous_eps: Optional[float] = None
    previous_revenue: Optional[float] = None
    revenue_method: Optional[str] = None
    revenue_surprise: Optional[float] = None
    revenue_surprise_percent: Optional[float] = None
    ticker: Optional[str] = None
    time: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return BenzingaEarning(
            actual_eps=d.get("actual_eps"),
            actual_revenue=d.get("actual_revenue"),
            benzinga_id=d.get("benzinga_id"),
            company_name=d.get("company_name"),
            currency=d.get("currency"),
            date=d.get("date"),
            date_status=d.get("date_status"),
            eps_method=d.get("eps_method"),
            eps_surprise=d.get("eps_surprise"),
            eps_surprise_percent=d.get("eps_surprise_percent"),
            estimated_eps=d.get("estimated_eps"),
            estimated_revenue=d.get("estimated_revenue"),
            fiscal_period=d.get("fiscal_period"),
            fiscal_year=d.get("fiscal_year"),
            importance=d.get("importance"),
            last_updated=d.get("last_updated"),
            notes=d.get("notes"),
            previous_eps=d.get("previous_eps"),
            previous_revenue=d.get("previous_revenue"),
            revenue_method=d.get("revenue_method"),
            revenue_surprise=d.get("revenue_surprise"),
            revenue_surprise_percent=d.get("revenue_surprise_percent"),
            ticker=d.get("ticker"),
            time=d.get("time"),
        )


@modelclass
class BenzingaFirm:
    benzinga_id: Optional[str] = None
    currency: Optional[str] = None
    last_updated: Optional[str] = None
    name: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return BenzingaFirm(
            benzinga_id=d.get("benzinga_id"),
            currency=d.get("currency"),
            last_updated=d.get("last_updated"),
            name=d.get("name"),
        )


@modelclass
class BenzingaGuidance:
    benzinga_id: Optional[str] = None
    company_name: Optional[str] = None
    currency: Optional[str] = None
    date: Optional[str] = None
    eps_method: Optional[str] = None
    estimated_eps_guidance: Optional[float] = None
    estimated_revenue_guidance: Optional[float] = None
    fiscal_period: Optional[str] = None
    fiscal_year: Optional[int] = None
    importance: Optional[int] = None
    last_updated: Optional[str] = None
    max_eps_guidance: Optional[float] = None
    max_revenue_guidance: Optional[float] = None
    min_eps_guidance: Optional[float] = None
    min_revenue_guidance: Optional[float] = None
    notes: Optional[str] = None
    positioning: Optional[str] = None
    previous_max_eps_guidance: Optional[float] = None
    previous_max_revenue_guidance: Optional[float] = None
    previous_min_eps_guidance: Optional[float] = None
    previous_min_revenue_guidance: Optional[float] = None
    release_type: Optional[str] = None
    revenue_method: Optional[str] = None
    ticker: Optional[str] = None
    time: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return BenzingaGuidance(
            benzinga_id=d.get("benzinga_id"),
            company_name=d.get("company_name"),
            currency=d.get("currency"),
            date=d.get("date"),
            eps_method=d.get("eps_method"),
            estimated_eps_guidance=d.get("estimated_eps_guidance"),
            estimated_revenue_guidance=d.get("estimated_revenue_guidance"),
            fiscal_period=d.get("fiscal_period"),
            fiscal_year=d.get("fiscal_year"),
            importance=d.get("importance"),
            last_updated=d.get("last_updated"),
            max_eps_guidance=d.get("max_eps_guidance"),
            max_revenue_guidance=d.get("max_revenue_guidance"),
            min_eps_guidance=d.get("min_eps_guidance"),
            min_revenue_guidance=d.get("min_revenue_guidance"),
            notes=d.get("notes"),
            positioning=d.get("positioning"),
            previous_max_eps_guidance=d.get("previous_max_eps_guidance"),
            previous_max_revenue_guidance=d.get("previous_max_revenue_guidance"),
            previous_min_eps_guidance=d.get("previous_min_eps_guidance"),
            previous_min_revenue_guidance=d.get("previous_min_revenue_guidance"),
            release_type=d.get("release_type"),
            revenue_method=d.get("revenue_method"),
            ticker=d.get("ticker"),
            time=d.get("time"),
        )


@modelclass
class BenzingaNews:
    author: Optional[str] = None
    benzinga_id: Optional[int] = None
    body: Optional[str] = None
    channels: Optional[List[str]] = None
    images: Optional[List[str]] = None
    last_updated: Optional[str] = None
    published: Optional[str] = None
    tags: Optional[List[str]] = None
    teaser: Optional[str] = None
    tickers: Optional[List[str]] = None
    title: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return BenzingaNews(
            author=d.get("author"),
            benzinga_id=d.get("benzinga_id"),
            body=d.get("body"),
            channels=d.get("channels", []),
            images=d.get("images", []),
            last_updated=d.get("last_updated"),
            published=d.get("published"),
            tags=d.get("tags", []),
            teaser=d.get("teaser"),
            tickers=d.get("tickers", []),
            title=d.get("title"),
            url=d.get("url"),
        )


@modelclass
class BenzingaRating:
    adjusted_price_target: Optional[float] = None
    analyst: Optional[str] = None
    benzinga_analyst_id: Optional[str] = None
    benzinga_calendar_url: Optional[str] = None
    benzinga_firm_id: Optional[str] = None
    benzinga_id: Optional[str] = None
    benzinga_news_url: Optional[str] = None
    company_name: Optional[str] = None
    currency: Optional[str] = None
    date: Optional[str] = None
    firm: Optional[str] = None
    importance: Optional[int] = None
    last_updated: Optional[str] = None
    notes: Optional[str] = None
    previous_adjusted_price_target: Optional[float] = None
    previous_price_target: Optional[float] = None
    previous_rating: Optional[str] = None
    price_percent_change: Optional[float] = None
    price_target: Optional[float] = None
    price_target_action: Optional[str] = None
    rating: Optional[str] = None
    rating_action: Optional[str] = None
    ticker: Optional[str] = None
    time: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return BenzingaRating(
            adjusted_price_target=d.get("adjusted_price_target"),
            analyst=d.get("analyst"),
            benzinga_analyst_id=d.get("benzinga_analyst_id"),
            benzinga_calendar_url=d.get("benzinga_calendar_url"),
            benzinga_firm_id=d.get("benzinga_firm_id"),
            benzinga_id=d.get("benzinga_id"),
            benzinga_news_url=d.get("benzinga_news_url"),
            company_name=d.get("company_name"),
            currency=d.get("currency"),
            date=d.get("date"),
            firm=d.get("firm"),
            importance=d.get("importance"),
            last_updated=d.get("last_updated"),
            notes=d.get("notes"),
            previous_adjusted_price_target=d.get("previous_adjusted_price_target"),
            previous_price_target=d.get("previous_price_target"),
            previous_rating=d.get("previous_rating"),
            price_percent_change=d.get("price_percent_change"),
            price_target=d.get("price_target"),
            price_target_action=d.get("price_target_action"),
            rating=d.get("rating"),
            rating_action=d.get("rating_action"),
            ticker=d.get("ticker"),
            time=d.get("time"),
        )


@modelclass
class BenzingaBullsBearsSay:
    bear_case: Optional[str] = None
    benzinga_id: Optional[str] = None
    bull_case: Optional[str] = None
    last_updated: Optional[str] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return BenzingaBullsBearsSay(
            bear_case=d.get("bear_case"),
            benzinga_id=d.get("benzinga_id"),
            bull_case=d.get("bull_case"),
            last_updated=d.get("last_updated"),
            ticker=d.get("ticker"),
        )
