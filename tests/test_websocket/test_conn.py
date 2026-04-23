from massive import WebSocketClient
from base_ws import BaseTest
from mock_server import subs, port
import asyncio
from massive.websocket import EquityTrade


class WebSocketsTest(BaseTest):
    async def test_conn(self):
        c = WebSocketClient(
            api_key="", feed=f"localhost:{port}", verbose=True, secure=False
        )
        self.expectResponse(
            [
                EquityTrade(
                    event_type="T",
                    symbol="AAPL",
                    exchange=10,
                    id="5096",
                    tape=3,
                    price=161.87,
                    size=300,
                    conditions=[14, 41],
                    timestamp=1651684192462,
                    sequence_number=4009402,
                )
            ]
        )
        c.subscribe("T.AAPL")

        def binded(msg):
            self.expectProcessor(msg)

        asyncio.get_event_loop().create_task(c.connect(binded))
        self.expectResponse(
            [
                EquityTrade(
                    event_type="T",
                    symbol="AMZN",
                    exchange=12,
                    id="72815",
                    tape=3,
                    price=161.87,
                    size=1,
                    conditions=[14, 37, 41],
                    timestamp=1651684192536,
                    sequence_number=4009408,
                ),
                EquityTrade(
                    event_type="T",
                    symbol="AMZN",
                    exchange=4,
                    id="799",
                    tape=3,
                    price=161.87,
                    size=100,
                    conditions=None,
                    timestamp=1651684192717,
                    sequence_number=4009434,
                ),
            ]
        )
        c.subscribe("T.AMZN")
        self.assertEqual(subs, c.subs)
        c.unsubscribe_all()
        self.assertEqual(subs, set())
        c.subscribe("T.*")
        self.assertEqual(subs, c.subs)
        c.unsubscribe("T.*")
        self.assertEqual(subs, set())
        await c.close()
