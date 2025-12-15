---
argument-hint:
description: Review current project status across implementation and tracking
---

## `/workflow-check` - Review project status

Use this command when needing to understand current project state.

This command provides a comprehensive view of implementation status and tracking.

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
source @.claude/lib/workflow-precheck.sh
workflow_precheck "workflow-check"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

**⚠️ Beads JSON:** All `bd` commands return arrays. See @.claude/rules/004-beads-json-patterns.md for correct jq usage.

### Process

**1. Active Features**: Review Beads epics and their status
```bash
bd $BD_FLAGS list -t epic --json
```

**2. Open Issues**: Check open issues by status
```bash
bd $BD_FLAGS list --status open --json
```

**3. Ready Work**: Find unblocked work available
```bash
bd $BD_FLAGS ready --json
```

**4. Stale Issues**: Identify forgotten work
```bash
bd $BD_FLAGS stale --days 7 --json
```

**5. Blocked Issues**: Check for dependency blocks
```bash
bd $BD_FLAGS blocked --json
```

**6. Project Statistics**: Review overall progress
```bash
bd $BD_FLAGS stats --json
```

---

### Information Summary

- Active feature epics and their completion status
- Open Beads issues by priority and type
- Ready work available for immediate implementation
- Stale issues that may need attention
- Blocked issues that need dependency resolution
- Overall project statistics and progress

### Use This Command To

- Understand current project state before starting new work
- Identify work that needs attention
- Find appropriate work to focus on next
- Assess overall project health and progress
- Detect stale or blocked work items

### Troubleshooting

**If status retrieval fails:**
```bash
# Check Beads database health
bd info --json

# Verify database file exists
ls -la .beads/beads.db

# Try basic list command
bd list --limit 5 --json
```

See @CLAUDE.md for comprehensive troubleshooting solutions.

**Example usage:**
```
/workflow-check
# This will provide a comprehensive status report across implementation and tracking
```

**What you'll see:**
- List of active feature epics
- Count of open issues by priority
- List of ready work (unblocked issues)
- Any stale issues that may need attention
- Overall project statistics
