import os
import ssl
import unittest
from unittest import mock

import certifi

from massive import WebSocketClient


class WebSocketSslTest(unittest.TestCase):
    def _client(self, secure=True):
        return WebSocketClient(api_key="test-key", secure=secure)

    def _loaded_bundle(self, client, env):
        with mock.patch.dict(os.environ, env, clear=True):
            with mock.patch.object(
                ssl.SSLContext, "load_verify_locations", autospec=True
            ) as load:
                context = client._ssl_context()
        self.assertIsNotNone(context)
        return load.call_args[0][0]

    def test_wss_uses_ssl_cert_file(self):
        self.assertEqual(
            self._loaded_bundle(self._client(), {"SSL_CERT_FILE": "/custom/ca.pem"}),
            "/custom/ca.pem",
        )

    def test_wss_uses_requests_ca_bundle(self):
        self.assertEqual(
            self._loaded_bundle(
                self._client(), {"REQUESTS_CA_BUNDLE": "/custom/requests-ca.pem"}
            ),
            "/custom/requests-ca.pem",
        )

    def test_wss_defaults_to_certifi(self):
        self.assertEqual(
            self._loaded_bundle(self._client(), {}),
            certifi.where(),
        )

    def test_plain_ws_has_no_ssl_context(self):
        self.assertIsNone(self._client(secure=False)._ssl_context())
