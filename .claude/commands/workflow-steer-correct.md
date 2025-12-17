---
argument-hint: "[epic-id | task-id]"
description: Course correction when human spots divergence mid-implementation
---

## `/workflow-steer-correct` - Course correction

Use this command when you discover AI divergence during implementation and need to correct course.

This command helps you steer an epic back on track when completed work doesn't match your intent.

**Usage:** `/workflow-steer-correct [epic-id | task-id]`

Example: `/workflow-steer-correct pydo-nh9` (epic)
Example: `/workflow-steer-correct pydo-nh9.4` (specific task)

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
uv run python .claude/lib/workflow.py precheck --name workflow-steer-correct
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

### Agent Instructions

This command guides you through an interactive course correction workflow. Follow these steps:

**1. Validate Epic/Task Exists**

Get the issue details to determine if it's an epic or task:
```bash
uv run python .claude/lib/workflow.py show $EPIC_OR_TASK --json
```

From the output, identify:
- Issue type (epic or task)
- Issue title
- If it's a task, extract the parent epic ID (e.g., `pydo-nh9.4` → `pydo-nh9`)

**2. Show Progress**

Display epic progress using the show-tasks command:
```bash
uv run python .claude/lib/workflow.py show-tasks $EPIC_ID
```

Then calculate and display:
- Total tasks for this epic
- Completed tasks count
- Remaining tasks count

Show completed tasks:
```bash
uv run python .claude/lib/workflow.py list --status closed --json
```
Filter output to show only tasks starting with `$EPIC_ID.`

Show remaining tasks:
```bash
uv run python .claude/lib/workflow.py list --status open --json
```
Filter output to show only tasks starting with `$EPIC_ID.`

**3. Interactive: Ask What Needs Correction**

Prompt the human:
```
⏺ Course Correction

Please describe what needs to be corrected:

(Example: 'Task 4 uses JSON storage but should use SQLite')

>
```

Wait for human response. Store as `CORRECTION_DESC`.

**4. Interactive: Identify Affected Tasks**

Show the remaining tasks again and ask which are affected:
```
Which tasks are affected by this correction?

Enter task IDs separated by spaces (or 'all' for all remaining tasks):

Remaining tasks:
[List from step 2]

>
```

Wait for human response. Parse the input:
- If "all": all remaining open tasks
- Otherwise: specific task IDs provided

Get affected task details:
```bash
uv run python .claude/lib/workflow.py show <task-id> --json
```

**5. Categorize Impact**

For each affected task, determine the action needed:
- **REOPEN**: If status is "closed" (completed but needs redo)
- **UPDATE**: If status is "open" or "in_progress" (pending but needs context)

Display impact table:
```
Affected tasks:
┌──────────────┬─────────────────────────────────┬──────────────┐
│ Task         │ Impact                          │ Action       │
├──────────────┼─────────────────────────────────┼──────────────┤
│ pydo-abc.4   │ Completed wrong - needs redo    │ REOPEN       │
│ pydo-abc.5   │ Description needs update        │ UPDATE       │
└──────────────┴─────────────────────────────────┴──────────────┘
```

**6. Show Proposed Plan**

Present the correction plan:
```
Proposed correction plan:

  1. Create correction task (P0): '$CORRECTION_DESC'
  2. Reopen <count> task(s) with correction note
  3. Update <count> task(s) with correction context
  4. Add blocking dependencies: affected tasks wait on correction

Apply course correction? (Y/n):
```

Wait for confirmation. If not confirmed, exit.

**7. Create Correction Task**

Create a P0 correction task under the epic:
```bash
uv run python .claude/lib/workflow.py show $EPIC_ID --json
```

Extract epic details, then create child task with full description:

**Correction task description template:**
```markdown
**Correction Required**

Human review identified divergence from intent:

<CORRECTION_DESC>

**Affected Tasks:** <count>
- Reopen: <reopen_count>
- Update: <update_count>

**Action Required:**
Address this correction before proceeding with affected tasks.
```

Use Python workflow tool to create the task with `--parent $EPIC_ID --force` for hierarchical ID.

Note: The Python workflow tool `bd_create()` handles parent relationships. Store the returned correction task ID.

