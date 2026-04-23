import unittest

from massive import RESTClient
from massive.rest.models.request import (
    RequestOptionBuilder,
    X_MASSIVE_EDGE_ID,
    X_MASSIVE_EDGE_USER_AGENT,
    X_MASSIVE_EDGE_IP_ADDRESS,
)


class RequestTest(unittest.TestCase):
    def test_empty_request_options(self):
        options = RequestOptionBuilder()

        expected_edge_headers = None
        assert expected_edge_headers == options.headers

    def test_request_options_with_initialized_values(self):
        options = RequestOptionBuilder(
            edge_id="test", edge_ip_address="test", edge_user="test"
        )

        expected_object = {
            X_MASSIVE_EDGE_ID: "test",
            X_MASSIVE_EDGE_IP_ADDRESS: "test",
            X_MASSIVE_EDGE_USER_AGENT: "test",
        }

        assert expected_object == options.headers

    def test_request_options_builder(self):
        options = RequestOptionBuilder().edge_headers(
            edge_id="test", edge_ip_address="test"
        )

        required_options = {
            X_MASSIVE_EDGE_ID: "test",
            X_MASSIVE_EDGE_IP_ADDRESS: "test",
        }
        print(options.headers, required_options)
        self.assertDictEqual(required_options, options.headers)

        all_options = {
            X_MASSIVE_EDGE_ID: "test",
            X_MASSIVE_EDGE_IP_ADDRESS: "test",
            X_MASSIVE_EDGE_USER_AGENT: "test",
        }

        options = options.update_edge_header(edge_user="test")
        self.assertDictEqual(all_options, options.headers)

    def test_header_update(self):
        options = RequestOptionBuilder(
            edge_id="test", edge_ip_address="test", edge_user="test"
        )

        # this mocks the expected behavior during the request.get function call
        # in the BaseClient.
        headers = options.headers

        expected_headers = {
            "X-Massive-Edge-ID": "test",
            "X-Massive-Edge-IP-Address": "test",
            "X-Massive-Edge-User-Agent": "test",
        }

        self.assertDictEqual(headers, expected_headers)

        expected_headers = {
            "X-Massive-Edge-ID": "test2",
            "X-Massive-Edge-IP-Address": "test2",
            "X-Massive-Edge-User-Agent": "test2",
        }

        options = options.update_edge_header(
            edge_id="test2", edge_ip_address="test2", edge_user="test2"
        )

        self.assertDictEqual(options.headers, expected_headers)

    def test_clint_headers_concat(self):
        client = RESTClient(api_key="test")
        options = RequestOptionBuilder("test", "test", "test")
        concat_headers = client._concat_headers(options.headers)

        expected = {
            "Authorization": "Bearer test",
            "User-Agent": "Massive.com PythonClient/0.0.0",
            "X-Massive-Edge-ID": "test",
            "X-Massive-Edge-IP-Address": "test",
            "X-Massive-Edge-User-Agent": "test",
        }

        self.assertDictEqual(concat_headers, expected)

        headers = None
        expected = {
            "Authorization": "Bearer test",
            "User-Agent": "Massive.com PythonClient/0.0.0",
        }

        self.assertDictEqual(expected, client._concat_headers(headers))
