from massive.rest.models import Split
from base import BaseTest


class SplitsTest(BaseTest):
    def test_list_splits(self):
        splits = [s for s in self.c.list_splits()]
        expected = [
            Split(
                execution_date="2022-07-18", split_from=1, split_to=20, ticker="GOOGL"
            ),
            Split(
                execution_date="2022-07-18", split_from=1, split_to=20, ticker="GOOG"
            ),
            Split(execution_date="2022-07-01", split_from=1, split_to=3, ticker="CTO"),
            Split(
                execution_date="2022-06-29", split_from=1, split_to=10, ticker="SHOP"
            ),
            Split(
                execution_date="2022-06-22", split_from=1, split_to=10, ticker="SHOP"
            ),
            Split(execution_date="2022-06-10", split_from=1, split_to=4, ticker="DXCM"),
            Split(
                execution_date="2022-06-06", split_from=1, split_to=20, ticker="AMZN"
            ),
            Split(execution_date="2022-05-20", split_from=2, split_to=1, ticker="BRW"),
            Split(execution_date="2022-05-16", split_from=1, split_to=2, ticker="CM"),
            Split(
                execution_date="2022-05-02", split_from=3, split_to=4, ticker="CIG.C"
            ),
        ]
        self.assertEqual(splits, expected)
