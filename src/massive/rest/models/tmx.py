from typing import Optional
from ...modelclass import modelclass


@modelclass
class TmxCorporateEvent:
    company_name: Optional[str] = None
    date: Optional[str] = None
    isin: Optional[str] = None
    name: Optional[str] = None
    status: Optional[str] = None
    ticker: Optional[str] = None
    tmx_company_id: Optional[int] = None
    tmx_record_id: Optional[str] = None
    trading_venue: Optional[str] = None
    type: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return TmxCorporateEvent(
            company_name=d.get("company_name"),
            date=d.get("date"),
            isin=d.get("isin"),
            name=d.get("name"),
            status=d.get("status"),
            ticker=d.get("ticker"),
            tmx_company_id=d.get("tmx_company_id"),
            tmx_record_id=d.get("tmx_record_id"),
            trading_venue=d.get("trading_venue"),
            type=d.get("type"),
            url=d.get("url"),
        )
