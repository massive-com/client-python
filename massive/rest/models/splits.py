from typing import Optional
from ...modelclass import modelclass


@modelclass
class Split:
    "Split contains data for a historical stock split, including the ticker symbol, the execution date, and the factors of the split ratio."
    id: Optional[int] = None
    execution_date: Optional[str] = None
    split_from: Optional[int] = None
    split_to: Optional[int] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return Split(**d)


@modelclass
class StockSplit:
    adjustment_type: Optional[str] = None
    execution_date: Optional[str] = None
    historical_adjustment_factor: Optional[float] = None
    id: Optional[str] = None
    split_from: Optional[float] = None
    split_to: Optional[float] = None
    ticker: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return StockSplit(
            adjustment_type=d.get("adjustment_type"),
            execution_date=d.get("execution_date"),
            historical_adjustment_factor=d.get("historical_adjustment_factor"),
            id=d.get("id"),
            split_from=d.get("split_from"),
            split_to=d.get("split_to"),
            ticker=d.get("ticker"),
        )
