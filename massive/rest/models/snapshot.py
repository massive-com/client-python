from typing import Optional, List, Dict
from .aggs import Agg
from .quotes import LastQuote
from .trades import LastTrade
from ...modelclass import modelclass


@modelclass
class MinuteSnapshot:
    """Most recent minute bar."""

    accumulated_volume: Optional[float] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None
    vwap: Optional[float] = None
    otc: Optional[bool] = None
    timestamp: Optional[int] = None
    transactions: Optional[int] = None
    fractional_volume: Optional[str] = None
    fractional_accumulated_volume: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return MinuteSnapshot(
            accumulated_volume=d.get("av"),
            open=d.get("o"),
            high=d.get("h"),
            low=d.get("l"),
            close=d.get("c"),
            volume=d.get("v"),
            vwap=d.get("vw"),
            otc=d.get("otc"),
            timestamp=d.get("t"),
            transactions=d.get("n"),
            fractional_volume=d.get("dv"),
            fractional_accumulated_volume=d.get("dav"),
        )


@modelclass
class IndicesSession:
    "Contains data for the most recent daily bar in an options contract."
    change: Optional[float] = None
    change_percent: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    previous_close: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return IndicesSession(**d)


@modelclass
class IndicesSnapshot:
    value: Optional[float] = None
    name: Optional[str] = None
    type: Optional[str] = None
    ticker: Optional[str] = None
    market_status: Optional[str] = None
    session: Optional[IndicesSession] = None
    error: Optional[str] = None
    message: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return IndicesSnapshot(
            value=d.get("value", None),
            name=d.get("name", None),
            type=d.get("type", None),
            ticker=d.get("ticker", None),
            market_status=d.get("market_status", None),
            session=(
                None if "session" not in d else IndicesSession.from_dict(d["session"])
            ),
            error=d.get("error", None),
            message=d.get("message", None),
        )


@modelclass
class TickerSnapshot:
    "Contains the most up-to-date market data for all traded ticker symbols."
    day: Optional[Agg] = None
    last_quote: Optional[LastQuote] = None
    last_trade: Optional[LastTrade] = None
    min: Optional[MinuteSnapshot] = None
    prev_day: Optional[Agg] = None
    ticker: Optional[str] = None
    todays_change: Optional[float] = None
    todays_change_percent: Optional[float] = None
    updated: Optional[int] = None
    fair_market_value: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return TickerSnapshot(
            day=None if "day" not in d else Agg.from_dict(d["day"]),
            last_quote=(
                None if "lastQuote" not in d else LastQuote.from_dict(d["lastQuote"])
            ),
            last_trade=(
                None if "lastTrade" not in d else LastTrade.from_dict(d["lastTrade"])
            ),
            min=None if "min" not in d else MinuteSnapshot.from_dict(d["min"]),
            prev_day=None if "prevDay" not in d else Agg.from_dict(d["prevDay"]),
            ticker=d.get("ticker", None),
            todays_change=d.get("todaysChange", None),
            todays_change_percent=d.get("todaysChangePerc", None),
            updated=d.get("updated", None),
            fair_market_value=d.get("fmv", None),
        )


@modelclass
class DayOptionContractSnapshot:
    "Contains data for the most recent daily bar in an options contract."
    change: Optional[float] = None
    change_percent: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    last_updated: Optional[int] = None
    low: Optional[float] = None
    open: Optional[float] = None
    previous_close: Optional[float] = None
    volume: Optional[float] = None
    vwap: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return DayOptionContractSnapshot(**d)


@modelclass
class OptionDetails:
    "Contains details for an options contract."
    contract_type: Optional[str] = None
    exercise_style: Optional[str] = None
    expiration_date: Optional[str] = None
    shares_per_contract: Optional[float] = None
    strike_price: Optional[float] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return OptionDetails(**d)


@modelclass
class LastQuoteOptionContractSnapshot:
    "Contains data for the most recent quote in an options contract."
    ask: Optional[float] = None
    ask_size: Optional[float] = None
    bid: Optional[float] = None
    bid_size: Optional[float] = None
    last_updated: Optional[int] = None
    midpoint: Optional[float] = None
    timeframe: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return LastQuoteOptionContractSnapshot(**d)


@modelclass
class LastTradeOptionContractSnapshot:
    "Contains data for the most recent trade for an options contract."
    price: Optional[float] = None
    sip_timestamp: Optional[int] = None
    size: Optional[int] = None
    conditions: Optional[List[int]] = None
    exchange: Optional[int] = None
    timeframe: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return LastTradeOptionContractSnapshot(**d)


@modelclass
class Greeks:
    "Contains data for the greeks in an options contract."
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return Greeks(**d)


@modelclass
class UnderlyingAsset:
    "Contains data for the underlying stock in an options contract."
    change_to_break_even: Optional[float] = None
    last_updated: Optional[int] = None
    price: Optional[float] = None
    value: Optional[float] = None
    ticker: Optional[str] = None
    timeframe: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return UnderlyingAsset(**d)


