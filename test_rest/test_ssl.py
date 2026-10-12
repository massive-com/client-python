import os
import unittest
from unittest import mock

import certifi

from massive import RESTClient
from massive.certs import ca_bundle_path


class CaBundlePathTest(unittest.TestCase):
    def test_ssl_cert_file_env_wins(self):
        with mock.patch.dict(
            os.environ, {"SSL_CERT_FILE": "/custom/ca.pem"}, clear=True
        ):
            self.assertEqual(ca_bundle_path(), "/custom/ca.pem")

    def test_requests_ca_bundle_env_used(self):
        with mock.patch.dict(
            os.environ, {"REQUESTS_CA_BUNDLE": "/custom/requests-ca.pem"}, clear=True
        ):
            self.assertEqual(ca_bundle_path(), "/custom/requests-ca.pem")

    def test_ssl_cert_file_preferred_over_requests_ca_bundle(self):
        with mock.patch.dict(
            os.environ,
            {
                "SSL_CERT_FILE": "/custom/ca.pem",
                "REQUESTS_CA_BUNDLE": "/custom/requests-ca.pem",
            },
            clear=True,
        ):
            self.assertEqual(ca_bundle_path(), "/custom/ca.pem")

    def test_defaults_to_certifi(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(ca_bundle_path(), certifi.where())


class RestClientSslTest(unittest.TestCase):
    def _pool_ca_certs(self):
        return RESTClient("test-key").client.connection_pool_kw["ca_certs"]

    def test_rest_client_uses_ssl_cert_file(self):
        with mock.patch.dict(
            os.environ, {"SSL_CERT_FILE": "/custom/ca.pem"}, clear=True
        ):
            self.assertEqual(self._pool_ca_certs(), "/custom/ca.pem")

    def test_rest_client_uses_requests_ca_bundle(self):
        with mock.patch.dict(
            os.environ, {"REQUESTS_CA_BUNDLE": "/custom/requests-ca.pem"}, clear=True
        ):
            self.assertEqual(self._pool_ca_certs(), "/custom/requests-ca.pem")

    def test_rest_client_defaults_to_certifi(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(self._pool_ca_certs(), certifi.where())
