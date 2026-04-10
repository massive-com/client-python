from typing import Optional
from ...modelclass import modelclass


@modelclass
class TreasuryYield:
    """
    Treasury yield data for a specific date.
    """

    date: Optional[str] = None
    yield_1_month: Optional[float] = None
    yield_3_month: Optional[float] = None
    yield_6_month: Optional[float] = None
    yield_1_year: Optional[float] = None
    yield_2_year: Optional[float] = None
    yield_3_year: Optional[float] = None
    yield_5_year: Optional[float] = None
    yield_7_year: Optional[float] = None
    yield_10_year: Optional[float] = None
    yield_20_year: Optional[float] = None
    yield_30_year: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return TreasuryYield(
            date=d.get("date"),
            yield_1_month=d.get("yield_1_month"),
            yield_3_month=d.get("yield_3_month"),
            yield_6_month=d.get("yield_6_month"),
            yield_1_year=d.get("yield_1_year"),
            yield_2_year=d.get("yield_2_year"),
            yield_3_year=d.get("yield_3_year"),
            yield_5_year=d.get("yield_5_year"),
            yield_7_year=d.get("yield_7_year"),
            yield_10_year=d.get("yield_10_year"),
            yield_20_year=d.get("yield_20_year"),
            yield_30_year=d.get("yield_30_year"),
        )


@modelclass
class FedInflation:
    cpi: Optional[float] = None
    cpi_core: Optional[float] = None
    cpi_year_over_year: Optional[float] = None
    date: Optional[str] = None
    pce: Optional[float] = None
    pce_core: Optional[float] = None
    pce_spending: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FedInflation(
            cpi=d.get("cpi"),
            cpi_core=d.get("cpi_core"),
            cpi_year_over_year=d.get("cpi_year_over_year"),
            date=d.get("date"),
            pce=d.get("pce"),
            pce_core=d.get("pce_core"),
            pce_spending=d.get("pce_spending"),
        )


@modelclass
class FedInflationExpectations:
    date: Optional[str] = None
    forward_years_5_to_10: Optional[float] = None
    market_10_year: Optional[float] = None
    market_5_year: Optional[float] = None
    model_10_year: Optional[float] = None
    model_1_year: Optional[float] = None
    model_30_year: Optional[float] = None
    model_5_year: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FedInflationExpectations(
            date=d.get("date"),
            forward_years_5_to_10=d.get("forward_years_5_to_10"),
            market_10_year=d.get("market_10_year"),
            market_5_year=d.get("market_5_year"),
            model_10_year=d.get("model_10_year"),
            model_1_year=d.get("model_1_year"),
            model_30_year=d.get("model_30_year"),
            model_5_year=d.get("model_5_year"),
        )


@modelclass
class FedLaborMarket:
    avg_hourly_earnings: Optional[float] = None
    date: Optional[str] = None
    job_openings: Optional[float] = None
    labor_force_participation_rate: Optional[float] = None
    unemployment_rate: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FedLaborMarket(
            avg_hourly_earnings=d.get("avg_hourly_earnings"),
            date=d.get("date"),
            job_openings=d.get("job_openings"),
            labor_force_participation_rate=d.get("labor_force_participation_rate"),
            unemployment_rate=d.get("unemployment_rate"),
        )


