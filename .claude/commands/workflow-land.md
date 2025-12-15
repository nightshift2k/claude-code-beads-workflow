---
argument-hint:
description: Complete a work session properly with local synchronization
---

## `/workflow-land` - Complete a work session properly

Use this command when finishing a work session (REQUIRED before stopping).

This command ensures proper session completion with all work tracked and locally consistent.

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
source .claude/lib/workflow-precheck.sh
workflow_precheck "workflow-land"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

### Setup Interruption Handler

Set up cleanup trap to handle unexpected interruptions:
```bash
trap 'workflow_cleanup "workflow-land"' EXIT INT TERM
```

---

**⚠️ Beads JSON:** All `bd` commands return arrays. See [Beads JSON Patterns](../.claude/rules/004-beads-json-patterns.md) for correct jq usage.

### Process (MANDATORY - COMPLETE ALL STEPS)

**1. File remaining work**: Create Beads issues for any follow-up tasks discovered
```bash
bd $BD_FLAGS create "Follow-up task" --description="[context]" -t task -p [priority] --deps discovered-from:[current-id] --json
```

**2. Update issue status**: Close completed issues, update in-progress issues with status/notes
```bash
bd $BD_FLAGS close [completed-ids] --reason "Completed [specific reason]" --json
bd $BD_FLAGS update [in-progress-id] --status in_progress --note "[progress update]" --json
```

**3. Run quality gates**: Only if code changes were made, run appropriate tests/linters
   - Use project-specific test commands (technology agnostic)
   - Ensure all quality gates pass before proceeding

**4. Persist changes**: In sandbox mode, run `bd sync --flush-only` to export changes to JSONL. In normal mode, changes auto-persist.
```bash
# Sandbox mode (default for Claude Code)
bd $BD_FLAGS sync --flush-only
```

**5. Commit locally if needed**: Optionally commit changes to local git for history
```bash
git add . && git commit -m "Workflow sync: [description of work completed]"
```

**6. Choose next work item**: Use `bd ready` to identify next available work
```bash
bd $BD_FLAGS ready --json
```

---

### Critical Points

- The session is NOT completed until changes are persisted to JSONL
- In sandbox mode, use `bd sync --flush-only` to export changes
- In normal mode, changes auto-persist after each operation
- Local git commits are optional for maintaining history
- If interrupted, cleanup trap will save state and attempt sync

### Troubleshooting

If you encounter errors, see [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting) for common solutions.

**Example usage:**
```
/workflow-land
# This will guide you through all required steps for proper session completion
```

This ensures that all work is properly tracked and locally consistent.
