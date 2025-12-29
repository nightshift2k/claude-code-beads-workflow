# Beads CLI JSON Patterns

> **Version Requirements:** This documentation targets Beads CLI v0.37.0+ (v0.39.1+ recommended).
> Run `bd version` to check. Features marked with version tags require that version or later.
>
> **⚠️ CRITICAL:** `bd create` returns an object `{...}`. ALL other commands return arrays `[{...}]`.
> Use `.id` for create, `.[0].id` for everything else.

<beads_json_critical>

## Critical: Know Which Commands Return Arrays vs Objects

Beads CLI commands with `--json` return **different formats** depending on the command:

| Command      | Returns             | jq Pattern                       |
| ------------ | ------------------- | -------------------------------- |
| `bd create`  | **object** `{...}`  | `.id`                            |
| `bd show`    | **array** `[{...}]` | `.[0].id`                        |
| `bd list`    | **array** `[{...}]` | `.[].id`                         |
| `bd ready`   | **array** `[{...}]` | `.[].id`                         |
| `bd blocked` | **array** `[{...}]` | `.[].id` with `blocked_by` field |
| `bd update`  | **array** `[{...}]` | `.[0].id`                        |
| `bd close`   | **array** `[{...}]` | `.[0].id`                        |

### Correct jq Patterns

| Scenario       | Pattern        | Example                                                  |
| -------------- | -------------- | -------------------------------------------------------- |
| After create   | `.field`       | `bd create "Task" --json \| jq -r '.id'`                 |
| Single result  | `.[0].field`   | `bd show $ID --json \| jq -r '.[0].id'`                  |
| All results    | `.[].field`    | `bd list --json \| jq -r '.[].id'`                       |
| Count          | `. \| length`  | `bd ready --json \| jq '. \| length'`                    |
| Formatted list | `.[] \| "..."` | `bd ready --json \| jq -r '.[] \| "[\(.id)] \(.title)"'` |

### Common Errors

```bash
# WRONG for bd create - causes "Cannot index object with number"
bd create "Task" --json | jq -r '.[0].id'

# RIGHT for bd create - it returns an object
bd create "Task" --json | jq -r '.id'

# WRONG for bd show - causes "Cannot index array with string"
bd show $ID --json | jq -r '.id'

# RIGHT for bd show - it returns an array
bd show $ID --json | jq -r '.[0].id'
```

### Why Different Formats?

- `bd create` returns the single created issue as an **object**
- `bd list/show/ready` return potentially multiple results as an **array**
- `bd update/close` return affected issues as an **array** (could be multiple)
  </beads_json_critical>

## Other Beads CLI Gotchas

### Stderr/Stdout Separation (CRITICAL)

Beads outputs JSON to **stdout** and warnings to **stderr**. Never combine them:

| Pattern                           | Result                    |
| --------------------------------- | ------------------------- |
| `bd create "X" --json \| jq`      | Works                     |
| `bd create "X" --json 2>&1 \| jq` | Breaks if warning emitted |

**Common warning triggers:**

- Missing description ("`--description` or `--body-file` recommended")
- Deprecated flags
- Sync reminders

**Prevention:** Always include a description to suppress warnings:

```bash
# WRONG - may emit warning, breaking jq
bd create "Task" --json | jq -r '.id'

# RIGHT - description suppresses warning
bd create "Task" --description "Brief description" --json | jq -r '.id'

# OR use --body-file for complex content
bd create "Task" --body-file /tmp/desc.md --json | jq -r '.id'
```

### bd blocked Output Structure

The `bd blocked` command returns issues that are blocked by dependencies:

```bash
bd blocked --json
# Returns array of blocked issues
```

**Expected structure** (from Beads CLI output):

```json
[
  {
    "id": "myproj-abc.2",
    "title": "Task 2",
    "blocked_by": ["myproj-abc.1"],
    "status": "open",
    ...other issue fields
  }
]
```

**Key field:** `blocked_by` contains an array of blocking issue IDs. Use defensive access: `.get("blocked_by", [])` or jq: `.[].blocked_by // []`.

| Command      | Returns         | Key Field                           | jq Pattern             |
| ------------ | --------------- | ----------------------------------- | ---------------------- |
| `bd blocked` | array of issues | `blocked_by` (list of blocking IDs) | `.[].blocked_by // []` |

**Example usage:**

```bash
# Get all blocked issues
bd blocked --json

# Get blocking IDs for first blocked issue
bd blocked --json | jq -r '.[0].blocked_by[]'

# Find issues blocked by specific ID
bd blocked --json | jq '.[] | select(.blocked_by | contains(["myproj-abc.1"]))'
```

### Retry Guidance for Parse Failures (CRITICAL)

A jq parse error does NOT mean the `bd` command failed:

