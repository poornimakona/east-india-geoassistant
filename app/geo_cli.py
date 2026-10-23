"""A conservative offline demo for exploring the supplied school-tagged features.
This is a data-inspection prototype, not the final RAG answer pipeline.
"""
import argparse, json, re
from pathlib import Path


def tokens(s):
    return set(re.findall(r"[a-z0-9]+", (s or '').lower()))


def score(query, props):
    q = tokens(query)
    name = str(props.get('name') or '')
    candidates = tokens(name)
    if not q or not candidates:
        return 0.0
    return len(q & candidates) / max(1, len(q))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', default='data/schools_features.jsonl')
    args = p.parse_args()
    path = Path(args.data)
    if not path.exists():
        raise SystemExit(f'Data file not found: {path}. Run ingest/geopackage_to_geojsonl.py first.')
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    print(f'Loaded {len(rows)} geographic features. Type a school name, or type exit.')
    print('This demo only searches feature names and reports available attributes; it does not contain admissions rules.')
    while True:
        query = input('\nQuestion/search: ').strip()
        if query.lower() in {'exit', 'quit'}:
            break
        ranked = sorted(((score(query, r['properties']), r) for r in rows), key=lambda x: (-x[0], str(x[1]['properties'].get('osm_id', ''))))
        hits = [(s, r) for s, r in ranked if s > 0][:5]
        if not hits:
            print('I cannot answer this from the available sources. No matching named feature was found.')
            continue
        for s, r in hits:
            props = r['properties']
            geom = r.get('geometry') or {}
            print(f"- name={props.get('name') or '[unnamed feature]'} | osm_id={props.get('osm_id')} | type={props.get('type')} | match={s:.2f} | geometry={geom.get('type')}")
        print('Note: match is a simple token-overlap score, not a calibrated probability. Verify identity before using results.')

if __name__ == '__main__':
    main()
