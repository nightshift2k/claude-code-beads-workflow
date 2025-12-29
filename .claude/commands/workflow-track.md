---
argument-hint: [path/to/implementation-plan.md]
description: Set up Beads issue tracking for planned work with proper hierarchy
---

## Intent

Convert implementation plan tasks into self-contained Beads issues with hierarchical IDs, then delete the plan file.

## When to Use

- Implementation plan complete from `/workflow-start` + planning
- Ready to convert plan tasks to trackable issues
- Epic exists from `/workflow-start`

## When NOT to Use

- No epic exists → use `/workflow-start` first
- Want to execute existing tracked work → use `/workflow-work`
- Adding ad-hoc task → use `bd create` directly

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-track
```

Gather before proceeding:

- Epic ID from `/workflow-start` output
- Path to implementation plan file
- Verify epic exists with `bd show [epic-id]`

## Decision Framework

| State              | Action                                    | Outcome                |
| ------------------ | ----------------------------------------- | ---------------------- |
| Plan path provided | Read and parse plan                       | Tasks identified       |
| No plan path       | List `docs/plans/`, prompt selection      | Plan selected          |
| Epic ID available  | Use `--parent --force`                    | Hierarchical IDs       |
| No epic ID         | Error, require `/workflow-start` first    | Blocked                |
| Tasks extracted    | Create issues with `--body-file`          | Self-contained issues  |
| All issues created | Update epic description, delete plan file | Single source of truth |

## Issue Type Selection

Select issue type based on task characteristics:

| Type      | Trigger                      | Example                      |
| --------- | ---------------------------- | ---------------------------- |
| `epic`    | Parent container for feature | "User authentication system" |
| `feature` | New user-facing capability   | "Add user login"             |
| `bug`     | Fixes broken behavior        | "Fix login validation error" |
| `chore`   | Maintenance work             | "Update dependencies"        |
| `task`    | Default for implementation   | "Implement SQLite layer"     |

**Selection precedence:** epic > feature > bug > chore > task

**When unclear:** Default to `task`.

## Agent Label Selection (Optional)

Auto-detect agent label from file types and keywords:

| Label                      | File Signals         | Keyword Signals                 |
| -------------------------- | -------------------- | ------------------------------- |
| `agent:python-expert`      | `.py`                | pytest, pip, uv, CLI            |
| `agent:golang-expert`      | `.go`                | Go modules, go test             |
| `agent:frontend-architect` | `.tsx`, `.vue`       | React, Vue, component           |
| `agent:backend-architect`  | -                    | server, database, system        |
| `agent:api-designer`       | -                    | API, endpoint, REST, GraphQL    |
| `agent:security-engineer`  | -                    | auth, validation, secrets       |
| `agent:devops-architect`   | `.yml`, `Dockerfile` | CI/CD, deploy, Docker           |
| `agent:refactoring-expert` | -                    | cleanup, restructure, tech debt |
| `agent:general-purpose`    | -                    | unclear scope, research         |

**Agent labels hint at expertise; they do not mandate dispatch.** Omit if unclear; the orchestrator can override.

## Hierarchical IDs (CRITICAL)

**Always use `--parent [epic-id] --force` for hierarchical IDs:**

| Without `--parent --force` | With `--parent --force`         |
| -------------------------- | ------------------------------- |
| `pydo-xyz` (random)        | `pydo-abc.1` (sequential)       |
| `pydo-def` (random)        | `pydo-abc.2` (sequential)       |
| No visible hierarchy       | Clear parent-child relationship |

**Why `--force`:** Required workaround for Beads quirk (false "prefix mismatch" error).

## Self-Contained Descriptions (CRITICAL)

Store COMPLETE task content in issue descriptions:

| Include           | Why                          |
| ----------------- | ---------------------------- |
| All file paths    | Agent knows what to modify   |
| All code examples | No need to re-read plan      |
| All commands      | Verification steps available |
| Expected outcomes | Success criteria clear       |

**Use `--body-file` for complex content.** The `--description` heredoc fails silently with code blocks.

## Epic Description Structure

After tracking, the epic description becomes the plan's single source of truth:

```markdown
## Status Summary