| Error Type          | Command Succeeded? | Retry Safe? | Action                   |
| ------------------- | ------------------ | ----------- | ------------------------ |
| `bd` exits non-zero | No                 | Yes         | Retry with fix           |
| jq parse error      | **Yes**            | **NO**      | Search for created issue |

**Why retrying is dangerous:** The `bd create` command succeeded before jq failed. Retrying creates a duplicate issue.

**Recovery pattern:**

```bash
# jq failed, but did bd succeed?
bd list --json | jq -r '.[-1]'  # Check most recent issue

# Or search by title
bd list --json | jq '.[] | select(.title | contains("Task title"))'
```

**Rule:** If jq fails, investigate before retrying. The issue likely already exists.

### Sandbox Mode (Auto-Detected)

Beads v0.21.1+ auto-detects Claude Code's sandboxed environment. No explicit flag needed:

```bash
bd list --json  # Sandbox mode detected automatically
```

**Note:** The `.claude/lib/workflow.py` tool still passes `--sandbox` for backwards compatibility with older Beads versions.

### Hierarchical IDs

Use `--parent --force` to create child issues with dotted IDs:

```bash
bd create "Task" --parent $EPIC_ID --force -t task --json
# Creates: pydo-abc.1, pydo-abc.2, etc.
```

### Flag Spelling: `--notes` not `--note`

Use the **plural** form:

```bash
# WRONG - unknown flag error
bd update $ID --note "Progress update" --json

# RIGHT - plural form
bd update $ID --notes "Progress update" --json
```

### Prefix Requirements

- Lowercase letters, numbers, hyphens only
- Must start with letter, end with hyphen
- Prefer short prefixes for readability (no hard limit)

See @CLAUDE.md for full prefix guidelines.

---

## Useful Flags and Commands

### Long Descriptions: `--body-file` (MANDATORY)

> **⚠️ CRITICAL:** `--description` with heredoc **FAILS SILENTLY** when content contains code blocks.
> Shell interprets backticks as command substitution, causing **complete data loss** with NO ERROR.
> **ALWAYS use `--body-file` for complex content.**

**Test results:**
| Method | Simple Text | Multi-line | Code Blocks |
|--------|-------------|------------|-------------|
| `--description="$VAR"` | ✅ | ❌ (newlines lost) | ❌ (0 bytes!) |
| `--body-file` | ✅ | ✅ | ✅ |

**CORRECT method for complex content:**

````bash
# Write content to temp file
cat > /tmp/task.md <<'EOF'
**Files:**
- Create: `app.py`

**Code:**
```python
def example():
    return True
````

EOF

# Create issue with --body-file (ONLY safe method)

bd create "Task title" --body-file /tmp/task.md --json

````

**WRONG - DO NOT USE with code blocks:**
```bash
# This SILENTLY LOSES DATA when content has backticks
bd create "Task title" --description="$(cat <<'EOF'
Code with `backticks` here
EOF
)" --json
# Result: Description is EMPTY (0 bytes, no error!)
````

### Filtering: `--type`

Filter issues by type:

```bash
# Get ready tasks only (excludes epics)
bd ready --type task --json

# List all epics
bd list --type epic --json

# List all tasks
bd list --type task --json
```

### Filtering by Parent (v0.37.0+)

Filter ready and blocked by epic:

```bash
# Ready issues under specific epic
bd ready --parent $EPIC_ID --json

# Blocked issues under specific epic
bd blocked --parent $EPIC_ID --json
```

### Close with Suggestions (v0.37.0+)

Show newly unblocked issues after closing:

```bash
bd close [id] --reason "Done" --suggest-next --json
# Returns closed issue plus list of newly unblocked issues
```

### Estimates: `--estimate`

Add time estimates to issues:

```bash
bd create "Task" --estimate "2h" --json
bd update [id] --estimate "4h" --json
```

### Status Management

New statuses available:

```bash
# Defer to icebox (not ready yet)
bd update [id] --status deferred --json
```

### Filtering by Parent

List children of a specific parent issue:

```bash
# All children of an epic
bd list --parent $EPIC_ID --json

# Open children only
bd list --parent $EPIC_ID --status open --json

# Count completed children
bd list --parent $EPIC_ID --status closed --json | jq '. | length'
```

**Replaces inefficient jq pattern:**

```bash
# Old (inefficient)
bd list --json | jq '.[] | select(.parent == "epic-id")'

# New (native)
bd list --parent epic-id --json
```

### Dependency Visualization

```bash
# Dependency graph for specific issue (required argument)
bd graph [issue-id]

# Dependency tree for specific issue
bd dep tree [issue-id]

# Detect circular dependencies
bd dep cycles
```

### Reparenting Issues (v0.39.1+)

Move an issue to a different parent:

```bash
bd update [id] --parent [new-parent-id] --json
```

### Diagnostic Commands

