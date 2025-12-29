---
argument-hint: "[epic-id] [--mode] [--output <file>]"
description: View plan state in different modes (summary, log, full, current, all)
---

## Intent

Display an epic's implementation plan state at configurable detail levels.

## When to Use

- Check progress on a feature epic
- Review steering history (what changed and why)
- Export plan state for sharing or documentation
- Compare current task status against original plan

## When NOT to Use

- Quick project-wide status → use `/workflow-check`
- Diagnosing workflow issues → use `/workflow-health`
- Finding available work → use `/workflow-work`

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-overview
```

## View Modes

| Mode    | Flag        | Shows                           | Use When                |
| ------- | ----------- | ------------------------------- | ----------------------- |
| Summary | (default)   | Progress bar, counts, next task | Quick status check      |
| Log     | `--log`     | Steering log entries            | See what changed        |
| Full    | `--full`    | Original plan + current status  | Compare plan vs reality |
| Current | `--current` | Task descriptions from Beads    | See current state       |
| All     | `--all`     | Complete markdown export        | Sharing, documentation  |

## Output Flag

| Flag              | Behavior               |
| ----------------- | ---------------------- |
| (none)            | Display content inline |
| `--output <file>` | Write content to file  |

The `--output` flag works with any mode. Use it to export plan state for sharing, archiving, or documentation.

## Decision Framework

| Argument              | Action                           | Output                     |
| --------------------- | -------------------------------- | -------------------------- |
| `[epic-id]` only      | Show summary mode                | Progress bar, counts       |
| `[epic-id] --log`     | Extract steering log             | Chronological changes      |
| `[epic-id] --full`    | Overlay status on original       | Plan with completion marks |
| `[epic-id] --current` | Pull from Beads issues           | Current task descriptions  |
| `[epic-id] --all`     | Combine all sections             | Full markdown document     |
| `--output <file>`     | Write to file instead of display | File created at path       |
| No epic-id            | Error with usage                 | Prompt for epic ID         |

## Execution

1. Parse epic ID and optional mode flag
2. Fetch epic details with `bd show`
3. Parse epic description into sections (summary, log, plan)
4. Fetch child issue status with `bd list` filtered by epic ID prefix
5. Calculate progress metrics
6. Display based on selected mode

## Success Criteria

- [ ] Epic ID exists and validates
- [ ] Content matches selected mode (displayed or written to file)
- [ ] Progress calculation accurate
- [ ] Child issues filtered correctly by epic prefix
- [ ] File created when `--output` specified

## Output Formats

**Summary (default):**

```
epic-id: Epic Title
────────────────────────────────────────
Progress: ████████░░░░░░░░ 50% (4/8)
Blocked:  2 tasks
Last:     STEER - Description (HH:MM)
Next:     task-id (Task Title)
```

**Log (--log):**

```
## Steering Log for epic-id

### [timestamp] STEER: Description
**Trigger:** Research issue-id
**Decision:** Change made
**Modified:** issue-id.N
```

## Edge Considerations

- **Epic not found**: Error with suggestion to check `bd list --type epic`
- **No steering log**: Display "No steering events recorded"
- **Empty tasks**: Display "No tasks tracked yet - run /workflow-track"
- **Child ID filtering**: Use `jq --arg` for proper shell variable expansion

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-overview

# Get epic details (returns array)
bd show $EPIC_ID --json | jq '.[0]'

# Filter child issues by epic prefix
bd list --json | jq --arg prefix "$EPIC_ID." '[.[] | select(.id | startswith($prefix))]'

# Count by status
bd list --json | jq --arg prefix "$EPIC_ID." '[.[] | select(.id | startswith($prefix)) | select(.status == "closed")] | length'

# Progress calculation
COMPLETED=$(bd list --json | jq --arg prefix "$EPIC_ID." '[.[] | select(.id | startswith($prefix)) | select(.status == "closed")] | length')
TOTAL=$(bd list --json | jq --arg prefix "$EPIC_ID." '[.[] | select(.id | startswith($prefix))] | length')
```

## Usage Examples

```bash
# Quick status check
/workflow-overview pydo-abc

# See steering history
/workflow-overview pydo-abc --log

# Full plan with status overlay
/workflow-overview pydo-abc --full

# Current task descriptions
/workflow-overview pydo-abc --current

# Export for sharing (shell redirect)
/workflow-overview pydo-abc --all > plan-export.md

# Export for sharing (--output flag)
/workflow-overview pydo-abc --all --output docs/plans/pydo-status.md

# Export steering log to file
/workflow-overview pydo-abc --log --output docs/plans/steering-history.md
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - Beads CLI patterns
- @.claude/commands/workflow-track.md - Plan tracking
- @.claude/commands/workflow-steer-research.md - Research steering
