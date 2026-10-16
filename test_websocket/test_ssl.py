import os
import tempfile
import unittest
from unittest import mock

import certifi

from massive import WebSocketClient


class WebSocketSSLTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.ssl_ca = os.path.join(tmp.name, "ssl-ca.pem")
        self.requests_ca = os.path.join(tmp.name, "requests-ca.pem")
        for path in (self.ssl_ca, self.requests_ca):
            open(path, "w").close()

    def ca_path(self, env=None, **kwargs):
        with mock.patch.dict(os.environ, env or {}, clear=True):
            c = WebSocketClient(api_key="key", **kwargs)
            with mock.patch("massive.websocket.ssl.SSLContext") as context:
                c._ssl_context()
            return context.return_value.load_verify_locations.call_args.args[0]

    def test_defaults_to_certifi(self):
        self.assertEqual(self.ca_path(), certifi.where())

    def test_env(self):
        self.assertEqual(self.ca_path({"SSL_CERT_FILE": self.ssl_ca}), self.ssl_ca)
        self.assertEqual(
            self.ca_path({"REQUESTS_CA_BUNDLE": self.requests_ca}), self.requests_ca
        )

    def test_missing_env_bundle_is_skipped_with_a_warning(self):
        with self.assertLogs("WebSocketClient", level="WARNING") as logs:
            path = self.ca_path({"SSL_CERT_FILE": "/does-not-exist.pem"})
        self.assertEqual(path, certifi.where())
        self.assertIn("SSL_CERT_FILE", logs.output[0])

    def test_ca_certs_argument_wins_over_env(self):
        self.assertEqual(
            self.ca_path({"SSL_CERT_FILE": self.ssl_ca}, ca_certs="/explicit-ca.pem"),
            "/explicit-ca.pem",
        )

    def test_no_context_without_tls(self):
        c = WebSocketClient(api_key="key", feed="localhost:8765", secure=False)
        self.assertIsNone(c._ssl_context())


if __name__ == "__main__":
    unittest.main()
