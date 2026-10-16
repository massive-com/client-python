import os
import unittest
from unittest import mock

import certifi

from massive import WebSocketClient


class WebSocketSSLTest(unittest.TestCase):
    def ca_path(self, env=None, **kwargs):
        with mock.patch.dict(os.environ, env or {}, clear=True):
            c = WebSocketClient(api_key="key", **kwargs)
            with mock.patch("massive.websocket.ssl.SSLContext") as context:
                c._ssl_context()
            return context.return_value.load_verify_locations.call_args.args[0]

    def test_defaults_to_certifi(self):
        self.assertEqual(self.ca_path(), certifi.where())

    def test_env(self):
        self.assertEqual(self.ca_path({"SSL_CERT_FILE": "/ssl-ca.pem"}), "/ssl-ca.pem")
        self.assertEqual(
            self.ca_path({"REQUESTS_CA_BUNDLE": "/requests-ca.pem"}), "/requests-ca.pem"
        )

    def test_ca_certs_argument_wins_over_env(self):
        self.assertEqual(
            self.ca_path({"SSL_CERT_FILE": "/ssl-ca.pem"}, ca_certs="/explicit-ca.pem"),
            "/explicit-ca.pem",
        )

    def test_no_context_without_tls(self):
        c = WebSocketClient(api_key="key", feed="localhost:8765", secure=False)
        self.assertIsNone(c._ssl_context())


if __name__ == "__main__":
    unittest.main()
