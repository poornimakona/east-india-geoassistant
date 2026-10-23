
"""Build deterministic source-reference relations for school entities."""
import hashlib
import json
from pathlib import Path


ENTITY_FILE = Path("data/entities.jsonl")
FEATURE_FILE = Path("data/schools_features.jsonl")
OUTPUT_FILE = Path("data/relations.jsonl")


def relation_id(source_id, target_id, relation_type):
    value = f"{source_id}|{target_id}|{relation_type}"
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main():
    if not ENTITY_FILE.exists() or not FEATURE_FILE.exists():
        raise FileNotFoundError("Required entity or feature file is missing.")

    features = {}
    with FEATURE_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip():
                continue
            feature = json.loads(line)
            props = feature.get("properties", {})
            source_id = str(
                feature.get("id")
                or props.get("osm_id")
                or props.get("osm_way_id")
                or line_number
            )
            features[source_id] = feature

    relations = []
    with ENTITY_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            entity = json.loads(line)
            entity_id = entity["entity_id"]

            for mention in entity.get("mentions", []):
                source_id = str(mention.get("chunk_id", ""))

                if not source_id or source_id not in features:
                    continue

                rid = relation_id(entity_id, source_id, "mentions")
                relations.append({
                    "relation_id": rid,
                    "source_id": entity_id,
                    "target_id": source_id,
                    "type": "mentions",
                    "confidence": 1.0,
                    "evidence": {
                        "source": "schools_features.jsonl",
                        "chunk_id": source_id
                    }
                })

    unique = {r["relation_id"]: r for r in relations}
    output = [unique[key] for key in sorted(unique)]

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for relation in output:
            file.write(json.dumps(relation, ensure_ascii=False) + "\n")

    print(f"Feature records indexed for lookup: {len(features)}")
    print(f"Relations written: {len(output)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
