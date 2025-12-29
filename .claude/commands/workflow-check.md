---
argument-hint:
description: Review current project status across implementation and tracking
---

## Intent

Show project state: epics, issues, and work availability.

## When to Use

- Before starting new work
- Identifying work needing attention
- Assessing project health and progress
- Finding the next work item

## When NOT to Use

- For diagnostic issues → use `/workflow-health`
- To claim work → use `/workflow-work`
- To view specific plan → use `/workflow-overview [epic-id]`

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-check
```

## Decision Framework

| Query            | What It Shows                 | When Useful              |
| ---------------- | ----------------------------- | ------------------------ |
| Active epics     | Feature containers and status | Understanding scope      |
| Open issues      | All work not yet closed       | Full backlog view        |
| Ready work       | Unblocked, claimable issues   | Finding next task        |
| Stale issues     | Untouched 7+ days             | Detecting forgotten work |
| Blocked issues   | Waiting on dependencies       | Identifying bottlenecks  |
| Dependency graph | Visual DAG of relationships   | Understanding flow       |
| Pinned issues    | Persistent reference items    | Excluded from ready      |

## Execution

1. Run precheck to validate environment
2. Query each category relevant to need
3. Summarize findings with counts and highlights
4. Recommend next actions based on state

## Success Criteria

- [ ] Environment validated
- [ ] Active epics listed with status
- [ ] Open/ready/stale/blocked counts reported
- [ ] Actionable recommendations provided

## Edge Considerations

- **Precheck failure**: Follow guidance before continuing.
- **Empty results**: May indicate healthy state (no stale/blocked).
- **Many stale issues**: Session may have been interrupted.

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-check

# Active epics
bd list --type epic --json

# Open issues
bd list --status open --json

# Ready work
bd ready --json

# Stale issues (7+ days)
bd stale --days 7 --json

# Blocked issues
bd blocked --json

# Dependency visualization (requires issue-id)
bd graph [issue-id]         # Dependency graph for specific issue
bd dep tree [issue-id]      # Dependency tree for specific issue

# Orphaned issues (no parent)
bd orphans

# Epic progress via child status (native filter)
bd list --parent $EPIC_ID --status closed --json | jq '. | length'  # Completed
bd list --parent $EPIC_ID --status open --json | jq '. | length'    # Remaining
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - Beads CLI patterns
- @.claude/commands/workflow-work.md - Find available work
- @.claude/commands/workflow-health.md - System diagnostics
