from typing import Optional, Dict
from ...modelclass import modelclass


@modelclass
class EtfGlobalAnalytics:
    composite_ticker: Optional[str] = None
    effective_date: Optional[str] = None
    processed_date: Optional[str] = None
    quant_composite_behavioral: Optional[float] = None
    quant_composite_fundamental: Optional[float] = None
    quant_composite_global: Optional[float] = None
    quant_composite_quality: Optional[float] = None
    quant_composite_sentiment: Optional[float] = None
    quant_composite_technical: Optional[float] = None
    quant_fundamental_div: Optional[float] = None
    quant_fundamental_pb: Optional[float] = None
    quant_fundamental_pcf: Optional[float] = None
    quant_fundamental_pe: Optional[float] = None
    quant_global_country: Optional[float] = None
    quant_global_sector: Optional[float] = None
    quant_grade: Optional[str] = None
    quant_quality_diversification: Optional[float] = None
    quant_quality_firm: Optional[float] = None
    quant_quality_liquidity: Optional[float] = None
    quant_sentiment_iv: Optional[float] = None
    quant_sentiment_pc: Optional[float] = None
    quant_sentiment_si: Optional[float] = None
    quant_technical_it: Optional[float] = None
    quant_technical_lt: Optional[float] = None
    quant_technical_st: Optional[float] = None
    quant_total_score: Optional[float] = None
    reward_score: Optional[float] = None
    risk_country: Optional[float] = None
    risk_deviation: Optional[float] = None
    risk_efficiency: Optional[float] = None
    risk_liquidity: Optional[float] = None
    risk_structure: Optional[float] = None
    risk_total_score: Optional[float] = None
    risk_volatility: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return EtfGlobalAnalytics(
            composite_ticker=d.get("composite_ticker"),
            effective_date=d.get("effective_date"),
            processed_date=d.get("processed_date"),
            quant_composite_behavioral=d.get("quant_composite_behavioral"),
            quant_composite_fundamental=d.get("quant_composite_fundamental"),
            quant_composite_global=d.get("quant_composite_global"),
            quant_composite_quality=d.get("quant_composite_quality"),
            quant_composite_sentiment=d.get("quant_composite_sentiment"),
            quant_composite_technical=d.get("quant_composite_technical"),
            quant_fundamental_div=d.get("quant_fundamental_div"),
            quant_fundamental_pb=d.get("quant_fundamental_pb"),
            quant_fundamental_pcf=d.get("quant_fundamental_pcf"),
            quant_fundamental_pe=d.get("quant_fundamental_pe"),
            quant_global_country=d.get("quant_global_country"),
            quant_global_sector=d.get("quant_global_sector"),
            quant_grade=d.get("quant_grade"),
            quant_quality_diversification=d.get("quant_quality_diversification"),
            quant_quality_firm=d.get("quant_quality_firm"),
            quant_quality_liquidity=d.get("quant_quality_liquidity"),
            quant_sentiment_iv=d.get("quant_sentiment_iv"),
            quant_sentiment_pc=d.get("quant_sentiment_pc"),
            quant_sentiment_si=d.get("quant_sentiment_si"),
            quant_technical_it=d.get("quant_technical_it"),
            quant_technical_lt=d.get("quant_technical_lt"),
            quant_technical_st=d.get("quant_technical_st"),
            quant_total_score=d.get("quant_total_score"),
            reward_score=d.get("reward_score"),
            risk_country=d.get("risk_country"),
            risk_deviation=d.get("risk_deviation"),
            risk_efficiency=d.get("risk_efficiency"),
            risk_liquidity=d.get("risk_liquidity"),
            risk_structure=d.get("risk_structure"),
            risk_total_score=d.get("risk_total_score"),
            risk_volatility=d.get("risk_volatility"),
        )


@modelclass
class EtfGlobalConstituent:
    asset_class: Optional[str] = None
    composite_ticker: Optional[str] = None
    constituent_name: Optional[str] = None
    constituent_ticker: Optional[str] = None
    country_of_exchange: Optional[str] = None
    currency_traded: Optional[str] = None
    effective_date: Optional[str] = None
    exchange: Optional[str] = None
    figi: Optional[str] = None
    isin: Optional[str] = None
    market_value: Optional[float] = None
    processed_date: Optional[str] = None
    security_type: Optional[str] = None
    sedol: Optional[str] = None
    shares_held: Optional[float] = None
    us_code: Optional[str] = None
    weight: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return EtfGlobalConstituent(
            asset_class=d.get("asset_class"),
            composite_ticker=d.get("composite_ticker"),
            constituent_name=d.get("constituent_name"),
            constituent_ticker=d.get("constituent_ticker"),
            country_of_exchange=d.get("country_of_exchange"),
            currency_traded=d.get("currency_traded"),
            effective_date=d.get("effective_date"),
            exchange=d.get("exchange"),
            figi=d.get("figi"),
            isin=d.get("isin"),
            market_value=d.get("market_value"),
            processed_date=d.get("processed_date"),
            security_type=d.get("security_type"),
            sedol=d.get("sedol"),
            shares_held=d.get("shares_held"),
            us_code=d.get("us_code"),
            weight=d.get("weight"),
        )


