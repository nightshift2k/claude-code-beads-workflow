# Agentic Workflow - Validation Test

This document provides a complete test to validate the agentic workflow. Follow these steps exactly in a fresh Claude Code instance.

## Purpose

Build a Python CLI task manager (`pydo`) while exercising every workflow command. This validates:

- Beads issue tracking integrates properly
- Workflow commands produce expected results
- Error recovery works
- Multi-session continuity functions correctly

---

## Part 1: Prerequisites (Before Anything Else)

### 1.1 Check Required Tools

Run these in your terminal FIRST:

```bash
# Check Beads CLI (minimum version: 0.37.0, recommended: 0.39.1+)
bd version
# Expected: bd version 0.37.0 or higher

# Check uv (Python package manager, minimum version: 0.1.0)
uv --version
# Expected: uv 0.1.0 or higher

# Check Python via uv (minimum version: 3.9)
uv python list
# Expected: Shows available Python versions (3.9+)

# Check Git (minimum version: 2.0)
git --version
# Expected: git version 2.0 or higher
```

**If tools are missing, install them:**

- **bd (Beads CLI)**:

  ```bash
  # Via Go
  go install github.com/steveyegge/beads/cmd/bd@latest
  export PATH="$PATH:$(go env GOPATH)/bin"

  # Or via Homebrew (macOS)
  brew install steveyegge/tap/beads
  ```

  Reference: https://github.com/steveyegge/beads

- **uv (Python package manager)**:

  ```bash
  # Via curl (Unix)
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # Or via Homebrew (macOS)
  brew install uv
  ```

  Reference: https://docs.astral.sh/uv/getting-started/installation/

- **Python 3.9+**: If not available, install via `uv python install 3.9` or higher
- **Git 2.0+**: Should be pre-installed on most systems; if not, see https://git-scm.com/downloads

---

## Part 2: Workflow Setup (Still in Regular Terminal)

### 2.1 Create Test Directory

```bash
mkdir -p ~/pydo-validation-test
cd ~/pydo-validation-test
```

### 2.2 Copy Workflow Files

**IMPORTANT:** Set the BOILERPLATE path to your actual workflow source location before running these commands.

```bash
# REQUIRED: Set this to YOUR workflow source location before running
# Uncomment and customize ONE of the examples below:
#   export BOILERPLATE=~/code/claude-code-beads-workflow
#   export BOILERPLATE=/Users/yourname/projects/claude-code-beads-workflow
#   export BOILERPLATE=/path/to/wherever/you/cloned/the/workflow

# Use environment variable, fail with clear error if not set
: "${BOILERPLATE:?ERROR: BOILERPLATE environment variable not set. Set it to your workflow source location before running.}"

# Verify the path exists
if [ ! -d "$BOILERPLATE" ]; then
  echo "ERROR: BOILERPLATE directory not found at: $BOILERPLATE"
  echo "Verify your BOILERPLATE path is correct and the directory exists"
  exit 1
fi

# Verify required files exist
if [ ! -f "$BOILERPLATE/CLAUDE.md.example" ]; then
  echo "ERROR: CLAUDE.md.example not found in $BOILERPLATE"
  exit 1
fi

if [ ! -d "$BOILERPLATE/.claude" ]; then
  echo "ERROR: .claude directory not found in $BOILERPLATE"
  exit 1
fi

# Copy .claude directory (commands, rules, lib)
cp -r "$BOILERPLATE/.claude" ~/pydo-validation-test/

# Copy CLAUDE.md.example to CLAUDE.md (main workflow instructions)
cp "$BOILERPLATE/CLAUDE.md.example" ~/pydo-validation-test/CLAUDE.md

# Copy the pydo design document
mkdir -p ~/pydo-validation-test/docs/plans
cp "$BOILERPLATE/docs/plans/pydo-design.md" ~/pydo-validation-test/docs/plans/

echo "Workflow files copied successfully"
```

### 2.3 Verify Workflow Structure

