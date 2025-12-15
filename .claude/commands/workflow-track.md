---
argument-hint: [path/to/implementation-plan.md]
description: Set up Beads issue tracking for planned work with proper hierarchy
---

## `/workflow-track` - Set up Beads tracking for planned work

**Usage:** `/workflow-track [path/to/implementation-plan.md]`

Use this command when ready to track planned work in Beads issue system.

This command converts your implementation plan tasks into **self-contained** Beads issues with full task content stored in descriptions.

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

**1. Read Implementation Plan**: Parse the plan document to identify all tasks

**2. Extract Full Task Content**: For each task, extract the COMPLETE content including:
   - File paths to create/modify
   - Code examples (tests, implementations)
   - Commands to run (test commands, verification steps)
   - Expected outcomes

**3. Create Self-Contained Issues**: Store the full task content in each issue's description field. This eliminates the need to re-read the entire plan when working on individual tasks.

**4. Establish Hierarchy**: Link all task issues to the parent epic using `--parent`

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

Create the issue with FULL content:
```bash
bd $BD_FLAGS create "Task 3: Task Model" --parent [epic-id] -t task -p 2 --description="$(cat <<'EOF'
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

### Issue Creation Guidelines

**IMPORTANT:** Do NOT specify a custom ID or prefix. Beads auto-generates IDs using the project directory name.

**EFFICIENCY:** Create all issues in batch mode:

```bash
# Create all tasks in one batch with full descriptions
bd $BD_FLAGS create "Task 1: Project Setup" --parent $EPIC_ID -t task -p 2 --description="$(cat <<'EOF'
[Full Task 1 content from plan]
EOF
)" --json && \
bd $BD_FLAGS create "Task 2: Exceptions" --parent $EPIC_ID -t task -p 2 --description="$(cat <<'EOF'
[Full Task 2 content from plan]
EOF
)" --json && \
bd $BD_FLAGS create "Task 3: Task Model" --parent $EPIC_ID -t task -p 2 --description="$(cat <<'EOF'
[Full Task 3 content from plan]
EOF
)" --json
# ... continue for all tasks
```

---

### Before Using This Command

- Ensure you have a completed implementation plan (from writing-plans skill)
- Verify that Beads has been initialized with `bd init --quiet`
- Identify the epic ID to use as parent (from `/workflow-start`)

### After Using This Command

- Use `/workflow-work` to begin implementation
- Each issue is self-contained - no need to re-read the full plan
- Issues available via `bd ready` for tracking

### Mapping Guidelines

- Implementation plan → Beads epic (auto-generated ID like `project-name-abc`)
- Plan tasks → Beads child issues (auto-generated like `project-name-abc.1`, `project-name-abc.2`)
- See [001-project-principles.md](../.claude/rules/001-project-principles.md#priority_system) for priority guidelines
- Default to Priority 2 (Medium) for most tasks

### Troubleshooting

If issue creation fails, see [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting) for common solutions.

**Common issues:**
- "prefix mismatch" → Don't specify custom IDs, let Beads auto-generate
- Description too long → Beads handles 10K+ chars fine, not a real limit
- Special characters → Use heredoc (`<<'EOF'`) for proper escaping
