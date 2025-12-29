---
argument-hint:
description: Find and claim available work from Beads issue tracking system
---

## Intent

Find unblocked work, claim it, execute with a specialized agent, then stop for human approval.

## When to Use

- Ready to start working on next task
- Resuming after session break
- Manual task-by-task execution (vs automated `/workflow-execute`)

## When NOT to Use

- Want automated full-plan execution → use `/workflow-execute`
- Quick isolated task outside epics → use `/workflow-do`
- Completing session → use `/workflow-land`
- Checking status only → use `/workflow-check`

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-work
```

## Decision Framework

| State                   | Action                           | Outcome             |
| ----------------------- | -------------------------------- | ------------------- |
| Ready work available    | Show list, let user select       | Task claimed        |
| No ready work           | Check blocked/stale/open issues  | Diagnose cause      |
| Work in progress exists | Warn, offer to resume or reset   | Clean state         |
| Task selected           | Mark in_progress, dispatch agent | Execution begins    |
| Task complete           | Commit, close issue, STOP        | Human approves next |

## Branch-Epic Validation (BEFORE claiming work)

| Current Branch       | In-Progress Epic | Action                                |
| -------------------- | ---------------- | ------------------------------------- |
| `main`               | None             | Proceed normally                      |
| `main`               | Exists           | Warn, suggest creating feature branch |
| `feature/<epic-X>-*` | None             | Proceed (orphan branch OK)            |
| `feature/<epic-X>-*` | Same epic X      | Proceed (aligned)                     |
| `feature/<epic-X>-*` | Different epic Y | Error, require resolution             |

**Validate branch-epic consistency before claiming work.**

## Task Checkpoint (CRITICAL)

**ONE TASK PER INVOCATION**

After completing any task:

1. Commit changes (REQUIRED before closing)
2. Close the issue
3. **STOP** - Return control to human
4. Human runs `/workflow-work` again for next task OR `/workflow-land` to end session

**Do not chain automatically to the next task.**

## Execution Flow

| Step | Action                                   | Purpose                   |
| ---- | ---------------------------------------- | ------------------------- |
| 1    | Validate branch-epic alignment           | Prevent context conflicts |
| 2    | Find ready work (`bd ready --type task`) | Identify available tasks  |
| 3    | Present options with priority context    | User selects              |
| 4    | Claim task (`--status in_progress`)      | Prevent conflicts         |
| 5    | Read full description (`bd show`)        | Get complete context      |
| 6    | Dispatch to specialized agent            | Domain expertise          |
| 7    | Commit changes                           | Version control           |
| 8    | Close issue                              | Mark complete             |
| 9    | **STOP**                                 | Await human approval      |

## Agent Dispatch (CRITICAL)

**Dispatch to specialized agents.** Never implement code directly.

See @.claude/rules/agent-dispatch.md for agent selection.

## Success Criteria

- [ ] Branch-epic alignment validated
- [ ] Task selected from ready work
- [ ] Issue marked in_progress before work
- [ ] Agent dispatched (not implemented directly)
- [ ] Changes committed with issue ID
- [ ] Issue closed with completion reason
- [ ] Control returned to human

## Edge Considerations

- **No ready work**: Check `bd blocked`, `bd stale --days 7`, `bd list --status open`
- **Blocked by research**: Use `/workflow-steer-research` to resolve
- **AI diverged**: Use `/workflow-steer-correct` for course correction
- **Work already in progress**: Warn, offer resume or reset options
- **Orphaned issues**: Check with `bd orphans` for issues without parent
- **Branch mismatch**: On `feature/epic-X-*` but epic Y in progress → error, require resolution
- **Multiple epics**: If multiple in-progress epics, use first, warn about others
- **No feature branch**: On main with active epic → warn, suggest creating branch

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-work

# Branch-epic validation
BRANCH=$(git branch --show-current)

# Extract epic ID from branch name (if feature/fix branch)
# Pattern: feature/<epic-id>-<slug> or fix/<epic-id>-<slug>
if [[ "$BRANCH" =~ ^(feature|fix)/([a-z]+-[a-z0-9]+) ]]; then
  EPIC_FROM_BRANCH="${BASH_REMATCH[2]}"
fi

# Find in-progress epic
bd list --type epic --status in_progress --json | jq -r '.[0].id'

# Find matching feature branch for epic
git branch --list "feature/${EPIC_ID}-*" | head -1

# Find ready work (returns array)
bd ready --json
bd ready --type task --json
bd ready --parent $EPIC_ID --json  # Filter by epic (v0.37.0+)

# Format ready work
bd ready --json | jq -r '.[] | "[\(.id)] P\(.priority) \(.title)"'

# Check dependencies
bd dep tree [issue-id]

# Claim task
bd update [issue-id] --status in_progress --json

# Read full description
bd show [issue-id] --json | jq -r '.[0].description'

# Commit changes (see git-conventions.md)
git add .
git commit -m "type(scope): [issue-id] description"

# Close issue (--suggest-next shows newly unblocked issues)
bd close [issue-id] --reason "Completed: [summary]" --suggest-next --json

# Create follow-up issue
bd create "Discovered: [issue]" --deps discovered-from:[current-id] --json

# Troubleshooting: no ready work
bd blocked
bd blocked --parent $EPIC_ID  # Filter blocked by epic (v0.37.0+)
bd list --status open
bd stale --days 7
bd orphans
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - Beads CLI patterns
- @.claude/rules/agent-dispatch.md - Agent selection
- @.claude/rules/git-conventions.md - Commit format
- @.claude/commands/workflow-land.md - Session completion
