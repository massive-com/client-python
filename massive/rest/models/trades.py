from typing import Optional, List
from ...modelclass import modelclass


@modelclass
class Trade:
    "Trade contains trade data for a specified ticker symbol."

    conditions: Optional[List[int]] = None
    correction: Optional[int] = None
    exchange: Optional[int] = None
    id: Optional[str] = None
    participant_timestamp: Optional[int] = None
    price: Optional[float] = None
    sequence_number: Optional[int] = None
    sip_timestamp: Optional[int] = None
    size: Optional[float] = None
    tape: Optional[int] = None
    trf_id: Optional[int] = None
    trf_timestamp: Optional[int] = None
    decimal_size: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return Trade(**d)


@modelclass
class LastTrade:
    """Contains data for the most recent trade for a given ticker symbol."""

    ticker: Optional[str] = None
    trf_timestamp: Optional[int] = None
    sequence_number: Optional[float] = None
    sip_timestamp: Optional[int] = None
    participant_timestamp: Optional[int] = None
    conditions: Optional[List[int]] = None
    correction: Optional[int] = None
    id: Optional[str] = None
    price: Optional[float] = None
    trf_id: Optional[int] = None
    size: Optional[float] = None
    exchange: Optional[int] = None
    tape: Optional[int] = None
    fractional_size: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return LastTrade(
            ticker=d.get("T"),
            trf_timestamp=d.get("f"),
            sequence_number=d.get("q"),
            sip_timestamp=d.get("t"),
            participant_timestamp=d.get("y"),
            conditions=d.get("c"),
            correction=d.get("e"),
            id=d.get("i"),
            price=d.get("p"),
            trf_id=d.get("r"),
            size=d.get("s"),
            exchange=d.get("x"),
            tape=d.get("z"),
            fractional_size=d.get("ds"),
        )


@modelclass
class CryptoTrade:
    "Contains data for a crypto trade."

    conditions: Optional[List[int]] = None
    exchange: Optional[int] = None
    price: Optional[float] = None
    size: Optional[float] = None
    timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return CryptoTrade(**d)


@modelclass
class OptionsUnusualTrade:
    "An unusual trade for a US options contract."

    ticker: Optional[str] = None
    underlying_ticker: Optional[str] = None
    root: Optional[str] = None
    sip_timestamp: Optional[int] = None
    sequence_number: Optional[int] = None
    price: Optional[float] = None
    size: Optional[int] = None
    exchange: Optional[int] = None
    conditions: Optional[List[int]] = None
    flags: Optional[List[str]] = None

    @staticmethod
    def from_dict(d):
        return OptionsUnusualTrade(
            ticker=d.get("ticker"),
            underlying_ticker=d.get("underlying_ticker"),
            root=d.get("root"),
            sip_timestamp=d.get("sip_timestamp"),
            sequence_number=d.get("sequence_number"),
            price=d.get("price"),
            size=d.get("size"),
            exchange=d.get("exchange"),
            conditions=d.get("conditions"),
            flags=d.get("flags"),
        )