@modelclass
class OptionContractSnapshot:
    "Contains data for the snapshot of an option contract of a stock equity."
    break_even_price: Optional[float] = None
    day: Optional[DayOptionContractSnapshot] = None
    details: Optional[OptionDetails] = None
    greeks: Optional[Greeks] = None
    implied_volatility: Optional[float] = None
    last_quote: Optional[LastQuoteOptionContractSnapshot] = None
    last_trade: Optional[LastTradeOptionContractSnapshot] = None
    open_interest: Optional[float] = None
    underlying_asset: Optional[UnderlyingAsset] = None
    fair_market_value: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return OptionContractSnapshot(
            break_even_price=d.get("break_even_price", None),
            day=(
                None
                if "day" not in d
                else DayOptionContractSnapshot.from_dict(d["day"])
            ),
            details=(
                None if "details" not in d else OptionDetails.from_dict(d["details"])
            ),
            greeks=None if "greeks" not in d else Greeks.from_dict(d["greeks"]),
            implied_volatility=d.get("implied_volatility", None),
            last_quote=(
                None
                if "last_quote" not in d
                else LastQuoteOptionContractSnapshot.from_dict(d["last_quote"])
            ),
            last_trade=(
                None
                if "last_trade" not in d
                else LastTradeOptionContractSnapshot.from_dict(d["last_trade"])
            ),
            open_interest=d.get("open_interest", None),
            underlying_asset=(
                None
                if "underlying_asset" not in d
                else UnderlyingAsset.from_dict(d["underlying_asset"])
            ),
            fair_market_value=d.get("fmv", None),
        )


@modelclass
class OrderBookQuote:
    "Contains data for a book bid or ask."
    price: Optional[float] = None
    exchange_shares: Optional[Dict[str, float]] = None

    @staticmethod
    def from_dict(d):
        return OrderBookQuote(
            d.get("p", None),
            d.get("x", None),
        )


@modelclass
class SnapshotTickerFullBook:
    "Contains the current level 2 book of a single ticker. This is the combined book from all of the exchanges."
    ticker: Optional[str] = None
    bids: Optional[List[OrderBookQuote]] = None
    asks: Optional[List[OrderBookQuote]] = None
    bid_count: Optional[float] = None
    ask_count: Optional[float] = None
    spread: Optional[float] = None
    updated: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return SnapshotTickerFullBook(
            ticker=d.get("ticker", None),
            bids=(
                None
                if "bids" not in d
                else [OrderBookQuote.from_dict(o) for o in d["bids"]]
            ),
            asks=(
                None
                if "asks" not in d
                else [OrderBookQuote.from_dict(o) for o in d["asks"]]
            ),
            bid_count=d.get("bidCount", None),
            ask_count=d.get("askCount", None),
            spread=d.get("spread", None),
            updated=d.get("updated", None),
        )


@modelclass
class UniversalSnapshotSession:
    """Contains data about the most recent trading session for an asset."""

    price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    early_trading_change: Optional[float] = None
    early_trading_change_percent: Optional[float] = None
    regular_trading_change: Optional[float] = None
    regular_trading_change_percent: Optional[float] = None
    late_trading_change: Optional[float] = None
    late_trading_change_percent: Optional[float] = None
    open: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    previous_close: Optional[float] = None
    volume: Optional[float] = None
    vwap: Optional[float] = None
    last_updated: Optional[int] = None
    fractional_volume: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return UniversalSnapshotSession(
            price=d.get("price"),
            change=d.get("change"),
            change_percent=d.get("change_percent"),
            early_trading_change=d.get("early_trading_change"),
            early_trading_change_percent=d.get("early_trading_change_percent"),
            regular_trading_change=d.get("regular_trading_change"),
            regular_trading_change_percent=d.get("regular_trading_change_percent"),
            late_trading_change=d.get("late_trading_change"),
            late_trading_change_percent=d.get("late_trading_change_percent"),
            open=d.get("open"),
            close=d.get("close"),
            high=d.get("high"),
            low=d.get("low"),
            previous_close=d.get("previous_close"),
            volume=d.get("volume"),
            vwap=d.get("vwap"),
            last_updated=d.get("last_updated"),
            fractional_volume=d.get("decimal_volume"),
        )


@modelclass
class UniversalSnapshotLastQuote:
    """Contains the most recent quote for an asset."""

    ask: Optional[float] = None
    ask_size: Optional[float] = None
    ask_exchange: Optional[int] = None
    bid: Optional[float] = None
    bid_size: Optional[float] = None
    bid_exchange: Optional[int] = None
    midpoint: Optional[float] = None
    exchange: Optional[int] = None
    timeframe: Optional[str] = None
    last_updated: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return UniversalSnapshotLastQuote(
            ask=d.get("ask"),
            ask_size=d.get("ask_size"),
            ask_exchange=d.get("ask_exchange"),
            bid=d.get("bid"),
            bid_size=d.get("bid_size"),
            bid_exchange=d.get("bid_exchange"),
            midpoint=d.get("midpoint"),
            exchange=d.get("exchange"),
            timeframe=d.get("timeframe"),
            last_updated=d.get("last_updated"),
        )