```bash
cd ~/pydo-validation-test

# Check directory structure
ls -la
# Expected to show:
# .claude/
# docs/
# CLAUDE.md

ls -la .claude/
# Expected to show:
# commands/
# lib/
# rules/

# Verify command files (should be 14 workflow-*.md files)
ls .claude/commands/workflow-*.md | wc -l
# Expected: 14

# Verify key files exist and are non-empty
ls -lh .claude/commands/workflow-*.md | awk '{if ($5 == "0") print "ERROR: " $9 " is empty"; else print "OK: " $9}'

# Verify workflow.py exists and is valid
if [ -f ".claude/lib/workflow.py" ]; then
  echo "OK: workflow.py exists"
  if uv run python -c "import ast; ast.parse(open('.claude/lib/workflow.py').read())" 2>/dev/null; then
    echo "OK: workflow.py is valid Python"
  else
    echo "ERROR: workflow.py has syntax errors"
  fi
else
  echo "ERROR: workflow.py not found"
fi

# Verify pydo-design.md was copied
if [ -f "docs/plans/pydo-design.md" ]; then
  echo "OK: pydo-design.md exists"
  # Check it's not empty
  if [ -s "docs/plans/pydo-design.md" ]; then
    echo "OK: pydo-design.md is non-empty"
  else
    echo "ERROR: pydo-design.md is empty"
  fi
else
  echo "ERROR: pydo-design.md not found"
fi

# Count total files copied (should be around 20-22)
find .claude docs CLAUDE.md -type f | wc -l
# Expected: 20-22 files
```

### 2.4 Customize CLAUDE.md for pydo

Edit `CLAUDE.md` and update the **Project Information** section at the top:

```markdown
## Project Information

<!-- CUSTOMIZE THIS SECTION FOR YOUR PROJECT -->

Project: pydo
Description: CLI task manager with add, list, complete, delete commands
Tech Stack: Python 3.9+, Click, pytest, uv, JSON storage
Design Doc: docs/plans/pydo-design.md

<!-- END CUSTOMIZATION SECTION -->
```

The rest of CLAUDE.md contains generic workflow instructions that work for any project.

### 2.5 Initialize Git

```bash
# Initialize git repository
cd ~/pydo-validation-test
git init

# Stage all workflow files
git add .

# Create initial commit
git commit -m "Initial workflow setup for pydo validation"
```

### 2.6 Checkpoint: Ready for Claude Code

Verify your directory structure:

```
~/pydo-validation-test/
├── .claude/
│   ├── commands/           # 14 workflow-*.md files
│   │   ├── workflow-init.md
│   │   ├── workflow-start.md
│   │   ├── workflow-track.md
│   │   ├── workflow-execute.md
│   │   ├── workflow-work.md
│   │   ├── workflow-land.md
│   │   ├── workflow-check.md
│   │   ├── workflow-do.md
│   │   ├── workflow-health.md
│   │   ├── workflow-overview.md
│   │   ├── workflow-config.md
│   │   ├── workflow-question-ask.md
│   │   ├── workflow-steer-research.md
│   │   └── workflow-steer-correct.md
│   ├── lib/                # Shared utilities
│   │   └── workflow.py     # Python workflow CLI tool (stdlib only)
│   └── rules/              # Project rules
│       ├── project-principles.md
│       ├── multi-agent-coordination.md
│       ├── beads-patterns.md
│       ├── agent-dispatch.md
│       └── git-conventions.md
├── docs/
│   └── plans/
│       └── pydo-design.md
└── CLAUDE.md
```

---

## Part 3: Launch Claude Code

Now that setup is complete, launch Claude Code:

### 3.1 Start Claude Code Session

```bash
# Change to test directory
cd ~/pydo-validation-test

# Launch Claude Code
claude
```

**Session Recording:** Run `/export` before exiting to save a clean transcript.

---

## Part 4: Project Initialization (Inside Claude Code)

### 4.1 Initialize Workflow Environment

**Command to Claude:**

```
/workflow-init
```

