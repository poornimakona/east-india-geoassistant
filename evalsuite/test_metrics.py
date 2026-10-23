import unittest
from metrics import (
    precision_at_k,
    recall_at_k,
    mean_reciprocal_rank,
    ndcg_at_k,
)


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.relevant = {"A": 2, "B": 1, "C": 0}

    def test_precision(self):
        self.assertAlmostEqual(
            precision_at_k(self.relevant, ["A", "C"], 2), 0.5
        )

    def test_recall(self):
        self.assertAlmostEqual(
            recall_at_k(self.relevant, ["A", "B"], 2), 1.0
        )

    def test_mrr(self):
        self.assertAlmostEqual(
            mean_reciprocal_rank(self.relevant, ["C", "A"]), 0.5
        )

    def test_ndcg(self):
        self.assertGreater(
            ndcg_at_k(self.relevant, ["A", "B", "C"], 3), 0.9
        )


if __name__ == "__main__":
    unittest.main()