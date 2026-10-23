"""Export the supplied GeoPackage layer to line-delimited GeoJSON records."""
import argparse, json
from pathlib import Path
import geopandas as gpd


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True, help='Path to schools.gpkg')
    p.add_argument('--output', default='data/schools_features.jsonl')
    p.add_argument('--layer', default=None, help='Optional layer name')
    args = p.parse_args()
    gdf = gpd.read_file(args.input, layer=args.layer) if args.layer else gpd.read_file(args.input)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    named = 0
    with out.open('w', encoding='utf-8') as f:
        for _, row in gdf.iterrows():
            props = {k: (None if v is None else (v.item() if hasattr(v, 'item') else v))
                     for k, v in row.drop(labels=[gdf.geometry.name]).to_dict().items()}
            name = props.get('name')
            if name is not None and str(name).strip():
                named += 1
            geom = row[gdf.geometry.name]
            record = {'properties': props, 'geometry': None if geom is None else geom.__geo_interface__}
            f.write(json.dumps(record, ensure_ascii=False, default=str) + '\n')
    print(f'Layer: {gdf.attrs.get("name", "default layer")}')
    print(f'Features exported: {len(gdf)}')
    print(f'Features with names: {named}')
    print(f'Features without names: {len(gdf) - named}')
    print(f'CRS: {gdf.crs}')
    print(f'Output: {out.resolve()}')

if __name__ == '__main__':
    main()
