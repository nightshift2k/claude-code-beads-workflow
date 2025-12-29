<!-- CLAUDE-workflow.md v1.0.0 | Last updated: 2025-12-28 -->

# Agentic Development Workflow Instructions

<ai_instruction_principles>

## AI Instruction Design Principles

This workflow is designed for AI consumption. Instructions follow these principles:

1. **Principle-Based**: Describe WHAT to achieve, not HOW step-by-step
2. **Decision Frameworks**: Use situation/action/outcome tables, not if/then bash
3. **Context Gathering**: Specify what to query, not variable assignments
4. **Success Criteria**: Define measurable outcomes, not echo statements
5. **Edge Considerations**: Trust AI judgment for novel situations

**Reference material** (command syntax, gotchas) is preserved for accuracy.
**Procedural instructions** are replaced with decision frameworks.
</ai_instruction_principles>

## Overview

This project follows agentic development workflow using Beads distributed issue tracking with integrated skill-based planning. This workflow ensures:

- Issue tracking during implementation
- Clear task breakdown and Beads coordination
- Local consistency across sessions
- Complete audit trail

## Key Slash Commands for Common Tasks

### `/workflow-init` - Initialize project for workflow

```
When: Setting up new project or starting fresh
Process: Validates environment, initializes Beads with short prefix (recommended), creates directories
Result: Project ready for workflow with clean issue IDs (e.g., myproj-abc)
```

### `/workflow-health` - Diagnose workflow issues

```
When: Encountering workflow problems or verifying system health
Process: Checks environment, Beads status, configuration, git state
Result: Health report identifying issues
```

### `/workflow-start` - Begin a new feature

```
When: Starting new feature or capability
Process: Creates Beads epic and feature branch
Result:
  - Epic created (e.g., myproj-abc) - SAVE for /workflow-track
  - Feature branch created: feature/myproj-abc-feature-slug
IMPORTANT: Note epic ID - required for --parent in child issues
```

### `/workflow-track` - Set up Beads tracking for planned work

```
Usage: /workflow-track [path/to/implementation-plan.md]
When: Ready to track planned work
Process: Converts plan tasks into Beads issues:
  - Hierarchical IDs via --parent $EPIC_ID --force (e.g., myproj-abc.1, myproj-abc.2)
  - Full content in descriptions via --body-file (token-efficient)
Template: Write content to temp file, then:
  bd create "[Task]" --parent $EPIC_ID --force -t task -p 2 --body-file /tmp/task.md --json
Result: Self-contained issues with sequential IDs under epic
```

### `/workflow-execute` - Execute implementation plan with Beads tracking

```
When: Ready to implement from plan
Process: /workflow-execute [path/to/implementation/plan.md]
Result: Executes plan with integrated tracking per task
```

### `/workflow-work` - Find and claim available work

```
When: Ready to start working
Process: bd ready --json finds unblocked issues, bd update [id] --status in_progress claims work
Result: Identifies and claims work
```

### `/workflow-land` - Complete a work session properly

```
When: Finishing session (REQUIRED before stopping)
Process:
1. Detect work completion (epic children or ad-hoc issues)
2. Create follow-up work: bd create
3. Close completed: bd close [id] --reason
4. Update in-progress: bd update [id] --notes
5. Handle git based on state (see Branch Behavior below)
Result: Clean completion, all work tracked

Branch Behavior (feature/* branches):
- Epic complete -> Prompt: merge to main or create PR
- Epic incomplete -> Stay on branch, push if remote exists
- Protected branch flag -> Create/update PR instead of merge
```

### `/workflow-check` - Review project status

```
When: Need current project state
Process: Reviews active issues (bd list --status open) and outstanding work
Result: Current implementation and tracking state

For live monitoring during long sessions:
  bd list --pretty --watch    # Auto-refreshing tree view
```

### `/workflow-question-ask` - Interactive research question capture

