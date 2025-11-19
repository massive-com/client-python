from typing import Optional, List
from ...modelclass import modelclass


@modelclass
class FuturesAgg:
    """
    A single aggregate bar for a futures contract in a given time window.
    Corresponds to /futures/vX/aggs/{ticker}.
    """

    ticker: Optional[str] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[float] = None
    dollar_volume: Optional[float] = None
    transactions: Optional[int] = None
    window_start: Optional[int] = None
    session_end_date: Optional[str] = None
    settlement_price: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FuturesAgg(
            ticker=d.get("ticker"),
            open=d.get("open"),
            high=d.get("high"),
            low=d.get("low"),
            close=d.get("close"),
            volume=d.get("volume"),
            dollar_volume=d.get("dollar_volume"),
            transactions=d.get("transactions"),
            window_start=d.get("window_start"),
            session_end_date=d.get("session_end_date"),
            settlement_price=d.get("settlement_price"),
        )


@modelclass
class FuturesContract:
    """
    Represents a single futures contract (or a 'combo' contract).
    Corresponds to /futures/vX/contracts endpoints.
    """

    ticker: Optional[str] = None
    product_code: Optional[str] = None
    trading_venue: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    as_of: Optional[str] = None
    active: Optional[bool] = None
    first_trade_date: Optional[str] = None
    last_trade_date: Optional[str] = None
    days_to_maturity: Optional[int] = None
    min_order_quantity: Optional[int] = None
    max_order_quantity: Optional[int] = None
    settlement_date: Optional[str] = None
    settlement_tick_size: Optional[float] = None
    spread_tick_size: Optional[float] = None
    trade_tick_size: Optional[float] = None
    maturity: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return FuturesContract(
            ticker=d.get("ticker"),
            product_code=d.get("product_code"),
            trading_venue=d.get("trading_venue"),
            name=d.get("name"),
            type=d.get("type"),
            as_of=d.get("as_of"),
            active=d.get("active"),
            first_trade_date=d.get("first_trade_date"),
            last_trade_date=d.get("last_trade_date"),
            days_to_maturity=d.get("days_to_maturity"),
            min_order_quantity=d.get("min_order_quantity"),
            max_order_quantity=d.get("max_order_quantity"),
            settlement_date=d.get("settlement_date"),
            settlement_tick_size=d.get("settlement_tick_size"),
            spread_tick_size=d.get("spread_tick_size"),
            trade_tick_size=d.get("trade_tick_size"),
            maturity=d.get("maturity"),
        )


@modelclass
class FuturesProduct:
    """
    Represents a single futures product (or product 'combo').
    Corresponds to /futures/vX/products endpoints.
    """

    product_code: Optional[str] = None
    name: Optional[str] = None
    as_of: Optional[str] = None
    trading_venue: Optional[str] = None
    asset_class: Optional[str] = None
    asset_sub_class: Optional[str] = None
    clearing_channel: Optional[str] = None
    sector: Optional[str] = None
    sub_sector: Optional[str] = None
    type: Optional[str] = None
    last_updated: Optional[str] = None
    price_quotation: Optional[str] = None
    settlement_currency_code: Optional[str] = None
    settlement_method: Optional[str] = None
    settlement_type: Optional[str] = None
    trade_currency_code: Optional[str] = None
    unit_of_measure: Optional[str] = None
    unit_of_measure_quantity: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FuturesProduct(
            product_code=d.get("product_code"),
            name=d.get("name"),
            as_of=d.get("as_of"),
            trading_venue=d.get("trading_venue"),
            asset_class=d.get("asset_class"),
            clearing_channel=d.get("clearing_channel"),
            asset_sub_class=d.get("asset_sub_class"),
            sector=d.get("sector"),
            sub_sector=d.get("sub_sector"),
            type=d.get("type"),
            last_updated=d.get("last_updated"),
            price_quotation=d.get("price_quotation"),
            settlement_currency_code=d.get("settlement_currency_code"),
            settlement_method=d.get("settlement_method"),
            settlement_type=d.get("settlement_type"),
            trade_currency_code=d.get("trade_currency_code"),
            unit_of_measure=d.get("unit_of_measure"),
            unit_of_measure_quantity=d.get("unit_of_measure_quantity"),
        )


@modelclass
class FuturesQuote:
    """
    Represents a futures NBBO quote within a given time range.
    Corresponds to /futures/vX/quotes/{ticker}
    """

    ticker: Optional[str] = None
    timestamp: Optional[int] = None
    session_end_date: Optional[str] = None
    ask_price: Optional[float] = None
    ask_size: Optional[float] = None
    ask_timestamp: Optional[int] = None
    bid_price: Optional[float] = None
    bid_size: Optional[float] = None
    bid_timestamp: Optional[int] = None

    @staticmethod
    def from_dict(d):
        return FuturesQuote(
            ticker=d.get("ticker"),
            timestamp=d.get("timestamp"),
            session_end_date=d.get("session_end_date"),
            ask_price=d.get("ask_price"),
            ask_size=d.get("ask_size"),
            ask_timestamp=d.get("ask_timestamp"),
            bid_price=d.get("bid_price"),
            bid_size=d.get("bid_size"),
            bid_timestamp=d.get("bid_timestamp"),
        )


@modelclass
class FuturesTrade:
    """
    Represents a futures trade within a given time range.
    Corresponds to /futures/vX/trades/{ticker}
    """

    ticker: Optional[str] = None
    timestamp: Optional[int] = None
    session_end_date: Optional[str] = None
    price: Optional[float] = None
    size: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FuturesTrade(
            ticker=d.get("ticker"),
            timestamp=d.get("timestamp"),
            session_end_date=d.get("session_end_date"),
            price=d.get("price"),
            size=d.get("size"),
        )