**8. Reopen Affected Completed Tasks**

For each task to reopen:
```bash
# Add note explaining reopen
uv run python .claude/lib/workflow.py update $TASK_ID \
  --notes "Reopened for course correction: $CORRECTION_DESC (see $CORRECTION_ID)"

# Change status to open
uv run python .claude/lib/workflow.py update $TASK_ID --status open

# Add blocking dependency (use bd dep directly - not in Python tool yet)
bd --sandbox dep add $TASK_ID $CORRECTION_ID
```

Display progress as you go.

**9. Update Pending Tasks**

For each task to update, append correction context to description:

Get current description:
```bash
uv run python .claude/lib/workflow.py show $TASK_ID --json
```

Append to description:
```markdown
---

**Steering Update (<date>):**

**Note:** Blocked pending correction: <CORRECTION_DESC> (see <CORRECTION_ID>)
```

Update the task:
```bash
uv run python .claude/lib/workflow.py update $TASK_ID --description="<new_description>"

# Add blocking dependency
bd --sandbox dep add $TASK_ID $CORRECTION_ID
```

**10. Display Summary**

Show completion summary:
```
⏺ Course Correction Complete

Summary:
┌─────────────────────────────────────────────────────────┐
│ Created:   1 correction task (<CORRECTION_ID>)          │
│ Reopened:  <count> task(s)                              │
│ Updated:   <count> task(s)                              │
└─────────────────────────────────────────────────────────┘

Ready work (correction-first):
```

Show ready work (correction will be P0, so it appears first):
```bash
uv run python .claude/lib/workflow.py ready
```

Display:
```
To continue: /workflow-work (will pick up P0 correction first)
```

---

### Before Using This Command

- Epic must be in progress with some tasks completed
- Human has reviewed work and identified divergence
- Understand which tasks are affected by the correction

### After Using This Command

- Correction task created with P0 priority (surfaces first in ready work)
- Affected completed tasks reopened with notes
- Affected pending tasks updated and blocked
- Blocking dependencies ensure correction happens first
- Epic can continue with corrected direction

### Workflow Example

```
Epic: pydo-nh9 - Build pydo CLI
├─ pydo-nh9.1 ✅ Project Setup (complete)
├─ pydo-nh9.2 ✅ Exceptions Module (complete)
├─ pydo-nh9.3 ✅ Task Model (complete)
├─ pydo-nh9.4 ✅ Storage Layer (complete - WRONG!)
├─ pydo-nh9.5 ⏳ CLI Add Command (pending)
├─ pydo-nh9.6 ⏳ CLI List Command (pending)
└─ ...

Human discovers: "Storage uses JSON but should use SQLite!"

/workflow-steer-correct pydo-nh9

# Interactive prompts:
# - Shows progress (4 complete, 8 remaining)
# - Asks: "What needs correction?"
# - Human: "Task 4 uses JSON storage but should use SQLite"
# - Shows affected tasks: pydo-nh9.4 through pydo-nh9.8
# - Confirms correction plan

# Results:
# - Creates pydo-nh9.13 "Correction: Refactor storage to SQLite" (P0)
# - Reopens pydo-nh9.4 with note about correction
# - Updates pydo-nh9.5-8: adds blocking dependency on pydo-nh9.13
# - Correction surfaces first in ready work
```

### Troubleshooting

**If epic/task not found:**
```bash
# List active epics
uv run python .claude/lib/workflow.py list --json
# Filter for type=epic, status=open

# Show tasks for epic
uv run python .claude/lib/workflow.py show-tasks $EPIC_ID
```

**If no tasks are affected:**
- May be exploratory concern only
- Document in epic notes instead
- No correction task needed

**If correction scope is unclear:**
- Refine understanding before proceeding
- Break into multiple smaller corrections
- Consult implementation plan for context

See @CLAUDE.md for comprehensive troubleshooting.

---

### Related Files

- @.claude/commands/workflow-question-ask.md - Creates research issues
- @CLAUDE.md - Main workflow instructions
- @.claude/rules/004-beads-json-patterns.md - Beads JSON patterns
- @.claude/rules/003-multi-agent-coordination.md - Multi-agent coordination
