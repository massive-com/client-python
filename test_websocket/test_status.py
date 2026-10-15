from massive import WebSocketClient
from base_ws import BaseTest
from mock_server import port
from websockets.asyncio.client import connect
import asyncio


class StatusTest(BaseTest):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        # wait until the mock server is accepting connections
        for _ in range(100):
            try:
                async with connect(f"ws://localhost:{port}"):
                    return
            except OSError:
                await asyncio.sleep(0.05)
        self.fail("mock server did not start")

    async def asyncTearDown(self):
        # wait for the server to shut down so the next test can bind the port
        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError:
            pass

    async def run_client(self, *subscriptions):
        c = WebSocketClient(api_key="", feed=f"localhost:{port}", secure=False)
        c.subscribe(*subscriptions)
        task = asyncio.create_task(c.connect(lambda msgs: asyncio.sleep(0)))
        await asyncio.sleep(0.5)
        await c.close()
        await task

    async def test_server_errors_are_logged(self):
        with self.assertLogs("WebSocketClient", level="WARNING") as logs:
            await self.run_client("ERR.X")
        self.assertEqual(
            logs.output,
            [
                "WARNING:WebSocketClient:server error: "
                "Subscription limit reached for feed. (x2)"
            ],
        )

    async def test_server_errors_are_grouped(self):
        # one subscription with many rejected channels logs a single line
        with self.assertLogs("WebSocketClient", level="WARNING") as logs:
            await self.run_client(*[f"ERR.X{i}" for i in range(50)])
        self.assertEqual(
            logs.output,
            [
                "WARNING:WebSocketClient:server error: "
                "Subscription limit reached for feed. (x100)"
            ],
        )

    async def test_success_statuses_are_not_logged(self):
        with self.assertNoLogs("WebSocketClient", level="WARNING"):
            await self.run_client("T.AAPL")
