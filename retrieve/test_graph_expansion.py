import json
from pathlib import Path
from retrieve.graph import RelationGraph

with Path("data/relations.jsonl").open(encoding="utf-8") as f:
    relations = [json.loads(line) for line in f if line.strip()]

graph = RelationGraph(relations)

with Path("data/entities.jsonl").open(encoding="utf-8") as f:
    entity = json.loads(next(line for line in f if line.strip()))

result = graph.expand([entity["entity_id"]], hops=1)

print("School:", entity["canonical_name"])
print("Entity ID:", entity["entity_id"])
print("Expanded entities:", len(result["entities"]))
print("Linked feature IDs:", result["chunk_ids"])
print("Graph stats:", graph.stats())
