from base import BaseTest
from massive.rest.models import (
    Trade,
    LastTrade,
    CryptoTrade,
)


class TradesTest(BaseTest):
    def test_get_last_trade(self):
        last_trade = self.c.get_last_trade("AAPL")
        expected = LastTrade(
            ticker="AAPL",
            trf_timestamp=1651179319310588400,
            sequence_number=7084210,
            sip_timestamp=1651179319310617300,
            participant_timestamp=1651179319308000000,
            conditions=[12, 37],
            correction=None,
            id="237688",
            price=166.25,
            trf_id=202,
            size=2,
            exchange=4,
            tape=3,
        )

        self.assertEqual(last_trade, expected)

    def test_get_last_crypto_trade(self):
        last_trade_crypto = self.c.get_last_crypto_trade("BTC", "USD")
        expected = CryptoTrade(
            conditions=[2],
            exchange=2,
            price=39976.89682331,
            size=0.005,
            timestamp=1651180409688,
        )
        self.assertEqual(last_trade_crypto, expected)

    def test_trades(self):
        trades = [t for t in self.c.list_trades(ticker="AAPL", limit=2)]
        expected = [
            Trade(
                conditions=[12, 37],
                correction=1,
                exchange=11,
                id="183276",
                participant_timestamp=1651181822461636600,
                price=156.43,
                sequence_number=7179341,
                sip_timestamp=1651181822461979400,
                size=10,
                tape=3,
                trf_id=3,
                trf_timestamp=1651181557090806500,
            ),
            Trade(
                conditions=[12, 37],
                correction=1,
                exchange=12,
                id="183276",
                participant_timestamp=1651181822461636600,
                price=157.43,
                sequence_number=7179341,
                sip_timestamp=1651181822461979400,
                size=10,
                tape=3,
                trf_id=3,
                trf_timestamp=1651181557090806500,
            ),
        ]
        self.assertEqual(trades, expected)
