#!/bin/bash
# usage: sweep.sh <label> <nseeds> [extra env assignments...]
LABEL="$1"; N="$2"; shift 2
OUT=/workspace/ep_leg2/results_${LABEL}.txt
: > "$OUT"
cd /workspace/pyautofit
seq 0 $((N-1)) | xargs -P 4 -I{} env "$@" TOY_SEED={} \
  timeout 1800 /workspace/venv312/bin/python /workspace/ep_leg2/run_once.py \
  2>/dev/null | grep '^RESULT' >> "$OUT"
echo "=== $LABEL ==="
sort -t= -k2 "$OUT"
echo "--- tally ---"
grep -o 'outcome=[A-Z]*' "$OUT" | sort | uniq -c
