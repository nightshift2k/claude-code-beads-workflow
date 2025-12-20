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
uv run python _claude/lib/workflow.py precheck --name workflow-land
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

**⚠️ Beads JSON:** All `bd` commands return arrays. See @.claude/rules/004-beads-json-patterns.md for correct jq usage.

### Process (MANDATORY - COMPLETE ALL STEPS)

**1. File remaining work**: Create Beads issues for any follow-up tasks discovered
```bash
bd  create "Follow-up task" --description="[context]" -t task -p [priority] --deps discovered-from:[current-id] --json
```

**2. Review current status**: Check what needs closing/updating (use `&&` to chain commands)
```bash
echo "=== Closed ===" && bd  list --status closed --json | jq -r '.[] | "[\(.id)] \(.title)"' && echo "" && echo "=== In-Progress ===" && bd  list --status in_progress --json | jq -r '.[] | "[\(.id)] \(.title)"' && echo "" && echo "=== Open ===" && bd  list --status open --json | jq -r '.[] | "[\(.id)] \(.title)"'
```

**3. Update issue status**: Close completed issues, update in-progress issues with notes
```bash
# Close completed work (run separately for each issue)
bd  close [issue-id] --reason "Completed: [specific reason]" --json

# Update in-progress issues with status notes
bd  update [issue-id] --notes "[progress update]" --json
```

**Note:** Run each `bd close` and `bd update` as separate commands. Do NOT combine with newlines.

**4. Run quality gates**: Only if code changes were made, run appropriate tests/linters
   - Use project-specific test commands (technology agnostic)
   - Ensure all quality gates pass before proceeding

**5. Persist changes**: In sandbox mode, run `bd sync --flush-only` to export changes to JSONL. In normal mode, changes auto-persist.
```bash
# Sandbox mode (default for Claude Code)
bd  sync --flush-only
```

**6. Commit locally**: Commit Beads state and any uncommitted work
```bash
# Workflow sync commit (Beads state)
git add .beads/issues.jsonl && git commit -m "chore(workflow): sync Beads state"

# Or if code changes exist, include them with proper message format
git add . && git commit -m "chore(workflow): sync session - [summary]"
```

See @.claude/rules/006-git-conventions.md for commit message format.

**7. Choose next work item**: Use `uv run python _claude/lib/workflow.py ready` to identify next available work
```bash
bd  ready --json | jq -r '.[] | "[\(.id)] P\(.priority) \(.title)"'
```

---

### Critical Points

- The session is NOT completed until changes are persisted to JSONL
- In sandbox mode, use `bd sync --flush-only` to export changes
- In normal mode, changes auto-persist after each operation
- **Commit Beads state** to preserve tracking across sessions
- If interrupted, cleanup trap will save state and attempt sync

### Troubleshooting

**If sync fails in sandbox mode:**
```bash
# Check if .beads directory exists
ls -la .beads/

# Verify JSONL file is writable
test -w .beads/issues.jsonl && echo "Writable" || echo "Not writable"

# Manual export if needed
bd  export > .beads/issues.jsonl.backup
```

See @CLAUDE.md for comprehensive troubleshooting solutions.

**Example usage:**
```
/workflow-land
# This will guide you through all required steps for proper session completion
```

This ensures that all work is properly tracked and locally consistent.