**Expected behavior:**

- Creates `.beads/` directory if missing
- Validates environment (bd CLI, Python)
- Reports "Environment ready for agentic workflow"

**Checkpoint:** Verify `.beads/` directory exists:

```bash
# Verify .beads directory was created
ls -la .beads/
# Expected: beads.db, config.yaml, metadata.json, README.md, .gitignore
# Note: issues.jsonl appears after first issue is created

# Verify prefix follows naming rules
bd config | grep prefix
# Expected: Shows prefix like "pydo-" (lowercase, starts with letter, ends with hyphen)
```

### 4.2 Create Feature Epic

**Command to Claude:**

```
/workflow-start Build pydo - a Python CLI task manager with add, list, complete, delete commands and priority support
```

**Expected behavior:**

- Creates a Beads epic issue
- Returns epic ID (e.g., `pydo-abc`)
- Epic is now trackable with `bd show <id>`

**Checkpoint:** Verify epic created:

```bash
# List all Beads issues
bd list --json
# Expected: Shows the newly created epic with type="epic"

# Save the epic ID for later use
EPIC_ID=$(bd list --json | jq -r '.[0].id')
echo "Epic ID: $EPIC_ID"
```

Record the epic ID: `____________`

---

## Part 5: Implementation Planning

### 5.1 Create Implementation Plan

The design document `docs/plans/pydo-design.md` (copied in Part 2) contains the full specification. Now ask Claude to create an implementation plan from it.

**Command to Claude:**

```
I have a design document at docs/plans/pydo-design.md for a CLI task manager called pydo.

Please read the design document and create a detailed implementation plan using the superpowers:writing-plans skill.

The plan should have bite-sized tasks with proper dependencies, following TDD (write test, run to fail, implement, run to pass, commit).
```

**Expected behavior:**

- Claude reads pydo-design.md
- Uses the writing-plans skill
- Creates implementation plan with 6-8 tasks
- Each task has exact file paths, code examples, and test commands
- Plan saved to `docs/plans/` directory (e.g., `pydo-implementation-plan.md`)

**Note on Plan File Lifecycle:**
The plan file is TEMPORARY. After `/workflow-track`:

- Plan content is stored in epic description
- Plan file is DELETED
- Use `/workflow-overview` to see plan state

**Checkpoint:** Verify plan exists:

```bash
# List all plan documents
ls docs/plans/
# Expected: pydo-design.md and the new implementation plan

# Preview first 50 lines of implementation plan
cat docs/plans/pydo-implementation-plan.md | head -50
# Expected: Shows task breakdown with file paths and test commands
```

---

## Part 6: Issue Tracking Setup

### 6.1 Convert Plan to Beads Issues

**Command to Claude:**

```
/workflow-track docs/plans/pydo-implementation-plan.md
```

(Adjust path if your implementation plan has a different name)

**Expected behavior:**

- Claude reads the specified implementation plan
- Creates Beads issues for each task
- Sets up dependency relationships
- Links all issues to the feature epic

**Checkpoint:** Verify issues created with dependencies:

```bash
# List all issues with details
bd list --json | head -50
# Expected: Shows multiple task issues linked to epic

# Check blocked issues (tasks waiting on dependencies)
bd blocked
# Expected: Shows tasks blocked by incomplete dependencies

# Check ready issues (tasks with no blockers)
bd ready
# Expected: Shows at least one ready task (likely project setup)
```

Record number of issues created: `____________`

---

## Part 7: Implementation Phase

You have two options for implementation: **automated** (recommended) or **manual**. Choose one approach.

### Option A: Automated Execution (Recommended)

This uses the `superpowers:executing-plans` skill with domain-specific agents for higher quality output.

**Expected Duration:** 10-20 minutes for the pydo project (5-8 tasks).

**Command to Claude:**

```
/workflow-execute docs/plans/pydo-implementation-plan.md
```

(Adjust path if your implementation plan has a different name)

**Expected behavior:**

