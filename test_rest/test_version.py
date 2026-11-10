import unittest
from importlib.metadata import version

import massive
from massive import RESTClient


class VersionTest(unittest.TestCase):
    def test_version(self):
        self.assertEqual(massive.__version__, version("massive"))

    def test_user_agent(self):
        self.assertEqual(
            RESTClient(api_key="key").headers["User-Agent"],
            f"Massive.com PythonClient/{version('massive')}",
        )


if __name__ == "__main__":
    unittest.main()
