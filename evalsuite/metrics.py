
"""Ranking metrics for retrieval evaluation."""
import math


def precision_at_k(relevant, ranked, k):
    if k <= 0:
        return 0.0
    relevant_ids = {
        x for x, grade in relevant.items() if grade > 0
    }
    return sum(1 for x in ranked[:k] if x in relevant_ids) / k


def recall_at_k(relevant, ranked, k):
    relevant_ids = {
        x for x, grade in relevant.items() if grade > 0
    }
    if k <= 0 or not relevant_ids:
        return 0.0
    found = set(ranked[:k]) & relevant_ids
    return len(found) / len(relevant_ids)


def mean_reciprocal_rank(relevant, ranked):
    relevant_ids = {
        x for x, grade in relevant.items() if grade > 0
    }
    for rank, item in enumerate(ranked, 1):
        if item in relevant_ids:
            return 1.0 / rank
    return 0.0


def dcg_at_k(relevant, ranked, k):
    if k <= 0:
        return 0.0
    total = 0.0
    for i, item in enumerate(ranked[:k], 1):
        grade = max(0, relevant.get(item, 0))
        total += (2 ** grade - 1) / math.log2(i + 1)
    return total


def ndcg_at_k(relevant, ranked, k):
    if k <= 0:
        return 0.0
    actual = dcg_at_k(relevant, ranked, k)
    ideal_ranked = sorted(
        relevant, key=lambda x: relevant[x], reverse=True
    )
    ideal = dcg_at_k(relevant, ideal_ranked, k)
    return actual / ideal if ideal else 0.0