@modelclass
class UniversalSnapshotLastTrade:
    """Contains the most recent trade for an asset."""

    id: Optional[int] = None
    price: Optional[float] = None
    size: Optional[int] = None
    exchange: Optional[int] = None
    conditions: Optional[List[int]] = None
    timeframe: Optional[str] = None
    last_updated: Optional[int] = None
    participant_timestamp: Optional[int] = None
    sip_timestamp: Optional[int] = None
    fractional_size: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return UniversalSnapshotLastTrade(
            id=d.get("id"),
            price=d.get("price"),
            size=d.get("size"),
            exchange=d.get("exchange"),
            conditions=d.get("conditions"),
            timeframe=d.get("timeframe"),
            last_updated=d.get("last_updated"),
            participant_timestamp=d.get("participant_timestamp"),
            sip_timestamp=d.get("sip_timestamp"),
            fractional_size=d.get("decimal_size"),
        )


@modelclass
class UniversalSnapshotLastMinute:
    """Contains the most recent minute-level aggregate for the asset."""

    open: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[float] = None
    vwap: Optional[float] = None
    transactions: Optional[int] = None
    last_updated: Optional[int] = None
    fractional_volume: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return UniversalSnapshotLastMinute(
            open=d.get("open"),
            close=d.get("close"),
            high=d.get("high"),
            low=d.get("low"),
            volume=d.get("volume"),
            vwap=d.get("vwap"),
            transactions=d.get("transactions"),
            last_updated=d.get("last_updated"),
            fractional_volume=d.get("decimal_volume"),
        )


@modelclass
class UniversalSnapshotUnderlyingAsset:
    """Contains data for the underlying stock in an options contract."""

    ticker: Optional[str] = None
    price: Optional[float] = None
    value: Optional[float] = None
    change_to_break_even: Optional[float] = None
    timeframe: Optional[str] = None
    last_updated: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return UniversalSnapshotUnderlyingAsset(
            ticker=d.get("ticker"),
            price=d.get("price"),
            value=d.get("value"),
            change_to_break_even=d.get("change_to_break_even"),
            timeframe=d.get("timeframe"),
            last_updated=d.get("last_updated"),
        )


@modelclass
class UniversalSnapshotDetails:
    """Contains details for an options contract."""

    contract_type: Optional[str] = None
    exercise_style: Optional[str] = None
    expiration_date: Optional[str] = None
    shares_per_contract: Optional[float] = None
    strike_price: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return UniversalSnapshotDetails(
            contract_type=d.get("contract_type"),
            exercise_style=d.get("exercise_style"),
            expiration_date=d.get("expiration_date"),
            shares_per_contract=d.get("shares_per_contract"),
            strike_price=d.get("strike_price"),
        )


@modelclass
class UniversalSnapshot:
    """Contains snapshot data for an asset (stocks, options, indices, fx, crypto)."""

    ticker: Optional[str] = None
    type: Optional[str] = None
    session: Optional[UniversalSnapshotSession] = None
    last_quote: Optional[UniversalSnapshotLastQuote] = None
    last_trade: Optional[UniversalSnapshotLastTrade] = None
    last_minute: Optional[UniversalSnapshotLastMinute] = None
    greeks: Optional[Greeks] = None
    underlying_asset: Optional[UniversalSnapshotUnderlyingAsset] = None
    details: Optional[UniversalSnapshotDetails] = None
    break_even_price: Optional[float] = None
    implied_volatility: Optional[float] = None
    open_interest: Optional[float] = None
    market_status: Optional[str] = None
    name: Optional[str] = None
    fair_market_value: Optional[float] = None
    error: Optional[str] = None
    message: Optional[str] = None
    value: Optional[float] = None
    last_updated: Optional[int] = None
    timeframe: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return UniversalSnapshot(
            ticker=d.get("ticker"),
            type=d.get("type"),
            session=(
                None
                if "session" not in d
                else UniversalSnapshotSession.from_dict(d["session"])
            ),
            last_quote=(
                None
                if "last_quote" not in d
                else UniversalSnapshotLastQuote.from_dict(d["last_quote"])
            ),
            last_trade=(
                None
                if "last_trade" not in d
                else UniversalSnapshotLastTrade.from_dict(d["last_trade"])
            ),
            last_minute=(
                None
                if "last_minute" not in d
                else UniversalSnapshotLastMinute.from_dict(d["last_minute"])
            ),
            greeks=(None if "greeks" not in d else Greeks.from_dict(d["greeks"])),
            underlying_asset=(
                None
                if "underlying_asset" not in d
                else UniversalSnapshotUnderlyingAsset.from_dict(d["underlying_asset"])
            ),
            details=(
                None
                if "details" not in d
                else UniversalSnapshotDetails.from_dict(d["details"])
            ),
            break_even_price=d.get("break_even_price"),
            implied_volatility=d.get("implied_volatility"),
            open_interest=d.get("open_interest"),
            market_status=d.get("market_status"),
            name=d.get("name"),
            fair_market_value=d.get("fmv"),
            error=d.get("error"),
            message=d.get("message"),
            value=d.get("value"),
            last_updated=d.get("last_updated"),
            timeframe=d.get("timeframe"),
        )
