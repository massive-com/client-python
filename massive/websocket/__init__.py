import os
from collections import Counter
from enum import Enum
from typing import Optional, Union, List, Set, Callable, Awaitable, Any
import logging
import json
import asyncio
import ssl
import time
from .models import *
from websockets.asyncio.client import connect, ClientConnection
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from ..certs import ca_bundle_path
from ..logging import get_logger
import logging
from ..exceptions import AuthError

env_key = "MASSIVE_API_KEY"
logger = get_logger("WebSocketClient")

# Status messages that mean things are working. Any other status (e.g. "error",
# "max_connections", "slow_consumer", "force_disconnect") is logged as a warning.
OK_STATUSES = {"connected", "auth_success", "success"}


class WebSocketClient:
    def __init__(
        self,
        api_key: Optional[str] = os.getenv(env_key),
        feed: Union[str, Feed] = Feed.RealTime,
        market: Union[str, Market] = Market.Stocks,
        raw: bool = False,
        verbose: bool = False,
        subscriptions: Optional[List[str]] = None,
        max_reconnects: Optional[int] = 5,
        secure: bool = True,
        custom_json: Optional[Any] = None,
        ca_certs: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize a Massive WebSocketClient.

        :param api_key: Your API key.
        :param feed: The feed to subscribe to.
        :param raw: Whether to pass raw Union[str, bytes] to user callback.
        :param verbose: Whether to log client and server status messages.
        :param subscriptions: List of subscription parameters.
        :param max_reconnects: How many times to reconnect on network outage before ending .connect event loop.
        :param custom_json: Optional module exposing loads/dumps functions (similar to Python's json module) to be used for JSON conversions.
        :param ca_certs: Path to a CA bundle to verify TLS with. Defaults to the SSL_CERT_FILE or REQUESTS_CA_BUNDLE environment variable, then certifi.
        :return: A client.
        """
        if api_key is None:
            raise AuthError(
                f"Must specify env var {env_key} or pass api_key in constructor"
            )
        self.api_key = api_key
        self.feed = feed
        if isinstance(market, str):
            self.market = Market(market)  # converts str input to enum
        else:
            self.market = market

        self.market_value = self.market.value
        self.raw = raw
        if verbose:
            logger.setLevel(logging.DEBUG)
        self.websocket_cfg = kwargs
        if isinstance(feed, Enum):
            feed = feed.value
        self.url = f"ws{'s' if secure else ''}://{feed}/{self.market_value}"
        self.subscribed = False
        self.subs: Set[str] = set()
        self.max_reconnects = max_reconnects
        self.websocket: Optional[ClientConnection] = None
        if subscriptions is None:
            subscriptions = []
        self.scheduled_subs: Set[str] = set(subscriptions)
        self.schedule_resub = True
        self._server_errors: Counter = Counter()
        self._server_errors_since = 0.0
        self.ca_certs = ca_certs
        if custom_json:
            self.json = custom_json
        else:
            self.json = json

    # https://websockets.readthedocs.io/en/stable/reference/client.html#opening-a-connection
    async def connect(
        self,
        processor: Union[
            Callable[[List[WebSocketMessage]], Awaitable],
            Callable[[Union[str, bytes]], Awaitable],
        ],
        close_timeout: int = 1,
        **kwargs,
    ):
        """
        Connect to websocket server and run `processor(msg)` on every new `msg`.

        :param processor: The callback to process messages.
        :param close_timeout: How long to wait for handshake when calling .close.
        :raises AuthError: If invalid API key is supplied.
        """
        reconnects = 0
        logger.debug("connect: %s", self.url)
        ssl_context = self._ssl_context()

        last_exc = None
        async for s in connect(
            self.url,
            close_timeout=close_timeout,
            ssl=ssl_context,
            process_exception=lambda exc: None,
            **kwargs,
        ):
            self.websocket = s
            try:
                msg = await s.recv()
                logger.debug("connected: %s", msg)
                self._log_server_statuses(self.json.loads(msg))
                logger.debug("authing...")
                await s.send(
                    self.json.dumps({"action": "auth", "params": self.api_key})
                )
                auth_msg = await s.recv()
                auth_msg_parsed = self.json.loads(auth_msg)
                logger.debug("authed: %s", auth_msg)
                if auth_msg_parsed[0]["status"] == "auth_failed":
                    raise AuthError(auth_msg_parsed[0]["message"])
                # e.g. max_connections, which the server sends before closing
                self._log_server_statuses(auth_msg_parsed)
                self._flush_server_errors(force=True)
                while True:
                    if self.schedule_resub:
                        logger.debug(
                            "reconciling: %s %s", self.subs, self.scheduled_subs
                        )
                        new_subs = self.scheduled_subs.difference(self.subs)
                        await self._subscribe(new_subs)
                        old_subs = self.subs.difference(self.scheduled_subs)
                        await self._unsubscribe(old_subs)
                        self.subs = self.scheduled_subs
                        self.subs = set(self.scheduled_subs)
                        self.schedule_resub = False

                    try:
                        cmsg: Union[List[WebSocketMessage], Union[str, bytes]] = (
                            await asyncio.wait_for(s.recv(), timeout=1)
                        )
                    except asyncio.TimeoutError:
                        self._flush_server_errors()
                        continue

                    if not self.raw:
                        # we know cmsg is Data
                        msgJson = self.json.loads(cmsg)  # type: ignore
                        for m in msgJson:
                            if m["ev"] == "status":
                                logger.debug("status: %s", m["message"])
                        self._log_server_statuses(msgJson)
                        cmsg = parse(msgJson, logger, self.market)
                    self._flush_server_errors()

                    if len(cmsg) > 0:
                        await processor(cmsg)  # type: ignore
            except ConnectionClosedOK as e:
                logger.debug("connection closed (OK): %s", e)
                # the server sends a status (e.g. slow_consumer) before closing
                self._flush_server_errors(force=True)
                return
            except ConnectionClosedError as e:
                last_exc = e
                logger.debug("connection closed (ERR): %s", e)
                self._flush_server_errors(force=True)
                reconnects += 1
                self.scheduled_subs = set(self.subs)
                self.subs = set()
                self.schedule_resub = True
                if self.max_reconnects is not None and reconnects > self.max_reconnects:
                    break
                continue

        if (
            last_exc
            and self.max_reconnects is not None
            and reconnects > self.max_reconnects
        ):
            raise last_exc

    def _ssl_context(self) -> Optional[ssl.SSLContext]:
        # darwin needs some extra <3
        if not self.url.startswith("wss://"):
            return None
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(self.ca_certs or ca_bundle_path(logger))
        return context

    def run(
        self,
        handle_msg: Union[
            Callable[[List[WebSocketMessage]], None],
            Callable[[Union[str, bytes]], None],
        ],
        close_timeout: int = 1,
        **kwargs,
    ):
        """
        Connect to websocket server and run `processor(msg)` on every new `msg`. Synchronous version of `.connect`.

        :param processor: The callback to process messages.
        :param close_timeout: How long to wait for handshake when calling .close.
        :raises AuthError: If invalid API key is supplied.
        """

        async def handle_msg_wrapper(msgs):
            handle_msg(msgs)

        asyncio.run(self.connect(handle_msg_wrapper, close_timeout, **kwargs))

    def _log_server_statuses(self, msgs: List[Any]):
        # status messages are dropped by parse(), so problems (e.g. subscriptions
        # the server rejected, or why it disconnected) are logged here. The server
        # can send one error per channel, so identical ones are counted and logged
        # once a second.
        for m in msgs:
            if m.get("ev") != "status" or m.get("status") in OK_STATUSES:
                continue
            if not self._server_errors:
                self._server_errors_since = time.monotonic()
            self._server_errors[(m.get("status"), m.get("message"))] += 1

    def _flush_server_errors(self, force: bool = False):
        if not self._server_errors:
            return
        if not force and time.monotonic() - self._server_errors_since < 1:
            return
        for (status, message), count in self._server_errors.items():
            logger.warning(
                "server %s: %s%s", status, message, f" (x{count})" if count > 1 else ""
            )
        self._server_errors = Counter()

    async def _subscribe(self, topics: Union[List[str], Set[str]]):
        if self.websocket is None or len(topics) == 0:
            return
        subs = ",".join(topics)
        logger.debug("subbing: %s", subs)
        await self.websocket.send(
            self.json.dumps({"action": "subscribe", "params": subs})
        )

    async def _unsubscribe(self, topics: Union[List[str], Set[str]]):
        if self.websocket is None or len(topics) == 0:
            return
        subs = ",".join(topics)
        logger.debug("unsubbing: %s", subs)
        await self.websocket.send(
            self.json.dumps({"action": "unsubscribe", "params": subs})
        )

    @staticmethod
    def _parse_subscription(s: str):
        s = s.strip()
        split = s.split(".", 1)  # Split at the first period
        if len(split) != 2:
            logger.warning("invalid subscription:", s)
            return [None, None]

        return split

    def subscribe(self, *subscriptions: str):
        """
        Subscribe to given subscriptions.

        :param subscriptions: Subscriptions (args)
        """
        for s in subscriptions:
            topic, sym = self._parse_subscription(s)
            if topic == None:
                continue
            logger.debug("sub desired: %s", s)
            self.scheduled_subs.add(s)
            # If user subs to X.*, remove other X.\w+
            if sym == "*":
                for t in list(self.subs):
                    if t.startswith(topic):
                        self.scheduled_subs.discard(t)

        self.schedule_resub = True

    def unsubscribe(self, *subscriptions: str):
        """
        Unsubscribe from given subscriptions.

        :param subscriptions: Subscriptions (args)
        """
        for s in subscriptions:
            topic, sym = self._parse_subscription(s)
            if topic == None:
                continue
            logger.debug("sub undesired: %s", s)
            self.scheduled_subs.discard(s)

            # If user unsubs to X.*, remove other X.\w+
            if sym == "*":
                for t in list(self.subs):
                    if t.startswith(topic):
                        self.scheduled_subs.discard(t)

        self.schedule_resub = True

    def unsubscribe_all(self):
        """
        Unsubscribe from all subscriptions.
        """
        self.scheduled_subs = set()
        self.schedule_resub = True

    async def close(self):
        """
        Close the websocket connection.
        """
        logger.debug("closing")
        self._flush_server_errors(force=True)

        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        else:
            logger.warning("no websocket open to close")
