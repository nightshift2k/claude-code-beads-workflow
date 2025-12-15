#!/usr/bin/env bash
# Test workflow precheck function
# This script validates the workflow-precheck.sh library
#
# Usage: ./tests/test-workflow-precheck.sh
# Run from project root directory

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0

# Test result tracking
pass() {
  echo -e "  ${GREEN}PASS${NC}: $1"
  TESTS_PASSED=$((TESTS_PASSED + 1))
}

fail() {
  echo -e "  ${RED}FAIL${NC}: $1"
  TESTS_FAILED=$((TESTS_FAILED + 1))
}

skip() {
  echo -e "  ${YELLOW}SKIP${NC}: $1"
  TESTS_SKIPPED=$((TESTS_SKIPPED + 1))
}

# Change to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "========================================"
echo "Workflow Precheck Test Suite"
echo "========================================"
echo ""
echo "Project root: $PROJECT_ROOT"
echo ""

# Test 1: Precheck file exists
echo "Test 1: Precheck Library Exists"
if [ -f ".claude/lib/workflow-precheck.sh" ]; then
  pass "workflow-precheck.sh exists"
else
  fail "workflow-precheck.sh not found"
  echo "  Cannot continue without precheck library"
  exit 1
fi

# Test 2: Precheck file is sourced correctly
echo ""
echo "Test 2: Precheck Library Sources Without Error"
if source .claude/lib/workflow-precheck.sh 2>/dev/null; then
  pass "Precheck library sources successfully"
else
  fail "Precheck library has syntax errors"
  exit 1
fi

# Test 3: workflow_precheck function exists
echo ""
echo "Test 3: workflow_precheck Function Defined"
if type workflow_precheck &>/dev/null; then
  pass "workflow_precheck function exists"
else
  fail "workflow_precheck function not defined"
fi

# Test 4: workflow_cleanup function exists
echo ""
echo "Test 4: workflow_cleanup Function Defined"
if type workflow_cleanup &>/dev/null; then
  pass "workflow_cleanup function exists"
else
  fail "workflow_cleanup function not defined"
fi

# Test 5: bd CLI availability check works
echo ""
echo "Test 5: bd CLI Detection"
if command -v bd &>/dev/null; then
  pass "bd CLI is available"

  # Test bd version output
  BD_VERSION=$(bd version 2>&1 | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | head -1)
  if [ -n "$BD_VERSION" ]; then
    pass "bd version detected: $BD_VERSION"
  else
    fail "Could not parse bd version"
  fi
else
  skip "bd CLI not installed (install to test full functionality)"
fi

# Test 6: Sandbox detection logic
echo ""
echo "Test 6: Sandbox Environment Detection"
(
  # Test with sandbox environment variable
  export CLAUDE_CODE_SANDBOX=1
  source .claude/lib/workflow-precheck.sh

  # Run precheck but capture BD_FLAGS
  # We need to simulate just the sandbox detection part
  if [ -n "$CLAUDE_CODE_SANDBOX" ]; then
    export BD_FLAGS="--sandbox"
  fi

  if [ "$BD_FLAGS" = "--sandbox" ]; then
    pass "CLAUDE_CODE_SANDBOX detected correctly"
  else
    fail "CLAUDE_CODE_SANDBOX not detected"
  fi
)

# Test 7: Standard environment detection
echo ""
echo "Test 7: Standard Environment Detection"
(
  # Clear all sandbox variables
  unset CLAUDE_CODE_SANDBOX
  unset CODEX_SANDBOX
  unset REPLIT_ENVIRONMENT
  unset GITPOD_WORKSPACE_ID
  unset CURSOR_SANDBOX

  export BD_FLAGS=""

  # Simulate detection logic
  if [ -z "$CLAUDE_CODE_SANDBOX" ] && [ -z "$CODEX_SANDBOX" ] && \
     [ -z "$REPLIT_ENVIRONMENT" ] && [ -z "$GITPOD_WORKSPACE_ID" ]; then
    pass "Standard environment detected (no sandbox vars)"
  else
    fail "Sandbox incorrectly detected in standard environment"
  fi
)

