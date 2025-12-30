# Beads CLI Critical Gotchas

> **⚠️ CRITICAL:** `bd create` returns object `{...}`. ALL other commands return arrays `[{...}]`.
> Use `.id` for create, `.[0].id` for everything else.

For full command reference, see @docs/beads-reference.md

---

<beads_json_critical>

## Array vs Object Returns

| Command                      | Returns    | jq Pattern            |
| ---------------------------- | ---------- | --------------------- |
| `bd create`                  | **object** | `.id`                 |
| `bd show/list/ready/blocked` | **array**  | `.[0].id` or `.[].id` |
| `bd update/close`            | **array**  | `.[0].id`             |

```bash
# WRONG - "Cannot index object with number"
bd create "Task" --json | jq -r '.[0].id'

# RIGHT
bd create "Task" --json | jq -r '.id'
bd show $ID --json | jq -r '.[0].id'
```

</beads_json_critical>

---

## Stderr Breaks jq (CRITICAL)

Beads outputs JSON to **stdout**, warnings to **stderr**. Never combine:

```bash
# WRONG - breaks if warning emitted
bd create "Task" --json 2>&1 | jq

# RIGHT - include description to suppress warnings
bd create "Task" --description "Brief" --json | jq -r '.id'
```

---

## Retry After jq Failure (CRITICAL)

| Error Type          | Command Succeeded? | Action                   |
| ------------------- | ------------------ | ------------------------ |
| `bd` exits non-zero | No                 | Retry with fix           |
| jq parse error      | **Yes**            | Search for created issue |

**If jq fails, the issue likely already exists.** Check before retrying:

```bash
bd list --json | jq -r '.[-1]'  # Most recent issue
```

---

<body_file_critical>

## Use --body-file for Code Blocks (MANDATORY)

> **⚠️ CRITICAL:** `--description` with heredoc **SILENTLY LOSES DATA** when content contains backticks.

| Method                 | Simple Text | Code Blocks   |
| ---------------------- | ----------- | ------------- |
| `--description="$VAR"` | ✅          | ❌ (0 bytes!) |
| `--body-file`          | ✅          | ✅            |

````bash
# Write to temp file first
cat > /tmp/task.md <<'EOF'
**Code:**
```python
def example():
    return True
````

EOF

# Create with --body-file (ONLY safe method)

bd create "Task" --body-file /tmp/task.md --json

````

</body_file_critical>

---

## Quick Reference

| Gotcha | Fix |
|--------|-----|
| Hierarchical IDs | `bd create "Task" --parent $EPIC_ID --force` |
| Flag spelling | `--notes` (plural), not `--note` |
| Prefix format | Lowercase, start with letter, end with hyphen |

---

<self_contained_descriptions_critical>

## Self-Contained Descriptions (CRITICAL)

Issue descriptions must be **fully self-contained**. Agents receive ONLY the issue content via `bd show`.

**NEVER use:** "see above", "see implementation plan", "as described earlier"

**ALWAYS include:** file paths, code examples, commands, expected outcomes.

```markdown
# WRONG
Implement user login. See implementation plan for details.

# RIGHT
**Files:** Create `auth.py`
**Test:** `def test_login(): assert login("user", "pass")`
**Implement:** Login function with password validation
````

</self_contained_descriptions_critical>

---

## Related Files

- @docs/beads-reference.md - Full command reference
- @CLAUDE.md - Workflow instructions