@modelclass
class EUMerchantAggregate:
    """
    Aggregated consumer transactions from European credit card panels.
    Each row represents daily credit card, debit card, or open banking transactions
    (7-day lag) at a tagged merchant or payment processor.
    """

    channel: Optional[str] = None
    consumer_type: Optional[str] = None
    eight_day_rolling_category_accounts: Optional[int] = None
    eight_day_rolling_total_accounts: Optional[int] = None
    mcc_group: Optional[str] = None
    merchant_industry: Optional[str] = None
    merchant_ticker: Optional[str] = None
    name: Optional[str] = None
    parent_name: Optional[str] = None
    published_date: Optional[str] = None
    spend_in_distinct_account_key_count: Optional[int] = None
    spend_in_spend: Optional[float] = None
    spend_in_transaction_count: Optional[int] = None
    spend_out_distinct_account_key_count: Optional[int] = None
    spend_out_spend: Optional[float] = None
    spend_out_transaction_count: Optional[int] = None
    total_accounts: Optional[int] = None
    total_spend: Optional[float] = None
    total_transactions: Optional[int] = None
    transaction_currency: Optional[str] = None
    transaction_date: Optional[str] = None
    twenty_eight_day_rolling_category_accounts: Optional[int] = None
    twenty_eight_day_rolling_total_accounts: Optional[int] = None
    type: Optional[str] = None
    user_country: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return EUMerchantAggregate(
            channel=d.get("channel"),
            consumer_type=d.get("consumer_type"),
            eight_day_rolling_category_accounts=d.get(
                "eight_day_rolling_category_accounts"
            ),
            eight_day_rolling_total_accounts=d.get("eight_day_rolling_total_accounts"),
            mcc_group=d.get("mcc_group"),
            merchant_industry=d.get("merchant_industry"),
            merchant_ticker=d.get("merchant_ticker"),
            name=d.get("name"),
            parent_name=d.get("parent_name"),
            published_date=d.get("published_date"),
            spend_in_distinct_account_key_count=d.get(
                "spend_in_distinct_account_key_count"
            ),
            spend_in_spend=d.get("spend_in_spend"),
            spend_in_transaction_count=d.get("spend_in_transaction_count"),
            spend_out_distinct_account_key_count=d.get(
                "spend_out_distinct_account_key_count"
            ),
            spend_out_spend=d.get("spend_out_spend"),
            spend_out_transaction_count=d.get("spend_out_transaction_count"),
            total_accounts=d.get("total_accounts"),
            total_spend=d.get("total_spend"),
            total_transactions=d.get("total_transactions"),
            transaction_currency=d.get("transaction_currency"),
            transaction_date=d.get("transaction_date"),
            twenty_eight_day_rolling_category_accounts=d.get(
                "twenty_eight_day_rolling_category_accounts"
            ),
            twenty_eight_day_rolling_total_accounts=d.get(
                "twenty_eight_day_rolling_total_accounts"
            ),
            type=d.get("type"),
            user_country=d.get("user_country"),
        )


@modelclass
class EUMerchantHierarchy:
    """
    Reference data mapping merchants to parent companies, tickers, sectors,
    and industries across Fable's European consumer transaction panel.
    """

    active_from: Optional[str] = None
    active_to: Optional[str] = None
    category: Optional[str] = None
    grandparent_name: Optional[str] = None
    grandparent_ticker: Optional[str] = None
    great_grandparent_name: Optional[str] = None
    great_grandparent_ticker: Optional[str] = None
    industry: Optional[str] = None
    industry_group: Optional[str] = None
    listing_status: Optional[str] = None
    lookup_name: Optional[str] = None
    normalized_name: Optional[str] = None
    parent_name: Optional[str] = None
    parent_ticker: Optional[str] = None
    sector: Optional[str] = None
    sub_industry: Optional[str] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return EUMerchantHierarchy(
            active_from=d.get("active_from"),
            active_to=d.get("active_to"),
            category=d.get("category"),
            grandparent_name=d.get("grandparent_name"),
            grandparent_ticker=d.get("grandparent_ticker"),
            great_grandparent_name=d.get("great_grandparent_name"),
            great_grandparent_ticker=d.get("great_grandparent_ticker"),
            industry=d.get("industry"),
            industry_group=d.get("industry_group"),
            listing_status=d.get("listing_status"),
            lookup_name=d.get("lookup_name"),
            normalized_name=d.get("normalized_name"),
            parent_name=d.get("parent_name"),
            parent_ticker=d.get("parent_ticker"),
            sector=d.get("sector"),
            sub_industry=d.get("sub_industry"),
            ticker=d.get("ticker"),
        )
