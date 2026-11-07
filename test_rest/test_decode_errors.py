import unittest

import pook  # type: ignore

from massive import RESTClient


class DecodeErrorLogTest(unittest.TestCase):
    """A response body that is not JSON is logged with the request URL (#1031)."""

    def setUp(self):
        self.c = RESTClient("test-key")
        pook.on()  # the shared REST test setup also leaves pook on; mocks below are used once

    def test_get_logs_url_on_decode_error(self):
        url = self.c.BASE + "/v1/test-decode-error/one?date=2026-01-02"
        pook.get(url, reply=200, response_body="<html>not json</html>")
        with self.assertLogs("RESTClient", level="ERROR") as logs:
            result = self.c._get(
                "/v1/test-decode-error/one", params={"date": "2026-01-02"}
            )
        self.assertEqual(result, [])
        self.assertEqual(len(logs.output), 1)
        self.assertIn(url, logs.output[0])
        self.assertIn("Error decoding json response", logs.output[0])

    def test_paginate_logs_url_on_decode_error(self):
        url = self.c.BASE + "/v1/test-decode-error/pages?limit=5"
        pook.get(url, reply=200, response_body="not json")
        with self.assertLogs("RESTClient", level="ERROR") as logs:
            items = list(
                self.c._paginate_iter(
                    path="/v1/test-decode-error/pages",
                    params={"limit": 5},
                    deserializer=lambda x: x,
                )
            )
        self.assertEqual(items, [])
        self.assertEqual(len(logs.output), 1)
        self.assertIn(url, logs.output[0])

    def test_url_never_contains_api_key(self):
        url = self.c.BASE + "/v1/test-decode-error/key"
        pook.get(url, reply=200, response_body="not json")
        with self.assertLogs("RESTClient", level="ERROR") as logs:
            self.c._get("/v1/test-decode-error/key")
        self.assertNotIn("test-key", logs.output[0])


if __name__ == "__main__":
    unittest.main()
