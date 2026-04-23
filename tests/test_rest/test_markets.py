from massive.rest.models import (
    MarketHoliday,
    MarketStatus,
    MarketCurrencies,
    MarketExchanges,
)
from base import BaseTest


class MarketsTest(BaseTest):
    def test_get_market_holidays(self):
        holidays = self.c.get_market_holidays()
        expected = [
            MarketHoliday(
                close=None,
                date="2022-05-30",
                exchange="NYSE",
                name="Memorial Day",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-05-30",
                exchange="NASDAQ",
                name="Memorial Day",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-06-20",
                exchange="NASDAQ",
                name="Juneteenth",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-06-20",
                exchange="NYSE",
                name="Juneteenth",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-07-04",
                exchange="NYSE",
                name="Independence Day",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-07-04",
                exchange="NASDAQ",
                name="Independence Day",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-09-05",
                exchange="NYSE",
                name="Labor Day",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-09-05",
                exchange="NASDAQ",
                name="Labor Day",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-11-24",
                exchange="NYSE",
                name="Thanksgiving",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-11-24",
                exchange="NASDAQ",
                name="Thanksgiving",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close="2022-11-25T18:00:00.000Z",
                date="2022-11-25",
                exchange="NYSE",
                name="Thanksgiving",
                open="2022-11-25T14:30:00.000Z",
                status="early-close",
            ),
            MarketHoliday(
                close="2022-11-25T18:00:00.000Z",
                date="2022-11-25",
                exchange="NASDAQ",
                name="Thanksgiving",
                open="2022-11-25T14:30:00.000Z",
                status="early-close",
            ),
            MarketHoliday(
                close=None,
                date="2022-12-26",
                exchange="NYSE",
                name="Christmas",
                open=None,
                status="closed",
            ),
            MarketHoliday(
                close=None,
                date="2022-12-26",
                exchange="NASDAQ",
                name="Christmas",
                open=None,
                status="closed",
            ),
        ]
        self.assertEqual(holidays, expected)

    def test_get_market_status(self):
        status = self.c.get_market_status()
        expected = MarketStatus(
            after_hours=True,
            currencies=MarketCurrencies(crypto="open", fx="open"),
            early_hours=False,
            exchanges=MarketExchanges(
                nasdaq="extended-hours", nyse="extended-hours", otc="extended-hours"
            ),
            market="extended-hours",
            server_time="2022-04-28T16:48:08-04:00",
        )
        self.assertEqual(status, expected)
