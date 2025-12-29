---
argument-hint:
description: Diagnostic command to check workflow health and identify issues
---

## Intent

Diagnose workflow issues and verify all system components operate correctly.

**READ-ONLY**: Reports status without modifying state.

## When to Use

- Diagnose workflow command failures
- After environment changes
- Before starting complex workflows
- Troubleshoot unexpected behavior

## Health Check Categories

| Category    | Checks                                          |
| ----------- | ----------------------------------------------- |
| Environment | bd CLI, git, jq availability                    |
| Beads       | .beads directory, database, JSONL integrity     |
| Issues      | open, in_progress, ready, blocked, stale counts |
| Git         | repository status, branch, working tree         |
| Flags       | team-mode, strict-quality status                |

## Decision Framework

| Health Level | Meaning                     | Action                         |
| ------------ | --------------------------- | ------------------------------ |
| HEALTHY      | All systems operational     | Proceed with work              |
| DEGRADED     | Non-critical issues present | Review warnings, may proceed   |
| CRITICAL     | Workflow cannot function    | Must resolve before proceeding |

## Execution

Run comprehensive health check:

```bash
uv run python .claude/lib/workflow.py health
```

## Prohibited Actions

This command is diagnostic only. It MUST NOT modify state:

| Prohibited                       | Why                                                              |
| -------------------------------- | ---------------------------------------------------------------- |
| `bd update --status in_progress` | Claims work (use `/workflow-work` instead)                       |
| `bd close`                       | Closes issues (use `/workflow-land` instead)                     |
| `bd create`                      | Creates issues (use `/workflow-start` or `/workflow-do` instead) |
| Implementation work              | Health check, not execution                                      |
| File modifications               | Read-only diagnostics                                            |

**If issues require action:** Report them with remediation steps; let the user decide when to act.

## Success Criteria

- All categories checked
- Issues identified with clear remediation
- Overall health level reported
- **No Beads issues modified**
- **No files written**

## Remediation Guide

| Issue                     | Resolution                                                                  |
| ------------------------- | --------------------------------------------------------------------------- |
| bd CLI missing            | Install Beads CLI                                                           |
| .beads not initialized    | Run `/workflow-init`                                                        |
| Database corrupted        | `bd doctor --fix` (auto-repair) or `bd reset` (full rebuild)                |
| Stale issues              | Review with `bd stale`                                                      |
| Blocked issues            | Check dependencies with `bd blocked`                                        |
| Circular dependencies     | Visualize with `bd graph [issue-id]`, detect with `bd dep cycles`           |
| Orphaned issues           | Find with `bd orphans`, reparent with `bd update [id] --parent [parent-id]` |
| Unknown database location | Run `bd where` to show active database path                                 |

## Edge Considerations

- Unknown flags trigger warning
- Database/JSONL mismatch indicates sync issues
- Multiple in_progress issues suggest interrupted sessions

## Reference Commands

```bash
# Manual health check
uv run python .claude/lib/workflow.py health

# Check Beads database integrity
sqlite3 .beads/*.db "PRAGMA integrity_check;"

# Auto-repair database issues (v0.38.0+)
bd doctor --fix

# Show database location (v0.39.1+)
bd where

# View stale issues
bd stale --days 7

# Find orphaned issues (v0.39.0+)
bd orphans

# Visualize dependencies (requires issue-id)
bd graph [issue-id]

# Detect circular dependencies
bd dep cycles
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - Beads CLI patterns
- @.claude/commands/workflow-init.md - Project initialization
- @.claude/commands/workflow-check.md - Status review
