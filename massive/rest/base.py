import certifi
import json
import os
import urllib3
import inspect
from urllib3.util.retry import Retry
from enum import Enum
from typing import Optional, Any, Dict
from datetime import datetime
from importlib.metadata import version, PackageNotFoundError
from .models.request import RequestOptionBuilder
from ..logging import get_logger
import logging
from urllib.parse import urlencode, urlparse
from ..exceptions import AuthError, BadResponse

logger = get_logger("RESTClient")
version_number = "unknown"
try:
    version_number = version("massive-api-client")
except PackageNotFoundError:
    pass


class BaseClient:
    def __init__(
        self,
        api_key: Optional[str],
        connect_timeout: float,
        read_timeout: float,
        num_pools: int,
        retries: int,
        base: str,
        pagination: bool,
        verbose: bool,
        trace: bool,
        custom_json: Optional[Any] = None,
    ):
        if api_key is None:
            raise AuthError(
                f"Must specify env var MASSIVE_API_KEY or pass api_key in constructor"
            )

        self.API_KEY = api_key
        self.BASE = base
        self.pagination = pagination

        self.headers = {
            "Authorization": "Bearer " + self.API_KEY,
            "Accept-Encoding": "gzip",
            "User-Agent": f"Massive.com PythonClient/{version_number}",
        }

        # initialize self.retries with the parameter value before using it
        self.retries = retries

        # https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry.RETRY_AFTER_STATUS_CODES
        retry_strategy = Retry(
            total=self.retries,
            status_forcelist=[
                413,
                429,
                499,
                500,
                502,
                503,
                504,
            ],  # default 413, 429, 503
            backoff_factor=0.1,  # [0.0s, 0.2s, 0.4s, 0.8s, 1.6s, ...]
        )

        # https://urllib3.readthedocs.io/en/stable/reference/urllib3.poolmanager.html
        # https://urllib3.readthedocs.io/en/stable/reference/urllib3.connectionpool.html#urllib3.HTTPConnectionPool
        pool_kwargs = dict(
            num_pools=num_pools,
            headers=self.headers,  # default headers sent with each request.
            ca_certs=certifi.where(),
            cert_reqs="CERT_REQUIRED",
            retries=retry_strategy,  # use the customized Retry instance
        )

        # Check for proxy environment variables (HTTPS_PROXY or HTTP_PROXY)
        proxy_url = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") \
                    or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
        if proxy_url:
            self.client = urllib3.ProxyManager(proxy_url, **pool_kwargs)
        else:
            self.client = urllib3.PoolManager(**pool_kwargs)

        self.timeout = urllib3.Timeout(connect=connect_timeout, read=read_timeout)

        if verbose:
            logger.setLevel(logging.DEBUG)
        self.trace = trace
        if custom_json:
            self.json = custom_json
        else:
            self.json = json

    def _decode(self, resp):
        return self.json.loads(resp.data.decode("utf-8"))

    def _get(
        self,
        path: str,
        params: Optional[dict] = None,
        result_key: Optional[str] = None,
        deserializer=None,
        raw: bool = False,
        options: Optional[RequestOptionBuilder] = None,
    ) -> Any:
        option = options if options is not None else RequestOptionBuilder()

        headers = self._concat_headers(option.headers)

        if self.trace:
            full_url = f"{self.BASE}{path}"
            if params:
                full_url += f"?{urlencode(params)}"
            print_headers = headers.copy()
            if "Authorization" in print_headers:
                print_headers["Authorization"] = print_headers["Authorization"].replace(
                    self.API_KEY, "REDACTED"
                )
            logger.info("Request URL: %s", full_url)
            logger.info("Request Headers: %s", print_headers)

        resp = self.client.request(
            "GET",
            self.BASE + path,
            fields=params,
            headers=headers,
        )

        if self.trace:
            resp_headers_dict = dict(resp.headers.items())
            logger.info(
                "Request URL: %s, Response Headers: %s", full_url, resp_headers_dict
            )

        if resp.status != 200:
            raise BadResponse(resp.data.decode("utf-8"))

        if raw:
            return resp

        try:
            obj = self._decode(resp)
        except ValueError as e:
            logger.error("Error decoding json response: %s", e)
            return []

        if result_key:
            if result_key not in obj:
                return []
            obj = obj[result_key]

        if deserializer:
            if type(obj) == list:
                obj = [deserializer(o) for o in obj]
            else:
                obj = deserializer(obj)

        return obj

    @staticmethod
    def time_mult(timestamp_res: str) -> int:
        if timestamp_res == "nanos":
            return 1000000000
        elif timestamp_res == "micros":
            return 1000000
        elif timestamp_res == "millis":
            return 1000

        return 1

    def _get_params(
        self, fn, caller_locals: Dict[str, Any], datetime_res: str = "nanos"
    ):
        params = caller_locals["params"]
        if params is None:
            params = {}
        # https://docs.python.org/3.8/library/inspect.html#inspect.Signature
        for argname, v in inspect.signature(fn).parameters.items():
            # https://docs.python.org/3.8/library/inspect.html#inspect.Parameter
            if argname in ["params", "raw"]:
                continue
            if v.default != v.empty:
                # timestamp_lt -> timestamp.lt
                val = caller_locals.get(argname, v.default)
                if isinstance(val, Enum):
                    val = val.value
                elif isinstance(val, bool):
                    val = str(val).lower()
                elif isinstance(val, datetime):
                    val = int(val.timestamp() * self.time_mult(datetime_res))
                if val is not None:
                    for ext in ["lt", "lte", "gt", "gte", "any_of"]:
                        if argname.endswith(f"_{ext}"):
                            # lop off ext, then rebuild argname with ext,
                            # using ., and not _ (removesuffix would work)
                            # but that is python 3.9+
                            argname = argname[: -len(f"_{ext}")] + f".{ext}"
                    if argname.endswith("any_of"):
                        val = ",".join(val)
                    params[argname] = val

        return params

    def _concat_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        if headers is None:
            return self.headers
        return {**headers, **self.headers}

    def _paginate_iter(
        self,
        path: str,
        params: dict,
        deserializer,
        result_key: str = "results",
        options: Optional[RequestOptionBuilder] = None,
    ):
        while True:
            resp = self._get(
                path=path,
                params=params,
                deserializer=deserializer,
                result_key=result_key,
                raw=True,
                options=options,
            )

            try:
                decoded = self._decode(resp)
            except ValueError as e:
                logger.error("Error decoding json response: %s", e)
                return []

            if result_key not in decoded:
                return []
            for t in decoded[result_key]:
                yield deserializer(t)
            if not self.pagination or "next_url" not in decoded:
                return
            next_url = decoded["next_url"]
            parsed = urlparse(next_url)
            path = parsed.path
            if parsed.query:
                path += "?" + parsed.query
            params = {}

    def _paginate(
        self,
        path: str,
        params: dict,
        raw: bool,
        deserializer,
        result_key: str = "results",
        options: Optional[RequestOptionBuilder] = None,
    ):
        if raw:
            return self._get(
                path=path,
                params=params,
                deserializer=deserializer,
                raw=True,
                options=options,
            )

        return self._paginate_iter(
            path=path,
            params=params,
            deserializer=deserializer,
            result_key=result_key,
            options=options,
        )
