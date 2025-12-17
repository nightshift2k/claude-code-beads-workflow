# Beads CLI JSON Patterns

<beads_json_critical>
## Critical: Know Which Commands Return Arrays vs Objects

Beads CLI commands with `--json` return **different formats** depending on the command:

| Command | Returns | jq Pattern |
|---------|---------|------------|
| `bd create` | **object** `{...}` | `.id` |
| `bd show` | **array** `[{...}]` | `.[0].id` |
| `bd list` | **array** `[{...}]` | `.[].id` |
| `bd ready` | **array** `[{...}]` | `.[].id` |
| `bd update` | **array** `[{...}]` | `.[0].id` |
| `bd close` | **array** `[{...}]` | `.[0].id` |

### Correct jq Patterns

| Scenario | Pattern | Example |
|----------|---------|---------|
| After create | `.field` | `bd create "Task" --json \| jq -r '.id'` |
| Single result | `.[0].field` | `bd show $ID --json \| jq -r '.[0].id'` |
| All results | `.[].field` | `bd list --json \| jq -r '.[].id'` |
| Count | `. \| length` | `bd ready --json \| jq '. \| length'` |
| Formatted list | `.[] \| "..."` | `bd ready --json \| jq -r '.[] \| "[\(.id)] \(.title)"'` |

### Common Errors

```bash
# WRONG for bd create - causes "Cannot index object with number"
bd create "Task" --json | jq -r '.[0].id'

# RIGHT for bd create - it returns an object
bd create "Task" --json | jq -r '.id'

# WRONG for bd show - causes "Cannot index array with string"
bd show $ID --json | jq -r '.id'

# RIGHT for bd show - it returns an array
bd show $ID --json | jq -r '.[0].id'
```

### Why Different Formats?

- `bd create` returns the single created issue as an **object**
- `bd list/show/ready` return potentially multiple results as an **array**
- `bd update/close` return affected issues as an **array** (could be multiple)
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

### Flag Spelling: `--notes` not `--note`

The flag is **plural**:
```bash
# WRONG - unknown flag error
bd update $ID --note "Progress update" --json

# RIGHT - plural form
bd update $ID --notes "Progress update" --json
```

### Prefix Requirements

- Maximum 8 characters (including trailing hyphen)
- Lowercase letters, numbers, hyphens only
- Must start with letter, end with hyphen

See @CLAUDE.md for full prefix guidelines.

---

## Related Files

- @CLAUDE.md - Main workflow instructions and troubleshooting
- @.claude/commands/workflow-track.md - Hierarchical ID usage examples
- @.claude/commands/workflow-init.md - Prefix initialization
