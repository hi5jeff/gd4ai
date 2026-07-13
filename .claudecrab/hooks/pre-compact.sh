#!/usr/bin/env bash
# Fired right before context compaction. Pins state into the conversation so
# the compaction summary preserves pointers to disk files.
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
echo "=== SESSION STATE BEFORE COMPACTION ==="
if [ -f "$ACTIVE" ]; then
  echo "## Active state ($ACTIVE)"
  cat "$ACTIVE"
  echo ""
fi
echo "## Working tree status"
( cd "$CWD" && git status --short 2>/dev/null | head -20 ) || echo "(not a git repo)"
echo ""
echo "## Recovery: read $ACTIVE after compaction to restore working context."
echo "=== END PRE-COMPACT ==="
exit 0
