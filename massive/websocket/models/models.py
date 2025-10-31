from typing import Optional, List, Union, NewType
from .common import EventType
from ...modelclass import modelclass


@modelclass
class EquityAgg:
    """EquityAgg contains aggregate data for either stock tickers, option contracts or index tickers."""

    event_type: Optional[Union[str, EventType]] = None
    symbol: Optional[str] = None
    volume: Optional[float] = None
    accumulated_volume: Optional[float] = None
    official_open_price: Optional[float] = None
    vwap: Optional[float] = None
    open: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    aggregate_vwap: Optional[float] = None
    average_size: Optional[float] = None
    start_timestamp: Optional[int] = None
    end_timestamp: Optional[int] = None
    otc: Optional[bool] = None

    @staticmethod
    def from_dict(d):
        return EquityAgg(
            d.get("ev", None),
            d.get("sym", None),
            d.get("v", None),
            d.get("av", None),
            d.get("op", None),
            d.get("vw", None),
            d.get("o", None),
            d.get("c", None),
            d.get("h", None),
            d.get("l", None),
            d.get("a", None),
            d.get("z", None),
            d.get("s", None),
            d.get("e", None),
            d.get("otc", None),
        )


@modelclass
class CurrencyAgg:
    "CurrencyAgg contains aggregate data for either forex currency pairs or crypto pairs."
    event_type: Optional[Union[str, EventType]] = None
    pair: Optional[str] = None
    open: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[float] = None
    vwap: Optional[float] = None
    start_timestamp: Optional[int] = None
    end_timestamp: Optional[int] = None
    avg_trade_size: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return CurrencyAgg(
            d.get("ev", None),
            d.get("pair", None),
            d.get("o", None),
            d.get("c", None),
            d.get("h", None),
            d.get("l", None),
            d.get("v", None),
            d.get("vw", None),
            d.get("s", None),
            d.get("e", None),
            d.get("z", None),
        )


@modelclass
class EquityTrade:
    "EquityTrade contains trade data for either stock tickers or option contracts."
    event_type: Optional[Union[str, EventType]] = None
    symbol: Optional[str] = None
    exchange: Optional[int] = None
    id: Optional[str] = None
    tape: Optional[int] = None
    price: Optional[float] = None
    size: Optional[int] = None
    conditions: Optional[List[int]] = None
    timestamp: Optional[int] = None
    sequence_number: Optional[int] = None
    trf_id: Optional[int] = None
    trf_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return EquityTrade(
            d.get("ev", None),
            d.get("sym", None),
            d.get("x", None),
            d.get("i", None),
            d.get("z", None),
            d.get("p", None),
            d.get("s", None),
            d.get("c", None),
            d.get("t", None),
            d.get("q", None),
            d.get("trfi", None),
            d.get("trft", None),
        )


@modelclass
class CryptoTrade:
    "CryptoTrade contains trade data for a crypto pair."
    event_type: Optional[Union[str, EventType]] = None
    pair: Optional[str] = None
    exchange: Optional[int] = None
    id: Optional[str] = None
    price: Optional[float] = None
    size: Optional[float] = None
    conditions: Optional[List[int]] = None
    timestamp: Optional[int] = None
    received_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return CryptoTrade(
            d.get("ev", None),
            d.get("pair", None),
            d.get("x", None),
            d.get("i", None),
            d.get("p", None),
            d.get("s", None),
            d.get("c", None),
            d.get("t", None),
            d.get("r", None),
        )


@modelclass
class EquityQuote:
    "EquityQuote contains quote data for either stock tickers or option contracts."
    event_type: Optional[Union[str, EventType]] = None
    symbol: Optional[str] = None
    bid_exchange_id: Optional[int] = None
    bid_price: Optional[float] = None
    bid_size: Optional[int] = None
    ask_exchange_id: Optional[int] = None
    ask_price: Optional[float] = None
    ask_size: Optional[int] = None
    condition: Optional[int] = None
    indicators: Optional[List[int]] = None
    timestamp: Optional[int] = None
    tape: Optional[int] = None
    sequence_number: Optional[int] = None
    trf_id: Optional[int] = None
    trf_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return EquityQuote(
            d.get("ev", None),
            d.get("sym", None),
            d.get("bx", None),
            d.get("bp", None),
            d.get("bs", None),
            d.get("ax", None),
            d.get("ap", None),
            d.get("as", None),
            d.get("c", None),
            d.get("i", None),
            d.get("t", None),
            d.get("z", None),
            d.get("q", None),
            d.get("trfi", None),
            d.get("trft", None),
        )


@modelclass
class ForexQuote:
    "ForexQuote contains quote data for a forex currency pair."
    event_type: Optional[Union[str, EventType]] = None
    pair: Optional[str] = None
    exchange_id: Optional[int] = None
    ask_price: Optional[float] = None
    bid_price: Optional[float] = None
    timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return ForexQuote(
            d.get("ev", None),
            d.get("p", None),
            d.get("x", None),
            d.get("a", None),
            d.get("b", None),
            d.get("t", None),
        )


@modelclass
class CryptoQuote:
    "CryptoQuote contains quote data for a crypto pair."
    event_type: Optional[Union[str, EventType]] = None
    pair: Optional[str] = None
    bid_price: Optional[int] = None
    bid_size: Optional[float] = None
    ask_price: Optional[int] = None
    ask_size: Optional[int] = None
    timestamp: Optional[float] = None
    exchange_id: Optional[int] = None
    received_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return CryptoQuote(
            d.get("ev", None),
            d.get("pair", None),
            d.get("bp", None),
            d.get("bs", None),
            d.get("ap", None),
            d.get("as", None),
            d.get("t", None),
            d.get("x", None),
            d.get("r", None),
        )


