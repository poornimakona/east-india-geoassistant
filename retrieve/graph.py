
"""Graph traversal, expansion, statistics, and PageRank."""
from collections import defaultdict, deque
import networkx as nx


class RelationGraph:
    def __init__(self, relations):
        self.adj = defaultdict(list)
        self.reverse_adj = defaultdict(list)
        self.relations = list(relations)
        self.graph = nx.DiGraph()

        for r in self.relations:
            source = r["source_id"]
            target = r["target_id"]
            rel_type = r["type"]

            self.adj[source].append((target, rel_type))
            self.reverse_adj[target].append((source, rel_type))
            self.graph.add_edge(source, target, type=rel_type)

        for node in self.adj:
            self.adj[node].sort(key=lambda x: (x[0], x[1]))
        for node in self.reverse_adj:
            self.reverse_adj[node].sort(key=lambda x: (x[0], x[1]))

    def neighbours(self, entity_id, hops=1, types=None, max_expand=100):
        if hops < 1 or max_expand < 1:
            return []

        allowed = set(types) if types else None
        queue = deque([(entity_id, 0, [entity_id])])
        visited = {entity_id}
        results = []
        expanded_total = 0

        while queue and expanded_total < max_expand:
            node, depth, path = queue.popleft()
            if depth >= hops:
                continue

            for nxt, rel_type in self.adj.get(node, []):
                if allowed is not None and rel_type not in allowed:
                    continue

                expanded_total += 1
                if expanded_total > max_expand:
                    break
                if nxt in visited:
                    continue

                visited.add(nxt)
                new_path = path + [nxt]
                results.append({
                    "entity_id": nxt,
                    "via": rel_type,
                    "hops": depth + 1,
                    "path": new_path
                })
                queue.append((nxt, depth + 1, new_path))

        return results

    def expand(self, query_entities, hops=1, types=None):
        """Return related entity IDs and any linked chunk IDs."""
        expanded = []
        seen = set()

        for entity_id in query_entities:
            for item in self.neighbours(entity_id, hops=hops, types=types):
                related_id = item["entity_id"]
                if related_id not in seen:
                    seen.add(related_id)
                    expanded.append(item)

        chunk_ids = set()
        for relation in self.relations:
            if relation["source_id"] in seen or relation["target_id"] in seen:
                chunk_id = relation.get("chunk_id")
                if chunk_id:
                    chunk_ids.add(chunk_id)
                evidence = relation.get("evidence", {})
                if isinstance(evidence, dict):
                    chunk_id = evidence.get("chunk_id")
                    if chunk_id:
                        chunk_ids.add(chunk_id)

        return {
            "entities": expanded,
            "chunk_ids": sorted(chunk_ids)
        }

    def stats(self):
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "relation_types": dict(
                sorted(
                    __import__("collections").Counter(
                        r["type"] for r in self.relations
                    ).items()
                )
            ),
            "top_degree": sorted(
                self.graph.degree(),
                key=lambda item: (-item[1], item[0])
            )[:10]
        }

    def page_rank(self):
        if self.graph.number_of_nodes() == 0:
            return {}
        scores = nx.pagerank(self.graph)
        return dict(sorted(scores.items(), key=lambda item: (-item[1], item[0])))
