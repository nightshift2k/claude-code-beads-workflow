# Beads CLI Reference

> **Load on demand.** This reference supplements the critical gotchas in `.claude/rules/beads-patterns.md`.

## Version Requirements

- **Minimum:** v0.37.0 (has `--parent` flags)
- **Recommended:** v0.39.1+ (all features)

Check: `bd version`

---

## Filtering Commands

```bash
# By type
bd ready --type task --json
bd list --type epic --json

# By parent (v0.37.0+)
bd ready --parent $EPIC_ID --json
bd blocked --parent $EPIC_ID --json

# By status
bd list --status open --json
```

## Close with Suggestions (v0.37.0+)

```bash
bd close [id] --reason "Done" --suggest-next --json
```

## Estimates

```bash
bd create "Task" --estimate "2h" --json
bd update [id] --estimate "4h" --json
```

## Dependency Visualization

```bash
bd graph [issue-id] --no-daemon   # Graph (requires --no-daemon)
bd dep tree [issue-id]            # Tree view
bd dep cycles                      # Detect cycles
```

## Diagnostic Commands

```bash
bd doctor --fix   # Auto-repair (v0.38.0+)
bd where          # Database location (v0.39.1+)
bd orphans        # Orphaned issues (v0.39.0+)
bd reset          # Full database reset
bd import --force # Rebuild from JSONL
```

## Live Monitoring (v0.36.0+)

```bash
bd list --pretty --watch   # Auto-refresh tree view
```

## Searching (v0.36.0+)

```bash
bd search "keyword" --type task --json
bd search "bug" --priority-min 0 --priority-max 1 --json
bd search "refactor" --created-after 2025-01-01 --json
```

Filters: `--type`, `--status`, `--priority-min/max`, `--created-after/before`, `--assignee`, `--label`, `--sort`

## Reparenting (v0.39.1+)

```bash
bd update [id] --parent [new-parent-id] --json
```

## Status Management

```bash
bd update [id] --status deferred --json   # Move to icebox
```

---

## bd blocked Structure

```json
[{"id": "abc.2", "blocked_by": ["abc.1"], ...}]
```

```bash
bd blocked --json | jq -r '.[0].blocked_by[]'
```

---

## Sandbox Mode

Auto-detected since v0.21.1. No configuration needed.
