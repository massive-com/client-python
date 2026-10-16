import os
import tempfile
import unittest
from unittest import mock

import certifi
import urllib3

from massive import RESTClient


class ConnectionOptionsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.ssl_ca = os.path.join(tmp.name, "ssl-ca.pem")
        self.requests_ca = os.path.join(tmp.name, "requests-ca.pem")
        for path in (self.ssl_ca, self.requests_ca):
            open(path, "w").close()

    def client(self, env=None, **kwargs):
        with mock.patch.dict(os.environ, env or {}, clear=True):
            return RESTClient(api_key="key", **kwargs)

    def test_ca_bundle_defaults_to_certifi(self):
        c = self.client()
        self.assertEqual(c.client.connection_pool_kw["ca_certs"], certifi.where())

    def test_ca_bundle_from_env(self):
        c = self.client({"REQUESTS_CA_BUNDLE": self.requests_ca})
        self.assertEqual(c.client.connection_pool_kw["ca_certs"], self.requests_ca)
        c = self.client(
            {"SSL_CERT_FILE": self.ssl_ca, "REQUESTS_CA_BUNDLE": self.requests_ca}
        )
        self.assertEqual(c.client.connection_pool_kw["ca_certs"], self.ssl_ca)

    def test_missing_env_bundle_is_skipped_with_a_warning(self):
        with self.assertLogs("RESTClient", level="WARNING") as logs:
            c = self.client({"SSL_CERT_FILE": "/does-not-exist.pem"})
        self.assertEqual(c.client.connection_pool_kw["ca_certs"], certifi.where())
        self.assertEqual(c.vx.client.connection_pool_kw["ca_certs"], certifi.where())
        self.assertEqual(len(logs.output), 1, logs.output)
        self.assertIn("SSL_CERT_FILE", logs.output[0])
        with self.assertLogs("RESTClient", level="WARNING"):
            c = self.client(
                {
                    "SSL_CERT_FILE": "/does-not-exist.pem",
                    "REQUESTS_CA_BUNDLE": self.requests_ca,
                }
            )
        self.assertEqual(c.client.connection_pool_kw["ca_certs"], self.requests_ca)

    def test_ca_certs_argument_wins_over_env(self):
        c = self.client({"SSL_CERT_FILE": self.ssl_ca}, ca_certs="/explicit-ca.pem")
        self.assertEqual(c.client.connection_pool_kw["ca_certs"], "/explicit-ca.pem")

    def test_ca_certs_applies_to_vx(self):
        c = self.client(ca_certs="/explicit-ca.pem")
        self.assertEqual(c.vx.client.connection_pool_kw["ca_certs"], "/explicit-ca.pem")

    def test_maxsize(self):
        self.assertEqual(self.client().client.connection_pool_kw["maxsize"], 10)
        c = self.client(maxsize=32)
        self.assertEqual(c.client.connection_pool_kw["maxsize"], 32)

    def test_connection_pool_kw_overrides_defaults(self):
        timeout = urllib3.Timeout(connect=1, read=2)
        c = self.client(connection_pool_kw={"block": True, "timeout": timeout})
        self.assertTrue(c.client.connection_pool_kw["block"])
        self.assertIs(c.client.connection_pool_kw["timeout"], timeout)
        # defaults that weren't overridden are kept
        self.assertEqual(c.client.connection_pool_kw["cert_reqs"], "CERT_REQUIRED")

    def test_no_proxy_by_default(self):
        c = self.client({"HTTPS_PROXY": "http://proxy.example:8080"})
        self.assertNotIsInstance(c.client, urllib3.ProxyManager)

    def test_proxy(self):
        c = self.client(proxy="http://user:secret@proxy.example:8080")
        self.assertIsInstance(c.client, urllib3.ProxyManager)
        self.assertEqual(c.client.proxy.host, "proxy.example")
        self.assertEqual(
            c.client.proxy_headers["proxy-authorization"],
            urllib3.make_headers(proxy_basic_auth="user:secret")["proxy-authorization"],
        )
        self.assertEqual(c.client.connection_pool_kw["maxsize"], 10)


if __name__ == "__main__":
    unittest.main()
