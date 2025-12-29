---
argument-hint: "[epic-id | task-id]"
description: Course correction when human spots divergence mid-implementation
---

## Intent

Steer an epic back on track when completed work diverges from intent by creating a P0 correction task.

## When to Use

- Human review identifies divergence from intent
- Completed tasks require rework
- Pending tasks need context update before execution

## When NOT to Use

- Research question needs answering → use `/workflow-question-ask`
- Research findings ready to apply → use `/workflow-steer-research`
- Adding notes only → use `bd update --notes`

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-steer-correct
```

Gather before proceeding:

- Epic ID (or task ID to derive epic)
- List of completed and remaining tasks
- Human description of what needs correction

## Decision Framework

| State                    | Action                       | Outcome                 |
| ------------------------ | ---------------------------- | ----------------------- |
| Task ID provided         | Extract epic ID (before `.`) | Epic context available  |
| Epic not found           | Error with guidance          | User corrects ID        |
| No tasks affected        | Document in epic notes       | No correction task      |
| Completed tasks affected | Mark as REOPEN               | Tasks need redo         |
| Pending tasks affected   | Mark as UPDATE               | Tasks need context      |
| User confirms plan       | Create P0 correction         | Surfaces first in ready |

## Interactive Flow (CRITICAL)

This command requires human interaction:

| Step | Prompt                              | Wait For               |
| ---- | ----------------------------------- | ---------------------- |
| 1    | Show progress (completed/remaining) | -                      |
| 2    | "What needs correction?"            | Correction description |
| 3    | "Which tasks affected?"             | Task IDs or "all"      |
| 4    | Show impact table                   | -                      |
| 5    | "Apply correction? (Y/n)"           | Confirmation           |

## Execution

1. Validate epic/task exists, extract epic ID if task provided
2. Display progress (completed vs remaining tasks)
3. Ask human: "What needs correction?"
4. Ask human: "Which tasks are affected?"
5. Categorize impact (REOPEN completed, UPDATE pending)
6. Show proposed plan, wait for confirmation
7. Create P0 correction task under epic (`--parent --force`)
8. Update epic steering log with CORRECT entry
9. Reopen affected completed tasks with notes + blocking dependency
10. Update affected pending tasks with context + blocking dependency
11. **Related tasks review** (scan for stale references)
12. Display summary and ready work

## Related Tasks Review (CRITICAL)

After updating directly affected tasks, scan ALL open tasks in the epic for stale references:

**Process:**

1. Extract correction keywords (the OLD value being replaced)
2. Search all open task descriptions for those keywords
3. Report matches with task ID and keyword found
4. Ask user whether to update additional tasks

**Decision Framework:**

| User Response | Action                                            |
| ------------- | ------------------------------------------------- |
| Yes           | Update task descriptions with corrected details   |
| No            | Continue, note in steering log that user declined |

**Example:**

```
Correction: "JSON storage" → "SQLite storage"
Keywords to scan: "json", "tasks.json", "JSON storage"

Found stale references:
- pydo-abc.7 (Docs): Contains "tasks.json" in description
- pydo-abc.9 (Tests): Contains "JSON storage" in description

Update these tasks with SQLite references? (Y/n)
```

**Why this matters:** Without this check, tasks created before the correction may still reference obsolete approaches, confusing agents during execution.

## Success Criteria

- [ ] Correction task created with P0 priority
- [ ] All affected completed tasks reopened
- [ ] All affected pending tasks updated with context
- [ ] Blocking dependencies established (affected → correction)
- [ ] Epic steering log updated with CORRECT entry
- [ ] Related tasks scanned for stale references
- [ ] User prompted about additional task updates (if matches found)
- [ ] Correction task appears first in `bd ready`

## Steering Log Entry (CRITICAL)

Every correction MUST be logged in the epic description:

```markdown
### [YYYY-MM-DDTHH:MM:SSZ] CORRECT: Short Description