```
Usage: /workflow-question-ask [rough question]
When: Capturing research question with context and blocking relationships
Process:
  1. Asks clarifying questions (context, impact, owner, due date, research)
  2. Identifies potentially blocked issues
  3. Presents summary for confirmation
  4. Creates Beads issue with full context (via --body-file for complex content)
  5. Establishes blocking dependencies
Template: Write context to temp file, then:
  bd create "Research: [description]" --body-file /tmp/research.md -t task -p [priority] --json
Result: Self-contained research issue with blocking dependencies
Note: Stores everything in Beads (no external file)
```

### `/workflow-steer-research` - Resolve research and update blocked tasks

```
When: Research complete, findings ready to apply
Process: Loads context, conducts research, updates blocked tasks, closes issue
Result: Research resolved, tasks unblocked and ready
```

### `/workflow-steer-correct` - Course correction mid-implementation

```
When: Human spots AI divergence
Process: Shows progress, describes correction, identifies affected tasks, creates P0 task, reopens/updates tasks
Result: P0 correction task created, affected tasks updated with blocking dependencies, surfaces first in ready work
```

### `/workflow-do` - Execute isolated task without epic overhead

```
Usage: /workflow-do [task description]
When: Quick bug fix or small change (<2 hours) that doesn't warrant an epic
Process:
  1. Checks for active work (offers pause/abort if conflict)
  2. Creates Beads task with description
  3. Marks in_progress, dispatches to appropriate agent
  4. On completion: closes with outcome, commits changes
Result: Task tracked from start to finish without epic ceremony

When NOT to Use:
- Task touches 3+ files -> use /workflow-start
- Task relates to active epic -> use /workflow-steer-correct
- Complex change requiring design -> use brainstorming + /workflow-start
```

<workflow_principles>

## Key Principles

1. **Plan-Driven Development**: Base all implementation on detailed plans (from writing-plans skill)
2. **Issue Tracking**: Track all work in Beads
3. **Local Consistency**: Maintain consistency across sessions via Beads sync
4. **Constitutional Compliance**: Follow project constitution
   </workflow_principles>

## bd vs TodoWrite Decision

Beads (`bd`) and TodoWrite serve different purposes:

| Use bd when...                       | Use TodoWrite when...       |
| ------------------------------------ | --------------------------- |
| Work spans multiple sessions         | Single-session tasks        |
| Complex dependencies exist           | Linear step-by-step work    |
| Need to survive context compaction   | Just need a quick checklist |
| Knowledge work with fuzzy boundaries | Clear, immediate tasks      |
| Collaboration with team (git sync)   | Personal task tracking      |

**Decision Rule**: If resuming in 2 weeks would be hard without bd, use bd.

**In this workflow**: All `/workflow-*` commands use bd internally. Use TodoWrite only for ephemeral within-session checklists that don't need tracking.

## Integration Process

### From Idea to Implementation

1. Create feature epic with `/workflow-start`
2. Create implementation plan (using writing-plans skill)
3. Set up tracking with `/workflow-track`
4. Execute with `/workflow-execute` or work incrementally with `/workflow-work`

### Agent Session Flow

1. **Start**: Check `/workflow-work` for available tasks or use `/workflow-execute` for full plan execution
2. **Execute**: Use Beads CLI for issue management during work
3. **Complete**: Always finish with `/workflow-land` for proper session closure

### Workflow Lifecycle

