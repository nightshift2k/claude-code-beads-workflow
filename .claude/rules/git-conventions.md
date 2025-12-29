# Git Conventions

**Priority**: CRITICAL - All commits must follow these conventions.

---

## Conventional Commits with Beads Integration

**Format**: `type(scope): [issue-id] description`

### Types

| Type       | Usage                            |
| ---------- | -------------------------------- |
| `feat`     | New feature implementation       |
| `fix`      | Bug fix                          |
| `refactor` | Code change (no new feature/fix) |
| `docs`     | Documentation only               |
| `test`     | Adding/correcting tests          |
| `chore`    | Build, tooling, deps             |
| `style`    | Formatting (no logic change)     |
| `perf`     | Performance improvement          |
| `build`    | Build system changes             |
| `ci`       | CI/CD configuration              |

### Rules

1. **Include Beads issue ID** when working on tracked tasks
2. **Imperative mood**: "add" not "added"
3. **Subject**: <72 characters
4. **Lowercase** after `type(scope):`
5. **No period** at end

### Examples

```text
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

**Avoid:**

- Batching multiple tasks into one commit
- Closing tasks without committing
- Continuing to next task without human approval
  </commit_timing_critical>

---

## Branch Workflow

**Rule**: Use feature branches for significant work. Isolated quick fixes may go to main.

| Pattern      | Usage         | Example                  |
| ------------ | ------------- | ------------------------ |
| `feature/*`  | New features  | `feature/user-auth`      |
| `fix/*`      | Bug fixes     | `fix/storage-error`      |
| `refactor/*` | Refactoring   | `refactor/cli-structure` |
| `docs/*`     | Documentation | `docs/api-reference`     |

### When to Use Branches

| Scenario                   | Branch?  | Reason                       |
| -------------------------- | -------- | ---------------------------- |
| Multi-file feature         | Yes      | Isolate changes for review   |
| Single task from epic      | Optional | Depends on risk/complexity   |
| Workflow fixes (this repo) | Yes      | Template changes need review |
| Beads sync commits         | No       | Just state persistence       |

**Note:** Define merge strategy (squash, merge, or rebase) per-project in CLAUDE.md based on team preferences.

---

## Pre-Commit Checklist

| Change Type        | Required Checks                   | Skip Allowed? |
| ------------------ | --------------------------------- | ------------- |
| Code changes       | Tests + linting                   | No            |
| Workflow sync only | None                              | Yes           |
| Documentation only | Markdown lint (if available)      | Yes           |
| Emergency fix      | Document reason in commit message | Yes           |

### Stack-Specific Commands

| Stack   | Test Command    | Lint Command          | Format Command         |
| ------- | --------------- | --------------------- | ---------------------- |
| Python  | `uv run pytest` | `uv run ruff check .` | `uv run ruff format .` |
| Go      | `make test`     | `make lint`           | `make fmt`             |
| General | `git status`    | `git diff --staged`   | -                      |

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
