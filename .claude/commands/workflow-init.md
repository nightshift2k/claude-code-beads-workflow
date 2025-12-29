---
argument-hint:
description: Initialize project for agentic workflow with Beads tracking
---

## Intent

Initialize a project for agentic development with Beads tracking.

## When to Use

- Setting up a new project
- After cloning this template
- When workflow commands fail with environment errors
- To verify configuration

## When NOT to Use

- Project already initialized → use `/workflow-health` to verify
- Just checking status → use `/workflow-check`
- Starting feature work → use `/workflow-start`

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-init
```

## Decision Framework

| State                  | Action                             | Outcome             |
| ---------------------- | ---------------------------------- | ------------------- |
| No `.beads/` directory | Initialize with short prefix       | Tracking enabled    |
| `.beads/` exists       | Skip initialization, verify prefix | Use existing        |
| Missing directories    | Create required structure          | Ready for workflow  |
| bd CLI missing         | Provide installation instructions  | User installs first |

## Prefix Requirements

| Rule       | Requirement                       | Examples             |
| ---------- | --------------------------------- | -------------------- |
| Ending     | Must end with hyphen              | `api-` not `api`     |
| Characters | Lowercase, numbers, hyphens       | `web2-` OK           |
| Starting   | Must start with letter            | `auth-` not `2auth-` |
| Length     | Short recommended (no hard limit) | `pydo-`, `auth-`     |

| Good Prefixes | Bad Prefixes | Why Bad            |
| ------------- | ------------ | ------------------ |
| `pydo-`       | `API-`       | Uppercase          |
| `auth-`       | `web_app-`   | Underscore         |
| `web2-`       | `2auth-`     | Starts with number |

## Execution

1. Validate environment (precheck command above)
2. Determine prefix from project name (first 6 chars, lowercase, alphanumeric)
3. Initialize Beads if `.beads/` missing
4. Create required directories
5. Report status and next steps

## Success Criteria

- [ ] `.beads/` directory exists with database
- [ ] Prefix follows naming rules (lowercase, letter start, hyphen end)
- [ ] `.claude/commands/` and `.claude/rules/` exist
- [ ] `docs/plans/` exists
- [ ] `bd info --json` returns valid response

## What Gets Created

| Component      | Purpose                                 |
| -------------- | --------------------------------------- |
| `.beads/`      | Beads issue tracking database and JSONL |
| `.claude/lib/` | Shared workflow utilities               |
| `docs/plans/`  | Implementation plan documents           |

## Edge Considerations

- **Long existing prefix**: Warn, continue. User fixes with `bd rename-prefix`.
- **Missing CLAUDE.md**: Warn, continue. User copies from CLAUDE.md.example.
- **Git not initialized**: Initialize git or warn before proceeding.

## Flag Configuration (Optional)

After initialization, optionally configure workflow flags:

| Flag           | File                               | Effect                              |
| -------------- | ---------------------------------- | ----------------------------------- |
| team-mode      | `.claude/ccbw-flag-team-mode`      | Full git sync instead of flush-only |
| strict-quality | `.claude/ccbw-flag-strict-quality` | Require quality gate before closing |

Use `/workflow-config` to manage flags.

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-init

# Check bd CLI
bd version

# Initialize Beads (replace PREFIX)
bd init -p PREFIX- --quiet

# Verify prefix
bd info --json | jq -r '.config.issue_prefix'

# Fix long prefix
bd rename-prefix short- --dry-run   # Preview
bd rename-prefix short-             # Apply

# Create required directories
mkdir -p .claude/commands .claude/lib .claude/rules docs/plans

# Enable team mode
touch .claude/ccbw-flag-team-mode

# bd CLI installation
# Go: go install github.com/steveyegge/beads/cmd/bd@latest
# Homebrew: brew install steveyegge/tap/beads
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - Beads CLI patterns
- @.claude/commands/workflow-start.md - Begin new feature
- @.claude/commands/workflow-health.md - System diagnostics
