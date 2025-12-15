# Agentic Workflow - Validation Test

This document provides a complete, step-by-step test to validate that the agentic workflow works correctly. Follow this exactly in a fresh Claude Code instance.

## Purpose

Build a simple Python CLI task manager (`pydo`) while exercising every workflow command. This validates:
- Issue tracking with Beads integrates properly
- Workflow commands produce expected results
- Error recovery works when things go wrong
- Multi-session continuity functions correctly

---

## Part 1: Prerequisites (Before Anything Else)

### 1.1 Check Required Tools

Run these in your terminal FIRST:

```bash
# Check Beads CLI (minimum version: 0.2.0)
bd version
# Expected: bd version 0.2.0 or higher

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
# Set this to YOUR workflow source location
# Examples:
#   BOILERPLATE=~/code/claude-code-beads-workflow
#   BOILERPLATE=/Users/yourname/projects/claude-code-beads-workflow
#   BOILERPLATE=/path/to/wherever/you/cloned/the/workflow
BOILERPLATE=~/code/claude-code-beads-workflow

# Verify the path exists before proceeding
if [ ! -d "$BOILERPLATE" ]; then
  echo "ERROR: BOILERPLATE directory not found at: $BOILERPLATE"
  echo "Update the BOILERPLATE variable to point to your actual workflow source location"
  exit 1
fi

# Verify required files exist
if [ ! -f "$BOILERPLATE/CLAUDE.md" ]; then
  echo "ERROR: CLAUDE.md not found in $BOILERPLATE"
  exit 1
fi

if [ ! -d "$BOILERPLATE/.claude" ]; then
  echo "ERROR: .claude directory not found in $BOILERPLATE"
  exit 1
fi

# Copy .claude directory (commands, rules, lib)
cp -r "$BOILERPLATE/.claude" ~/pydo-validation-test/

# Copy CLAUDE.md (main workflow instructions)
cp "$BOILERPLATE/CLAUDE.md" ~/pydo-validation-test/

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

# Verify command files (should be 9 workflow-*.md files)
ls .claude/commands/ | wc -l
# Expected: 9

# Verify key files exist and are non-empty
ls -lh .claude/commands/workflow-*.md | awk '{if ($5 == "0") print "ERROR: " $9 " is empty"; else print "OK: " $9}'

# Verify lib/workflow-precheck.sh exists and contains functions
if grep -q "workflow_precheck" .claude/lib/workflow-precheck.sh; then
  echo "OK: workflow-precheck.sh contains expected functions"
else
  echo "ERROR: workflow-precheck.sh missing or incomplete"
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

# Count total files copied (should be around 14-16)
find .claude docs CLAUDE.md -type f | wc -l
# Expected: 14-16 files
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

**That's it** - the rest of CLAUDE.md is generic workflow instructions that work for any project.

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
│   ├── commands/
│   │   ├── workflow-init.md
│   │   ├── workflow-start.md
│   │   ├── workflow-track.md
│   │   ├── workflow-work.md
│   │   ├── workflow-execute.md
│   │   ├── workflow-land.md
│   │   ├── workflow-check.md
│   │   ├── workflow-questions.md
│   │   └── workflow-health.md
│   ├── lib/
│   │   └── workflow-precheck.sh
│   └── rules/
│       ├── 001-project-principles.md
│       ├── 002-open-questions-template.md
│       └── 003-multi-agent-coordination.md
├── docs/
│   └── plans/
│       └── pydo-design.md
└── CLAUDE.md
```

---

## Part 3: Start Recording & Launch Claude Code

Now that setup is complete, start the recorded session:

### 3.1 Start Session Recording

```bash
# Change to test directory
cd ~/pydo-validation-test

# Start recording (captures everything from here on)
# -q flag suppresses script's startup/exit messages
script -q pydo-validation-session.log

# Now start Claude Code
claude
```

**Important:** When finished with the entire validation, type `exit` to stop recording. The file `pydo-validation-session.log` will contain the complete Claude Code session.

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
# Expected: issues.jsonl, README.md, etc.
```

### 4.2 Create Feature Epic

**Command to Claude:**
```
/workflow-start Build pydo - a Python CLI task manager with add, list, complete, delete commands and priority support
```

**Expected behavior:**
- Creates a Beads epic issue
- Returns epic ID (e.g., `bd-abc123`)
- Epic is now trackable with `bd show <id>`

**Checkpoint:** Verify epic created:
```bash
# List all Beads issues
bd list --json
# Expected: Shows the newly created epic with type="epic"
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

During execution, you should see:
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

Skip to **7.4 Run Tests** when execution completes.

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

