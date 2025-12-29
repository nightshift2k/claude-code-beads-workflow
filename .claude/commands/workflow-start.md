---
argument-hint: "[feature-description]"
description: Begin a new feature with Beads epic creation
---

## Intent

Create a Beads epic as the parent container for a new feature.

## When to Use

- Starting a new feature
- Beginning work spanning multiple tasks
- Creating a tracking container for planned work

## When NOT to Use

- Quick isolated task → use `/workflow-do`
- Adding to existing feature → use existing epic ID with `/workflow-track`
- Just checking status → use `/workflow-check`

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-start
```

## Decision Framework

| State                        | Action                             | Outcome                    |
| ---------------------------- | ---------------------------------- | -------------------------- |
| Feature description provided | Create epic                        | Epic ID returned           |
| No description               | Prompt user for description        | Clear scope                |
| Related epic exists          | Ask: extend existing or create new | Prevent duplicates         |
| Epic just created            | Create feature branch              | `feature/<epic-id>-<slug>` |
| Branch already exists        | Warn, offer switch                 | Use existing branch        |

## Execution

1. Validate feature description provided
2. Create epic with `bd create` (type: epic, priority: 1)
3. Extract and prominently display epic ID
4. Generate branch slug from title (lowercase, hyphenated, max 30 chars)
5. Create and checkout feature branch: `feature/<epic-id>-<slug>`
6. Instruct user to save ID for `/workflow-track`

## Success Criteria

- [ ] Epic created with valid ID (format: `prefix-xxx`)
- [ ] Epic ID clearly displayed to user
- [ ] Feature branch created and checked out
- [ ] Branch name embeds epic ID (extractable via regex)
- [ ] User instructed to save ID for tracking phase

## Epic ID Output (CRITICAL)

The epic ID (e.g., `pydo-abc`) enables hierarchical child issues.

| Without Epic ID                                | With Epic ID                                 |
| ---------------------------------------------- | -------------------------------------------- |
| Random independent IDs: `pydo-xyz`, `pydo-def` | Hierarchical IDs: `pydo-abc.1`, `pydo-abc.2` |
| No visible relationship                        | Clear parent-child structure                 |

**Always display prominently:**

```
==========================================
EPIC CREATED: [epic-id]
==========================================

IMPORTANT: Save this epic ID for /workflow-track
```

## Edge Considerations

- **bd create returns object**: Use `.id` not `.[0].id` (see beads-patterns.md)
- **Brainstorming gate**: For features touching >3 files, recommend brainstorming first
- **Existing branch**: If branch already exists, prompt for suffix or offer to switch
- **Special characters**: Sanitize title to `[a-z0-9-]` only for slug
- **Long titles**: Truncate slug at 30 characters

## Brainstorming Gate

For complex features, brainstorm before coding:

| Complexity    | Recommendation                     |
| ------------- | ---------------------------------- |
| ≤3 files      | Proceed directly                   |
| >3 files      | Use `superpowers:brainstorm` first |
| Unclear scope | Brainstorm to clarify requirements |

## Next Steps After Epic Creation

1. Save the epic ID (e.g., `pydo-abc`)
2. Create implementation plan (using writing-plans skill)
3. Track plan: `/workflow-track [plan-path]`
4. Execute: `/workflow-execute` or `/workflow-work`

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-start

# Create epic (returns OBJECT, not array)
bd create "Feature description" --description="Feature epic: description" -t epic -p 1 --json
# Output: {"id": "pydo-abc", ...}
# Extract: jq -r '.id'

# Generate slug from title (lowercase, hyphenated, max 30 chars)
TITLE="User Authentication Flow"
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g' | cut -c1-30)
# Result: user-authentication-flow

# Create feature branch with embedded epic ID
EPIC_ID="pydo-abc"
BRANCH="feature/${EPIC_ID}-${SLUG}"
git checkout -b "$BRANCH"
# Result: feature/pydo-abc-user-authentication-flow

# Extract epic ID from branch name (regex pattern)
# Pattern: feature/([a-z]+-[a-z0-9]+)-

# Child issues use --parent --force for hierarchical IDs
bd create "Task 1" --parent pydo-abc --force -t task -p 2 --json
# Output: {"id": "pydo-abc.1", ...}

# Fix long prefix
bd rename-prefix short- --dry-run
bd rename-prefix short-
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - bd create returns object
- @.claude/rules/project-principles.md - Brainstorming gate
- @.claude/commands/workflow-track.md - Track implementation plan
- @.claude/commands/workflow-work.md - Find available work
