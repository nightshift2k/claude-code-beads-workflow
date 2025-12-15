# Git Conventions

**Priority**: CRITICAL - All commits must follow these conventions.

---

## Conventional Commits with Beads Integration

**Format**: `type(scope): [issue-id] description`

### Types

| Type | Usage |
|------|-------|
| `feat` | New feature implementation |
| `fix` | Bug fix |
| `refactor` | Code change (no new feature/fix) |
| `docs` | Documentation only |
| `test` | Adding/correcting tests |
| `chore` | Build, tooling, deps |
| `style` | Formatting (no logic change) |
| `perf` | Performance improvement |
| `build` | Build system changes |
| `ci` | CI/CD configuration |

### Rules

1. **Include Beads issue ID** when working on tracked tasks
2. **Imperative mood**: "add" not "added"
3. **Subject**: <72 characters
4. **Lowercase** after `type(scope):`
5. **No period** at end

### Examples

```bash
# With Beads issue ID (preferred during workflow)
feat(storage): [pydo-nh9.4] implement SQLite backend
fix(cli): [pydo-nh9.5] resolve argument parsing error
test(models): [pydo-nh9.3] add Task model unit tests

# Without issue ID (for workflow sync, docs, etc.)
chore(workflow): sync Beads state
docs(readme): update installation instructions

# Wrong
Updated files                    # No type, no issue
fixed bug                        # Wrong tense, no scope
feat(auth): Add Auth.            # Capitalized, has period
feat: [pydo-nh9.1] setup         # Missing scope
```

---

## Commit Timing

<commit_timing_critical>
### Critical: Commit After Each Task

**Rule**: One task = One commit (minimum)

```
/workflow-work
├── Claim task (bd update --status in_progress)
├── Execute task (via agent dispatch)
├── Commit changes ← REQUIRED before closing
├── Close task (bd close --reason)
└── STOP - Return control to human
```

**Do NOT:**
- Batch multiple tasks into one commit
- Close tasks without committing
- Continue to next task without human approval
</commit_timing_critical>

---

## Branch Workflow

**Rule**: Feature branches for significant work. Quick fixes can go to main if isolated.

| Pattern | Usage | Example |
|---------|-------|---------|
| `feature/*` | New features | `feature/user-auth` |
| `fix/*` | Bug fixes | `fix/storage-error` |
| `refactor/*` | Refactoring | `refactor/cli-structure` |
| `docs/*` | Documentation | `docs/api-reference` |

### When to Use Branches

| Scenario | Branch? | Reason |
|----------|---------|--------|
| Multi-file feature | Yes | Isolate changes for review |
| Single task from epic | Optional | Depends on risk/complexity |
| Workflow fixes (this repo) | Yes | Template changes need review |
| Beads sync commits | No | Just state persistence |

---

## Pre-Commit Checklist

Before committing, ensure:

```bash
# Run project-specific checks (adapt to your stack)
# Python example:
uv run pytest           # Tests pass
uv run ruff check .     # Linting passes
uv run ruff format .    # Formatting applied

# Go example:
make test               # Tests pass
make lint               # Lint passes
make fmt                # Formatted

# General:
git status              # Review staged changes
git diff --staged       # Verify what's being committed
```

**Skip checks only for:**
- Workflow sync commits (Beads state only)
- Documentation-only changes
- Emergency fixes (document why in commit message)

---

## Workflow Integration

### During `/workflow-work`

```bash
# After agent completes task:
git add .
git commit -m "feat(module): [issue-id] implement feature X"
```

### During `/workflow-land`

```bash
# Sync commit (no issue ID needed):
git add .beads/issues.jsonl
git commit -m "chore(workflow): sync Beads state"
```

### Commit Message Templates

**Task completion:**
```
type(scope): [issue-id] short description

- Detail 1
- Detail 2

Closes: issue-id
```

**Workflow sync:**
```
chore(workflow): sync Beads state

- Closed: issue-id-1, issue-id-2
- Updated: issue-id-3
```

---

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/commands/workflow-work.md - Task execution workflow
- @.claude/commands/workflow-land.md - Session completion workflow
