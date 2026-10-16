import logging
import unittest

from massive.websocket import EquityTrade, Market, WebSocketMessage
from massive.websocket.models import parse, parse_single


def accept_message(message: WebSocketMessage) -> WebSocketMessage:
    """Exercise the public single-message type contract under mypy."""
    return message


class WebSocketModelTypesTest(unittest.TestCase):
    trade = {
        "ev": "T",
        "sym": "AAPL",
        "x": 10,
        "i": "5096",
        "z": 3,
        "p": 161.87,
        "s": 300,
        "c": [14, 41],
        "t": 1651684192462,
        "q": 4009402,
    }

    def test_single_parsed_event_matches_message_contract(self):
        message = parse_single(self.trade, logging.getLogger(), Market.Stocks)

        self.assertIsInstance(message, EquityTrade)
        self.assertIs(accept_message(message), message)

    def test_parse_returns_a_batch_of_messages(self):
        messages = parse([self.trade], logging.getLogger(), Market.Stocks)

        self.assertEqual(len(messages), 1)
        self.assertIsInstance(messages[0], EquityTrade)


if __name__ == "__main__":
    unittest.main()
