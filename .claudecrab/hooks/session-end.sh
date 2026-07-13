#!/usr/bin/env bash
# Fired at session end. Archives this session's active.md to session-log.md.
# Does NOT delete active.md — it persists so the next session can recover.
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
LOG="$BASE/session-log.md"
if [ -s "$ACTIVE" ]; then
  {
    echo "---"
    echo ""
    echo "## Session ${SID:-unknown} — $(date -Iseconds)"
    echo ""
    cat "$ACTIVE"
    echo ""
  } >> "$LOG"
fi
exit 0
