from typing import Optional, List
from ...modelclass import modelclass


@modelclass
class Underlying:
    "Underlying contains data for an underlying or deliverable associated with an option contract."

    amount: Optional[float] = None
    type: Optional[str] = None
    underlying: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return Underlying(**d)


@modelclass
class OptionsContract:
    "OptionsContract contains data for a specified ticker symbol."

    additional_underlyings: Optional[List[Underlying]] = None
    cfi: Optional[str] = None
    contract_type: Optional[str] = None
    correction: Optional[str] = None
    exercise_style: Optional[str] = None
    expiration_date: Optional[str] = None
    primary_exchange: Optional[str] = None
    shares_per_contract: Optional[float] = None
    strike_price: Optional[float] = None
    ticker: Optional[str] = None
    underlying_ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return OptionsContract(
            additional_underlyings=(
                None
                if "additional_underlyings" not in d
                else [Underlying.from_dict(u) for u in d["additional_underlyings"]]
            ),
            cfi=d.get("cfi", None),
            contract_type=d.get("contract_type", None),
            correction=d.get("correction", None),
            exercise_style=d.get("exercise_style", None),
            expiration_date=d.get("expiration_date", None),
            primary_exchange=d.get("primary_exchange", None),
            shares_per_contract=d.get("shares_per_contract", None),
            strike_price=d.get("strike_price", None),
            size=d.get("size", None),
            ticker=d.get("ticker", None),
            underlying_ticker=d.get("underlying_ticker", None),
        )


@modelclass
class OptionsOpenInterest:
    "Daily open interest for a single options contract."

    ticker: Optional[str] = None
    underlying_ticker: Optional[str] = None
    root: Optional[str] = None
    contract_type: Optional[str] = None
    expiration_date: Optional[str] = None
    strike_price: Optional[float] = None
    date: Optional[str] = None
    open_interest: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return OptionsOpenInterest(
            ticker=d.get("ticker"),
            underlying_ticker=d.get("underlying_ticker"),
            root=d.get("root"),
            contract_type=d.get("contract_type"),
            expiration_date=d.get("expiration_date"),
            strike_price=d.get("strike_price"),
            date=d.get("date"),
            open_interest=d.get("open_interest"),
        )


@modelclass
class OptionsUnderlyingOpenInterest:
    "Daily options open interest rolled up across all contracts for an underlying ticker."

    underlying_ticker: Optional[str] = None
    date: Optional[str] = None
    open_interest: Optional[int] = None
    open_interest_calls: Optional[int] = None
    open_interest_puts: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return OptionsUnderlyingOpenInterest(
            underlying_ticker=d.get("underlying_ticker"),
            date=d.get("date"),
            open_interest=d.get("open_interest"),
            open_interest_calls=d.get("open_interest_calls"),
            open_interest_puts=d.get("open_interest_puts"),
        )


@modelclass
class OptionsAnalytics:
    "Daily end-of-day greeks and implied volatility for a single options contract."

    ticker: Optional[str] = None
    underlying_ticker: Optional[str] = None
    root: Optional[str] = None
    contract_type: Optional[str] = None
    exercise_style: Optional[str] = None
    expiration_date: Optional[str] = None
    strike_price: Optional[float] = None
    date: Optional[str] = None
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    rho: Optional[float] = None
    implied_volatility: Optional[float] = None
    option_price: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    quote_timestamp: Optional[int] = None
    underlying_price: Optional[float] = None
    underlying_timestamp: Optional[int] = None
    risk_free_rate: Optional[float] = None
    dividend_yield: Optional[float] = None
    model: Optional[str] = None
    open_interest: Optional[int] = None
    volume: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return OptionsAnalytics(
            ticker=d.get("ticker"),
            underlying_ticker=d.get("underlying_ticker"),
            root=d.get("root"),
            contract_type=d.get("contract_type"),
            exercise_style=d.get("exercise_style"),
            expiration_date=d.get("expiration_date"),
            strike_price=d.get("strike_price"),
            date=d.get("date"),
            delta=d.get("delta"),
            gamma=d.get("gamma"),
            theta=d.get("theta"),
            vega=d.get("vega"),
            rho=d.get("rho"),
            implied_volatility=d.get("implied_volatility"),
            option_price=d.get("option_price"),
            bid=d.get("bid"),
            ask=d.get("ask"),
            quote_timestamp=d.get("quote_timestamp"),
            underlying_price=d.get("underlying_price"),
            underlying_timestamp=d.get("underlying_timestamp"),
            risk_free_rate=d.get("risk_free_rate"),
            dividend_yield=d.get("dividend_yield"),
            model=d.get("model"),
            open_interest=d.get("open_interest"),
            volume=d.get("volume"),
        )


