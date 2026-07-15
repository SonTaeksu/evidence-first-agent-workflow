#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <image> [regions.json] [output-root]" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE="$1"
REGIONS="${2:-}"
OUTPUT_ROOT="${3:-reference-assets/evidence}"
NAME="$(basename "$IMAGE")"
NAME="${NAME%.*}"
OUTPUT="$ROOT/$OUTPUT_ROOT/$NAME"

mkdir -p "$OUTPUT"

ARGS=(
  "$ROOT/tools/reference-image-manifest/extract_reference_image.py"
  "$IMAGE"
  --output "$OUTPUT/manifest.json"
  --normalized-png "$OUTPUT/normalized.png"
)

if [[ -n "$REGIONS" ]]; then
  ARGS+=(--regions "$REGIONS")
fi

python3 "${ARGS[@]}"
echo "Reference evidence: $OUTPUT"