- Invokes the `superpowers:executing-plans` skill
- Uses `python-expert` agent for Python implementation
- Follows TDD workflow (test first, run to fail, implement, run to pass)
- Updates Beads issue status automatically as it progresses
- Creates follow-up issues for any discoveries
- Commits after each major task

**Progress Indicators to Watch For:**

During execution, expect to see:

1. Task batch announcements (e.g., "Batch 1: Setting up project structure")
2. TDD cycle messages (e.g., "Writing test for Task model", "Test failed as expected", "Implementing model", "Test passed")
3. Beads status updates (e.g., "Marking bd-xxx.1 as in_progress", "Closing bd-xxx.1 as completed")
4. Git commits after major milestones
5. Batch completion summaries with next steps

**Checkpoint during execution:**

```bash
# In another terminal window, monitor progress:
bd list --status in_progress --json  # See current work
bd list --status completed --json    # See completed work

# Watch for file creation:
watch -n 5 'find pydo -type f 2>/dev/null | wc -l'
```

Skip to **7.4 Run Tests** after execution completes.

---

### Option B: Manual Implementation

Use this approach if you want fine-grained control over each task.

#### 7.1 Find Available Work

**Command to Claude:**

```
/workflow-work
```

**Expected behavior:**

- Shows ready (unblocked) issues
- Recommends which to work on first
- Waits for you to select one

**Checkpoint:** At least one issue should be ready (likely project setup).

#### 7.2 Implement First Task

**Command to Claude:**

```
Implement the first ready task (project setup - pyproject.toml and directory structure)
```

**Expected behavior:**

- Claude claims the issue (`bd update <id> --status in_progress`)
- Creates project structure
- Creates pyproject.toml with dependencies
- Marks issue complete when done

**Checkpoint:** Verify files created:

```bash
# List pydo directory structure
ls -la pydo/
# Expected: Shows pydo package directory

# Verify pyproject.toml configuration
cat pyproject.toml
# Expected: Shows project dependencies (click, pytest, etc.)
```

#### 7.3 Continue Implementation

**Command to Claude:**

```
/workflow-work
```

Then implement each task in order. For each task:

1. Claude should claim the issue
2. Implement the code
3. Write tests for it
4. Mark complete when done

**Key tasks to implement:**

- [ ] models.py - Task dataclass
- [ ] exceptions.py - Custom exceptions
- [ ] storage.py - JSON persistence
- [ ] cli.py - Click commands
- [ ] tests/ - Test suite

**Checkpoint after each task:**

```bash
# See completed work
bd list --status completed --json

# See what's next
bd ready --json
# Expected: Shows next unblocked task
```

---

### 7.4 Run Tests

After cli.py is complete:

**Command to Claude:**

```
Run the test suite and fix any failures
```

**Expected behavior:**

- Installs dependencies if needed (via uv)
- Runs pytest
- All tests pass (or Claude fixes failures)

**Checkpoint:**

```bash
# Navigate to pydo directory, install dependencies, and run tests
cd pydo && uv sync && uv run pytest -v
# Expected: All tests pass with green output
```

---

## Part 8: Session Management

### 8.1 Mid-Session Status Check

**Command to Claude:**

```
/workflow-check
```

**Expected behavior:**

- Shows summary of open/completed issues
- Shows any blocked work
- Identifies what's left to do

### 8.2 Proper Session Landing

**Command to Claude:**

```
/workflow-land
```

**Expected behavior:**

- Creates issues for any discovered follow-up work
- Closes all completed issues with reasons
- Updates in-progress issues with notes
- Runs `bd sync --flush-only` (sandbox mode) to export changes to JSONL
- Optionally commits to git

**Checkpoint:**

```bash
# Verify all issues have updated status
bd list --json
# Expected: All issues show correct status (completed, in_progress, etc.)

# Verify JSONL file exists and contains issues
ls -lh .beads/issues.jsonl
# Expected: Shows non-empty file
```

---

## Part 9: Steering & Course Correction

This critical test verifies that steering mandates structural changes.

