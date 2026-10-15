from massive.rest.models import Dividend, StockDividend
from base import BaseTest


class DividendsTest(BaseTest):
    def test_list_dividends(self):
        dividends = [d for d in self.c.list_dividends()]
        expected = [
            Dividend(
                cash_amount=0.59375,
                declaration_date="2020-09-09",
                dividend_type="CD",
                ex_dividend_date="2025-06-12",
                frequency=4,
                pay_date="2025-06-30",
                record_date="2025-06-15",
                ticker="CSSEN",
            ),
            Dividend(
                cash_amount=0.59375,
                declaration_date="2020-09-09",
                dividend_type="CD",
                ex_dividend_date="2025-03-13",
                frequency=4,
                pay_date="2025-03-31",
                record_date="2025-03-15",
                ticker="CSSEN",
            ),
            Dividend(
                cash_amount=0.59375,
                declaration_date="2020-09-09",
                dividend_type="CD",
                ex_dividend_date="2024-12-12",
                frequency=4,
                pay_date="2024-12-31",
                record_date="2024-12-15",
                ticker="CSSEN",
            ),
            Dividend(
                cash_amount=0.59375,
                declaration_date="2020-09-09",
                dividend_type="CD",
                ex_dividend_date="2024-09-12",
                frequency=4,
                pay_date="2024-09-30",
                record_date="2024-09-15",
                ticker="CSSEN",
            ),
            Dividend(
                cash_amount=0.59375,
                declaration_date="2020-09-09",
                dividend_type="CD",
                ex_dividend_date="2024-06-13",
                frequency=4,
                pay_date="2024-06-30",
                record_date="2024-06-15",
                ticker="CSSEN",
            ),
            Dividend(
                cash_amount=0.59375,
                declaration_date="2020-09-09",
                dividend_type="CD",
                ex_dividend_date="2024-03-14",
                frequency=4,
                pay_date="2024-03-31",
                record_date="2024-03-15",
                ticker="CSSEN",
            ),
            Dividend(
                cash_amount=0.59375,
                declaration_date="2020-09-09",
                dividend_type="CD",
                ex_dividend_date="2023-12-14",
                frequency=4,
                pay_date="2023-12-31",
                record_date="2023-12-15",
                ticker="CSSEN",
            ),
            Dividend(
                cash_amount=0.5,
                declaration_date="2022-02-10",
                dividend_type="CD",
                ex_dividend_date="2023-11-13",
                frequency=4,
                pay_date="2023-11-15",
                record_date="2023-11-14",
                ticker="AIRTP",
            ),
            Dividend(
                cash_amount=0.59375,
                declaration_date="2020-09-09",
                dividend_type="CD",
                ex_dividend_date="2023-09-14",
                frequency=4,
                pay_date="2023-09-30",
                record_date="2023-09-15",
                ticker="CSSEN",
            ),
            Dividend(
                cash_amount=0.5,
                declaration_date="2022-02-10",
                dividend_type="CD",
                ex_dividend_date="2023-08-11",
                frequency=4,
                pay_date="2023-08-15",
                record_date="2023-08-14",
                ticker="AIRTP",
            ),
        ]
        self.assertEqual(dividends, expected)

    def test_list_stocks_dividends_ticker_any_of(self):
        expected = [
            StockDividend(
                cash_amount=0.27,
                currency="USD",
                declaration_date="2026-07-30",
                distribution_type="recurring",
                ex_dividend_date="2026-08-10",
                frequency=4,
                historical_adjustment_factor=0.999138,
                id="E1e778b36bcedb4d1589a970be52c16294ad4bc89c8627d56a3b970f6cf2a6e10",
                pay_date="2026-08-13",
                record_date="2026-08-10",
                split_adjusted_cash_amount=0.27,
                ticker="AAPL",
            ),
            StockDividend(
                cash_amount=0.7075,
                currency="USD",
                declaration_date="2026-09-09",
                distribution_type="recurring",
                ex_dividend_date="2026-10-09",
                frequency=4,
                historical_adjustment_factor=0.984736,
                id="Ebff20941049b81e8d1cc80d5ef0cf7b9e44318993597f922292327578e468954",
                pay_date="2026-11-02",
                record_date="2026-10-09",
                split_adjusted_cash_amount=0.7075,
                ticker="VZ",
            ),
        ]
        # a comma-separated str must be sent as-is, not split into characters
        dividends = [d for d in self.c.list_stocks_dividends(ticker_any_of="AAPL,VZ")]
        self.assertEqual(dividends, expected)
        # a list of values is still joined with commas
        dividends = [
            d for d in self.c.list_stocks_dividends(ticker_any_of=["AAPL", "VZ"])  # type: ignore
        ]
        self.assertEqual(dividends, expected)
