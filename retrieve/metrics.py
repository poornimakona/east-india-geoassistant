
"""Ranking metrics for retrieval evaluation."""
import math


def precision_at_k(ranked_ids, relevant_ids, k):
    if k <= 0:
        return 0.0
    relevant = set(relevant_ids)
    return sum(1 for x in ranked_ids[:k] if x in relevant) / k


def recall_at_k(ranked_ids, relevant_ids, k):
    relevant = set(relevant_ids)
    if k <= 0 or not relevant:
        return 0.0
    return len(set(ranked_ids[:k]) & relevant) / len(relevant)


def mean_reciprocal_rank(ranked_ids, relevant_ids):
    relevant = set(relevant_ids)
    for rank, item in enumerate(ranked_ids, 1):
        if item in relevant:
            return 1.0 / rank
    return 0.0


def dcg_at_k(ranked_ids, grades, k):
    if k <= 0:
        return 0.0
    total = 0.0
    for i, item in enumerate(ranked_ids[:k], 1):
        rel = max(0, grades.get(item, 0))
        total += (2 ** rel - 1) / math.log2(i + 1)
    return total


def ndcg_at_k(ranked_ids, grades, k):
    if k <= 0:
        return 0.0
    actual = dcg_at_k(ranked_ids, grades, k)
    ideal_ids = sorted(
        grades, key=lambda x: grades[x], reverse=True
    )
    ideal = dcg_at_k(ideal_ids, grades, k)
    return actual / ideal if ideal else 0.0


def mean_metric(values):
    """Calculate the average of metric values."""
    return sum(values) / len(values) if values else 0.0


# Backward compatibility for code using the old function name.
def reciprocal_rank(ranked_ids, relevant_ids):
    return mean_reciprocal_rank(ranked_ids, relevant_ids)
