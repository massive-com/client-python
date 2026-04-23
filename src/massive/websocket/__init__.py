import os
from enum import Enum
from typing import Optional, Union, List, Set, Callable, Awaitable, Any
import logging
import json
import asyncio
import ssl
import certifi
from .models import *
from websockets.asyncio.client import connect, ClientConnection
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from ..logging import get_logger
import logging
from ..exceptions import AuthError

env_key = "MASSIVE_API_KEY"
logger = get_logger("WebSocketClient")


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
        # darwin needs some extra <3
        ssl_context = None
        if self.url.startswith("wss://"):
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_verify_locations(certifi.where())

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
                logger.debug("authing...")
                await s.send(
                    self.json.dumps({"action": "auth", "params": self.api_key})
                )
                auth_msg = await s.recv()
                auth_msg_parsed = self.json.loads(auth_msg)
                logger.debug("authed: %s", auth_msg)
                if auth_msg_parsed[0]["status"] == "auth_failed":
                    raise AuthError(auth_msg_parsed[0]["message"])
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
                        continue

                    if not self.raw:
                        # we know cmsg is Data
                        msgJson = self.json.loads(cmsg)  # type: ignore
                        for m in msgJson:
                            if m["ev"] == "status":
                                logger.debug("status: %s", m["message"])
                                continue
                        cmsg = parse(msgJson, logger, self.market)

                    if len(cmsg) > 0:
                        await processor(cmsg)  # type: ignore
            except ConnectionClosedOK as e:
                logger.debug("connection closed (OK): %s", e)
                return
            except ConnectionClosedError as e:
                last_exc = e
                logger.debug("connection closed (ERR): %s", e)
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

        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        else:
            logger.warning("no websocket open to close")