### Why These Outcomes Are Mandatory

This test validates the core steering contract:

1. **Block tasks** - Research must identify affected work that cannot proceed until resolved
2. **Rewrite tasks** - Research findings must change implementation approach (not just add notes)
3. **Add tasks** - Research complexity requires new work items (schema design, migration, etc.)

Missing any outcome means steering failed to maintain plan integrity.
Partial steering (adding notes without rewriting) defeats the steering mechanism's purpose.

### 9.1 Inject Research Question

After completing Tasks 1-2 (setup, models), but BEFORE completing Task 3 (storage):

**Command to Claude:**

```
/workflow-question-ask The pydo design specifies JSON file storage, but we've discovered it will be used in CI/CD pipelines where multiple agents may update tasks concurrently. This introduces race conditions with JSON. Should we switch to SQLite with proper locking?
```

**Expected behavior:**

- Creates research issue blocking storage task
- Stores full context in issue description

**Checkpoint - Verify blocking:**

```bash
RESEARCH_ID=$(bd list --json | jq -r '[.[] | select(.title | contains("Research:"))][0].id')
if [ -z "$RESEARCH_ID" ]; then
  echo "ERROR: No research issue found - /workflow-question-ask may have failed"
  exit 1
fi
echo "Research issue: $RESEARCH_ID"

# Verify it blocks something
BLOCKED=$(bd show $RESEARCH_ID --json | jq '.[0].blocks | length')
echo "Blocked tasks: $BLOCKED"
# Expected: >= 1
```

### 9.2 Resolve Research (Forces Modification)

**Command to Claude:**

```
/workflow-steer-research $RESEARCH_ID
```

**Expected behavior:**

- Research concludes SQLite is necessary
- Storage task REWRITTEN (JSON → SQLite)
- New tasks ADDED (schema, migration)
- Steering log UPDATED in epic

**Checkpoint - Verify mandatory outcomes:**

```bash
# Requirement 1: Tasks were blocked (already verified above)

# Requirement 2: Storage task rewritten
STORAGE_TASK=$(bd list --json | jq -r --arg prefix "$EPIC_ID." '[.[] | select(.id | startswith($prefix)) | select(.title | contains("storage") or .title | contains("Storage"))][0].id')
if [ -z "$STORAGE_TASK" ]; then
  echo "ERROR: No storage task found under epic"
  exit 1
fi
STORAGE_DESC=$(bd show $STORAGE_TASK --json | jq -r '.[0].description')
if echo "$STORAGE_DESC" | grep -qi "sqlite"; then
  echo "PASS: Storage task rewritten for SQLite"
else
  echo "FAIL: Storage task should mention SQLite"
fi

# Requirement 3: New tasks added
NEW_TASKS=$(bd list --json | jq --arg prefix "$EPIC_ID." '[.[] | select(.id | startswith($prefix)) | select(.title | test("schema|migration|Schema|Migration"; "i"))] | length')
if [ "$NEW_TASKS" -ge 1 ]; then
  echo "PASS: New tasks added ($NEW_TASKS found)"
else
  echo "FAIL: Should have added schema or migration tasks"
fi

# Bonus: Verify steering log updated
EPIC_DESC=$(bd show $EPIC_ID --json | jq -r '.[0].description')
if echo "$EPIC_DESC" | grep -q "STEER:"; then
  echo "PASS: Steering log contains STEER entry"
else
  echo "FAIL: Steering log should have STEER entry"
fi
```

### 9.3 View Plan State

**Command to Claude:**

```
/workflow-overview $EPIC_ID --log
```

**Expected behavior:**

- Shows steering log with INIT and STEER entries
- Visible record of what changed

**Checkpoint:**

```bash
# Verify /workflow-overview shows log
/workflow-overview $EPIC_ID --log
# Expected: Shows INIT and STEER entries
```

### 9.4 Course Correction

After steering resolves, apply a course correction:

**Command to Claude:**

```
/workflow-steer-correct $EPIC_ID
```

