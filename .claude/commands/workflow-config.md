---
argument-hint: "[flag-name] [on|off] | --list"
description: Manage workflow configuration flags
---

## Intent

Enable, disable, or list workflow configuration flags.

## When to Use

- Switching between solo and team workflows
- Enabling or disabling quality gate requirements
- Checking current configuration state

## Context Required

- Verify `.claude/` directory exists
- Check for existing flag files in `.claude/ccbw-flag-*`

## Available Flags

| Flag               | Effect                                          | Default |
| ------------------ | ----------------------------------------------- | ------- |
| `team-mode`        | Use `bd sync` instead of `bd sync --flush-only` | OFF     |
| `strict-quality`   | Require quality gate before closing issues      | OFF     |
| `protected-branch` | Use PRs instead of direct merge to main         | OFF     |
| `auto-cleanup`     | Clear stash + prune remotes on land             | OFF     |

## Decision Framework

| Command      | Action                             | Expected Outcome |
| ------------ | ---------------------------------- | ---------------- |
| `--list`     | Show all flags with current status | Status report    |
| `[flag] on`  | Create flag file, confirm enabled  | Flag active      |
| `[flag] off` | Remove flag file, confirm disabled | Flag inactive    |
| Unknown flag | Report error, list valid flags     | No change        |

## Execution

1. Parse command arguments
2. Apply decision framework based on command type
3. Modify flag file state as needed
4. Report outcome to user

## Success Criteria

- Flag state matches requested action
- Unknown flags rejected with helpful message
- Status reflects actual file system state
- Flag files created or removed correctly

## Edge Considerations

- **Unknown flags**: Warn about `.claude/ccbw-flag-*` files not in the known list
- **Team workflow**: Commit flag files to git for shared configuration
- **Missing directory**: Create `.claude/` if absent

## Reference Material

### Flag File Format

```bash
# Flag files location
.claude/ccbw-flag-team-mode
.claude/ccbw-flag-strict-quality
.claude/ccbw-flag-protected-branch
.claude/ccbw-flag-auto-cleanup

# Valid flags for validation
team-mode|strict-quality|protected-branch|auto-cleanup

# Check if flag enabled
[ -f ".claude/ccbw-flag-[name]" ]

# Enable flag
touch ".claude/ccbw-flag-[name]"

# Disable flag
rm ".claude/ccbw-flag-[name]"
```

### Example Commands

```bash
# Enable team mode for multi-developer workflow
/workflow-config team-mode on

# Check current flags
/workflow-config --list

# Disable strict quality requirement
/workflow-config strict-quality off
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - Beads CLI patterns
- @.claude/commands/workflow-land.md - Session completion
- @.claude/commands/workflow-health.md - System diagnostics
