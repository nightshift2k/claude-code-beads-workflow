---
argument-hint: [path/to/implementation-plan.md]
description: Set up Beads issue tracking for planned work with proper hierarchy
---

## `/workflow-track` - Set up Beads tracking for planned work

**Usage:** `/workflow-track [path/to/implementation-plan.md]`

Use this command when ready to track planned work in Beads issue system.

This command converts your implementation plan tasks into **self-contained** Beads issues with:
- Full task content stored in descriptions (token-efficient)
- Hierarchical IDs using `--parent --force` (e.g., `pydo-abc.1`, `pydo-abc.2`)

### Argument

- `path/to/implementation-plan.md` - Path to the implementation plan document to track
- If not provided, will prompt to select from available plans in `docs/plans/`

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
source .claude/lib/workflow-precheck.sh
workflow_precheck "workflow-track"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

### Process

**1. Get Epic ID**: Retrieve the parent epic from `/workflow-start`
```bash
# Get the epic ID (should be from /workflow-start output)
EPIC_ID="<epic-id-from-workflow-start>"

# Verify epic exists (NOTE: bd show returns an ARRAY, not object)
bd show $EPIC_ID --json
# Returns: [{...}] - use jq '.[0].field' to access fields, NOT jq '.field'
```

**⚠️ Beads JSON:** All `bd` commands return arrays. See @.claude/rules/004-beads-json-patterns.md for correct jq usage.

**2. Read Implementation Plan**: Parse the plan document to identify all tasks

**3. Extract Full Task Content**: For each task, extract the COMPLETE content including:
   - File paths to create/modify
   - Code examples (tests, implementations)
   - Commands to run (test commands, verification steps)
   - Expected outcomes

**4. Create Hierarchical Child Issues**: Use `--parent $EPIC_ID --force` for sequential IDs

---

### Critical: Hierarchical IDs with `--parent --force`

<hierarchical_ids>
**WHY `--parent`:** Creates child issues with sequential dotted IDs:
- Epic: `pydo-abc`
- Child 1: `pydo-abc.1`
- Child 2: `pydo-abc.2`
- Child 3: `pydo-abc.3`

**WHY `--force`:** Required to work around a Beads quirk where `--parent` triggers a false "prefix mismatch" error. The `--force` flag is safe here - it just allows the hierarchical ID creation.

**Without `--parent --force`:** Each task gets an independent random ID:
- Epic: `pydo-abc`
- Task 1: `pydo-xyz` (no relationship visible in ID)
- Task 2: `pydo-def` (no relationship visible in ID)
</hierarchical_ids>

**ALWAYS use both flags together:**
```bash
bd $BD_FLAGS create "Task Title" --parent $EPIC_ID --force -t task -p 2 --description="..." --json
```

---

### Critical: Store Full Task Content in Descriptions

**WHY:** Implementation plans can be 2000+ lines. Reading the entire file for each task is token-inefficient. By storing full task content in descriptions, `/workflow-work` only needs to read the specific issue.

**WHAT TO STORE:** Each issue description should contain the COMPLETE task from the plan:
- All file paths
- All code examples (test code, implementation code)
- All bash commands
- Expected outcomes and verification steps

**Example - extracting Task 3 from a plan:**

From the plan:
```markdown
## Task 3: Task Model

**Files:**
- Modify: `pydo/models.py`
- Create: `tests/test_models.py`

**Step 1: Write failing test**
\`\`\`python
def test_create_task():
    task = Task(description="Test")
    assert task.status == "pending"
\`\`\`

**Step 2: Run test**
\`\`\`bash
uv run pytest tests/test_models.py -v
\`\`\`
Expected: FAIL

**Step 3: Implement**
...
```

Create the issue with FULL content AND hierarchical ID:
```bash
bd $BD_FLAGS create "Task 3: Task Model" --parent $EPIC_ID --force -t task -p 2 --description="$(cat <<'EOF'
**Files:**
- Modify: `pydo/models.py`
- Create: `tests/test_models.py`

**Step 1: Write failing test**
```python
def test_create_task():
    task = Task(description="Test")
    assert task.status == "pending"
```

**Step 2: Run test**
```bash
uv run pytest tests/test_models.py -v
```
Expected: FAIL

**Step 3: Implement**
[full implementation code here]
EOF
)" --json
```

---

### Issue Creation: Batch Mode with Hierarchical IDs

**EFFICIENCY:** Create all issues in batch mode with `--parent --force`:

```bash
# Set epic ID from /workflow-start
EPIC_ID="pydo-abc"  # Replace with actual epic ID

# Create all tasks in one batch with full descriptions and hierarchical IDs
bd $BD_FLAGS create "Task 1: Project Setup" --parent $EPIC_ID --force -t task -p 2 --description="$(cat <<'EOF'
[Full Task 1 content from plan]
EOF
)" --json && \
bd $BD_FLAGS create "Task 2: Exceptions" --parent $EPIC_ID --force -t task -p 2 --description="$(cat <<'EOF'
[Full Task 2 content from plan]
EOF
)" --json && \
bd $BD_FLAGS create "Task 3: Task Model" --parent $EPIC_ID --force -t task -p 2 --description="$(cat <<'EOF'
[Full Task 3 content from plan]
EOF
)" --json
# ... continue for all tasks
```

**Result:** Issues created with IDs `pydo-abc.1`, `pydo-abc.2`, `pydo-abc.3`, etc.

---

### Verify Hierarchy After Creation

```bash
# Check epic status shows children
bd epic status $EPIC_ID --json

# List all children (dotted IDs)
bd list --json | jq '.[] | select(.id | contains("."))'
```

---

### Before Using This Command

- Ensure you have a completed implementation plan (from writing-plans skill)
- Verify that Beads has been initialized with short prefix (`bd init -p <short>-`)
- **Identify the epic ID** from `/workflow-start` output - you need this for `--parent`

### After Using This Command

- Use `/workflow-work` to begin implementation
- Each issue is self-contained - no need to re-read the full plan
- Issues available via `bd ready` for tracking
- Hierarchical IDs make it easy to identify which tasks belong to which epic

### Mapping Guidelines

- Implementation plan → Beads epic (e.g., `pydo-abc`)
- Plan tasks → Beads child issues (e.g., `pydo-abc.1`, `pydo-abc.2`)
- See @.claude/rules/001-project-principles.md for priority guidelines
- Default to Priority 2 (Medium) for most tasks

### Troubleshooting

If issue creation fails, see [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting) for common solutions.

**Common issues:**
| Error | Cause | Solution |
|-------|-------|----------|
| "prefix mismatch" with `--parent` | Beads quirk | Add `--force` flag |
| Random IDs instead of `.1`, `.2` | Missing `--parent` | Use `--parent $EPIC_ID --force` |
| "parent issue not found" | Wrong epic ID | Verify with `bd show $EPIC_ID` |
| Description too long | Not a real limit | Beads handles 10K+ chars fine |
| Special characters breaking | Escaping issue | Use heredoc (`<<'EOF'`) |
| jq "Cannot index array with string" | bd returns array `[{...}]` | See @.claude/rules/004-beads-json-patterns.md |

### Cleanup: Deleting Child Issues

If you need to recreate issues:
```bash
# List all child IDs
bd list --json | jq -r '.[] | select(.id | contains(".")) | .id'

# Delete all children (keeps epic)
bd list --json | jq -r '.[] | select(.id | contains(".")) | .id' | xargs -I {} bd delete {} --force

# Or delete by issue_type
bd list --json | jq -r '.[] | select(.issue_type == "task") | .id' | xargs -I {} bd delete {} --force
```
