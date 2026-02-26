from typing import Optional
from ...modelclass import modelclass


@modelclass
class Dividend:
    "Dividend contains data for a historical cash dividend, including the ticker symbol, declaration date, ex-dividend date, record date, pay date, frequency, and amount."
    id: Optional[int] = None
    cash_amount: Optional[float] = None
    currency: Optional[str] = None
    declaration_date: Optional[str] = None
    dividend_type: Optional[str] = None
    ex_dividend_date: Optional[str] = None
    frequency: Optional[int] = None
    pay_date: Optional[str] = None
    record_date: Optional[str] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return Dividend(**d)


@modelclass
class StockDividend:
    cash_amount: Optional[float] = None
    currency: Optional[str] = None
    declaration_date: Optional[str] = None
    distribution_type: Optional[str] = None
    ex_dividend_date: Optional[str] = None
    frequency: Optional[int] = None
    historical_adjustment_factor: Optional[float] = None
    id: Optional[str] = None
    pay_date: Optional[str] = None
    record_date: Optional[str] = None
    split_adjusted_cash_amount: Optional[float] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return StockDividend(
            cash_amount=d.get("cash_amount"),
            currency=d.get("currency"),
            declaration_date=d.get("declaration_date"),
            distribution_type=d.get("distribution_type"),
            ex_dividend_date=d.get("ex_dividend_date"),
            frequency=d.get("frequency"),
            historical_adjustment_factor=d.get("historical_adjustment_factor"),
            id=d.get("id"),
            pay_date=d.get("pay_date"),
            record_date=d.get("record_date"),
            split_adjusted_cash_amount=d.get("split_adjusted_cash_amount"),
            ticker=d.get("ticker"),
        )
