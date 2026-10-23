
"""Create deterministic School entities from school feature records."""
import hashlib
import json
import re
from pathlib import Path


INPUT_FILE = Path("data/schools_features.jsonl")
OUTPUT_FILE = Path("data/entities.jsonl")


def normalize_name(name):
    return re.sub(r"\s+", " ", str(name)).strip()


def make_entity_id(entity_type, canonical_name, source_id):
    raw = f"{entity_type}|{canonical_name.casefold()}|{source_id}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {INPUT_FILE}")

    entities = []
    seen = set()
    unnamed = 0

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            if not line.strip():
                continue

            feature = json.loads(line)
            properties = feature.get("properties", {})
            name = normalize_name(
                properties.get("name") or properties.get("Name") or ""
            )

            if not name:
                unnamed += 1
                continue

            source_id = str(
                feature.get("id")
                or properties.get("osm_id")
                or properties.get("osm_way_id")
                or line_number
            )

            entity_id = make_entity_id("School", name, source_id)
            if entity_id in seen:
                continue
            seen.add(entity_id)

            attributes = {}
            for key in ("osm_id", "osm_way_id", "amenity", "operator",
                        "addr:city", "addr:street"):
                value = properties.get(key)
                if value is not None:
                    attributes[key] = value

            geometry = feature.get("geometry")
            if isinstance(geometry, dict):
                coords = geometry.get("coordinates")
                if geometry.get("type") == "Point" and isinstance(coords, list):
                    if len(coords) >= 2:
                        attributes["geo_point"] = {
                            "lon": coords[0],
                            "lat": coords[1]
                        }

            entities.append({
                "entity_id": entity_id,
                "type": "School",
                "canonical_name": name,
                "mentions": [{
                    "chunk_id": source_id,
                    "char_start": 0,
                    "char_end": len(name)
                }],
                "attributes": attributes
            })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        for entity in entities:
            file.write(json.dumps(entity, ensure_ascii=False) + "\n")

    print(f"School entities created: {len(entities)}")
    print(f"Unnamed records skipped: {unnamed}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
