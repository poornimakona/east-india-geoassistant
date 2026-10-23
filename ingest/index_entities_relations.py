"""Index entity and relation JSONL records into Elasticsearch."""
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

load_dotenv()

url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
user = os.getenv("ELASTICSEARCH_USER", "elastic")
password = os.getenv("ELASTICSEARCH_PASSWORD")

es = Elasticsearch(
    url,
    basic_auth=(user, password) if password else None
)

configs = {
    "east_india_entities": ("data/entities.jsonl", "entity_id", {
        "entity_id": {"type": "keyword"},
        "type": {"type": "keyword"},
        "canonical_name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "mentions": {"type": "object", "enabled": True},
        "attributes": {"type": "object", "enabled": True}
    }),
    "east_india_relations": ("data/relations.jsonl", "relation_id", {
        "relation_id": {"type": "keyword"},
        "source_id": {"type": "keyword"},
        "target_id": {"type": "keyword"},
        "type": {"type": "keyword"},
        "confidence": {"type": "float"},
        "evidence": {"type": "object", "enabled": True}
    })
}

for index, (filename, id_field, properties) in configs.items():
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    if not es.indices.exists(index=index):
        es.indices.create(index=index, mappings={"properties": properties})
    elif not es.indices.get_mapping(index=index)[index]["mappings"].get("properties"):
        es.indices.put_mapping(index=index, properties=properties)

    def records():
        with path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    if not item.get(id_field):
                        raise ValueError(f"Missing {id_field} in {filename}")
                    yield {
                        "_op_type": "index",
                        "_index": index,
                        "_id": item[id_field],
                        "_source": item
                    }

    count, errors = helpers.bulk(es, records(), stats_only=True)
    es.indices.refresh(index=index)
    print(f"{index}: indexed {count}; errors {errors}; total {es.count(index=index)['count']}")

print("Finished. east_india_chunks was not modified.")