```
+------------------------------------------------------------------+
|                     AGENTIC WORKFLOW LIFECYCLE                   |
+------------------------------------------------------------------+

  SETUP          PLANNING            TRACKING         EXECUTION
    |                |                   |                |
    v                v                   v                v
/workflow-init -> /workflow-start -> /workflow-track -> /workflow-execute
    |           (create epic)    (plan -> issues)    (run full plan)
    |                |                   |                |
    |                v                   |           OR   v
    |           brainstorm +             |        /workflow-work <--+
    |           writing-plans            |        (task by task)    |
    |                |                   |                |         |
    |                +-------------------+                |         |
    |                                                     |         |
    |              MONITORING & STEERING                  |         |
    |                  |                                  |         |
    |     /workflow-check (status review)                 |         |
    |     /workflow-health (diagnostics)                  |         |
    |     /workflow-overview (view plan state)            |         |
    |     /workflow-config (manage flags)                 |         |
    |     /workflow-question-ask (capture research)       |         |
    |     /workflow-steer-research (resolve research)     |         |
    |     /workflow-steer-correct (course correction)     |         |
    |     /workflow-do (quick isolated task)              |         |
    |                                                     |         |
    |                                    SESSION END      |         |
    |                                        |            |         |
    +----------------------------------------+------------+         |
                                             v                      |
                                      /workflow-land                |
                                             |                      |
                           +-----------------+-----------------+    |
                           |                                   |    |
                     epic complete?                      epic incomplete
                           |                                   |    |
                           v                                   +----+
                    merge/PR + done                     (stay on branch,
                                                         next session)
```

## Beads Issue ID Guidelines

<beads_prefix_rules>

### Prefix Requirements

Beads issue IDs consist of a **prefix** + **hash** (e.g., `myproj-abc`).

**Prefix rules:**

- Must end with a hyphen (e.g., `myproj-`, `auth-`, `api-`)
- Lowercase letters, numbers, hyphens only
- Must start with a letter
- Short prefixes recommended for readability (no hard limit)

| Good Prefixes | Bad Prefixes                  |
| ------------- | ----------------------------- |
| `myproj-`     | `MyProject-` (uppercase)      |
| `auth-`       | `web_app-` (underscore)       |
| `api-`        | `2auth-` (starts with number) |

**Set prefix during initialization:**

```bash
bd init -p myproj- --quiet
```

**Useful prefix commands:**

```bash
bd rename-prefix myproj- --dry-run   # Preview prefix change
bd rename-prefix myproj-             # Apply prefix change
bd where                             # Show active beads database location
```

</beads_prefix_rules>

### Hierarchical Issue IDs

Use `--parent --force` to create child issues with sequential dotted IDs:

```bash
# Create epic
bd create "Feature name" -t epic -p 1 --json
# Returns: myproj-abc

# Create child tasks with hierarchical IDs
bd create "Task 1" --parent myproj-abc --force -t task -p 2 --json
# Returns: myproj-abc.1

bd create "Task 2" --parent myproj-abc --force -t task -p 2 --json
# Returns: myproj-abc.2
```

**Why `--force`?** Required to work around a Beads quirk where `--parent` triggers a false "prefix mismatch" error. Safe to use.

**Without `--parent --force`:** Each task gets a random independent ID (`myproj-xyz`, `myproj-def`) with no visible relationship to the epic.

### Branch Naming Convention

Feature branches embed the epic ID for traceability:

**Format:** `feature/<epic-id>-<slug>`

| Component | Rules                               | Example               |
| --------- | ----------------------------------- | --------------------- |
| Prefix    | Always `feature/`                   | `feature/`            |
| Epic ID   | From `/workflow-start`              | `myproj-abc`          |
| Slug      | Lowercase, hyphenated, max 30 chars | `user-authentication` |

**Examples:**

```
feature/myproj-abc-user-auth
feature/api-xyz-rate-limiting
feature/auth-def-oauth-integration
```

**Slug generation rules:**

- Lowercase the epic title
- Replace spaces/special chars with hyphens
- Remove consecutive hyphens
- Truncate to 30 characters
- Strip leading/trailing hyphens

**Why embed epic ID?**

- `/workflow-work` validates branch matches claimed epic
- `/workflow-land` detects work completion from branch context
- Git history links directly to Beads tracking

---

## Issue Creation Best Practices

When creating Beads issues from implementation plans:

### Include Context Links

For simple descriptions without code blocks, inline text works:

```bash
bd create "Implement user login" \
  -t task -p 2 --parent $EPIC_ID --force --json
```

For descriptions with code blocks, use `--body-file`:

