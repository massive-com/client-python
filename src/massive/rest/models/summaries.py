from typing import Optional
from ...modelclass import modelclass
from .tickers import Branding


@modelclass
class Session:
    "Contains Session data for the summaries endpoint."
    change: Optional[float] = None
    change_percent: Optional[float] = None
    early_trading_change: Optional[float] = None
    early_trading_change_percent: Optional[float] = None
    late_trading_change: Optional[float] = None
    late_trading_change_percent: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    previous_close: Optional[float] = None
    volume: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return Session(**d)


@modelclass
class Options:
    "Contains options data for the summaries endpoint"
    contract_type: Optional[str] = None
    exercise_style: Optional[str] = None
    expiration_date: Optional[str] = None
    shares_per_contract: Optional[float] = None
    strike_price: Optional[float] = None
    underlying_ticker: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return Options(**d)


@modelclass
class SummaryResult:
    "Contains summary result data for a list of tickers"
    price: Optional[float] = None
    name: Optional[str] = None
    ticker: Optional[str] = None
    branding: Optional[Branding] = None
    market_status: Optional[str] = None
    last_updated: Optional[int] = None
    type: Optional[str] = None
    session: Optional[Session] = None
    options: Optional[Options] = None
    error: Optional[str] = None
    message: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return SummaryResult(
            price=d.get("price", None),
            name=d.get("name", None),
            ticker=d.get("ticker", None),
            branding=None if "branding" not in d else Branding.from_dict(d["branding"]),
            market_status=d.get("market_status", None),
            last_updated=d.get("last_updated", None),
            type=d.get("type", None),
            session=None if "session" not in d else Session.from_dict(d["session"]),
            options=None if "options" not in d else Options.from_dict(d["options"]),
            error=d.get("error", None),
            message=d.get("message", None),
        )