When prompted for correction, enter:

```
The schema task should include indexes for priority-based queries
```

**Expected behavior:**

- Creates P0 correction task
- Updates affected tasks
- CORRECT entry added to steering log

**Checkpoint:**

```bash
# Verify CORRECT entry in log
EPIC_DESC=$(bd show $EPIC_ID --json | jq -r '.[0].description')
if echo "$EPIC_DESC" | grep -q "CORRECT:"; then
  echo "PASS: Steering log contains CORRECT entry"
else
  echo "FAIL: Steering log should have CORRECT entry"
fi

# Verify correction task is P0
CORRECTION=$(bd list --json | jq -r --arg prefix "$EPIC_ID." '.[] | select(.id | startswith($prefix)) | select(.title | contains("Correction") or .title | contains("correction")) | .priority')
if [ "$CORRECTION" = "0" ]; then
  echo "PASS: Correction task is P0"
else
  echo "FAIL: Correction task should be P0"
fi
```

### 9.5 Test Health Diagnostics

**Command to Claude:**

```
/workflow-health
```

**Expected behavior:**

- Checks environment (bd CLI, Python, git)
- Reports flag status (team-mode, strict-quality)
- Validates .beads/ directory
- All checks should pass

### 9.6 Test Configuration Management

**Command to Claude:**

```
/workflow-config --list
```

**Expected behavior:**

- Shows all flags with current status
- Both flags disabled by default

**Command to Claude:**

```
/workflow-config team-mode on
```

**Expected behavior:**

- Creates flag file
- Reports "Flag 'team-mode' ENABLED"

**Checkpoint:**

```bash
# Verify flag file created
if [ -f ".claude/ccbw-flag-team-mode" ]; then
  echo "PASS: team-mode flag file exists"
else
  echo "FAIL: team-mode flag file not created"
fi
```

**Command to Claude:**

```
/workflow-config team-mode off
```

**Expected behavior:**

- Removes flag file
- Reports "Flag 'team-mode' disabled"

**Checkpoint:**

```bash
# Verify flag file removed
if [ ! -f ".claude/ccbw-flag-team-mode" ]; then
  echo "PASS: team-mode flag file removed"
else
  echo "FAIL: team-mode flag file still exists"
fi
```

---

## Part 10: Final Validation

### 10.1 Verify Complete Implementation

```bash
# Navigate to pydo and install dependencies via uv
cd pydo
uv sync

# Test all commands work (via uv run)
# Add a high-priority task
uv run pydo add "Test task" -p 1

# Add a low-priority task
uv run pydo add "Another task" -p 3

# List all active tasks
uv run pydo list

# Show details of a specific task (replace <id-from-list> with actual ID)
uv run pydo show <id-from-list>

# Mark a task as complete
uv run pydo complete <id>

# List all tasks including completed ones
uv run pydo list --all

# Delete a task
uv run pydo delete <id>
```

### 10.2 Verify Beads State

```bash
# All issues should be closed or have clear status
bd list --json
# Expected: All issues show appropriate final status

# Check for any orphaned work
bd ready --json
# Expected: Empty array if all work completed

bd blocked --json
# Expected: Empty array if all work completed

# Verify epic is complete (replace <epic-id> with actual ID from Part 4.2)
bd show <epic-id>
# Expected: Shows epic with all child tasks completed
```

### 10.3 Final Checklist

Check each item that worked correctly:

**Workflow Commands (All 14):**

- [ ] `/workflow-init` - Environment initialized correctly
- [ ] `/workflow-start` - Epic created with proper tracking
- [ ] `/workflow-track` - Plan converted to issues with dependencies
- [ ] `/workflow-execute` - Automated plan execution worked (or skipped if using manual approach)
- [ ] `/workflow-work` - Found and claimed available work
- [ ] `/workflow-check` - Status review worked
- [ ] `/workflow-do` - Isolated task execution worked (without epic overhead)
- [ ] `/workflow-land` - Session closed properly with sync
- [ ] `/workflow-health` - Diagnostics ran and reported accurately
- [ ] `/workflow-question-ask` - Research question captured and issue created
- [ ] `/workflow-steer-research` - Research issue resolved and tasks updated
- [ ] `/workflow-steer-correct` - Course correction applied with CORRECT log entry
- [ ] `/workflow-overview` - Plan state displayed correctly
- [ ] `/workflow-config` - Flag management worked correctly