@modelclass
class EtfGlobalFundFlow:
    composite_ticker: Optional[str] = None
    effective_date: Optional[str] = None
    fund_flow: Optional[float] = None
    nav: Optional[float] = None
    processed_date: Optional[str] = None
    shares_outstanding: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return EtfGlobalFundFlow(
            composite_ticker=d.get("composite_ticker"),
            effective_date=d.get("effective_date"),
            fund_flow=d.get("fund_flow"),
            nav=d.get("nav"),
            processed_date=d.get("processed_date"),
            shares_outstanding=d.get("shares_outstanding"),
        )


@modelclass
class EtfGlobalProfile:
    administrator: Optional[str] = None
    advisor: Optional[str] = None
    asset_class: Optional[str] = None
    aum: Optional[float] = None
    avg_daily_trading_volume: Optional[float] = None
    bid_ask_spread: Optional[float] = None
    call_volume: Optional[float] = None
    category: Optional[str] = None
    composite_ticker: Optional[str] = None
    coupon_exposure: Optional[Dict[str, float]] = None
    creation_fee: Optional[float] = None
    creation_unit_size: Optional[float] = None
    currency_exposure: Optional[Dict[str, float]] = None
    custodian: Optional[str] = None
    description: Optional[str] = None
    development_class: Optional[str] = None
    discount_premium: Optional[float] = None
    distribution_frequency: Optional[str] = None
    distributor: Optional[str] = None
    effective_date: Optional[str] = None
    fee_waivers: Optional[float] = None
    fiscal_year_end: Optional[str] = None
    focus: Optional[str] = None
    futures_commission_merchant: Optional[str] = None
    geographic_exposure: Optional[Dict[str, float]] = None
    inception_date: Optional[str] = None
    industry_exposure: Optional[Dict[str, float]] = None
    industry_group_exposure: Optional[Dict[str, float]] = None
    issuer: Optional[str] = None
    lead_market_maker: Optional[str] = None
    leverage_style: Optional[str] = None
    levered_amount: Optional[float] = None
    listing_exchange: Optional[str] = None
    management_classification: Optional[str] = None
    management_fee: Optional[float] = None
    maturity_exposure: Optional[Dict[str, float]] = None
    net_expenses: Optional[float] = None
    num_holdings: Optional[float] = None
    options_available: Optional[int] = None
    options_volume: Optional[float] = None
    other_expenses: Optional[float] = None
    portfolio_manager: Optional[str] = None
    primary_benchmark: Optional[str] = None
    processed_date: Optional[str] = None
    product_type: Optional[str] = None
    put_call_ratio: Optional[float] = None
    put_volume: Optional[float] = None
    region: Optional[str] = None
    sector_exposure: Optional[Dict[str, float]] = None
    short_interest: Optional[float] = None
    subadvisor: Optional[str] = None
    subindustry_exposure: Optional[Dict[str, float]] = None
    tax_classification: Optional[str] = None
    total_expenses: Optional[float] = None
    transfer_agent: Optional[str] = None
    trustee: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return EtfGlobalProfile(
            administrator=d.get("administrator"),
            advisor=d.get("advisor"),
            asset_class=d.get("asset_class"),
            aum=d.get("aum"),
            avg_daily_trading_volume=d.get("avg_daily_trading_volume"),
            bid_ask_spread=d.get("bid_ask_spread"),
            call_volume=d.get("call_volume"),
            category=d.get("category"),
            composite_ticker=d.get("composite_ticker"),
            coupon_exposure=d.get("coupon_exposure"),
            creation_fee=d.get("creation_fee"),
            creation_unit_size=d.get("creation_unit_size"),
            currency_exposure=d.get("currency_exposure"),
            custodian=d.get("custodian"),
            description=d.get("description"),
            development_class=d.get("development_class"),
            discount_premium=d.get("discount_premium"),
            distribution_frequency=d.get("distribution_frequency"),
            distributor=d.get("distributor"),
            effective_date=d.get("effective_date"),
            fee_waivers=d.get("fee_waivers"),
            fiscal_year_end=d.get("fiscal_year_end"),
            focus=d.get("focus"),
            futures_commission_merchant=d.get("futures_commission_merchant"),
            geographic_exposure=d.get("geographic_exposure"),
            inception_date=d.get("inception_date"),
            industry_exposure=d.get("industry_exposure"),
            industry_group_exposure=d.get("industry_group_exposure"),
            issuer=d.get("issuer"),
            lead_market_maker=d.get("lead_market_maker"),
            leverage_style=d.get("leverage_style"),
            levered_amount=d.get("levered_amount"),
            listing_exchange=d.get("listing_exchange"),
            management_classification=d.get("management_classification"),
            management_fee=d.get("management_fee"),
            maturity_exposure=d.get("maturity_exposure"),
            net_expenses=d.get("net_expenses"),
            num_holdings=d.get("num_holdings"),
            options_available=d.get("options_available"),
            options_volume=d.get("options_volume"),
            other_expenses=d.get("other_expenses"),
            portfolio_manager=d.get("portfolio_manager"),
            primary_benchmark=d.get("primary_benchmark"),
            processed_date=d.get("processed_date"),
            product_type=d.get("product_type"),
            put_call_ratio=d.get("put_call_ratio"),
            put_volume=d.get("put_volume"),
            region=d.get("region"),
            sector_exposure=d.get("sector_exposure"),
            short_interest=d.get("short_interest"),
            subadvisor=d.get("subadvisor"),
            subindustry_exposure=d.get("subindustry_exposure"),
            tax_classification=d.get("tax_classification"),
            total_expenses=d.get("total_expenses"),
            transfer_agent=d.get("transfer_agent"),
            trustee=d.get("trustee"),
        )


