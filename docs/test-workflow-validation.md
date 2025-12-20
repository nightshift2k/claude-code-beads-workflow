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

# Verify command files (should be 11 workflow-*.md files)
ls .claude/commands/ | wc -l
# Expected: 11

# Verify key files exist and are non-empty
ls -lh .claude/commands/workflow-*.md | awk '{if ($5 == "0") print "ERROR: " $9 " is empty"; else print "OK: " $9}'

# Verify workflow.py exists and is valid
if [ -f "_claude/lib/workflow.py" ]; then
  echo "OK: workflow.py exists"
  if uv run python -c "import ast; ast.parse(open('_claude/lib/workflow.py').read())" 2>/dev/null; then
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

# Count total files copied (should be around 16-18)
find .claude docs CLAUDE.md -type f | wc -l
# Expected: 16-18 files
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
│   ├── commands/           # 11 workflow-*.md files
│   │   ├── workflow-init.md
│   │   ├── workflow-start.md
│   │   ├── workflow-track.md
│   │   ├── workflow-execute.md
│   │   ├── workflow-work.md
│   │   ├── workflow-land.md
│   │   ├── workflow-check.md
│   │   ├── workflow-health.md
│   │   ├── workflow-question-ask.md
│   │   ├── workflow-steer-research.md
│   │   └── workflow-steer-correct.md
│   ├── lib/
│   │   └── workflow.py     # Python workflow CLI tool (stdlib only)
│   └── rules/
│       ├── 001-project-principles.md
│       ├── 003-multi-agent-coordination.md
│       ├── 004-beads-json-patterns.md
│       ├── 005-agent-dispatch.md
│       └── 006-git-conventions.md
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

**Session Recording:** Use Claude Code's `/export` command before exiting to save a clean transcript.

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

# Verify prefix is 8 chars or less (including hyphen)
bd config | grep prefix
# Expected: Shows prefix like "pydo-" (5 chars total)
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

# Verify JSONL file exists and contains issues
ls -lh .beads/issues.jsonl
# Expected: Shows non-empty file
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

Choose one method to force-quit:
- **Option A**: Press `Ctrl+C` twice rapidly (force quit)
- **Option B**: Close the terminal window directly
- **Option C**: Run `pkill -9 claude` from another terminal

**Important**: Do NOT use `/workflow-land` - we're simulating a crash/interruption.

**Step 3: Restart Claude Code**

```bash
# Now start Claude Code again
claude
```

**Step 4: Verify recovery**

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
# Verify the in-progress issue persisted
bd list --status in_progress --json
# Expected: Shows the same claimed issue with status="in_progress"
```

---

### 9.4 Test Research Question Workflow

This tests the interactive research question capture and resolution workflow.

**Step 1: Capture a research question**

Tell Claude:
```
/workflow-question-ask Should we use SQLite or DuckDB for analytics queries in pydo?
```

**Expected behavior:**
- Claude asks clarifying questions (context, impact, owner, due date, initial research)
- Claude identifies potentially blocked issues (e.g., storage implementation tasks)
- Claude presents a summary for confirmation
- Claude creates a Beads issue with type=task and full context in description
- Claude establishes blocking dependencies on relevant tasks

**Checkpoint:**
```bash
# Verify research issue was created
bd list --json | jq '.[] | select(.title | contains("Research:"))'
# Expected: Shows research issue with full description

# Record the research issue ID
RESEARCH_ID=$(bd list --json | jq -r '.[] | select(.title | contains("Research:")) | .id' | head -1)
echo "Research issue: $RESEARCH_ID"

# Verify blocking dependencies were established
bd show $RESEARCH_ID --json | jq '.[0].blocks'
# Expected: Shows IDs of blocked tasks
```

**Step 2: Resolve the research question**

Tell Claude:
```
/workflow-steer-research $RESEARCH_ID
```

(Replace `$RESEARCH_ID` with the actual ID from Step 1)

**Expected behavior:**
- Claude loads the research context from the issue
- Claude conducts research (may use web search, documentation lookup)
- Claude updates blocked tasks with research findings
- Claude closes the research issue with resolution summary

**Checkpoint:**
```bash
# Verify research issue is closed
bd show $RESEARCH_ID --json | jq '.[0].status'
# Expected: "completed"

# Verify blocked tasks were updated
bd show $RESEARCH_ID --json | jq '.[0].blocks[]' | while read blocked_id; do
  bd show "$blocked_id" --json | jq '.[0].notes'
done
# Expected: Shows research findings in task notes
```

**Step 3: Course correction (brief mention)**

The `/workflow-steer-correct` command handles human-spotted divergence during implementation. This is typically used when:
- Human reviews work-in-progress and spots an issue
- AI has gone off-track during implementation
- Requirements need mid-implementation adjustment

We won't test this in the validation (requires simulating divergence), but verify the command exists:

```bash
# Verify command file exists
ls -lh .claude/commands/workflow-steer-correct.md
# Expected: Shows the command file
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

**Workflow Commands (All 11):**
- [ ] `/workflow-init` - Environment initialized correctly
- [ ] `/workflow-start` - Epic created with proper tracking
- [ ] `/workflow-track` - Plan converted to issues with dependencies
- [ ] `/workflow-execute` - Automated plan execution worked (or skipped if using manual approach)
- [ ] `/workflow-work` - Found and claimed available work
- [ ] `/workflow-check` - Status review worked
- [ ] `/workflow-land` - Session closed properly with sync
- [ ] `/workflow-health` - Diagnostics ran and reported accurately
- [ ] `/workflow-question-ask` - Research question captured and issue created
- [ ] `/workflow-steer-research` - Research issue resolved and tasks updated
- [ ] `/workflow-steer-correct` - Command exists (not fully tested in validation)

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

# Note: Sandbox mode is required for Claude Code environments
# All bd commands should use --sandbox flag in Claude Code
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