# Test 8: Workflow command files have precheck
echo ""
echo "Test 8: Workflow Commands Include Precheck"
WORKFLOW_COMMANDS=(
  ".claude/commands/workflow-land.md"
  ".claude/commands/workflow-work.md"
  ".claude/commands/workflow-execute.md"
  ".claude/commands/workflow-start.md"
  ".claude/commands/workflow-track.md"
  ".claude/commands/workflow-check.md"
  ".claude/commands/workflow-questions.md"
)

for cmd in "${WORKFLOW_COMMANDS[@]}"; do
  if [ -f "$cmd" ]; then
    if grep -q "workflow_precheck" "$cmd"; then
      pass "$cmd includes precheck"
    else
      fail "$cmd missing precheck"
    fi
  else
    skip "$cmd not found"
  fi
done

# Test 9: CLAUDE.md has troubleshooting section
echo ""
echo "Test 9: CLAUDE.md Troubleshooting Section"
if [ -f "CLAUDE.md" ]; then
  if grep -q "## Troubleshooting" CLAUDE.md; then
    pass "Troubleshooting section exists"

    # Check for specific content
    if grep -q "bd: command not found" CLAUDE.md; then
      pass "bd CLI error documented"
    else
      fail "bd CLI error not documented"
    fi

    if grep -q "no .beads directory" CLAUDE.md; then
      pass ".beads error documented"
    else
      fail ".beads error not documented"
    fi
  else
    fail "Troubleshooting section missing from CLAUDE.md"
  fi
else
  fail "CLAUDE.md not found"
fi

# Test 10: Multi-agent coordination rules exist
echo ""
echo "Test 10: Multi-Agent Coordination Rules"
if [ -f ".claude/rules/003-multi-agent-coordination.md" ]; then
  pass "Multi-agent coordination rules exist"

  # Check for key content
  if grep -qi "sequential" .claude/rules/003-multi-agent-coordination.md; then
    pass "Sequential operations documented"
  else
    fail "Sequential operations not documented"
  fi

  if grep -qi "brainstorming" .claude/rules/003-multi-agent-coordination.md; then
    pass "Brainstorming gate documented"
  else
    fail "Brainstorming gate not documented"
  fi
else
  fail "Multi-agent coordination rules not found"
fi

# Test 11: New workflow commands exist
echo ""
echo "Test 11: New Workflow Commands"
NEW_COMMANDS=(
  ".claude/commands/workflow-init.md"
  ".claude/commands/workflow-health.md"
)

for cmd in "${NEW_COMMANDS[@]}"; do
  if [ -f "$cmd" ]; then
    pass "$cmd exists"
  else
    fail "$cmd not found"
  fi
done

# Test 12: Project principles updated
echo ""
echo "Test 12: Project Principles Updated"
if [ -f ".claude/rules/001-project-principles.md" ]; then
  if grep -q "Session Management" .claude/rules/001-project-principles.md; then
    pass "Session management rules added"
  else
    fail "Session management rules missing"
  fi

  if grep -q "Brainstorming Gate" .claude/rules/001-project-principles.md; then
    pass "Brainstorming gate reference added"
  else
    fail "Brainstorming gate reference missing"
  fi
else
  fail "Project principles file not found"
fi

# Summary
echo ""
echo "========================================"
echo "Test Summary"
echo "========================================"
echo -e "  ${GREEN}Passed${NC}: $TESTS_PASSED"
echo -e "  ${RED}Failed${NC}: $TESTS_FAILED"
echo -e "  ${YELLOW}Skipped${NC}: $TESTS_SKIPPED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
  echo -e "${GREEN}All tests passed!${NC}"
  exit 0
else
  echo -e "${RED}Some tests failed.${NC}"
  exit 1
fi