# Verify changes persisted to JSONL
bd sync --flush-only
# Expected: Shows changes exported or "already in sync"
```

---

## Part 9: Error Recovery Testing

### 9.1 Test Health Diagnostics

**Command to Claude:**
```
/workflow-health
```

**Expected behavior:**
- Checks environment (bd CLI, Python, git)
- Validates .beads/ directory
- Reports any issues found
- All checks should pass

### 9.2 Simulate Error: Missing Issue

Try to complete a non-existent issue:

**Command to Claude:**
```
Mark issue bd-nonexistent as complete
```

**Expected behavior:**
- Claude attempts `bd update bd-nonexistent --status completed`
- Gets "issue not found" error
- Handles gracefully with helpful message

### 9.3 Simulate Recovery: Interrupted Session

This tests whether the workflow properly recovers from an abrupt session end.

**Step 1: Claim a task but don't finish it**

Tell Claude:
```
Use /workflow-work to find a task, claim it (mark in_progress), but then STOP before implementing it.
Just claim the issue and confirm it's in_progress status.
```

Verify the issue is claimed:
```bash
# Check for in-progress issues
bd list --status in_progress --json
# Expected: Shows at least one issue with status="in_progress"
```

**Step 2: Force-quit Claude Code**

**Important**: If using `script` for recording (from Part 3.1), the recording will ALSO be interrupted. You'll need to restart it in append mode after the force-quit.

Choose one method to force-quit:
- **Option A**: Press `Ctrl+C` twice rapidly (force quit)
- **Option B**: Close the terminal window directly
- **Option C**: Run `pkill -9 claude` from another terminal

**Important**: Do NOT use `/workflow-land` - we're simulating a crash/interruption.

**Step 3: Restart session recording (if using script)**

If you were recording with `script` in Part 3.1, restart it in append mode:

```bash
cd ~/pydo-validation-test

# Restart script in APPEND mode to continue recording
script -a pydo-validation-session.log

# The -a flag appends to the existing log instead of overwriting
```

**Step 4: Restart Claude Code**

```bash
# Now start Claude Code again
claude
```

**Step 5: Verify recovery**

Tell Claude:
```
/workflow-work
```

**Expected behavior:**
- The previously claimed in-progress issue should appear
- Claude should offer to resume that task
- No work should be lost
- Beads state should be consistent

**Checkpoint:**
```bash
# Verify the in-progress issue persisted across the interruption
bd list --status in_progress --json
# Expected: Shows the same issue from Step 1 with status="in_progress"
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

**Workflow Commands:**
- [ ] `/workflow-init` - Environment initialized correctly
- [ ] `/workflow-start` - Epic created with proper tracking
- [ ] `/workflow-track` - Plan converted to issues with dependencies
- [ ] `/workflow-work` - Found and claimed available work
- [ ] `/workflow-check` - Status review worked
- [ ] `/workflow-land` - Session closed properly with sync
- [ ] `/workflow-health` - Diagnostics ran and reported accurately

**Beads Integration:**
- [ ] Issues created with proper types (epic, task)
- [ ] Issue hierarchy works (epic → child tasks with --parent)
- [ ] Dependencies tracked correctly (blocked/ready)
- [ ] Issue status updates worked
- [ ] `bd sync --flush-only` exported changes to JSONL
- [ ] Issue closure with reasons worked

**Error Handling:**
- [ ] Missing issue handled gracefully
- [ ] Recovery from interruption worked
- [ ] Health check identified issues correctly

**Implementation Quality:**
- [ ] pydo commands all work
- [ ] Tests pass
- [ ] Code is organized as specified

---

## Part 11: Session Wrap-up

### 11.1 Stop Recording

```bash
# Exit Claude Code first (type 'exit' or Ctrl+D)

# Then stop the script recording (type 'exit' again)
exit
# This closes the script session and saves to pydo-validation-session.log
```

### 11.2 Collect Artifacts

Gather these files for analysis:
1. `pydo-validation-session.log` - Full session transcript
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
bd-xxx (epic): Build pydo CLI task manager
├── bd-xxx.1 (task): Set up project structure
├── bd-xxx.2 (task): Implement Task model [depends: xxx.1]
├── bd-xxx.3 (task): Implement exceptions [depends: xxx.1]
├── bd-xxx.4 (task): Implement storage layer [depends: xxx.2, xxx.3]
├── bd-xxx.5 (task): Implement CLI commands [depends: xxx.4]
├── bd-xxx.6 (task): Write test suite [depends: xxx.5]
└── bd-xxx.7 (task): Documentation and polish [depends: xxx.6]
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
# Sandbox mode is used by default for Claude Code
# If you see this error, try:
bd import --force
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

## Document Info

- **Version:** 1.0
- **Created:** 2025-12-14
- **Purpose:** End-to-end validation of agentic workflow
- **Estimated time:** 30-60 minutes
- **Difficulty:** Intermediate (requires basic CLI and Python knowledge)
