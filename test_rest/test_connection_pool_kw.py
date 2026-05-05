import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import unittest
from unittest.mock import patch, MagicMock
from massive import RESTClient


class ConnectionPoolKwTest(unittest.TestCase):
    def _make_client(self, **kwargs):
        with patch("urllib3.PoolManager") as mock_pm:
            mock_pm.return_value = MagicMock()
            RESTClient(api_key="test", **kwargs)
            return mock_pm

    def test_default_no_extra_kwargs(self):
        """connection_pool_kw=None passes no extra kwargs to PoolManager."""
        mock_pm = self._make_client()
        _, call_kwargs = mock_pm.call_args
        self.assertNotIn("connection_pool_kw", call_kwargs)

    def test_connection_pool_kw_passed_as_kwargs(self):
        """connection_pool_kw dict is unpacked into PoolManager as kwargs."""
        extra = {"maxsize": 20, "block": True}
        mock_pm = self._make_client(connection_pool_kw=extra)
        _, call_kwargs = mock_pm.call_args
        self.assertEqual(call_kwargs["maxsize"], 20)
        self.assertEqual(call_kwargs["block"], True)

    def test_empty_connection_pool_kw(self):
        """Empty dict connection_pool_kw adds no extra kwargs to PoolManager."""
        mock_pm = self._make_client(connection_pool_kw={})
        _, call_kwargs = mock_pm.call_args
        self.assertNotIn("connection_pool_kw", call_kwargs)