@modelclass
class OptionsUnderlyingAnalytics:
    "Daily options analytics for an underlying ticker: open interest, put/call ratio, gamma and delta exposure, call and put walls, and gamma flip."

    underlying_ticker: Optional[str] = None
    date: Optional[str] = None
    underlying_price: Optional[float] = None
    open_interest: Optional[int] = None
    open_interest_calls: Optional[int] = None
    open_interest_puts: Optional[int] = None
    put_call_ratio: Optional[float] = None
    open_interest_with_greeks: Optional[int] = None
    excluded_open_interest: Optional[int] = None
    gamma_exposure: Optional[float] = None
    gamma_exposure_calls: Optional[float] = None
    gamma_exposure_puts: Optional[float] = None
    delta_exposure: Optional[float] = None
    call_wall: Optional[float] = None
    put_wall: Optional[float] = None
    gamma_flip: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return OptionsUnderlyingAnalytics(
            underlying_ticker=d.get("underlying_ticker"),
            date=d.get("date"),
            underlying_price=d.get("underlying_price"),
            open_interest=d.get("open_interest"),
            open_interest_calls=d.get("open_interest_calls"),
            open_interest_puts=d.get("open_interest_puts"),
            put_call_ratio=d.get("put_call_ratio"),
            open_interest_with_greeks=d.get("open_interest_with_greeks"),
            excluded_open_interest=d.get("excluded_open_interest"),
            gamma_exposure=d.get("gamma_exposure"),
            gamma_exposure_calls=d.get("gamma_exposure_calls"),
            gamma_exposure_puts=d.get("gamma_exposure_puts"),
            delta_exposure=d.get("delta_exposure"),
            call_wall=d.get("call_wall"),
            put_wall=d.get("put_wall"),
            gamma_flip=d.get("gamma_flip"),
        )


@modelclass
class OptionsExpirationAnalytics:
    "Daily options analytics for an underlying ticker and expiration date: open interest, max pain, and gamma and delta exposure."

    underlying_ticker: Optional[str] = None
    expiration_date: Optional[str] = None
    date: Optional[str] = None
    underlying_price: Optional[float] = None
    open_interest: Optional[int] = None
    open_interest_calls: Optional[int] = None
    open_interest_puts: Optional[int] = None
    open_interest_with_greeks: Optional[int] = None
    excluded_open_interest: Optional[int] = None
    max_pain: Optional[float] = None
    gamma_exposure: Optional[float] = None
    gamma_exposure_calls: Optional[float] = None
    gamma_exposure_puts: Optional[float] = None
    delta_exposure: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return OptionsExpirationAnalytics(
            underlying_ticker=d.get("underlying_ticker"),
            expiration_date=d.get("expiration_date"),
            date=d.get("date"),
            underlying_price=d.get("underlying_price"),
            open_interest=d.get("open_interest"),
            open_interest_calls=d.get("open_interest_calls"),
            open_interest_puts=d.get("open_interest_puts"),
            open_interest_with_greeks=d.get("open_interest_with_greeks"),
            excluded_open_interest=d.get("excluded_open_interest"),
            max_pain=d.get("max_pain"),
            gamma_exposure=d.get("gamma_exposure"),
            gamma_exposure_calls=d.get("gamma_exposure_calls"),
            gamma_exposure_puts=d.get("gamma_exposure_puts"),
            delta_exposure=d.get("delta_exposure"),
        )


@modelclass
class OptionsStrikeAnalytics:
    "Daily options analytics for an underlying ticker and strike price, summed over all expirations: open interest, and gamma and delta exposure."

    underlying_ticker: Optional[str] = None
    strike_price: Optional[float] = None
    date: Optional[str] = None
    underlying_price: Optional[float] = None
    open_interest: Optional[int] = None
    open_interest_calls: Optional[int] = None
    open_interest_puts: Optional[int] = None
    open_interest_with_greeks: Optional[int] = None
    excluded_open_interest: Optional[int] = None
    gamma_exposure: Optional[float] = None
    gamma_exposure_calls: Optional[float] = None
    gamma_exposure_puts: Optional[float] = None
    delta_exposure: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return OptionsStrikeAnalytics(
            underlying_ticker=d.get("underlying_ticker"),
            strike_price=d.get("strike_price"),
            date=d.get("date"),
            underlying_price=d.get("underlying_price"),
            open_interest=d.get("open_interest"),
            open_interest_calls=d.get("open_interest_calls"),
            open_interest_puts=d.get("open_interest_puts"),
            open_interest_with_greeks=d.get("open_interest_with_greeks"),
            excluded_open_interest=d.get("excluded_open_interest"),
            gamma_exposure=d.get("gamma_exposure"),
            gamma_exposure_calls=d.get("gamma_exposure_calls"),
            gamma_exposure_puts=d.get("gamma_exposure_puts"),
            delta_exposure=d.get("delta_exposure"),
        )