@modelclass
class EtfGlobalTaxonomy:
    asset_class: Optional[str] = None
    category: Optional[str] = None
    composite_ticker: Optional[str] = None
    country: Optional[str] = None
    credit_quality_rating: Optional[str] = None
    description: Optional[str] = None
    development_class: Optional[str] = None
    duration: Optional[str] = None
    effective_date: Optional[str] = None
    esg: Optional[str] = None
    exposure_mechanism: Optional[str] = None
    factor: Optional[str] = None
    focus: Optional[str] = None
    hedge_reset: Optional[str] = None
    holdings_disclosure_frequency: Optional[str] = None
    inception_date: Optional[str] = None
    isin: Optional[str] = None
    issuer: Optional[str] = None
    leverage_reset: Optional[str] = None
    leverage_style: Optional[str] = None
    levered_amount: Optional[float] = None
    management_classification: Optional[str] = None
    management_style: Optional[str] = None
    maturity: Optional[str] = None
    objective: Optional[str] = None
    primary_benchmark: Optional[str] = None
    processed_date: Optional[str] = None
    product_type: Optional[str] = None
    rebalance_frequency: Optional[str] = None
    reconstitution_frequency: Optional[str] = None
    region: Optional[str] = None
    secondary_objective: Optional[str] = None
    selection_methodology: Optional[str] = None
    selection_universe: Optional[str] = None
    strategic_focus: Optional[str] = None
    targeted_focus: Optional[str] = None
    tax_classification: Optional[str] = None
    us_code: Optional[str] = None
    weighting_methodology: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return EtfGlobalTaxonomy(
            asset_class=d.get("asset_class"),
            category=d.get("category"),
            composite_ticker=d.get("composite_ticker"),
            country=d.get("country"),
            credit_quality_rating=d.get("credit_quality_rating"),
            description=d.get("description"),
            development_class=d.get("development_class"),
            duration=d.get("duration"),
            effective_date=d.get("effective_date"),
            esg=d.get("esg"),
            exposure_mechanism=d.get("exposure_mechanism"),
            factor=d.get("factor"),
            focus=d.get("focus"),
            hedge_reset=d.get("hedge_reset"),
            holdings_disclosure_frequency=d.get("holdings_disclosure_frequency"),
            inception_date=d.get("inception_date"),
            isin=d.get("isin"),
            issuer=d.get("issuer"),
            leverage_reset=d.get("leverage_reset"),
            leverage_style=d.get("leverage_style"),
            levered_amount=d.get("levered_amount"),
            management_classification=d.get("management_classification"),
            management_style=d.get("management_style"),
            maturity=d.get("maturity"),
            objective=d.get("objective"),
            primary_benchmark=d.get("primary_benchmark"),
            processed_date=d.get("processed_date"),
            product_type=d.get("product_type"),
            rebalance_frequency=d.get("rebalance_frequency"),
            reconstitution_frequency=d.get("reconstitution_frequency"),
            region=d.get("region"),
            secondary_objective=d.get("secondary_objective"),
            selection_methodology=d.get("selection_methodology"),
            selection_universe=d.get("selection_universe"),
            strategic_focus=d.get("strategic_focus"),
            targeted_focus=d.get("targeted_focus"),
            tax_classification=d.get("tax_classification"),
            us_code=d.get("us_code"),
            weighting_methodology=d.get("weighting_methodology"),
        )
