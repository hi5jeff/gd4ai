#!/usr/bin/env bash
# Fired at session start (source: startup/resume/clear/compact).
# Injects this session's own active.md into the conversation context.
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
if [ -s "$ACTIVE" ]; then
  echo "=== ACTIVE SESSION STATE DETECTED (source: $SOURCE) ==="
  echo ""
  cat "$ACTIVE"
  echo ""
  echo "=== END ACTIVE STATE ==="
  echo "Continue from where this state left off. This is your session's memory file:"
  echo "$ACTIVE"
  echo "Always write working state to THAT exact path (it is per-session)."
else
  echo "Your per-session memory file is: $ACTIVE"
  echo "Write your working state (current task, decisions, files in progress) to that exact path as you go."
fi
exit 0
