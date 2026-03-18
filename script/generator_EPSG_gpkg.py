#!/usr/bin/env bash
set -euo pipefail

URL="https://object.files.data.gouv.fr/hydra-geojson/hydra-geojson/fb6c3b2e-da8c-4e69-a719-6a96329e4cb2.geojson"
OUT="geozones.gpkg"
LAYER="geozones"

ogr2ogr -f GPKG "$OUT" "$URL" \
  -nln "$LAYER" \
  -t_srs EPSG:2154 \
  -lco SPATIAL_INDEX=YES

echo "GeoPackage créé : $OUT"
echo "Couche : $LAYER"
