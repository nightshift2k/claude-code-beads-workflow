---
argument-hint: "[task description]"
description: Execute isolated task without epic overhead
---

## Intent

Execute a quick, self-contained task (bug fix, small change) with tracking but without epic creation or full planning.

## When to Use

- Bug fix too small for an epic
- Small, isolated change (<2 hours)
- Quick task unrelated to active feature work
- Ad-hoc request requiring tracking

## When NOT to Use

- Task touches 3+ files → use /workflow-start for proper planning
- Task relates to active epic → use /workflow-steer-correct
- Complex change requiring design → use brainstorming + /workflow-start

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-do
```

Query current state:

- `bd list --status in_progress` - any active work?
- `bd list --type epic --status open` - any active epics?
- `git status` - uncommitted changes?

## Decision Framework

| Situation                   | Action                                   | Expected Outcome     |
| --------------------------- | ---------------------------------------- | -------------------- |
| No active work, clean state | Create task, execute, close              | Direct completion    |
| Task in progress (non-epic) | Offer: pause/abort current, or abort new | Clean context switch |
| Epic in progress            | Analyze overlap (see below)              | Proper routing       |
| Uncommitted changes         | Warn, offer stash                        | No lost work         |

## Epic Overlap Analysis

If active epic exists, analyze semantically:

1. Read epic description and child task descriptions
2. Determine if new work relates to epic scope
3. If related → route to /workflow-steer-correct (this is a steering job)
4. If unrelated → proceed with /workflow-do (truly isolated work)

_Use semantic understanding, not keyword matching._

## Execution

1. Gather context (queries above)
2. Apply decision framework
3. If proceeding:
   - Create Beads task with description
   - Mark in_progress
   - Dispatch to appropriate agent based on task domain
   - On completion: close with outcome
   - Commit changes with task ID

## Success Criteria

- Beads tracks task from start to finish
- No orphaned in-progress tasks remain
- Context switches complete cleanly
- Commit references task ID

## Edge Considerations

- **Complexity creep:** Convert to epic if task grows beyond estimate
- **Discovery work:** Create follow-up tasks for new issues found during execution
- **Agent selection:** Route to domain-appropriate agent (python-expert, golang-expert, etc.)

## Reference Commands

```bash
# Create task
bd create "[description]" -t task -p 2 --json

# Mark in progress
bd update [id] --status in_progress --json

# Close with reason
bd close [id] --reason "[outcome]" --json
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - Beads CLI patterns
- @.claude/rules/agent-dispatch.md - Agent selection guidance
- @.claude/commands/workflow-work.md - Full task workflow
- @.claude/commands/workflow-land.md - Session completion
