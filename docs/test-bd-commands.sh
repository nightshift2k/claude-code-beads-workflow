#!/bin/bash
# test-bd-commands.sh - Quality gate test script for bd command snippets
# Implements CLAUDE.md Prime Directive: validate all bd commands before documentation
#
# Usage: ./docs/test-bd-commands.sh
#
# Exit codes:
#   0 = all tests pass
#   1 = one or more tests failed

set -e

# Create isolated test environment
TEST_DIR=$(mktemp -d)
ORIG_DIR=$(pwd)

cleanup() {
  cd "$ORIG_DIR"
  rm -rf "$TEST_DIR"
}
trap cleanup EXIT

cd "$TEST_DIR"

# Initialize isolated git + Beads environment
git init --quiet
git config user.email "test@test.com"
git config user.name "Test"
bd init -p test- --quiet

echo "=== bd Command Quality Gate Tests ==="
echo ""

# Create test fixtures
echo "Creating test fixtures..."
EPIC_ID=$(bd create "Test Epic" -t epic -p 1 --json | jq -r '.id')
CHILD1=$(bd create "Child 1" --parent "$EPIC_ID" --force -t task -p 2 --json | jq -r '.id')
CHILD2=$(bd create "Child 2" --parent "$EPIC_ID" --force -t task -p 2 --json | jq -r '.id')
bd update "$EPIC_ID" --status in_progress --json > /dev/null
bd close "$CHILD1" --reason "Test complete" --json > /dev/null

PASS=0
FAIL=0

run_test() {
  local name="$1"
  local result="$2"
  local expected="$3"

  if [ "$result" = "$expected" ]; then
    echo "  [PASS] $name"
    PASS=$((PASS + 1))
  else
    echo "  [FAIL] $name (got: $result, expected: $expected)"
    FAIL=$((FAIL + 1))
  fi
}

echo ""
echo "Running tests..."
echo ""

# Test 1: bd create returns object
echo "Test 1: bd create returns object"
TYPE=$(bd create "Temp" -t task --json | jq -r 'type')
run_test "bd create returns object" "$TYPE" "object"

# Test 2: bd list returns array
echo "Test 2: bd list returns array"
TYPE=$(bd list --json | jq -r 'type')
run_test "bd list returns array" "$TYPE" "array"

# Test 3: bd show returns array
echo "Test 3: bd show returns array"
TYPE=$(bd show "$EPIC_ID" --json | jq -r 'type')
run_test "bd show returns array" "$TYPE" "array"

# Test 4: bd ready returns array
echo "Test 4: bd ready returns array"
TYPE=$(bd ready --json | jq -r 'type')
run_test "bd ready returns array" "$TYPE" "array"

# Test 5: bd update returns array
echo "Test 5: bd update returns array"
TYPE=$(bd update "$CHILD2" --notes "Test note" --json | jq -r 'type')
run_test "bd update returns array" "$TYPE" "array"

# Test 6: jq .[0].id extraction from bd show
echo "Test 6: jq .[0].id extraction from bd show"
ID=$(bd show "$EPIC_ID" --json | jq -r '.[0].id // "none"')
run_test ".[0].id extraction works" "$ID" "$EPIC_ID"

# Test 7: jq .[].id extraction from bd list
echo "Test 7: jq .[].id extraction from bd list"
COUNT=$(bd list --json | jq -r '.[].id' | wc -l | tr -d ' ')
[ "$COUNT" -ge 4 ] && RESULT="pass" || RESULT="fail"
run_test ".[].id extraction returns multiple IDs" "$RESULT" "pass"

# Test 8: --type filter works
echo "Test 8: --type filter works"
EPIC_COUNT=$(bd list --type epic --json | jq 'length')
[ "$EPIC_COUNT" -ge 1 ] && RESULT="pass" || RESULT="fail"
run_test "--type epic filter works" "$RESULT" "pass"

# Test 9: --status filter works
echo "Test 9: --status filter works"
CLOSED_COUNT=$(bd list --status closed --json | jq 'length')
[ "$CLOSED_COUNT" -ge 1 ] && RESULT="pass" || RESULT="fail"
run_test "--status closed filter works" "$RESULT" "pass"

# Test 10: Hierarchical IDs created correctly
echo "Test 10: Hierarchical IDs created correctly"
CHILD_PATTERN="${EPIC_ID}."
HAS_DOT=$(echo "$CHILD1" | grep -c '\.' || true)
[ "$HAS_DOT" -ge 1 ] && RESULT="pass" || RESULT="fail"
run_test "Child IDs have hierarchical format (epic.N)" "$RESULT" "pass"

echo ""
echo "=== Results ==="
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo ""

if [ "$FAIL" -eq 0 ]; then
  echo "All tests passed! Quality gate APPROVED."
  exit 0
else
  echo "Quality gate FAILED. Fix documentation snippets before proceeding."
  exit 1
fi
