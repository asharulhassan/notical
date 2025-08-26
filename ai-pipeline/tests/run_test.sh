#!/usr/bin/env bash
# tests/run_test.sh
# Usage: ./tests/run_test.sh path/to/sample.pdf
set -euo pipefail

PDF_PATH="$1"

if [ -z "$PDF_PATH" ]; then
  echo "Usage: $0 path/to/sample.pdf"
  exit 1
fi

if [ ! -f "$PDF_PATH" ]; then
  echo "File not found: $PDF_PATH"
  exit 1
fi

BASE_URL="http://127.0.0.1:8000"

echo "1) Uploading PDF to ${BASE_URL}/ingest/pdf ..."
RESP=$(curl -s -X POST -F "file=@${PDF_PATH}" "${BASE_URL}/ingest/pdf")
echo "Ingest response: $RESP"

DOC_ID=$(echo "$RESP" | python - <<'PY'
import sys, json
try:
    j = json.load(sys.stdin)
    print(j.get("doc_id",""))
except:
    print("")
PY
)

if [ -z "$DOC_ID" ]; then
  echo "Failed to retrieve doc_id from ingest response. Server output above."
  exit 1
fi
echo "doc_id: $DOC_ID"

echo
echo "2) Generating deck from doc_id..."
RESP2=$(curl -s -X POST "${BASE_URL}/generate/deck/${DOC_ID}?deck_title=sample_deck")
echo "Generate response: $RESP2"

DECK_ID=$(echo "$RESP2" | python - <<'PY'
import sys,json
try:
    j = json.load(sys.stdin)
    print(j.get("deck_id",""))
except:
    print("")
PY
)

CSV_PATH=$(echo "$RESP2" | python - <<'PY'
import sys,json
try:
    j = json.load(sys.stdin)
    print(j.get("csv",""))
except:
    print("")
PY
)

if [ -n "$DECK_ID" ]; then
  echo "deck_id: $DECK_ID"
else
  echo "No deck_id returned. Check server logs/output above."
fi

if [ -n "$CSV_PATH" ]; then
  echo "CSV path reported by server: $CSV_PATH"
  if [ -f "$CSV_PATH" ]; then
    echo "CSV file exists at: $CSV_PATH"
  else
    echo "CSV file not found at the reported path (the server writes to its local exports/ folder)."
    echo "If you are running the server locally, check: ./exports/"
  fi
else
  echo "No csv path returned."
fi

echo "Done."
