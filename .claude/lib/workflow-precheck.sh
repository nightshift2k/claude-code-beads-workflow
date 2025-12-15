#!/usr/bin/env bash
# Workflow precheck function - validates environment before workflow execution
# Source this file in all workflow commands: source .claude/lib/workflow-precheck.sh
#
# Technology-agnostic: Works with any language/framework project using Beads

# Validate environment before workflow execution
workflow_precheck() {
  local COMMAND_NAME="${1:-workflow}"

  echo "Running workflow prechecks for: $COMMAND_NAME"
  echo ""

  # Check 1: bd CLI availability
  if ! command -v bd &> /dev/null; then
    echo "CRITICAL: bd CLI not found in PATH"
    echo ""
    echo "   The Beads CLI (bd) is required for workflow tracking."
    echo ""
    echo "   Installation options:"
    echo "   1. Go install: go install github.com/steveyegge/beads/cmd/bd@latest"
    echo "   2. Homebrew (macOS): brew install steveyegge/tap/beads"
    echo "   3. See: https://github.com/steveyegge/beads/blob/main/docs/INSTALLING.md"
    echo ""
    echo "   After installation, verify with: bd version"
    echo ""
    return 1
  fi

  # Check 2: bd version
  BD_VERSION=$(bd version 2>&1 | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | head -1)
  echo "bd CLI found: $BD_VERSION"

  # Check 3: .beads directory existence
  if [ ! -d ".beads" ]; then
    echo "WARNING: No .beads directory found in $(pwd)"
    echo ""
    echo "   This project has not been initialized for Beads tracking."
    echo ""
    echo -n "   Initialize now? (Y/n): "
    read -r INIT_RESPONSE

    if [ "$INIT_RESPONSE" = "n" ] || [ "$INIT_RESPONSE" = "N" ]; then
      echo ""
      echo "ERROR: Cannot proceed without Beads initialization."
      echo "   Run 'bd init' manually when ready."
      echo ""
      return 1
    fi

    echo ""
    echo "   Initializing Beads..."
    if bd init --quiet; then
      echo "Beads initialized successfully"
    else
      echo "ERROR: Beads initialization failed"
      echo "   Try manually: bd init"
      return 1
    fi
  else
    echo ".beads directory found"
  fi

  # Check 4: Sandbox mode (Claude Code always sandboxed)
  # Always use --sandbox flag to ensure reliable operation
  BD_FLAGS="--sandbox"
  export BD_FLAGS
  echo "INFO: Using sandbox mode (daemon and auto-sync disabled)"
  echo "   (Required for Claude Code compatibility)"

  # Check 5: Database integrity (quick check)
  if ! bd $BD_FLAGS list --limit 1 &> /dev/null; then
    echo "WARNING: Database health check failed"
    echo "   This may indicate corruption or sync issues."
    echo ""
    echo -n "   Attempt recovery from JSONL? (y/N): "
    read -r RECOVERY_RESPONSE

    if [ "$RECOVERY_RESPONSE" = "y" ] || [ "$RECOVERY_RESPONSE" = "Y" ]; then
      echo ""
      echo "   Backing up database..."
      mkdir -p .beads/backup
      cp .beads/*.db .beads/backup/ 2>/dev/null || true

      echo "   Attempting recovery..."
      rm .beads/*.db 2>/dev/null || true
      bd init --quiet
      bd import -i .beads/issues.jsonl

      echo "Recovery complete"
    else
      echo ""
      echo "ERROR: Database issues detected. Workflow may fail."
      echo "   See: https://github.com/steveyegge/beads/blob/main/docs/TROUBLESHOOTING.md#database-issues"
      return 1
    fi
  fi

  echo ""
  echo "All prechecks passed - workflow ready"
  echo ""
  return 0
}

# Cleanup function for interrupted workflows
# Saves state and attempts sync when workflow is interrupted
workflow_cleanup() {
  local EXIT_CODE=$?
  local WORKFLOW_NAME="${1:-unknown}"

  if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "WARNING: Workflow interrupted: $WORKFLOW_NAME (exit code: $EXIT_CODE)"
    echo ""

    # Find in-progress issues
    IN_PROGRESS=$(bd $BD_FLAGS list --status in_progress --json 2>/dev/null | \
      jq -r '.[].id' 2>/dev/null | head -1)

    if [ -n "$IN_PROGRESS" ]; then
      echo "   Saving state for in-progress issue: $IN_PROGRESS"
      bd $BD_FLAGS update "$IN_PROGRESS" \
        --note "Session interrupted at $(date -Iseconds)" \
        --json > /dev/null 2>&1 || true
      echo "   State saved"
    fi

    # Attempt sync
    echo ""
    echo "   Attempting sync..."
    if bd $BD_FLAGS sync 2>&1 | grep -q "success\|Sync complete\|up to date"; then
      echo "   Sync successful"
    else
      echo "   WARNING: Sync may have failed - run 'bd sync' manually"
    fi

    echo ""
    echo "   Resume work with: /workflow-work"
    echo ""
  fi

  exit $EXIT_CODE
}

# Quick diagnostic function for troubleshooting
# Use this in troubleshooting sections instead of duplicating checks
workflow_quick_diagnose() {
  local CONTEXT="${1:-general}"

  echo "=== Quick Diagnostics ($CONTEXT) ==="
  echo ""

  # Check 1: bd CLI
  if command -v bd &> /dev/null; then
    echo "bd CLI: OK ($(bd version 2>&1 | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | head -1))"
  else
    echo "bd CLI: MISSING - install from https://github.com/steveyegge/beads"
    return 1
  fi

  # Check 2: .beads directory
  if [ -d ".beads" ]; then
    echo ".beads/: OK"
  else
    echo ".beads/: MISSING - run /workflow-init"
    return 1
  fi

  # Check 3: Database responds
  if bd ${BD_FLAGS:-} list --limit 1 &> /dev/null; then
    echo "Database: RESPONDING"
  else
    echo "Database: NOT RESPONDING - try 'bd import --force'"
    return 1
  fi

  # Check 4: Issue counts
  OPEN=$(bd ${BD_FLAGS:-} list --status open --json 2>/dev/null | jq '. | length' 2>/dev/null || echo "?")
  IN_PROGRESS=$(bd ${BD_FLAGS:-} list --status in_progress --json 2>/dev/null | jq '. | length' 2>/dev/null || echo "?")
  echo "Issues: $OPEN open, $IN_PROGRESS in-progress"

  echo ""
  echo "For comprehensive diagnostics, run: /workflow-health"
  echo ""
  return 0
}

# Export functions for use in sourced scripts
export -f workflow_precheck 2>/dev/null || true
export -f workflow_cleanup 2>/dev/null || true
export -f workflow_quick_diagnose 2>/dev/null || true
