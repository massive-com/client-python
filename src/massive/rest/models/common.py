from enum import Enum


class Sort(Enum):
    ASC = "asc"
    DESC = "desc"


class Order(Enum):
    ASC = "asc"
    DESC = "desc"


class Locale(Enum):
    US = "us"
    GLOBAL = "global"


class Market(Enum):
    STOCKS = "stocks"
    CRYPTO = "crypto"
    FX = "fx"
    OTC = "otc"
    INDICES = "indices"


class AssetClass(Enum):
    STOCKS = "stocks"
    OPTIONS = "options"
    CRYPTO = "crypto"
    FX = "fx"
    INDICES = "indices"


class DividendType(Enum):
    CD = "CD"
    SC = "SC"
    LT = "LT"
    ST = "ST"


class Frequency(Enum):
    ONE_TIME = 0
    ANUALLY = 1
    BIANUALLY = 2
    QUARTERLY = 4
    MONTHLY = 12


class DataType(Enum):
    DATA_TRADE = "trade"
    DATA_BBO = "bbo"
    DATA_NBBO = "nbbo"


class SIP(Enum):
    CTA = "CTA"
    UTP = "UTP"
    OPRA = "OPRA"


class ExchangeType(Enum):
    EXCHANGE = "exchange"
    TRF = "TRF"
    SIP = "SIP"


class Direction(Enum):
    GAINERS = "gainers"
    LOSERS = "losers"


class SnapshotMarketType(Enum):
    STOCKS = "stocks"
    FOREX = "forex"
    CRYPTO = "crypto"
    INDICES = "indices"


class Timeframe(Enum):
    ANNUAL = "annual"
    QUARTERLY = "quarterly"


class Precision(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4


class SeriesType(Enum):
    OPEN = "open"
    CLOSE = "close"
    HIGH = "high"
    LOW = "low"


class LaunchPadOptions(Enum):
    X_MASSIVE_EDGE_ID = "X-Massive-Edge-ID"
    X_MASSIVE_IP_ADDRESS = "X-Massive-Edge-IP-Address"
    X_MASSIVE_EDGE_USER_AGENT = "X-Massive-Edge-User-Agent"