**Progress:** 0/N tasks (0%)
**State:** Not Started

---

## Steering Log

### [YYYY-MM-DDTHH:MM:SSZ] INIT: Plan Tracked

**Source:** path/to/plan.md
**Epic:** epic-id
**Tasks Created:** N

---

## Original Plan

[Full plan content]
```

## Execution

1. Verify epic exists (from `/workflow-start`)
2. Read and parse implementation plan
3. For each task: extract COMPLETE content to temp file
4. Create issue with `--parent --force` + `--body-file`
5. Update epic description with steering log + plan
6. **Sync checkpoint (CRITICAL)** - Persist new issues before deleting plan:
   - Check team mode: `[ -f .claude/ccbw-flag-team-mode ]`
   - If team mode enabled: `git add .beads/ && bd sync`
   - If disabled: `bd sync --flush-only`
   - **Why sync here:** Session crashes after creation but before sync result in complete data loss. Syncing immediately after bulk creation protects against data loss.
7. Delete plan file (content now in Beads)
8. Report task count and next steps

## Success Criteria

- [ ] All tasks have hierarchical IDs (epic-id.1, epic-id.2, etc.)
- [ ] Each issue description is self-contained (no external references)
- [ ] Epic description contains steering log and original plan
- [ ] Sync checkpoint completed (issues persisted to JSONL)
- [ ] Plan file deleted
- [ ] `bd list` shows correct task count

## Edge Considerations

- **Long descriptions**: Beads handles 10K+ chars fine
- **Code blocks in descriptions**: MUST use `--body-file` (not `--description`)
- **Plan file deletion fails**: Warn but continue
- **Special characters**: Use heredoc with `<<'EOF'` (quoted)

## Reference Commands

````bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-track

# Verify epic exists (returns ARRAY)
bd show $EPIC_ID --json | jq '.[0]'

# Write task content to temp file
cat > /tmp/task-1.md <<'EOF'
**Files:**
- Create: `file.py`

**Code:**
```python
def example():
    pass
````

EOF

# Create child issue with hierarchical ID

bd create "Task 1: Title" --parent $EPIC_ID --force -t task -p 2 --body-file /tmp/task-1.md --json

# Returns: {"id": "epic-id.1", ...}

# Create with type and agent label

bd create "Implement SQLite storage" --parent $EPIC_ID --force \
 -t task -p 2 --label agent:python-expert --body-file /tmp/task.md --json

# Check for agent label during dispatch

bd show [issue-id] --json | jq -r '.[0].labels[]? | select(startswith("agent:"))'

# Count child tasks (native filter - preferred)

bd list --parent $EPIC_ID --json | jq '. | length'

# Verify child issues created (native filter)

bd list --parent $EPIC_ID --status open --json

# Update epic with structured description

bd update $EPIC_ID --body-file /tmp/epic-description.md --json

# Sync checkpoint - persist issues before deleting plan

# Check team mode

if [ -f .claude/ccbw-flag-team-mode ]; then
git add .beads/ && bd sync
else
bd sync --flush-only
fi

# Delete plan file after tracking

rm "$PLAN_PATH"

# Verify hierarchy

bd list --json | jq '.[] | select(.id | contains("."))'

# Cleanup: delete child issues if needed

bd list --json | jq -r '.[] | select(.id | contains(".")) | .id' | xargs -I {} bd delete {} --force

```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "prefix mismatch" with --parent | Beads quirk | Add `--force` flag |
| Random IDs instead of .1, .2 | Missing --parent | Use `--parent $EPIC_ID --force` |
| "parent issue not found" | Wrong epic ID | Verify with `bd show $EPIC_ID` |
| Empty description (0 bytes) | Used --description with code blocks | Use `--body-file` |

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/agent-dispatch.md - Agent label selection and dispatch rules
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - --body-file requirement
- @.claude/rules/project-principles.md - Priority guidelines
- @.claude/commands/workflow-start.md - Creates epic first
- @.claude/commands/workflow-execute.md - Execute tracked plan
```
