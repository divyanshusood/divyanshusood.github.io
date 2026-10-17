#!/bin/sh
# Rebuild the knowledge graph and write it straight into the published site.
#
#   ./tools/kg/build.sh
#
# Edit the entity lists at the top of build_kg.py, then run this. It writes
# kg.html and sood_kg.ttl at the repo root, which is what GitHub Pages serves.
set -e
cd "$(dirname "$0")"
python3 build_kg.py
python3 render_kg.py
python3 write_ttl.py
echo "kg.html and sood_kg.ttl updated at the repo root"
