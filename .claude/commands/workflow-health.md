---
argument-hint:
description: Diagnostic command to check workflow health and identify issues
---

## `/workflow-health` - Workflow Health Diagnostics

Use this command to diagnose workflow issues and verify system health.

This command performs comprehensive checks on all workflow components.

### Process

Run the Python workflow tool:

```bash
uv run python .claude/lib/workflow.py health
```

This performs comprehensive checks on:
1. Environment (bd CLI, git, jq)
2. Beads tracking (.beads directory, database, JSONL)
3. Issue status (open, in_progress, closed, ready, blocked, stale)
4. Git status (repository, branch, working tree)

---

### When to Use

- Diagnosing workflow command failures
- After environment changes
- Before starting a complex workflow
- Troubleshooting "weird" behavior

### Output Levels

| Level | Meaning |
|-------|---------|
| HEALTHY | All systems operational |
| DEGRADED | Non-critical issues present |
| CRITICAL | Workflow cannot function |

### Follow-Up Actions

| Issue | Action |
|-------|--------|
| bd CLI missing | Install Beads CLI |
| .beads not initialized | Run `/workflow-init` |
| Database corrupted | See recovery procedures in @CLAUDE.md |
| Stale issues | Review with `bd stale` |
| Blocked issues | Review dependencies with `bd blocked` |

**Example usage:**
```
/workflow-health
# Outputs comprehensive health report
```
