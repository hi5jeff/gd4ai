#!/usr/bin/env bash
# Fired right after context compaction. Commands the model to re-read active.md.
INPUT=$(cat)
CWD=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get(chr(99)+chr(119)+chr(100),''))" 2>/dev/null)
SID=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('session_id',''))" 2>/dev/null)
SOURCE=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('source',''))" 2>/dev/null)
[ -z "$CWD" ] && exit 0
BASE="$CWD/.claudecrab"
if [ -n "$SID" ]; then
  ACTIVE="$BASE/sessions/$SID/active.md"
  mkdir -p "$BASE/sessions/$SID" 2>/dev/null
  if [ ! -e "$ACTIVE" ] && [ -s "$BASE/active.md" ]; then cp "$BASE/active.md" "$ACTIVE" 2>/dev/null; fi
else
  ACTIVE="$BASE/active.md"
fi
if [ -f "$ACTIVE" ]; then
  echo "IMPORTANT: The conversation was just compacted. Read $ACTIVE now to restore"
  echo "the current task, decisions made, files in progress, and open questions."
fi
exit 0
