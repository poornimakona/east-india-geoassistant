import argparse
import json
import sys
from pathlib import Path

from dotenv import dotenv_values
from elasticsearch import Elasticsearch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from retrieve.graph import RelationGraph

def get_es():
    c = dotenv_values(".env")
    return Elasticsearch(
        c["ELASTICSEARCH_URL"],
        basic_auth=(
            c["ELASTICSEARCH_USERNAME"],
            c["ELASTICSEARCH_PASSWORD"]
        )
    )


def search_schools(query, limit=5):
    es = get_es()
    result = es.search(
        index="east_india_chunks",
        query={"match_phrase": {"search_text": query}},
        size=max(1, min(limit, 20))
    )

    schools = []
    for hit in result["hits"]["hits"]:
        d = hit["_source"]
        schools.append({
            "id": str(hit["_id"]),
            "name": d.get("name") or "Unnamed school",
            "score": round(hit["_score"], 2),
            "properties": d.get("properties", {})
        })
    return schools


def search_entities(query, limit=5):
    es = get_es()
    result = es.search(
        index="east_india_entities",
        query={"match": {"canonical_name": query}},
        size=max(1, min(limit, 20))
    )
    return [
        {
            "entity_id": h["_id"],
            "name": h["_source"].get("canonical_name", ""),
            "type": h["_source"].get("type", ""),
            "score": round(h["_score"], 2)
        }
        for h in result["hits"]["hits"]
    ]


def graph_expand(entity_ids, hops=1):
    with Path("data/relations.jsonl").open(encoding="utf-8") as f:
        relations = [json.loads(x) for x in f if x.strip()]
    return RelationGraph(relations).expand(
        entity_ids, hops=hops, types=["mentions"]
    )


def graph_enhanced_search(query, limit=5):
    entities = search_entities(query, limit)
    expanded = graph_expand([e["entity_id"] for e in entities])
    schools = search_schools(query, limit)
    linked_ids = expanded["chunk_ids"]

    if linked_ids:
        es = get_es()
        result = es.search(
            index="east_india_chunks",
            query={"ids": {"values": linked_ids}},
            size=max(1, min(limit, 20))
        )
        existing = {s["id"] for s in schools}
        for hit in result["hits"]["hits"]:
            if hit["_id"] in existing:
                continue
            d = hit["_source"]
            schools.append({
                "id": str(hit["_id"]),
                "name": d.get("name") or "Unnamed school",
                "score": round(hit["_score"], 2),
                "properties": d.get("properties", {}),
                "graph_expanded": True
            })
            existing.add(hit["_id"])

    return {"schools": schools[:limit], "entities": entities, "graph": expanded}


def main():
    parser = argparse.ArgumentParser(
        description="Search schools with optional graph expansion"
    )
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--graph", action="store_true")
    args = parser.parse_args()
    limit = max(1, min(args.limit, 20))

    try:
        if args.graph:
            result = graph_enhanced_search(args.query, limit)
            schools = result["schools"]
            print("Matched entities:", len(result["entities"]))
            print("Linked feature IDs:", result["graph"]["chunk_ids"])
        else:
            schools = search_schools(args.query, limit)

        if not schools:
            print("No matching schools found.")
            return

        for i, school in enumerate(schools, 1):
            tag = " [graph-expanded]" if school.get("graph_expanded") else ""
            print(f"{i}. {school['name']} (score: {school['score']}){tag}")

    except Exception as error:
        print("Search failed:", error)


if __name__ == "__main__":
    main()