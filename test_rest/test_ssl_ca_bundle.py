import os
import unittest
from unittest import mock

import certifi

from massive import RESTClient
from massive.rest.base import _default_ca_bundle


class SSLCaBundleTest(unittest.TestCase):
    def tearDown(self):
        for var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"):
            os.environ.pop(var, None)

    def test_ssl_cert_file_takes_precedence(self):
        with mock.patch.dict(
            os.environ,
            {
                "SSL_CERT_FILE": "/tmp/custom-ca.pem",
                "REQUESTS_CA_BUNDLE": "/tmp/other-ca.pem",
            },
        ):
            self.assertEqual(_default_ca_bundle(), "/tmp/custom-ca.pem")
            client = RESTClient("key")
            self.assertEqual(
                client.client.connection_pool_kw["ca_certs"], "/tmp/custom-ca.pem"
            )

    def test_requests_ca_bundle_fallback(self):
        os.environ.pop("SSL_CERT_FILE", None)
        with mock.patch.dict(os.environ, {"REQUESTS_CA_BUNDLE": "/tmp/other-ca.pem"}):
            self.assertEqual(_default_ca_bundle(), "/tmp/other-ca.pem")
            client = RESTClient("key")
            self.assertEqual(
                client.client.connection_pool_kw["ca_certs"], "/tmp/other-ca.pem"
            )

    def test_certifi_default_without_env(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(_default_ca_bundle(), certifi.where())
            client = RESTClient("key")
            self.assertEqual(
                client.client.connection_pool_kw["ca_certs"], certifi.where()
            )


if __name__ == "__main__":
    unittest.main()