@modelclass
class Imbalance:
    "Imbalance contains imbalance event data for a given stock ticker symbol."
    event_type: Optional[Union[str, EventType]] = None
    symbol: Optional[str] = None
    time_stamp: Optional[int] = None
    auction_time: Optional[int] = None
    auction_type: Optional[str] = None
    symbol_sequence: Optional[int] = None
    exchange_id: Optional[int] = None
    imbalance_quantity: Optional[int] = None
    paired_quantity: Optional[int] = None
    book_clearing_price: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return Imbalance(
            d.get("ev", None),
            d.get("T", None),
            d.get("t", None),
            d.get("at", None),
            d.get("a", None),
            d.get("i", None),
            d.get("x", None),
            d.get("o", None),
            d.get("p", None),
            d.get("b", None),
        )


@modelclass
class LimitUpLimitDown:
    "LimitUpLimitDown contains LULD event data for a given stock ticker symbol."
    event_type: Optional[Union[str, EventType]] = None
    symbol: Optional[str] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    indicators: Optional[List[int]] = None
    tape: Optional[int] = None
    timestamp: Optional[int] = None
    sequence_number: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return LimitUpLimitDown(
            d.get("ev", None),
            d.get("T", None),
            d.get("h", None),
            d.get("l", None),
            d.get("i", None),
            d.get("z", None),
            d.get("t", None),
            d.get("q", None),
        )


@modelclass
class Level2Book:
    "Level2Book contains level 2 book data for a given crypto pair."
    event_type: Optional[Union[str, EventType]] = None
    pair: Optional[str] = None
    bid_prices: Optional[float] = None
    ask_prices: Optional[float] = None
    timestamp: Optional[int] = None
    exchange_id: Optional[int] = None
    received_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return Level2Book(
            d.get("ev", None),
            d.get("pair", None),
            d.get("b", None),
            d.get("a", None),
            d.get("t", None),
            d.get("x", None),
            d.get("r", None),
        )


@modelclass
class IndexValue:
    event_type: Optional[Union[str, EventType]] = None
    value: Optional[float] = None
    ticker: Optional[str] = None
    timestamp: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return IndexValue(
            d.get("ev", None),
            d.get("val", None),
            d.get("T", None),
            d.get("t", None),
        )


@modelclass
class LaunchpadValue:
    event_type: Optional[Union[str, EventType]] = None
    value: Optional[float] = None
    symbol: Optional[str] = None
    timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return LaunchpadValue(
            event_type=d.get("ev", None),
            value=d.get("val", None),
            symbol=d.get("sym", None),
            timestamp=d.get("t", None),
        )


@modelclass
class FairMarketValue:
    event_type: Optional[Union[str, EventType]] = None
    fmv: Optional[float] = None
    ticker: Optional[str] = None
    timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return FairMarketValue(
            event_type=d.get("ev", None),
            fmv=d.get("fmv", None),
            ticker=d.get("sym", None),
            timestamp=d.get("t", None),
        )


@modelclass
class FuturesTrade:
    event_type: Optional[str] = None
    symbol: Optional[str] = None
    price: Optional[float] = None
    size: Optional[int] = None
    timestamp: Optional[int] = None
    sequence_number: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return FuturesTrade(
            event_type=d.get("ev"),
            symbol=d.get("sym"),
            price=d.get("p"),
            size=d.get("s"),
            timestamp=d.get("t"),
            sequence_number=d.get("q"),
        )


@modelclass
class FuturesQuote:
    event_type: Optional[str] = None
    symbol: Optional[str] = None
    bid_price: Optional[float] = None
    bid_size: Optional[int] = None
    bid_timestamp: Optional[int] = None
    ask_price: Optional[float] = None
    ask_size: Optional[int] = None
    ask_timestamp: Optional[int] = None
    sip_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return FuturesQuote(
            event_type=d.get("ev"),
            symbol=d.get("sym"),
            bid_price=d.get("bp"),
            bid_size=d.get("bs"),
            bid_timestamp=d.get("bt"),
            ask_price=d.get("ap"),
            ask_size=d.get("as"),
            ask_timestamp=d.get("at"),
            sip_timestamp=d.get("t"),
        )


@modelclass
class FuturesAgg:
    event_type: Optional[str] = None
    symbol: Optional[str] = None
    volume: Optional[int] = None
    total_value: Optional[int] = None
    open: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    transactions: Optional[int] = None
    start_timestamp: Optional[int] = None
    end_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return FuturesAgg(
            event_type=d.get("ev"),
            symbol=d.get("sym"),
            volume=d.get("v"),
            total_value=d.get("dv"),
            open=d.get("o"),
            close=d.get("c"),
            high=d.get("h"),
            low=d.get("l"),
            transactions=d.get("n"),
            start_timestamp=d.get("s"),
            end_timestamp=d.get("e"),
        )


WebSocketMessage = NewType(
    "WebSocketMessage",
    List[
        Union[
            EquityAgg,
            CurrencyAgg,
            EquityTrade,
            CryptoTrade,
            EquityQuote,
            ForexQuote,
            CryptoQuote,
            Imbalance,
            LimitUpLimitDown,
            Level2Book,
            IndexValue,
            LaunchpadValue,
            FairMarketValue,
            FuturesTrade,
            FuturesQuote,
            FuturesAgg,
        ]
    ],
)
