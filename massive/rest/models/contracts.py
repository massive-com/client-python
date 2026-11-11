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
    previous_open_interest: Optional[int] = None
    open_interest_change: Optional[int] = None
    open_interest_change_calls: Optional[int] = None
    open_interest_change_puts: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return OptionsUnderlyingOpenInterest(
            underlying_ticker=d.get("underlying_ticker"),
            date=d.get("date"),
            open_interest=d.get("open_interest"),
            open_interest_calls=d.get("open_interest_calls"),
            open_interest_puts=d.get("open_interest_puts"),
            previous_open_interest=d.get("previous_open_interest"),
            open_interest_change=d.get("open_interest_change"),
            open_interest_change_calls=d.get("open_interest_change_calls"),
            open_interest_change_puts=d.get("open_interest_change_puts"),
        )
