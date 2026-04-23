from base import BaseTest
from massive.rest.models import (
    TickerSnapshot,
    OptionContractSnapshot,
    SnapshotTickerFullBook,
    Agg,
    MinuteSnapshot,
    LastQuote,
    LastTrade,
    OrderBookQuote,
    UnderlyingAsset,
    LastQuoteOptionContractSnapshot,
    LastTradeOptionContractSnapshot,
    Greeks,
    OptionDetails,
    DayOptionContractSnapshot,
    UniversalSnapshot,
    UniversalSnapshotDetails,
    UniversalSnapshotLastQuote,
    UniversalSnapshotLastTrade,
    UniversalSnapshotUnderlyingAsset,
    UniversalSnapshotSession,
    IndicesSnapshot,
    IndicesSession,
)


class SnapshotsTest(BaseTest):
    def test_list_universal_snapshots(self):
        expected = [
            UniversalSnapshot(
                ticker="O:NCLH221014C00005000",
                implied_volatility=0.3048997097864957,
                type="options",
                market_status="closed",
                name="NCLH $5 Call",
                open_interest=8921,
                break_even_price=171.075,
                details=UniversalSnapshotDetails(
                    contract_type="call",
                    exercise_style="american",
                    expiration_date="2022-10-14",
                    shares_per_contract=100,
                    strike_price=5,
                    underlying_ticker="NCLH",
                ),
                fair_market_value=20.5,
                greeks=Greeks(
                    delta=0.5520187372272933,
                    gamma=0.00706756515659829,
                    theta=-0.018532772783847958,
                    vega=0.7274811132998142,
                ),
                last_quote=UniversalSnapshotLastQuote(
                    ask=21.25,
                    ask_size=110,
                    bid=20.9,
                    bid_size=172,
                    last_updated=1636573458756383500,
                    midpoint=21.075,
                    timeframe="REAL-TIME",
                ),
                last_trade=UniversalSnapshotLastTrade(
                    conditions=[209],
                    exchange=316,
                    price=0.05,
                    sip_timestamp=1675280958783136800,
                    size=2,
                    timeframe="REAL-TIME",
                ),
                session=UniversalSnapshotSession(
                    change=-0.05,
                    change_percent=-1.07,
                    close=6.65,
                    early_trading_change=-0.01,
                    early_trading_change_percent=-0.03,
                    high=7.01,
                    late_trading_change=-0.4,
                    late_trading_change_percent=-0.02,
                    low=5.42,
                    open=6.7,
                    previous_close=6.71,
                    volume=67,
                ),
                underlying_asset=UniversalSnapshotUnderlyingAsset(
                    change_to_break_even=23.123999999999995,
                    last_updated=1636573459862384600,
                    price=147.951,
                    ticker="AAPL",
                    timeframe="REAL-TIME",
                ),
            ),
            UniversalSnapshot(
                fair_market_value=0.05,
                last_quote=UniversalSnapshotLastQuote(
                    ask=21.25,
                    ask_size=110,
                    bid=20.9,
                    bid_size=172,
                    last_updated=1636573458756383500,
                    timeframe="REAL-TIME",
                ),
                last_trade=UniversalSnapshotLastTrade(
                    conditions=[209],
                    exchange=316,
                    id="4064",
                    last_updated=1675280958783136800,
                    price=0.05,
                    size=2,
                    timeframe="REAL-TIME",
                ),
                market_status="closed",
                name="Apple Inc.",
                session=UniversalSnapshotSession(
                    change=-1.05,
                    change_percent=-4.67,
                    close=21.4,
                    early_trading_change=-0.39,
                    early_trading_change_percent=-0.07,
                    high=22.49,
                    late_trading_change=1.2,
                    late_trading_change_percent=3.92,
                    low=21.35,
                    open=22.49,
                    previous_close=22.45,
                    volume=37,
                ),
                ticker="AAPL",
                type="stocks",
            ),
            UniversalSnapshot(
                error="NOT_FOUND", message="Ticker not found.", ticker="TSLAAPL"
            ),
        ]
        snapshots = [s for s in self.c.list_universal_snapshots()]
        self.assertEqual(snapshots, expected)

    def test_get_snapshot_all(self):
        snapshots = self.c.get_snapshot_all("stocks")
        expected = [
            TickerSnapshot(
                day=Agg(
                    open=20.64,
                    high=20.64,
                    low=20.506,
                    close=20.506,
                    volume=37216,
                    vwap=20.616,
                    timestamp=None,
                    transactions=None,
                ),
                fair_market_value=20.5,
                last_quote=LastQuote(
                    ticker=None,
                    trf_timestamp=None,
                    sequence_number=None,
                    sip_timestamp=1605192959994246100,
                    participant_timestamp=None,
                    ask_price=20.6,
                    ask_size=22,
                    ask_exchange=None,
                    conditions=None,
                    indicators=None,
                    bid_price=20.5,
                    bid_size=13,
                    bid_exchange=None,
                    tape=None,
                ),
                last_trade=LastTrade(
                    ticker=None,
                    trf_timestamp=None,
                    sequence_number=None,
                    sip_timestamp=1605192894630916600,
                    participant_timestamp=None,
                    conditions=[14, 41],
                    correction=None,
                    id="71675577320245",
                    price=20.506,
                    trf_id=None,
                    size=2416,
                    exchange=4,
                    tape=None,
                ),
                min=MinuteSnapshot(
                    accumulated_volume=37216,
                    open=20.506,
                    high=20.506,
                    low=20.506,
                    close=20.506,
                    volume=5000,
                    vwap=20.5105,
                    timestamp=1684428600000,
                    transactions=5,
                ),
                prev_day=Agg(
                    open=20.79,
                    high=21,
                    low=20.5,
                    close=20.63,
                    volume=292738,
                    vwap=20.6939,
                    timestamp=None,
                    transactions=None,
                ),
                ticker="BCAT",
                todays_change=-0.124,
                todays_change_percent=-0.601,
                updated=1605192894630916600,
            )
        ]
        self.assertEqual(snapshots, expected)

    def test_get_snapshot_ticker(self):
        snapshots = self.c.get_snapshot_ticker("stocks", "AAPL")
        expected = TickerSnapshot(
            day=Agg(
                open=161.84,
                high=166.2,
                low=159.8,
                close=160.315,
                volume=68840127,
                vwap=162.7124,
                timestamp=None,
                transactions=None,
            ),
            fair_market_value=160.315,
            last_quote=LastQuote(
                ticker=None,
                trf_timestamp=None,
                sequence_number=None,
                sip_timestamp=1651251948407646487,
                participant_timestamp=None,
                ask_price=159.99,
                ask_size=5,
                ask_exchange=None,
                conditions=None,
                indicators=None,
                bid_price=159.98,
                bid_size=3,
                bid_exchange=None,
                tape=None,
            ),
            last_trade=LastTrade(
                ticker=None,
                trf_timestamp=None,
                sequence_number=None,
                sip_timestamp=1651251948294080343,
                participant_timestamp=None,
                conditions=None,
                correction=None,
                id="121351",
                price=159.99,
                trf_id=None,
                size=200,
                exchange=12,
                tape=None,
            ),
            min=MinuteSnapshot(
                accumulated_volume=68834255,
                open=160.71,
                high=160.71,
                low=160.3,
                close=160.3,
                volume=197226,
                vwap=160.5259,
                timestamp=1684428600000,
                transactions=5,
            ),
            prev_day=Agg(
                open=159.25,
                high=164.515,
                low=158.93,
                close=163.64,
                volume=130149192,
                vwap=161.8622,
                timestamp=None,
                transactions=None,
            ),
            ticker="AAPL",
            todays_change=-3.65,
            todays_change_percent=-2.231,
            updated=1651251948294080343,
        )
        self.assertEqual(snapshots, expected)

    def test_get_snapshot_option(self):
        snapshots = self.c.get_snapshot_option("AAPL", "O:AAPL230616C00150000")
        expected = OptionContractSnapshot(
            break_even_price=179.075,
            day=DayOptionContractSnapshot(
                change=-2.3999999999999986,
                change_percent=-7.643312101910824,
                close=29,
                high=32.25,
                last_updated=1651204800000000000,
                low=29,
                open=29.99,
                previous_close=31.4,
                volume=8,
                vwap=30.7738,
            ),
            details=OptionDetails(
                contract_type="call",
                exercise_style="american",
                expiration_date="2023-06-16",
                shares_per_contract=100,
                strike_price=150,
                ticker="O:AAPL230616C00150000",
            ),
            fair_market_value=29.2,
            greeks=Greeks(
                delta=0.6436614934293701,
                gamma=0.0061735291012820675,
                theta=-0.028227189324641973,
                vega=0.6381159723175714,
            ),
            implied_volatility=0.3570277203465058,
            last_quote=LastQuoteOptionContractSnapshot(
                ask=29.25,
                ask_size=209,
                bid=28.9,
                bid_size=294,
                last_updated=1651254260800059648,
                midpoint=29.075,
                timeframe="REAL-TIME",
            ),
            last_trade=LastTradeOptionContractSnapshot(
                price=29.25,
                sip_timestamp=1678718527714665700,
                size=1,
                conditions=[209],
                exchange=309,
                timeframe="REAL-TIME",
            ),
            open_interest=8133,
            underlying_asset=UnderlyingAsset(
                change_to_break_even=19.11439999999999,
                last_updated=1651254263172073152,
                price=159.9606,
                ticker="AAPL",
                timeframe="REAL-TIME",
            ),
        )
        self.assertEqual(snapshots, expected)

    def test_list_snapshot_options_chain(self):
        snapshots = [s for s in self.c.list_snapshot_options_chain("AAPL")]
        expected = [
            OptionContractSnapshot(
                break_even_price=179.075,
                day=DayOptionContractSnapshot(
                    change=-2.3999999999999986,
                    change_percent=-7.643312101910824,
                    close=29,
                    high=32.25,
                    last_updated=1651204800000000000,
                    low=29,
                    open=29.99,
                    previous_close=31.4,
                    volume=8,
                    vwap=30.7738,
                ),
                details=OptionDetails(
                    contract_type="call",
                    exercise_style="american",
                    expiration_date="2023-06-16",
                    shares_per_contract=100,
                    strike_price=150,
                    ticker="O:AAPL230616C00150000",
                ),
                fair_market_value=20.5,
                greeks=Greeks(
                    delta=0.6436614934293701,
                    gamma=0.0061735291012820675,
                    theta=-0.028227189324641973,
                    vega=0.6381159723175714,
                ),
                implied_volatility=0.3570277203465058,
                last_quote=LastQuoteOptionContractSnapshot(
                    ask=29.25,
                    ask_size=209,
                    bid=28.9,
                    bid_size=294,
                    last_updated=1651254260800059648,
                    midpoint=29.075,
                    timeframe="REAL-TIME",
                ),
                last_trade=LastTradeOptionContractSnapshot(
                    price=29.25,
                    sip_timestamp=1678718527714665700,
                    size=1,
                    conditions=[209],
                    exchange=309,
                    timeframe="REAL-TIME",
                ),
                open_interest=8133,
                underlying_asset=UnderlyingAsset(
                    change_to_break_even=19.11439999999999,
                    last_updated=1651254263172073152,
                    price=159.9606,
                    ticker="AAPL",
                    timeframe="REAL-TIME",
                ),
            )
        ]
        self.assertEqual(snapshots, expected)

    def test_get_snapshot_crypto_book(self):
        snapshots = self.c.get_snapshot_crypto_book("X:BTCUSD")
        expected = SnapshotTickerFullBook(
            ticker="X:BTCUSD",
            bids=[
                OrderBookQuote(price=16303.17, exchange_shares={"1": 2}),
                OrderBookQuote(
                    price=16302.94, exchange_shares={"1": 0.02859424, "6": 0.023455}
                ),
            ],
            asks=[
                OrderBookQuote(price=11454, exchange_shares={"2": 1}),
                OrderBookQuote(price=11455, exchange_shares={"2": 1}),
            ],
            bid_count=694.951789670001,
            ask_count=593.1412981600005,
            spread=-4849.17,
            updated=1605295074162,
        )
        self.assertEqual(snapshots, expected)

    def test_get_snapshot_indices(self):
        ticker_any_of = ["SPX", "APx", "APy"]
        summary_results = self.c.get_snapshot_indices(ticker_any_of)
        expected = [
            IndicesSnapshot(
                value=3822.39,
                name="S&P 500",
                type="indices",
                ticker="SPX",
                market_status="closed",
                session=IndicesSession(
                    change=-50.01,
                    change_percent=-1.45,
                    close=3822.39,
                    high=3834.41,
                    low=38217.11,
                    open=3827.38,
                    previous_close=3812.19,
                ),
            ),
            IndicesSnapshot(
                ticker="APx",
                message="Ticker not found.",
                error="NOT_FOUND",
            ),
            IndicesSnapshot(
                ticker="APy",
                error="NOT_ENTITLED",
                message="Not entitled to this ticker.",
            ),
        ]
        self.assertEqual(summary_results, expected)
