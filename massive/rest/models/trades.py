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
    "Contains data for the most recent trade for a given ticker symbol."
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
    fractional_shares: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return LastTrade(
            d.get("T", None),
            d.get("f", None),
            d.get("q", None),
            d.get("t", None),
            d.get("y", None),
            d.get("c", None),
            d.get("e", None),
            d.get("i", None),
            d.get("p", None),
            d.get("r", None),
            d.get("s", None),
            d.get("x", None),
            d.get("z", None),
            d.get("ds", None),
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
