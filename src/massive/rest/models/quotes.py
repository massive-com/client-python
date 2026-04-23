from typing import Optional, List
from ...modelclass import modelclass


@modelclass
class Quote:
    "Quote contains quote data for a specified ticker symbol."
    ask_exchange: Optional[int] = None
    ask_price: Optional[float] = None
    ask_size: Optional[float] = None
    bid_exchange: Optional[int] = None
    bid_price: Optional[float] = None
    bid_size: Optional[float] = None
    conditions: Optional[List[int]] = None
    indicators: Optional[List[int]] = None
    participant_timestamp: Optional[int] = None
    sequence_number: Optional[int] = None
    sip_timestamp: Optional[int] = None
    tape: Optional[int] = None
    trf_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return Quote(**d)


@modelclass
class LastQuote:
    "LastQuote contains data for the most recent NBBO (Quote) tick for a given stock."
    ticker: Optional[str] = None
    trf_timestamp: Optional[int] = None
    sequence_number: Optional[int] = None
    sip_timestamp: Optional[int] = None
    participant_timestamp: Optional[int] = None
    ask_price: Optional[float] = None
    ask_size: Optional[int] = None
    ask_exchange: Optional[int] = None
    conditions: Optional[List[int]] = None
    indicators: Optional[List[int]] = None
    bid_price: Optional[float] = None
    bid_size: Optional[int] = None
    bid_exchange: Optional[int] = None
    tape: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return LastQuote(
            ticker=d.get("T", None),
            trf_timestamp=d.get("f", None),
            sequence_number=d.get("q", None),
            sip_timestamp=d.get("t", None),
            participant_timestamp=d.get("y", None),
            ask_price=d.get("P", None),
            ask_size=d.get("S", None),
            ask_exchange=d.get("X", None),
            conditions=d.get("c", None),
            indicators=d.get("i", None),
            bid_price=d.get("p", None),
            bid_size=d.get("s", None),
            bid_exchange=d.get("x", None),
            tape=d.get("z", None),
        )


@modelclass
class ForexQuote:
    "Contains data for a forex quote."
    ask: Optional[float] = None
    bid: Optional[float] = None
    exchange: Optional[int] = None
    timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return ForexQuote(**d)


@modelclass
class LastForexQuote:
    "ForexLastQuote contains data for the last quote tick for a forex currency pair."
    last: Optional[ForexQuote] = None
    symbol: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return LastForexQuote(
            last=None if "last" not in d else ForexQuote.from_dict(d["last"]),
            symbol=d.get("symbol", None),
        )


@modelclass
class RealTimeCurrencyConversion:
    "RealTimeCurrencyConversion contains data for currency conversions using the latest market conversion rates."
    converted: Optional[float] = None
    from_: Optional[str] = None
    initial_amount: Optional[float] = None
    last: Optional[ForexQuote] = None
    to: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return RealTimeCurrencyConversion(
            converted=d.get("converted", None),
            from_=d.get("from_", None),
            initial_amount=d.get("initialAmount", None),
            last=None if "last" not in d else ForexQuote.from_dict(d["last"]),
            to=d.get("to", None),
        )
