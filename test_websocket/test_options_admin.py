import json
import unittest
from massive.websocket import logger
from massive.websocket.models import parse, Market, OptionsAdmin

# frames captured verbatim from wss://socket.massive.com/options (AD.*)
SINGLE_FRAME = '[{"ev":"AD","i":"1794331349111117097-2270200655","t":1794331349111117097,"q":2270200655,"x":300,"m":"FLEX E   MDB   LST 127888 240 P EUR 12.18.26 631 @ 6 2MDB"}]'
MULTI_FRAME = '[{"ev":"AD","i":"1794331356867045949-2270938732","t":1794331356867045949,"q":2270938732,"x":300,"m":"FLEX E   PG    LST 96699 135 P EUR 12.18.26 1122 @ 0.05 2PG"},{"ev":"AD","i":"1794331356867503288-2270938735","t":1794331356867503288,"q":2270938735,"x":300,"m":"FLEX E   PG    LST 97132 135 C EUR 12.18.26 1122 @ 35.25 2PG"}]'


class OptionsAdminTest(unittest.TestCase):
    def test_parse_single(self):
        msgs = parse(json.loads(SINGLE_FRAME), logger, Market.Options)
        self.assertEqual(
            msgs,
            [
                OptionsAdmin(
                    event_type="AD",
                    id="1794331349111117097-2270200655",
                    exchange=300,
                    message="FLEX E   MDB   LST 127888 240 P EUR 12.18.26 631 @ 6 2MDB",
                    timestamp=1794331349111117097,
                    sequence_number=2270200655,
                    retransmission=None,
                )
            ],
        )

    def test_parse_multi(self):
        msgs = parse(json.loads(MULTI_FRAME), logger, Market.Options)
        self.assertEqual(
            msgs,
            [
                OptionsAdmin(
                    event_type="AD",
                    id="1794331356867045949-2270938732",
                    exchange=300,
                    message="FLEX E   PG    LST 96699 135 P EUR 12.18.26 1122 @ 0.05 2PG",
                    timestamp=1794331356867045949,
                    sequence_number=2270938732,
                    retransmission=None,
                ),
                OptionsAdmin(
                    event_type="AD",
                    id="1794331356867503288-2270938735",
                    exchange=300,
                    message="FLEX E   PG    LST 97132 135 C EUR 12.18.26 1122 @ 35.25 2PG",
                    timestamp=1794331356867503288,
                    sequence_number=2270938735,
                    retransmission=None,
                ),
            ],
        )

    def test_parse_retransmission(self):
        d = json.loads(SINGLE_FRAME)
        d[0]["rt"] = True
        msgs = parse(d, logger, Market.Options)
        self.assertEqual(msgs[0].retransmission, True)  # type: ignore
