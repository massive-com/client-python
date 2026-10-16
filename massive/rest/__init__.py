from .aggs import AggsClient
from .futures import FuturesClient
from .financials import FinancialsClient
from .benzinga import BenzingaClient
from .economy import EconomyClient
from .etf_global import EtfGlobalClient
from .tmx import TmxClient
from .trades import TradesClient
from .quotes import QuotesClient
from .snapshot import SnapshotClient
from .indicators import IndicatorsClient
from .summaries import SummariesClient
from .reference import (
    MarketsClient,
    TickersClient,
    SplitsClient,
    DividendsClient,
    ConditionsClient,
    ExchangesClient,
    ContractsClient,
)
from .vX import VXClient
from .base import logger
from ..certs import ca_bundle_path
from typing import Optional, Any, Dict
import os

BASE = "https://api.massive.com"
ENV_KEY = "MASSIVE_API_KEY"


class RESTClient(
    AggsClient,
    FuturesClient,
    FinancialsClient,
    BenzingaClient,
    EconomyClient,
    EtfGlobalClient,
    TmxClient,
    TradesClient,
    QuotesClient,
    SnapshotClient,
    MarketsClient,
    TickersClient,
    SplitsClient,
    DividendsClient,
    ConditionsClient,
    ExchangesClient,
    ContractsClient,
    IndicatorsClient,
    SummariesClient,
):
    def __init__(
        self,
        api_key: Optional[str] = os.getenv(ENV_KEY),
        connect_timeout: float = 10.0,
        read_timeout: float = 10.0,
        num_pools: int = 10,
        retries: int = 3,
        base: str = BASE,
        pagination: bool = True,
        verbose: bool = False,
        trace: bool = False,
        custom_json: Optional[Any] = None,
        maxsize: int = 10,
        ca_certs: Optional[str] = None,
        proxy: Optional[str] = None,
        connection_pool_kw: Optional[Dict[str, Any]] = None,
    ):
        """
        :param maxsize: Connections kept open per host, for reuse across threads.
        :param ca_certs: Path to a CA bundle to verify TLS with. Defaults to the
            SSL_CERT_FILE or REQUESTS_CA_BUNDLE environment variable, then certifi.
        :param proxy: Proxy URL to send requests through, e.g. "http://user:pass@proxy:8080".
            Environment proxy variables (HTTPS_PROXY etc.) are not used.
        :param connection_pool_kw: Other urllib3 PoolManager options. They override
            the client's defaults.
        """
        # resolve once, so the main and vx clients share it and warn only once
        ca_certs = ca_certs or ca_bundle_path(logger)
        super().__init__(
            api_key=api_key,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            num_pools=num_pools,
            retries=retries,
            base=base,
            pagination=pagination,
            verbose=verbose,
            trace=trace,
            custom_json=custom_json,
            maxsize=maxsize,
            ca_certs=ca_certs,
            proxy=proxy,
            connection_pool_kw=connection_pool_kw,
        )
        self.vx = VXClient(
            api_key=api_key,
            connect_timeout=connect_timeout,
            read_timeout=read_timeout,
            num_pools=num_pools,
            retries=retries,
            base=base,
            pagination=pagination,
            verbose=verbose,
            trace=trace,
            custom_json=custom_json,
            maxsize=maxsize,
            ca_certs=ca_certs,
            proxy=proxy,
            connection_pool_kw=connection_pool_kw,
        )
