import unittest
import asyncio
from mock_server import run_mock_server
from typing import List
from massive.websocket import WebSocketMessage

unittest.util._MAX_LENGTH = 30000  # type: ignore


# https://docs.python.org/3/library/unittest.html#unittest.IsolatedAsyncioTestCase
class BaseTest(unittest.IsolatedAsyncioTestCase):
    expected: List[WebSocketMessage] = []
    count = 0

    def expectProcessor(self, msg):
        self.assertEqual(msg, self.expected[self.count])
        self.count += 1

    def expectResponse(self, msg):
        self.expected.append(msg)

    async def asyncSetUp(self):
        self.maxDiff = None
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(run_mock_server())

    async def asyncTearDown(self):
        self.task.cancel()
