# Beads CLI JSON Patterns

<beads_json_critical>
## Critical: All Beads Commands Return Arrays

**Every** Beads CLI command with `--json` returns a JSON **array** `[{...}]`, not an object `{...}`.

This applies to ALL commands: `bd show`, `bd list`, `bd ready`, `bd update`, `bd create`, `bd close`, etc.

### Correct jq Patterns

| Scenario | Pattern | Example |
|----------|---------|---------|
| Single result | `.[0].field` | `bd show $ID --json \| jq -r '.[0].id'` |
| All results | `.[].field` | `bd list --json \| jq -r '.[].id'` |
| Count | `. \| length` | `bd ready --json \| jq '. \| length'` |
| Formatted list | `.[] \| "..."` | `bd ready --json \| jq -r '.[] \| "[\(.id)] \(.title)"'` |

### Common Errors

```bash
# WRONG - causes "Cannot index array with string" error
bd show $ID --json | jq -r '.id'
bd update $ID --json | jq -r '.status'

# RIGHT - use array indexing
bd show $ID --json | jq -r '.[0].id'
bd update $ID --json | jq -r '.[0].status'
```

### Why Arrays?

Beads uses arrays consistently because:
- `bd list` naturally returns multiple results
- `bd show` could theoretically match multiple (by pattern)
- Consistent API is easier to work with programmatically

Even when you expect exactly one result, always use `.[0]` to access it.
</beads_json_critical>

## Other Beads CLI Gotchas

### Sandbox Mode Required

Claude Code runs in a sandboxed environment. Always use `--sandbox` flag:
```bash
BD_FLAGS="--sandbox"
bd $BD_FLAGS list --json
```

### Hierarchical IDs

Use `--parent --force` to create child issues with dotted IDs:
```bash
bd create "Task" --parent $EPIC_ID --force -t task --json
# Creates: pydo-abc.1, pydo-abc.2, etc.
```

### Prefix Requirements

- Maximum 8 characters (including trailing hyphen)
- Lowercase letters, numbers, hyphens only
- Must start with letter, end with hyphen

See @CLAUDE.md for full prefix guidelines.