**Epic-Centric Plan Management:**

- [ ] Plan file deleted after /workflow-track
- [ ] Epic description contains full plan content
- [ ] Steering log has INIT entry
- [ ] Steering log has STEER entry (after research)
- [ ] Steering log has CORRECT entry (after correction)
- [ ] /workflow-overview shows plan state

**Beads Integration:**

- [ ] Issues created with proper types (epic, task)
- [ ] Issue hierarchy works (epic → child tasks with --parent)
- [ ] Dependencies tracked correctly (blocked/ready)
- [ ] Issue status updates worked
- [ ] `bd sync --flush-only` exported changes to JSONL
- [ ] Issue closure with reasons worked

**Steering Outcomes (Mandatory):**

- [ ] Research blocked affected tasks
- [ ] Research rewrote task descriptions (not just notes)
- [ ] Research added new tasks (schema, migration)
- [ ] Correction task created as P0

**Implementation Quality:**

- [ ] pydo commands all work
- [ ] Tests pass
- [ ] Code is organized as specified

---

## Part 11: Session Wrap-up

### 11.1 Export Session (Optional)

Before exiting Claude Code, optionally export the session transcript:

```
/export
```

This saves a clean, readable transcript of the session. Choose a filename like `pydo-validation-session.md`.

Then exit Claude Code:

```bash
# Type 'exit' or press Ctrl+D to exit Claude Code
exit
```

### 11.2 Collect Artifacts

Gather these files for analysis:

1. Exported session transcript (if created with `/export`)
2. `.beads/issues.jsonl` - Issue tracking state
3. `docs/plans/*.md` - Implementation plan created
4. `pydo/` - The implemented project

### 11.3 Share for Analysis

Return to the original Claude Code session with:

1. The session log (or key excerpts if very long)
2. Summary of checkboxes from section 10.3
3. Any issues or friction points encountered

---

## Appendix A: Expected Issue Structure

After `/workflow-track`, your Beads issues should look approximately like:

```
pydo-abc (epic): Build pydo CLI task manager
├── pydo-abc.1 (task): Set up project structure
├── pydo-abc.2 (task): Implement Task model [depends: abc.1]
├── pydo-abc.3 (task): Implement exceptions [depends: abc.1]
├── pydo-abc.4 (task): Implement storage layer [depends: abc.2, abc.3]
├── pydo-abc.5 (task): Implement CLI commands [depends: abc.4]
├── pydo-abc.6 (task): Write test suite [depends: abc.5]
└── pydo-abc.7 (task): Documentation and polish [depends: abc.6]
```

## Appendix B: Troubleshooting

### "bd: command not found"

```bash
# Install via Go
go install github.com/steveyegge/beads/cmd/bd@latest

# Add to PATH
export PATH="$PATH:$(go env GOPATH)/bin"
```

### "no .beads directory found"

```bash
# Initialize Beads in current directory
bd init --quiet
```

### "database out of sync"

```bash
# Rebuild database from JSONL
bd import --force

# Note: Beads v0.21.1+ auto-detects sandbox mode in Claude Code
# No --sandbox flag needed - it's detected automatically
```

### Tests fail to run

```bash
# Navigate to pydo directory
cd pydo

# Install all dependencies via uv
uv sync

# Run tests via uv
uv run pytest -v
```

---

## Alternative: Migration Test Path

This section validates migrating an existing project to the workflow.

### Setup: Simulate Existing Project