**Trigger:** Human review
**Correction:** correction-task-id created
**Reopened:** N task(s)
**Updated:** N task(s)
**Rationale:** Description of divergence
```

**Timestamp:** Use UTC (`date -u +"%Y-%m-%dT%H:%M:%SZ"`) for cross-timezone consistency.

## Impact Categories

| Task Status | Category | Action                                 |
| ----------- | -------- | -------------------------------------- |
| closed      | REOPEN   | Reopen + add blocking dependency       |
| open        | UPDATE   | Add context note + blocking dependency |
| in_progress | UPDATE   | Add context note + blocking dependency |

## Edge Considerations

- **Circular dependencies**: Check with `bd dep cycles` after adding dependencies
- **No tasks affected**: Document concern in epic notes instead
- **Scope unclear**: Break into smaller corrections
- **User cancels**: Exit gracefully; make no changes

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-steer-correct

# Validate epic/task
bd show $EPIC_OR_TASK --json | jq '.[0]'

# Extract epic ID from task (e.g., pydo-abc.4 → pydo-abc)
echo "$TASK_ID" | cut -d. -f1

# List completed tasks for epic
bd list --status closed --json | jq --arg prefix "$EPIC_ID." '.[] | select(.id | startswith($prefix))'

# List remaining tasks for epic
bd list --status open --json | jq --arg prefix "$EPIC_ID." '.[] | select(.id | startswith($prefix))'

# Create P0 correction task (MUST use --parent --force)
cat > /tmp/correction.md <<'EOF'
**Correction Required**

Human review identified divergence from intent:

[CORRECTION_DESC]

**Affected Tasks:** N
- Reopen: N
- Update: N

**Action Required:**
Address this correction before proceeding with affected tasks.
EOF
bd create "Correction: [short description]" --parent $EPIC_ID --force -t task -p 0 --body-file /tmp/correction.md --json

# Reopen completed task
bd update $TASK_ID --notes "Reopened for correction: [desc] (see $CORRECTION_ID)" --json
bd update $TASK_ID --status open --json
bd dep add $TASK_ID $CORRECTION_ID

# Update pending task with blocking
cat > /tmp/task-context.md <<'EOF'
[current description]

---

**Steering Update (YYYY-MM-DD):**

**Note:** Blocked pending correction: [desc] (see $CORRECTION_ID)
EOF
bd update $TASK_ID --body-file /tmp/task-context.md --json
bd dep add $TASK_ID $CORRECTION_ID

# Check for circular dependencies
bd dep cycles

# Update epic steering log (MUST use --body-file)
cat > /tmp/epic-update.md <<'EOF'
[full epic description with new CORRECT entry]
EOF
bd update $EPIC_ID --body-file /tmp/epic-update.md --json

# Check ready work (P0 correction should appear first)
bd ready --json | jq -r '.[] | "[\(.id)] P\(.priority) \(.title)"'

# Related tasks review: scan for stale keywords
# Extract keywords from correction (e.g., "json", "tasks.json")
KEYWORDS="json|tasks.json"
bd list --parent $EPIC_ID --status open --json | jq -r --arg kw "$KEYWORDS" \
  '.[] | select(.description | test($kw; "i")) | "[\(.id)] \(.title)"'
```

## Workflow Example

```
Epic: pydo-abc - Build pydo CLI
├─ pydo-abc.1 ✅ Project Setup (complete)
├─ pydo-abc.2 ✅ Exceptions Module (complete)
├─ pydo-abc.3 ✅ Task Model (complete)
├─ pydo-abc.4 ✅ Storage Layer (complete - WRONG!)
├─ pydo-abc.5 ⏳ CLI Add Command (pending)
└─ ...

Human discovers: "Storage uses JSON but should use SQLite!"

/workflow-steer-correct pydo-abc
  ├─> Shows progress (4 complete, 8 remaining)
  ├─> Asks: "What needs correction?"
  ├─> Human: "Task 4 uses JSON storage but should use SQLite"
  ├─> Shows affected tasks, asks confirmation
  ├─> Creates pydo-abc.13 "Correction: Refactor to SQLite" (P0)
  ├─> Reopens pydo-abc.4 with correction note
  ├─> Updates pydo-abc.5-8: adds blocking dependency
  └─> Correction surfaces first in ready work
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - --body-file requirement
- @.claude/rules/multi-agent-coordination.md - Multi-agent coordination
- @.claude/commands/workflow-overview.md - View steering log
- @.claude/commands/workflow-work.md - Resume corrected work
