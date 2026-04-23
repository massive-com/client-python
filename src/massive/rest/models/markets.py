from typing import Optional
from ...modelclass import modelclass


@modelclass
class MarketCurrencies:
    "Contains currency market status data."
    crypto: Optional[str] = None
    fx: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return MarketCurrencies(**d)


@modelclass
class MarketExchanges:
    "Contains exchange market status data."
    nasdaq: Optional[str] = None
    nyse: Optional[str] = None
    otc: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return MarketExchanges(**d)


@modelclass
class MarketIndices:
    "Contains indices market status data."
    s_and_p: Optional[str] = None
    societe_generale: Optional[str] = None
    cgi: Optional[str] = None
    msci: Optional[str] = None
    ftse_russell: Optional[str] = None
    mstar: Optional[str] = None
    mstarc: Optional[str] = None
    cccy: Optional[str] = None
    nasdaq: Optional[str] = None
    dow_jones: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return MarketIndices(**d)


@modelclass
class MarketHoliday:
    "MarketHoliday contains data for upcoming market holidays and their open/close times."
    close: Optional[str] = None
    date: Optional[str] = None
    exchange: Optional[str] = None
    name: Optional[str] = None
    open: Optional[str] = None
    status: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return MarketHoliday(**d)


@modelclass
class MarketStatus:
    "MarketStatus contains data for the current trading status of the exchanges and overall financial markets."
    after_hours: Optional[bool] = None
    currencies: Optional[MarketCurrencies] = None
    early_hours: Optional[bool] = None
    exchanges: Optional[MarketExchanges] = None
    indicesGroups: Optional[MarketIndices] = None
    market: Optional[str] = None
    server_time: Optional[str] = None

    @staticmethod
    def from_dict(d):
        return MarketStatus(
            after_hours=d.get("afterHours", None),
            currencies=(
                None
                if "currencies" not in d
                else MarketCurrencies.from_dict(d["currencies"])
            ),
            early_hours=d.get("earlyHours", None),
            exchanges=(
                None
                if "exchanges" not in d
                else MarketExchanges.from_dict(d["exchanges"])
            ),
            indicesGroups=(
                None
                if "indicesGroups" not in d
                else MarketIndices.from_dict(d["indicesGroups"])
            ),
            market=d.get("market", None),
            server_time=d.get("serverTime", None),
        )
