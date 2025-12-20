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

## Development Workflow

Follow the same workflow this template provides:

1. **Start features** with `/workflow-start` to create Beads epics
2. **Track work** with `/workflow-track` after creating implementation plans
3. **Execute tasks** with `/workflow-work` or `/workflow-execute`
4. **Complete sessions** with `/workflow-land`

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
- `004-beads-json-patterns.md` for Beads CLI issues
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
_claude/
└── lib/                # Shared utilities
    └── workflow.py     # Python workflow CLI tool (stdlib only)
.claude/
├── commands/           # 11 workflow slash commands
└── rules/              # Project rules and principles
    ├── 001-project-principles.md
    ├── 003-multi-agent-coordination.md
    ├── 004-beads-json-patterns.md
    ├── 005-agent-dispatch.md
    └── 006-git-conventions.md
docs/
├── plans/              # Implementation plans
├── QUICKSTART.md       # 5-minute introduction
└── test-workflow-validation.md  # Validation test
CLAUDE.md.example       # Template for users to copy
```

## Testing Changes

Use the validation test to verify workflow commands:

```bash
# Follow the pydo CLI example in docs/test-workflow-validation.md
# This exercises all 11 workflow commands
```

## Quality Gates

Before closing issues on this meta-project:

- [ ] Commands work as documented
- [ ] CHANGELOG.md updated
- [ ] CLAUDE.md.example updated (if template changes)
- [ ] README.md updated (if user-facing features change)
- [ ] Validation test passes (if commands modified)

## Beads Configuration

This project uses prefix `wf-` for workflow meta-development issues.

```bash
# Already initialized with
bd init -p wf- --quiet
```

## Related Files

- @CLAUDE.md.example - Template users copy to their projects
- @README.md - User-facing documentation
- @docs/QUICKSTART.md - Quick introduction for new users
- @.claude/rules/ - All workflow rules and patterns