```bash
cat > /tmp/task.md <<'EOF'
From implementation plan - implement the user login flow.

**Steps:**
- Create login endpoint
- Add authentication middleware
EOF

bd create "Implement user login" \
  --body-file /tmp/task.md -t task -p 2 \
  --parent $EPIC_ID --force --json
```

### Map Hierarchies Properly

- Feature epic -> Beads epic (type: epic, e.g., `myproj-abc`)
- Plan tasks -> Beads child issues (use `--parent <epic-id> --force`, e.g., `myproj-abc.1`)

Example:

```bash
# Create epic
bd create "Feature name" -t epic -p 1 --json
# Returns: myproj-abc

# Create child task under epic (ALWAYS use --parent --force)
bd create "Task name" --parent myproj-abc --force -t task -p 2 --json
# Returns: myproj-abc.1
```

### Store Full Task Content in Descriptions

For token efficiency, store complete task content in issue descriptions.

**CRITICAL:** Use `--body-file` for descriptions containing code blocks. The `--description` heredoc **silently loses data** when content contains backticks.

````bash
# Write task content to temp file
cat > /tmp/task-3.md <<'EOF'
**Files:**
- Modify: `pydo/models.py`
- Create: `tests/test_models.py`

**Step 1: Write failing test**
```python
def test_create_task():
    task = Task(description="Test")
    assert task.status == "pending"
````

**Step 2: Run test**

```bash
uv run pytest tests/test_models.py -v
```

Expected: FAIL
EOF

# Create issue with --body-file (ONLY safe method for code blocks)

bd create "Task 3: Task Model" --parent $EPIC_ID --force -t task -p 2 \
 --body-file /tmp/task-3.md --json

````

Agents work from self-contained issues without re-reading large implementation plans.

### Use Appropriate Priorities

See @.claude/rules/project-principles.md for the priority system.

Quick reference: P0=Critical, P1=High, P2=Medium (default), P3=Low, P4=Backlog

**Note:** Both numeric (`-p 0` through `-p 4`) and text labels (`P0`-`P4`) work in Beads. Use numeric format in bash commands; text labels appear in issue summaries and planning discussions.

### Issue Type Selection

Select issue type based on task characteristics:

| Type | Trigger | Example |
|------|---------|---------|
| `epic` | Parent container for feature | "User authentication system" |
| `feature` | New user-facing capability | "Add user login" |
| `bug` | Fixes broken behavior | "Fix login validation error" |
| `chore` | Maintenance work | "Update dependencies" |
| `task` | Default for implementation | "Implement SQLite layer" |

**Selection precedence:** epic > feature > bug > chore > task

**When unclear:** Default to `task`.

<session_completion_rules>
## Session Completion Principles

### Intent
Properly close a work session with all state persisted and no orphaned work.

### Completion Criteria

| Aspect | Requirement |
|--------|-------------|
| Follow-up work | All discovered tasks filed in Beads |
| Issue status | Completed work closed, in-progress updated |
| Quality gates | Tests/linters run if code changed |
| State persistence | Beads exported (solo: flush-only, team: full sync) |
| Git state | Changes committed with meaningful message |

### Decision Framework

| Situation | Action |
|-----------|--------|
| Discovered follow-up tasks | Create Beads issues before closing |
| Code changes made | Run quality gates first |
| Solo developer | Use `bd sync --flush-only` |
| Team collaboration | Use `bd sync` (includes git operations) |
| Session incomplete | Update in-progress issues with notes |

### Mid-Epic Landing Behavior

When landing on a feature branch with incomplete epic work:

| Branch | Epic State | Action |
|--------|------------|--------|
| `feature/*` | Children remain open | Stay on branch, push if remote |
| `feature/*` | All children closed | Prompt: merge or create PR |
| `main` | Any | Commit and push (if remote) |

**Why stay on branch?**
- Preserves work isolation until epic completes
- Next session resumes from same context
- PR can be created when ready (via `protected-branch` flag)
- Clean merge history when work finishes

**Draft PR support:** With `protected-branch` flag, incomplete work creates a draft PR that converts to ready when epic completes.

**Command:** Use `/workflow-land` for guided session completion.
</session_completion_rules>

## Team Collaboration

### Solo Developer (Default)

For individual developers or when not sharing state with a team:

```bash
# Export changes to JSONL only (no git operations)
bd sync --flush-only

# Then handle git manually if needed
git add . && git commit && git push
````

### Multi-Developer Team

For teams sharing Beads state via git:

```bash
# Full sync: export + commit + pull + import + push
bd sync
```

Run `bd sync` at task boundaries (start/end of each task).

**What `bd sync` does:**

1. Export pending changes to JSONL
2. `git add .beads/issues.jsonl`
3. `git commit -m "sync: Beads state update"`
4. `git pull` (merge remote changes)
5. Import updated JSONL
6. `git push`

### Sandbox Mode (Claude Code)

Beads auto-detects sandboxed environments since v0.21.1. When detected:

- You will see: "Sandbox detected, using direct mode"
- Automatic background sync is disabled
- Manual `bd sync` still works for team collaboration

**No configuration needed.** Just use `bd sync` when working with a team.

### Protected Branch Workflow

For teams requiring code review before merging to main:

**Setup (new project):**

```bash
bd init -p myproj- --branch beads-metadata --quiet
```

**Setup (existing project):**

```bash
bd migrate-sync beads-metadata
```

**Daily workflow:**

```bash
# Work normally
bd sync --flush-only  # Commits to beads-metadata branch
```

**Periodic merge:**
Human creates PR/MR to merge `beads-metadata` -> `main`

### GitLab Enterprise Setup

Beads works with any git remote. For GitLab Enterprise:

**Initial setup:**

```bash
git clone git@gitlab.company.com:team/project.git
cd project

# If using HTTPS with custom CA:
git config http.sslCAInfo /path/to/company-ca.crt

# Initialize Beads (same as GitHub)
bd init -p myproj- --quiet
```

**Workflow:**
Use Merge Requests (MR) instead of Pull Requests (PR). All git operations are identical.

## Epic-Centric Plan Management

### Plan File Lifecycle

Plan files are **ephemeral** - they exist only during drafting and review:

```
[DRAFT]   -> Plan file created by writing-plans skill
    |
[REVIEW]  -> Human reviews and approves
    |
[TRACK]   -> /workflow-track copies to Beads, DELETES file
    |
[WORK]    -> Execute from Beads only
```

After tracking, the plan content lives in the **epic description**.

### Viewing Plan State

Use `/workflow-overview` to see plan state:

```bash
/workflow-overview myproj-abc           # Quick summary
/workflow-overview myproj-abc --log     # Steering log
/workflow-overview myproj-abc --full    # Original plan + status
/workflow-overview myproj-abc --current # Current task state
/workflow-overview myproj-abc --all     # Export everything
```

### Steering Log

All plan modifications are logged in the epic description:

| Entry Type | Created By               | When                    |
| ---------- | ------------------------ | ----------------------- |
| INIT       | /workflow-track          | Plan first tracked      |
| STEER      | /workflow-steer-research | Research changes plan   |
| CORRECT    | /workflow-steer-correct  | Human course correction |

**Example steering log:**

```markdown
## Steering Log

### [2025-12-22T14:30:00Z] STEER: Storage Redesign

**Trigger:** Research myproj-xyz
**Decision:** JSON -> SQLite
**Modified:** myproj-abc.4
**Added:** myproj-abc.4a, myproj-abc.4b
**Rationale:** Concurrent access requirement

### [2025-12-22T10:00:00Z] INIT: Plan Tracked

**Source:** docs/plans/implementation-plan.md
**Tasks Created:** 7
```

### Why Ephemeral Plans?

1. **No accumulation** - Only drafts exist as files
2. **No sync drift** - Beads is sole source of truth
3. **Clear status** - File existence indicates draft
4. **Audit trail** - Steering log tracks all changes

## Workflow Flags

Configuration flags control workflow behavior. Flags are stored as files in `.claude/`.

### Available Flags

| Flag             | File                                 | Effect                                  |
| ---------------- | ------------------------------------ | --------------------------------------- |
| team-mode        | `.claude/ccbw-flag-team-mode`        | Use `bd sync` for full git sync         |
| strict-quality   | `.claude/ccbw-flag-strict-quality`   | Require quality gate before close       |
| protected-branch | `.claude/ccbw-flag-protected-branch` | Use PRs instead of direct merge to main |
| auto-cleanup     | `.claude/ccbw-flag-auto-cleanup`     | Clear stash + prune remotes on land     |

### Managing Flags

```bash
# Enable flag
/workflow-config team-mode on

# Disable flag
/workflow-config strict-quality off

# List all flags
/workflow-config --list

# Manual (equivalent)
touch .claude/ccbw-flag-team-mode   # Enable
rm .claude/ccbw-flag-team-mode      # Disable
```

### Team Setup

For team projects, commit the flag file so all members get team mode:

```bash
touch .claude/ccbw-flag-team-mode
git add .claude/ccbw-flag-team-mode
git commit -m "chore: enable team mode for workflow"
```

## Git Hooks Integration

The workflow integrates with git hooks via the pre-commit framework for automatic Beads synchronization.

### Hook Behavior

| Hook          | Trigger                 | Action                                               |
| ------------- | ----------------------- | ---------------------------------------------------- |
| pre-commit    | `git commit`            | Run `bd sync --flush-only` to export pending changes |
| post-merge    | `git merge`, `git pull` | Run `bd import --force` to load merged state         |
| post-checkout | Branch switch           | Run `bd import --force` to load branch state         |

### Setup (Optional)

```bash
# Install pre-commit (if not installed)
pip install pre-commit

# Install hooks for all stages
pre-commit install --hook-type pre-commit --hook-type post-merge --hook-type post-checkout
```

### Fallback Behavior

If hooks fail or are bypassed:

- `/workflow-land` handles sync as fallback
- Manual `bd sync --flush-only` always available
- Hook failures don't block commits

**Note:** See `.pre-commit-config.yaml` for hook configuration.

## Troubleshooting

### Environment Validation

All workflow commands validate the environment automatically. The precheck system guides you through resolution when issues occur.

**Manual precheck** (if needed):

```bash
uv run python .claude/lib/workflow.py precheck --name manual-check
```

### Version Requirements

This workflow requires specific Beads CLI versions for full functionality:

| Version         | Status          | Notes                                             |
| --------------- | --------------- | ------------------------------------------------- |
| < 0.37.0        | **Unsupported** | Missing `--parent` flags, workflow will fail      |
| 0.37.0 - 0.39.0 | Supported       | Core features work, some new commands unavailable |
| >= 0.39.1       | **Recommended** | All documented features available                 |

**Check your version:**

```bash
bd version
```

**Upgrade to latest:**

```bash
go install github.com/steveyegge/beads/cmd/bd@latest
# Or: brew upgrade steveyegge/tap/beads
```

The precheck automatically validates version requirements and warns if outdated.

---

### Common Error Messages and Solutions

#### "bd: command not found"

**Symptom:**

```
/workflow-start "New feature"
bash: bd: command not found
```

**Cause:** Beads CLI not installed or not in PATH

**Solutions:**

1. **Install via Go:**

   ```bash
   go install github.com/steveyegge/beads/cmd/bd@latest
   ```

2. **Install via Homebrew (macOS):**

   ```bash
   brew install steveyegge/tap/beads
   ```

3. **Verify installation:**

   ```bash
   bd version
   which bd
   ```

4. **Add to PATH if needed:**

   ```bash
   export PATH="$PATH:$(go env GOPATH)/bin"
   # Add to ~/.bashrc or ~/.zshrc for persistence
   ```

**Reference:** [Beads Installation Guide](https://github.com/steveyegge/beads/blob/main/docs/INSTALLING.md)

---

#### "no .beads directory found"

**Symptom:**

```
bd ready
Error: no .beads directory found
```

**Cause:** Project not initialized with Beads tracking

**Solutions:**

1. **Initialize automatically (workflow commands do this):**

   ```
   /workflow-start "First feature"
   # Will prompt to initialize
   ```

2. **Initialize manually:**

   ```bash
   bd init -p myproj- --quiet
   ```

3. **Verify initialization:**

   ```bash
   ls -la .beads/
   # Should show: beads.db, issues.jsonl, README.md, etc.
   ```

---

#### "database out of sync with JSONL"

**Symptom:**

```
bd ready
Error: database out of sync with JSONL
```

**Cause:** Sandbox mode defaults to on for Claude Code compatibility.

**Solution:** Sandbox mode is enabled. If you see this error:

```bash
bd import --force
```

**Reference:** [Beads Troubleshooting - Sandboxed Environments](https://github.com/steveyegge/beads/blob/main/docs/TROUBLESHOOTING.md#sandboxed-environments)

---

#### "merge conflict in .beads/issues.jsonl"

**Symptom:**

```
bd sync
Error: merge conflict in .beads/issues.jsonl
```

**Cause:** Same issue modified on different branches

**Solutions:**

1. **Use bd merge tool:**

   ```bash
   git show :1:.beads/issues.jsonl > base.jsonl
   git show :2:.beads/issues.jsonl > ours.jsonl
   git show :3:.beads/issues.jsonl > theirs.jsonl

   bd merge merged.jsonl base.jsonl ours.jsonl theirs.jsonl

   cp merged.jsonl .beads/issues.jsonl
   git add .beads/issues.jsonl
   git merge --continue
   ```

2. **Simple conflicts (different fields):**

   ```bash
   # Keep both changes (manual edit)
   # OR prefer one side:
   git checkout --ours .beads/issues.jsonl   # Keep your changes
   git checkout --theirs .beads/issues.jsonl # Keep their changes

   bd import --force
   git add .beads/issues.jsonl
   git merge --continue
   ```

**Reference:** [Beads Conflict Resolution](https://github.com/steveyegge/beads/blob/main/.agent/workflows/resolve-beads-conflict.md)

---

#### "bd ready" returns no issues

**Symptom:**

```
/workflow-work
bd ready --json
[]
```

**Cause:** No unblocked work available

**Diagnostic Commands:**

```bash
# Check for blocked issues
bd blocked

# View all open issues
bd list --status open

# Check for stale issues
bd stale --days 7

# Visualize dependency graph for specific issue (requires issue-id)
bd graph [issue-id]

# Check dependency tree for specific issue
bd dep tree [issue-id]

# Detect circular dependencies
bd dep cycles
```

**Solutions:**

1. **If issues are blocked:**
   - Resolve blocking issues first
   - Or remove blocking dependencies: `bd dep remove [from-id] [to-id]`

2. **If no open issues:**
   - All work complete!
   - Create new work: `/workflow-start "Next feature"`

3. **If blocked by circular dependencies:**

   ```bash
   bd dep cycles  # Detect cycles
   bd dep remove [from-id] [to-id]  # Break cycle
   ```

---

#### "Plan file not found after tracking"

**Expected behavior.** After `/workflow-track`, plan files are deleted.

**To view plan:**

```bash
/workflow-overview [epic-id] --full
```

---

#### "Steering log is empty"

**Symptom:**

```
/workflow-overview myproj-abc --log
# Shows only INIT entry, no STEER/CORRECT
```

**Cause:** No steering events have occurred yet.

**If steering DID happen but isn't logged:**

- Use `/workflow-steer-correct` to add a CORRECT entry documenting the change

---

### Recovery Decision Tree

When something goes wrong, try these in order:

```
1. FIRST: bd doctor --fix (v0.38.0+)
   +-- Auto-repair common issues (recommended first step)

2. IF doctor fails: bd import --force
   +-- Rebuilds database from JSONL (fixes most sync issues)

3. IF import fails: bd reset
   +-- Complete database reset (keeps JSONL, faster than manual recovery)

4. IF still broken: Database Corruption Recovery (below)
   +-- Manual backup, reinitialize, reimport from JSONL

5. IF context issues: Session State Recovery (below)
   +-- Check in-progress issues, resume or reset status

6. LAST RESORT: Full Reset (below)
   +-- Backup everything, delete DB, start fresh
```

**Rule:** Never jump to Full Reset without trying simpler fixes first.

---

### Emergency Recovery Procedures

#### Auto-Repair (v0.38.0+ - Recommended First)

```bash
# Automatically diagnose and fix common issues
bd doctor --fix

# Verify recovery
bd list --json | jq '. | length'
```

#### Quick Reset (If Auto-Repair Fails)

```bash
# Reset database completely (keeps JSONL)
bd reset

# Verify recovery
bd list --json | jq '. | length'
```

Rebuilds the database from JSONL without manual steps.

#### Database Corruption Recovery (Manual Method)

Use this if `bd doctor --fix` and `bd reset` both fail:

```bash
# 1. Verify corruption
sqlite3 .beads/*.db "PRAGMA integrity_check;"

# 2. Backup corrupted database
mkdir -p .beads/backup
mv .beads/*.db .beads/backup/

# 3. Recover from JSONL (use your project's prefix)
bd init -p myproj- --quiet
bd import --force

# 4. Verify recovery
bd list --json | jq '. | length'
```

#### Session State Recovery After Interruption

```bash
# 1. Check for in-progress issues
bd list --status in_progress

# 2. Review state
bd show [issue-id]

# 3. Resume work
/workflow-work
# Select the in-progress issue

# 4. Or mark as open and re-prioritize
bd update [issue-id] --status open
```

#### Full Reset (Nuclear Option)

Only use when other recovery methods fail:

```bash
# 1. Backup everything
cp -r .beads .beads.backup-$(date +%s)

# 2. Remove database
rm .beads/*.db

# 3. Reinitialize (use your project's prefix)
bd init -p myproj- --quiet

# 4. Reimport from JSONL
bd import --force

# 5. Verify
bd list --json | jq '. | length'
```

---

### Quick Reference

| Problem                  | Solution                                                                       |
| ------------------------ | ------------------------------------------------------------------------------ |
| Lost work (sandbox)      | `bd sync --flush-only` then check .beads/issues.jsonl                          |
| JSONL conflicts          | Use `bd merge` tool                                                            |
| Database out of sync     | `bd import --force` then `bd reset` if needed                                  |
| Multi-machine sync       | `bd sync` (full git sync)                                                      |
| Confusing dependencies   | `bd graph [issue-id]` for visualization, `bd dep tree [id]` for specific issue |
| Circular dependencies    | `bd dep cycles` to detect, `bd dep remove` to break                            |
| Stale issues             | `bd stale --days 7`                                                            |
| Database corruption      | `bd doctor --fix` (auto-repair) or `bd reset` (full rebuild)                   |
| Sandbox mode issues      | Auto-detected since v0.21.1; use `bd import --force` if sync issues            |
| Find database location   | `bd where`                                                                     |
| Orphaned issues          | `bd orphans`                                                                   |
| Move issue to new parent | `bd update [id] --parent [new-parent-id]`                                      |

### New Statuses

| Status     | Purpose                     | Usage                              |
| ---------- | --------------------------- | ---------------------------------- |
| `deferred` | Icebox (not ready for work) | `bd update [id] --status deferred` |

---

### Getting Additional Help

**Beads Documentation:**

- [Beads Troubleshooting](https://github.com/steveyegge/beads/blob/main/docs/TROUBLESHOOTING.md)
- [Beads Error Handling](https://github.com/steveyegge/beads/blob/main/docs/ERROR_HANDLING.md)
