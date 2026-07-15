#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <source> [output-root] [wait-ms] [language]" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="$1"
OUTPUT_ROOT="${2:-reference-assets/evidence}"
WAIT="${3:-2000}"
LANGUAGE="${4:-en}"
NAME="$(basename "$SOURCE")"
NAME="${NAME%.*}"
OUTPUT="$ROOT/$OUTPUT_ROOT/$NAME"

mkdir -p "$OUTPUT"

python3 "$ROOT/tools/spa-screen-extractor/extract_spa.py" \
  --browser "$SOURCE" \
  --wait "$WAIT" \
  --language "$LANGUAGE" \
  --save-dom "$OUTPUT/rendered.html" \
  --json "$OUTPUT/screen-spec.json" \
  --out "$OUTPUT/screen-spec.md"

echo "SPA evidence: $OUTPUT"