@modelclass
class FuturesScheduleEvent:
    """
    Represents a single market event for a schedule (preopen, open, closed, etc.).
    """

    event: Optional[str] = None
    timestamp: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return FuturesScheduleEvent(
            event=d.get("event"),
            timestamp=d.get("timestamp"),
        )


@modelclass
class FuturesSchedule:
    """
    Represents a single schedule for a given session_end_date, with events.
    Corresponds to /futures/vX/schedules, /futures/vX/schedules/{product_code}
    """

    session_end_date: Optional[str] = None
    product_code: Optional[str] = None
    trading_venue: Optional[str] = None
    product_name: Optional[str] = None
    schedule: Optional[List[FuturesScheduleEvent]] = None

    @staticmethod
    def from_dict(d):
        return FuturesSchedule(
            session_end_date=d.get("session_end_date"),
            product_code=d.get("product_code"),
            trading_venue=d.get("trading_venue"),
            product_name=d.get("product_name"),
            schedule=[
                FuturesScheduleEvent.from_dict(ev) for ev in d.get("schedule", [])
            ],
        )


@modelclass
class FuturesMarketStatus:
    trading_venue: Optional[str] = None
    market_status: Optional[str] = (
        None  # Enum: pre_open, open, close, pause, post_close_pre_open
    )
    product_code: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return FuturesMarketStatus(
            trading_venue=d.get("trading_venue"),
            market_status=d.get("market_status"),
            product_code=d.get("product_code"),
        )


@modelclass
class FuturesSnapshotDetails:
    open_interest: Optional[int] = None
    settlement_date: Optional[int] = None


@modelclass
class FuturesSnapshotMinute:
    close: Optional[float] = None
    high: Optional[float] = None
    last_updated: Optional[int] = None
    low: Optional[float] = None
    open: Optional[float] = None
    timeframe: Optional[str] = None
    volume: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FuturesSnapshotMinute(
            close=d.get("close"),
            high=d.get("high"),
            last_updated=d.get("last_updated"),
            low=d.get("low"),
            open=d.get("open"),
            timeframe=d.get("timeframe"),
            volume=d.get("volume"),
        )


@modelclass
class FuturesSnapshotQuote:
    ask: Optional[float] = None
    ask_size: Optional[int] = None
    ask_timestamp: Optional[int] = None
    bid: Optional[float] = None
    bid_size: Optional[int] = None
    bid_timestamp: Optional[int] = None
    last_updated: Optional[int] = None
    timeframe: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return FuturesSnapshotQuote(
            ask=d.get("ask"),
            ask_size=d.get("ask_size"),
            ask_timestamp=d.get("ask_timestamp"),
            bid=d.get("bid"),
            bid_size=d.get("bid_size"),
            bid_timestamp=d.get("bid_timestamp"),
            last_updated=d.get("last_updated"),
            timeframe=d.get("timeframe"),
        )


@modelclass
class FuturesSnapshotTrade:
    last_updated: Optional[int] = None
    price: Optional[float] = None
    size: Optional[int] = None
    timeframe: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return FuturesSnapshotTrade(
            last_updated=d.get("last_updated"),
            price=d.get("price"),
            size=d.get("size"),
            timeframe=d.get("timeframe"),
        )


@modelclass
class FuturesSnapshotSession:
    change: Optional[float] = None
    change_percent: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    previous_settlement: Optional[float] = None
    settlement_price: Optional[float] = None
    volume: Optional[float] = None

    @staticmethod
    def from_dict(d):
        return FuturesSnapshotSession(
            change=d.get("change"),
            change_percent=d.get("change_percent"),
            close=d.get("close"),
            high=d.get("high"),
            low=d.get("low"),
            open=d.get("open"),
            previous_settlement=d.get("previous_settlement"),
            settlement_price=d.get("settlement_price"),
            volume=d.get("volume"),
        )


@modelclass
class FuturesSnapshot:
    ticker: Optional[str] = None
    product_code: Optional[str] = None
    details: Optional[FuturesSnapshotDetails] = None
    last_minute: Optional[FuturesSnapshotMinute] = None
    last_quote: Optional[FuturesSnapshotQuote] = None
    last_trade: Optional[FuturesSnapshotTrade] = None
    session: Optional[FuturesSnapshotSession] = None

    @staticmethod
    def from_dict(d):
        return FuturesSnapshot(
            ticker=d.get("ticker"),
            product_code=d.get("product_code"),
            details=(
                FuturesSnapshotDetails.from_dict(d.get("details", {}))
                if d.get("details")
                else None
            ),
            last_minute=(
                FuturesSnapshotMinute.from_dict(d.get("last_minute", {}))
                if d.get("last_minute")
                else None
            ),
            last_quote=(
                FuturesSnapshotQuote.from_dict(d.get("last_quote", {}))
                if d.get("last_quote")
                else None
            ),
            last_trade=(
                FuturesSnapshotTrade.from_dict(d.get("last_trade", {}))
                if d.get("last_trade")
                else None
            ),
            session=(
                FuturesSnapshotSession.from_dict(d.get("session", {}))
                if d.get("session")
                else None
            ),
        )


@modelclass
class FuturesExchange:
    """
    Represents a futures exchange or trading venue.
    Corresponds to /futures/vX/exchanges endpoint.
    """

    acronym: Optional[str] = None
    id: Optional[str] = None
    locale: Optional[str] = None
    mic: Optional[str] = None
    name: Optional[str] = None
    operating_mic: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return FuturesExchange(
            acronym=d.get("acronym"),
            id=d.get("id"),
            locale=d.get("locale"),
            mic=d.get("mic"),
            name=d.get("name"),
            operating_mic=d.get("operating_mic"),
            type=d.get("type"),
            url=d.get("url"),
        )
