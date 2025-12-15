---
argument-hint:
description: Diagnostic command to check workflow health and identify issues
---

## `/workflow-health` - Workflow Health Diagnostics

Use this command to diagnose workflow issues and verify system health.

This command performs comprehensive checks on all workflow components.

### Process

**1. Environment Checks**
```bash
echo "=== Workflow Health Check ==="
echo ""
echo "1. ENVIRONMENT"
echo "   ----------"

# bd CLI
if command -v bd &> /dev/null; then
  BD_VERSION=$(bd version 2>&1 | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | head -1)
  echo "   bd CLI: OK ($BD_VERSION)"
else
  echo "   bd CLI: MISSING"
fi

# git
if command -v git &> /dev/null; then
  echo "   git: OK ($(git --version | cut -d' ' -f3))"
else
  echo "   git: MISSING"
fi

# jq (for JSON processing)
if command -v jq &> /dev/null; then
  echo "   jq: OK"
else
  echo "   jq: MISSING (some features unavailable)"
fi

# Sandbox detection
if [ -n "$CLAUDE_CODE_SANDBOX" ] || [ -n "$CODEX_SANDBOX" ] || \
   [ -n "$REPLIT_ENVIRONMENT" ] || [ -n "$GITPOD_WORKSPACE_ID" ]; then
  echo "   Mode: SANDBOX (use --sandbox flag)"
else
  echo "   Mode: STANDARD"
fi
```

**2. Beads Health**
```bash
echo ""
echo "2. BEADS TRACKING"
echo "   --------------"

if [ -d ".beads" ]; then
  echo "   .beads/: OK"

  # Check database
  if [ -f ".beads/beads.db" ]; then
    # Integrity check
    INTEGRITY=$(sqlite3 .beads/beads.db "PRAGMA integrity_check;" 2>&1)
    if [ "$INTEGRITY" = "ok" ]; then
      echo "   Database: HEALTHY"
    else
      echo "   Database: CORRUPTED - needs recovery"
    fi
  else
    echo "   Database: MISSING"
  fi

  # Check JSONL
  if [ -f ".beads/issues.jsonl" ]; then
    ISSUE_COUNT=$(wc -l < .beads/issues.jsonl | tr -d ' ')
    echo "   JSONL: OK ($ISSUE_COUNT entries)"
  else
    echo "   JSONL: MISSING"
  fi

  # Test bd commands
  if bd list --limit 1 &> /dev/null; then
    echo "   bd commands: WORKING"
  else
    echo "   bd commands: FAILING"
  fi
else
  echo "   .beads/: NOT INITIALIZED"
  echo "   Run: /workflow-init"
fi
```

**3. Issue Status**
```bash
echo ""
echo "3. ISSUE STATUS"
echo "   ------------"

if [ -d ".beads" ] && command -v bd &> /dev/null; then
  # Count by status
  OPEN=$(bd list --status open --json 2>/dev/null | jq '. | length' 2>/dev/null || echo "?")
  IN_PROGRESS=$(bd list --status in_progress --json 2>/dev/null | jq '. | length' 2>/dev/null || echo "?")
  CLOSED=$(bd list --status closed --json 2>/dev/null | jq '. | length' 2>/dev/null || echo "?")

  echo "   Open: $OPEN"
  echo "   In Progress: $IN_PROGRESS"
  echo "   Closed: $CLOSED"

  # Check for stale issues
  STALE=$(bd stale --days 7 --json 2>/dev/null | jq '. | length' 2>/dev/null || echo "?")
  if [ "$STALE" != "0" ] && [ "$STALE" != "?" ]; then
    echo "   WARN: $STALE stale issues (>7 days)"
  fi

  # Check for blocked issues
  BLOCKED=$(bd blocked --json 2>/dev/null | jq '. | length' 2>/dev/null || echo "?")
  if [ "$BLOCKED" != "0" ] && [ "$BLOCKED" != "?" ]; then
    echo "   WARN: $BLOCKED blocked issues"
  fi

  # Check for ready work
  READY=$(bd ready --json 2>/dev/null | jq '.issues | length' 2>/dev/null || echo "?")
  echo "   Ready to work: $READY"
else
  echo "   (Beads not available)"
fi
```

**4. Configuration Files**
```bash
echo ""
echo "4. CONFIGURATION"
echo "   -------------"

# Check required files
FILES=(
  "CLAUDE.md:Project instructions"
  ".claude/rules/001-project-principles.md:Project principles"
  ".claude/rules/003-multi-agent-coordination.md:Multi-agent rules"
  ".claude/lib/workflow-precheck.sh:Precheck library"
)

for entry in "${FILES[@]}"; do
  file="${entry%%:*}"
  desc="${entry#*:}"
  if [ -f "$file" ]; then
    echo "   $file: OK"
  else
    echo "   $file: MISSING ($desc)"
  fi
done
```

**5. Git Status**
```bash
echo ""
echo "5. GIT STATUS"
echo "   ----------"

if git rev-parse --is-inside-work-tree &> /dev/null; then
  BRANCH=$(git branch --show-current)
  echo "   Repository: OK"
  echo "   Branch: $BRANCH"

  # Check for uncommitted changes
  if git diff --quiet && git diff --cached --quiet; then
    echo "   Working tree: CLEAN"
  else
    CHANGES=$(git status --porcelain | wc -l | tr -d ' ')
    echo "   Working tree: $CHANGES uncommitted changes"
  fi

  # Check for .beads in gitignore (should NOT be ignored)
  if git check-ignore -q .beads 2>/dev/null; then
    echo "   WARN: .beads is gitignored (should be tracked)"
  fi
else
  echo "   Repository: NOT INITIALIZED"
fi
```

**6. Summary**
```bash
echo ""
echo "=== SUMMARY ==="
echo ""

# Determine overall health
HEALTH="HEALTHY"
ISSUES=""

if ! command -v bd &> /dev/null; then
  HEALTH="CRITICAL"
  ISSUES="$ISSUES\n- bd CLI not installed"
fi

if [ ! -d ".beads" ]; then
  HEALTH="CRITICAL"
  ISSUES="$ISSUES\n- Beads not initialized"
fi

if [ ! -f ".claude/lib/workflow-precheck.sh" ]; then
  if [ "$HEALTH" != "CRITICAL" ]; then
    HEALTH="DEGRADED"
  fi
  ISSUES="$ISSUES\n- Precheck library missing"
fi

echo "Overall: $HEALTH"

if [ -n "$ISSUES" ]; then
  echo ""
  echo "Issues found:"
  echo -e "$ISSUES"
  echo ""
  echo "Run /workflow-init to fix configuration issues"
fi
```

---

### When to Use

- Diagnosing workflow command failures
- After environment changes
- Before starting a complex workflow
- Troubleshooting "weird" behavior

### Output Levels

| Level | Meaning |
|-------|---------|
| HEALTHY | All systems operational |
| DEGRADED | Non-critical issues present |
| CRITICAL | Workflow cannot function |

### Follow-Up Actions

| Issue | Action |
|-------|--------|
| bd CLI missing | Install Beads CLI |
| .beads not initialized | Run `/workflow-init` |
| Database corrupted | See recovery procedures in CLAUDE.md |
| Stale issues | Review with `bd stale` |
| Blocked issues | Review dependencies with `bd blocked` |

**Example usage:**
```
/workflow-health
# Outputs comprehensive health report
```
