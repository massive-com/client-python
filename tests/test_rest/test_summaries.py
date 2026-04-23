from massive.rest.models import SummaryResult, Branding, Session, Options
from base import BaseTest


class SummariesTest(BaseTest):
    def test_get_summaries_list(self):
        ticker_any_of = ["NCLH", "O:NCLH221014C00005000", "C:EURUSD", "X:BTCUSD", "APx"]
        summary_results = self.c.get_summaries(ticker_any_of)
        expected = [
            SummaryResult(
                price=22.3,
                name="Norwegian Cruise Lines",
                ticker="NCLH",
                branding=Branding(
                    icon_url="https://api.massive.com/icon.png",
                    logo_url="https://api.massive.com/logo.svg",
                ),
                market_status="closed",
                type="stocks",
                session=Session(
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
            ),
            SummaryResult(
                price=6.6,
                name="NCLH $5 Call",
                ticker="O:NCLH221014C00005000",
                market_status="closed",
                type="options",
                session=Session(
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
                options=Options(
                    contract_type="call",
                    exercise_style="american",
                    expiration_date="2022-10-14",
                    shares_per_contract=100,
                    strike_price=5,
                    underlying_ticker="NCLH",
                ),
            ),
            SummaryResult(
                price=0.97989,
                name="Euro - United States Dollar",
                ticker="C:EURUSD",
                market_status="open",
                type="fx",
                session=Session(
                    change=-0.0001,
                    change_percent=-0.67,
                    close=0.97989,
                    high=0.98999,
                    low=0.96689,
                    open=0.97889,
                    previous_close=0.98001,
                ),
            ),
            SummaryResult(
                price=32154.68,
                name="Bitcoin - United States Dollar",
                ticker="X:BTCUSD",
                branding=Branding(
                    icon_url="https://api.massive.com/icon.png",
                    logo_url="https://api.massive.com/logo.svg",
                ),
                market_status="open",
                type="crypto",
                session=Session(
                    change=-201.23,
                    change_percent=-0.77,
                    close=32154.68,
                    high=33124.28,
                    low=28182.88,
                    open=31129.32,
                    previous_close=33362.18,
                ),
            ),
            SummaryResult(
                ticker="APx",
                error="NOT_FOUND",
                message="Ticker not found.",
            ),
        ]
        self.assertEqual(summary_results, expected)
