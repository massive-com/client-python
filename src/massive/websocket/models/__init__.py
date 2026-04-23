from typing import Dict, Any, List, Type, Protocol, cast
from .common import *
from .models import *
import logging


# Protocol to define classes with from_dict method
class FromDictProtocol(Protocol):
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FromDictProtocol":
        pass


# Define the mapping of market and event type to model class
MARKET_EVENT_MAP: Dict[Market, Dict[str, Type[FromDictProtocol]]] = {
    Market.Stocks: {
        "A": EquityAgg,
        "AM": EquityAgg,
        "T": EquityTrade,
        "Q": EquityQuote,
        "LULD": LimitUpLimitDown,
        "FMV": FairMarketValue,
        "NOI": Imbalance,
        "LV": LaunchpadValue,
    },
    Market.Options: {
        "A": EquityAgg,
        "AM": EquityAgg,
        "T": EquityTrade,
        "Q": EquityQuote,
        "FMV": FairMarketValue,
        "LV": LaunchpadValue,
    },
    Market.Indices: {
        "A": EquityAgg,
        "AM": EquityAgg,
        "V": IndexValue,
    },
    Market.Futures: {
        "A": FuturesAgg,
        "AM": FuturesAgg,
        "T": FuturesTrade,
        "Q": FuturesQuote,
    },
    Market.FuturesCME: {
        "A": FuturesAgg,
        "AM": FuturesAgg,
        "T": FuturesTrade,
        "Q": FuturesQuote,
    },
    Market.FuturesCBOT: {
        "A": FuturesAgg,
        "AM": FuturesAgg,
        "T": FuturesTrade,
        "Q": FuturesQuote,
    },
    Market.FuturesNYMEX: {
        "A": FuturesAgg,
        "AM": FuturesAgg,
        "T": FuturesTrade,
        "Q": FuturesQuote,
    },
    Market.FuturesCOMEX: {
        "A": FuturesAgg,
        "AM": FuturesAgg,
        "T": FuturesTrade,
        "Q": FuturesQuote,
    },
    Market.Crypto: {
        "XA": CurrencyAgg,
        "XAS": CurrencyAgg,
        "XT": CryptoTrade,
        "XQ": CryptoQuote,
        "XL2": Level2Book,
        "FMV": FairMarketValue,
        "AM": EquityAgg,
        "LV": LaunchpadValue,
    },
    Market.Forex: {
        "CA": CurrencyAgg,
        "CAS": CurrencyAgg,
        "C": ForexQuote,
        "FMV": FairMarketValue,
        "AM": EquityAgg,
        "LV": LaunchpadValue,
    },
}


def parse_single(
    data: Dict[str, Any], logger: logging.Logger, market: Market
) -> Optional[WebSocketMessage]:
    event_type = data["ev"]
    # Look up the model class based on market and event type
    model_class: Optional[Type[FromDictProtocol]] = MARKET_EVENT_MAP.get(
        market, {}
    ).get(event_type)
    if model_class:
        parsed = model_class.from_dict(data)
        return cast(
            WebSocketMessage, parsed
        )  # Ensure the return type is WebSocketMessage
    else:
        # Log a warning for unrecognized event types, unless it's a status message
        if event_type != "status":
            logger.warning("Unknown event type '%s' for market %s", event_type, market)
        return None


def parse(
    msg: List[Dict[str, Any]], logger: logging.Logger, market: Market
) -> List[WebSocketMessage]:
    res = []
    for m in msg:
        parsed = parse_single(m, logger, market)
        if parsed is None:
            if m["ev"] != "status":
                logger.warning("could not parse message %s", m)
        else:
            res.append(parsed)
    return res