```bash
# Auto-repair database corruption (v0.38.0+)
bd doctor --fix

# Show active database location (v0.39.1+)
bd where

# Find orphaned issues - no parent (v0.39.0+)
bd orphans
```

### Live Issue Monitoring (v0.36.0+)

For interactive sessions, use the built-in formatted viewer:

```bash
# Tree view with status/priority symbols
bd list --pretty

# Live updates (auto-refreshes on changes)
bd list --pretty --watch
```

**Output example:**

```
○ 🟠 myproj-abc - [EPIC] Feature name
├── ○ 🔴 myproj-abc.1 - Critical task
└── ○ 🟡 myproj-abc.2 - Normal task

Legend: ○ open | ◐ in progress | ⊗ blocked | 🔴 P0 | 🟠 P1 | 🟡 P2 | 🔵 P3 | ⚪ P4
```

**Use cases:**

- Long implementation sessions - monitor progress in a terminal
- Team coordination - watch for status changes
- Debugging blocked work - visualize dependencies

### Searching Issues (v0.36.0+)

Full-text search across title, description, and ID with filters:

```bash
# Basic keyword search (query REQUIRED)
bd search "authentication" --json

# Combined with filters
bd search "task" --type task --priority-min 0 --priority-max 1 --json

# Sort results
bd search "bug" --sort priority --json
bd search "feature" --sort created --reverse --json

# Date filtering
bd search "refactor" --created-after 2025-01-01 --json
bd search "bug" --updated-after 2025-01-01 --json
```

**Available filters:**

| Filter                   | Example                             | Description                                  |
| ------------------------ | ----------------------------------- | -------------------------------------------- |
| `--type`                 | `--type task`                       | bug, feature, task, epic, chore, gate        |
| `--status`               | `--status open`                     | open, in_progress, blocked, deferred, closed |
| `--priority-min/max`     | `--priority-min 0 --priority-max 1` | Filter by priority range                     |
| `--created-after/before` | `--created-after 2025-01-01`        | Date filter (YYYY-MM-DD)                     |
| `--updated-after/before` | `--updated-after 2025-01-01`        | Date filter (YYYY-MM-DD)                     |
| `--assignee`             | `--assignee alice`                  | Filter by assignee                           |
| `--label`                | `--label backend`                   | Filter by label (AND)                        |
| `--sort`                 | `--sort priority`                   | priority, created, updated, status, title    |

**Important:** `bd search` requires a query string. For filter-only queries, use `bd list` with filters instead:

```bash
# WRONG - prints help (empty query not allowed)
bd search "" --type task

# RIGHT - use bd list for filter-only
bd list --type task --status open --json
```

### `bd graph` Requirements and Workaround

The `bd graph` command requires an issue-id argument and does NOT auto-fallback to direct mode:

| Command         | Without Daemon | With `--no-daemon` |
| --------------- | -------------- | ------------------ |
| `bd list`       | Auto-fallback  | Works              |
| `bd ready`      | Auto-fallback  | Works              |
| `bd graph [id]` | **Fails**      | Works              |

**Always use `--no-daemon` with `bd graph`:**

```bash
# WRONG - missing issue-id argument
bd graph
bd graph --no-daemon

# RIGHT - includes required issue-id and --no-daemon
bd graph [issue-id]
bd graph [issue-id] --no-daemon

# Examples
bd graph pydo-abc --no-daemon
bd graph myproj-xyz.1 --no-daemon
```

**Note:** This is an upstream Beads CLI requirement. The issue-id argument is mandatory.

### Emergency Recovery

```bash
# Reset database completely (keeps JSONL)
bd reset

# Rebuild from JSONL (less aggressive)
bd import --force
```

---

## Self-Contained Descriptions

<self_contained_descriptions_critical>
**CRITICAL:** Make Beads issue descriptions fully self-contained. Each description must provide everything an agent needs to complete the task without accessing other files.

**NEVER use these phrases:**

- "see above"
- "see implementation plan"
- "as described earlier"
- "refer to [external document]"

**Why:** When dispatching work via `bd show [id]`, the agent receives ONLY the issue content. External references create hidden dependencies that break agent dispatch.

**WRONG:**

```markdown
Implement user login. See implementation plan for details.
```

**CORRECT:**

````markdown
**Files:**

- Create: `auth.py`

**Step 1: Write test**

```python
def test_login():
    assert login("user", "pass") == True
```
````

**Step 2: Implement**

```python
def login(username, password):
    # Implementation here
    pass
```

```

**When creating or updating issues:**
- Include all file paths
- Include all code examples
- Include all commands
- Include expected outcomes
- Write as if no other context exists
</self_contained_descriptions_critical>

---

## Related Files

- @CLAUDE.md - Main workflow instructions and troubleshooting
- @.claude/commands/workflow-track.md - Hierarchical ID usage examples
- @.claude/commands/workflow-init.md - Prefix initialization
```
