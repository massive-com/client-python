from types import SimpleNamespace
import unittest

from massive import RESTClient
from massive.exceptions import ResponseDecodeError

TRUNCATED = b'{"results":[{"p":1.0,"s":100},{"p'


def _decode_through_get_handler(client):
    """Run a truncated body through the same try/except that _get and _paginate_iter use."""
    resp = SimpleNamespace(data=TRUNCATED)
    try:
        return client._decode(resp)
    except ValueError as e:
        if client.raise_on_decode_error:
            raise ResponseDecodeError(f"Could not decode response body: {e}") from e
        return []


class DecodeErrorTest(unittest.TestCase):
    def test_default_returns_empty_result(self):
        """Unchanged behaviour: an undecodable body is logged and becomes an empty result."""
        c = RESTClient("")
        self.assertFalse(c.raise_on_decode_error)
        self.assertEqual(_decode_through_get_handler(c), [])

    def test_opt_in_raises(self):
        c = RESTClient("", raise_on_decode_error=True)
        self.assertTrue(c.raise_on_decode_error)
        with self.assertRaises(ResponseDecodeError):
            _decode_through_get_handler(c)

    def test_flag_reaches_the_vx_client(self):
        c = RESTClient("", raise_on_decode_error=True)
        self.assertTrue(c.vx.raise_on_decode_error)

    def test_a_good_body_is_unaffected(self):
        for flag in (False, True):
            c = RESTClient("", raise_on_decode_error=flag)
            resp = SimpleNamespace(data=b'{"results":[{"p":1.0}]}')
            self.assertEqual(c._decode(resp), {"results": [{"p": 1.0}]})


if __name__ == "__main__":
    unittest.main()
