# Claude Code Beads Workflow - Meta Project

> **⚠️ CRITICAL: Read MCP preferences before any file operations**
>
> @~/.claude/MCP_Usage_Preferences.md
>
> - **Code structure analysis** → Use Serena (not Read/Grep)
> - **Multi-file or pattern edits** → Use Morphllm (not Edit)
> - **Previous session context** → Use Claude-Mem (not re-reading files)

## Project Information

```
Project: claude-code-beads-workflow
Description: Template for agentic AI development using Beads issue tracking
Tech Stack: Bash, Markdown, Beads CLI
Repository: https://github.com/nightshift2k/claude-code-beads-workflow
```

## Overview

This project is the workflow template itself, not a project using the template. When contributing to the workflow commands, rules, or documentation, use this file.

**For projects using this template:** Copy `CLAUDE.md.example` to your project and customize it.

## Prime Directive: Test All Commands

> **⚠️ CRITICAL: Every `bd` command and bash snippet MUST be tested before inclusion in plans, documentation, or workflow commands.**

Untested commands ship broken documentation that users cannot debug. The `--help` flag is your first line of defense.

### Before Writing Any bd Command

1. **Verify command exists:** `bd <command> --help`
2. **Verify flags exist:** Check help output for exact flag names
3. **Verify output format:** Run with `--json` and confirm structure
4. **Verify jq patterns:** Test against actual output, not assumptions

### Common Mistakes This Prevents

| Mistake                                                  | How to Catch                              |
| -------------------------------------------------------- | ----------------------------------------- |
| Using non-existent flags (e.g., `--parent` on `bd list`) | Run `bd list --help` first                |
| Wrong jq patterns for JSON structure                     | Test: `bd <cmd> --json \| jq '<pattern>'` |
| Assuming command behavior                                | Read `--help`, don't guess                |

### Testing Checklist for Bash Snippets

```bash
# Before adding to documentation:
bd <command> --help              # Command exists?
bd <command> --json | jq '.'     # Valid JSON?
bd <command> --json | jq 'type'  # Array or object?
bd <command> --json | jq '.[0]'  # Expected structure?
```

**No exceptions.** If you cannot test a command (no Beads repo available), mark it as `UNTESTED` in the documentation.

## Meta-Project Constraint

**This project does NOT use its own Beads workflow.**

This is a META-PROJECT - the workflow template itself. Using Beads to track work on the template would be circular and confusing:

- The template defines how to use Beads
- We cannot use Beads to develop the template that teaches Beads

**Development approach for this project:**

- Use standard git workflow (branches, commits, PRs)
- Track work via GitHub issues (not Beads)
- Test workflow commands using `docs/test-workflow-validation.md`

## Contributing to Workflow Commands

When modifying commands in `.claude/commands/`:

1. **Test changes** using the validation test (`docs/test-workflow-validation.md`)
2. **Document decisions** in appropriate rule files
3. **Update CHANGELOG.md** with changes
4. **Update CLAUDE.md.example** if template instructions change

## Key Principles

### Keep Template Generic

Avoid project-specific patterns. Users customize after copying.

### Maintain Backward Compatibility

Existing users rely on command interfaces. Add features, don't break existing usage.

### Document Gotchas

When discovering Beads CLI quirks or Claude Code limitations, document them in:

- `beads-patterns.md` for Beads CLI issues
- Appropriate rule files for workflow patterns
- CLAUDE.md.example troubleshooting section

### Write Clearly

Apply Strunk's rules:

- Use active voice
- Omit needless words
- Put statements in positive form
- Use definite, specific, concrete language

## Project Structure

```
.claude/
├── commands/           # 14 workflow slash commands
├── lib/                # Shared utilities
│   └── workflow.py     # Python workflow CLI tool (stdlib only)
└── rules/              # Project rules and principles
    ├── project-principles.md
    ├── ai-native-instructions.md
    ├── multi-agent-coordination.md
    ├── beads-patterns.md
    ├── agent-dispatch.md
    └── git-conventions.md
docs/
├── plans/              # Implementation plans
└── test-workflow-validation.md  # Validation test
QUICKSTART.md           # 2-minute introduction
CLAUDE.md.example       # Template for users to copy
```

## Testing Changes

Use the validation test to verify workflow commands:

```bash
# Follow the pydo CLI example in docs/test-workflow-validation.md
# This exercises all 14 workflow commands
```

## Quality Gates

Before closing issues on this meta-project:

- [ ] **All bd commands tested** (see Prime Directive above)
- [ ] Commands work as documented
- [ ] CHANGELOG.md updated
- [ ] CLAUDE.md.example updated (if template changes)
- [ ] README.md updated (if user-facing features change)
- [ ] Validation test passes (if commands modified)

## Related Files

- @CLAUDE.md.example - Template users copy to their projects
- @README.md - User-facing documentation
- @QUICKSTART.md - Quick introduction for new users
- @.claude/rules/ - All workflow rules and patterns