```bash
# Create a test project with existing content
mkdir /tmp/existing-project && cd /tmp/existing-project
git init

# Create existing CLAUDE.md
cat > CLAUDE.md <<'EOF'
# My Existing Project

## Project Info
This is a Python CLI tool for task management.

## Tech Stack
- Python 3.11
- Click
- SQLite
EOF

# Create some existing files
mkdir -p src tests
echo "# placeholder" > src/__init__.py
echo "# placeholder" > tests/__init__.py

# Initial commit
git add .
git commit -m "Initial project structure"
```

### Run Migration

```bash
# Run the install script
curl -sL https://raw.githubusercontent.com/nightshift2k/claude-code-beads-workflow/main/install-workflow.sh | bash

# When prompted, accept adding @reference to CLAUDE.md
```

### Verify Migration

Check that all files were installed:

```bash
# Verify workflow files exist
[ -f "CLAUDE-workflow.md" ] && echo "OK: CLAUDE-workflow.md" || echo "FAIL: CLAUDE-workflow.md"

# Verify commands (14 files)
COMMANDS=$(ls .claude/commands/workflow-*.md 2>/dev/null | wc -l)
[ "$COMMANDS" -eq 14 ] && echo "OK: $COMMANDS command files" || echo "FAIL: Expected 14, got $COMMANDS"

# Verify rules (6 files)
RULES=$(ls .claude/rules/*.md 2>/dev/null | wc -l)
[ "$RULES" -eq 6 ] && echo "OK: $RULES rule files" || echo "FAIL: Expected 6, got $RULES"

# Verify utility library
[ -f ".claude/lib/workflow.py" ] && echo "OK: workflow.py" || echo "FAIL: workflow.py"

# Verify docs/plans directory
[ -d "docs/plans" ] && echo "OK: docs/plans/" || echo "FAIL: docs/plans/"
```

Verify CLAUDE.md was updated correctly:

```bash
# Check @reference was added
head -1 CLAUDE.md | grep -q "@CLAUDE-workflow.md" && echo "OK: @reference at top" || echo "FAIL: @reference missing"

# Verify original content preserved
grep -q "My Existing Project" CLAUDE.md && echo "OK: Original content preserved" || echo "FAIL: Content lost"
grep -q "Python CLI tool" CLAUDE.md && echo "OK: Description preserved" || echo "FAIL: Description lost"
```

### Test Update Mode

```bash
# Run install script again to test update
curl -sL https://raw.githubusercontent.com/nightshift2k/claude-code-beads-workflow/main/install-workflow.sh | bash

# When prompted "Update to latest?", accept

# Verify no duplicate @reference
REFS=$(grep -c "@CLAUDE-workflow.md" CLAUDE.md)
[ "$REFS" -eq 1 ] && echo "OK: Single @reference" || echo "FAIL: $REFS references found"
```

### Complete Workflow Test

After migration, test the full workflow:

```bash
# Open in Claude Code
cd /tmp/existing-project

# Run these commands in order:
# 1. /workflow-init
# 2. /workflow-health
# 3. /workflow-start "Test feature"
# 4. /workflow-check
# 5. /workflow-land
```

### Migration Checklist

- [ ] .claude/commands/workflow-\*.md exists (14 files)
- [ ] .claude/rules/\*.md exists (6 files)
- [ ] CLAUDE-workflow.md exists
- [ ] \.claude/lib/workflow.py exists
- [ ] docs/plans/ directory created
- [ ] CLAUDE.md has @reference at top
- [ ] Original CLAUDE.md content preserved
- [ ] CLAUDE.md.backup created (if CLAUDE.md existed)
- [ ] /workflow-init succeeds
- [ ] /workflow-health shows no errors

### Cleanup

```bash
rm -rf /tmp/existing-project
```

---

## Document Info

- **Version:** 1.1
- **Created:** 2025-12-14
- **Updated:** 2025-12-28 (added migration test path)
- **Purpose:** End-to-end validation of agentic workflow
- **Estimated time:** 30-60 minutes (pydo path), 15-20 minutes (migration path)
- **Difficulty:** Intermediate (requires basic CLI and Python knowledge)
