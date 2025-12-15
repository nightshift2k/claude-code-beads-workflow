# Agentic Development Workflow

A structured workflow template for agentic AI development using [Beads](https://github.com/steveyegge/beads) for distributed issue tracking.

## Overview

This template provides a complete workflow for AI-assisted development with:

- **9 slash commands** for workflow management
- **Beads integration** for issue tracking and dependencies
- **Multi-agent coordination** rules to prevent conflicts
- **Session management** with proper state persistence
- **Quality gates** and project principles

Designed for [Claude Code](https://claude.ai/claude-code) but adaptable to other AI assistants with slash command support.

## Quick Start

```bash
# 1. Clone or copy this template
git clone https://github.com/nightshift2k/claude-code-beads-workflow.git my-project
cd my-project

# 2. Install Beads CLI (if not installed)
go install github.com/steveyegge/beads/cmd/bd@latest
# Or: brew install steveyegge/tap/beads

# 3. Initialize Beads tracking (use short prefix, max 8 chars)
bd init -p myproj- --quiet

# 4. Open in Claude Code and run
/workflow-init
```

## Workflow Commands

| Command | Purpose |
|---------|---------|
| `/workflow-init` | Initialize project for agentic workflow |
| `/workflow-start` | Begin new feature with Beads epic |
| `/workflow-track` | Convert implementation plan to tracked issues |
| `/workflow-execute` | Execute plan with integrated tracking |
| `/workflow-work` | Find and claim available work |
| `/workflow-land` | Complete session properly (required before stopping) |
| `/workflow-check` | Review current project status |
| `/workflow-questions` | Track and resolve open questions |
| `/workflow-health` | Diagnose workflow issues |

## Workflow Lifecycle

```
/workflow-init → /workflow-start → /workflow-track → /workflow-execute
                 (create epic)    (plan → issues)   (or /workflow-work)
                                                            │
                              /workflow-land ◄──────────────┘
                              (close session)
```

## Project Structure

```
your-project/
├── .claude/
│   ├── commands/           # 9 workflow slash commands
│   ├── lib/                # Shared utilities (precheck.sh)
│   └── rules/              # Project rules and principles
│       ├── 001-project-principles.md
│       ├── 002-open-questions-template.md
│       ├── 003-multi-agent-coordination.md
│       ├── 004-beads-json-patterns.md
│       └── 005-agent-dispatch.md
├── docs/
│   └── plans/              # Design documents and implementation plans
├── CLAUDE.md               # Main workflow instructions
└── README.md
```

## Configuration

After copying this template, customize for your project:

1. **Edit `CLAUDE.md`** - Update the `<project_context>` section with your project details
2. **Review rules** - Adjust `.claude/rules/001-project-principles.md` for your standards
3. **Add design docs** - Place implementation plans in `docs/plans/`

## Prerequisites

### Required
- [Beads CLI](https://github.com/steveyegge/beads) - Distributed issue tracking
- [Claude Code](https://claude.ai/claude-code) or compatible AI assistant
- Git (for version control)

### Optional (Enhanced Features)

This workflow integrates with skills and sub-agents that may require additional setup:

| Feature | Dependency | Fallback |
|---------|------------|----------|
| `/workflow-execute` | `superpowers:executing-plans` skill | Manual task-by-task execution with `/workflow-work` |
| Brainstorming gate | `superpowers:brainstorming` skill | Manual design documentation |
| Implementation planning | `superpowers:writing-plans` skill | Manual plan creation in `docs/plans/` |
| Specialized code tasks | Sub-agents (`python-expert`, `golang-expert`, etc.) | Generic Claude Code capabilities |

**If skills are not available:**
- The workflow commands will still function
- You'll need to manually perform steps that would otherwise be automated
- `/workflow-work` provides task-by-task execution without skill dependencies

**To install superpowers skills:**
See [superpowers](https://github.com/obra/superpowers) for installation instructions.

## Key Concepts

### Session Management
Always complete sessions with `/workflow-land` to:
- Close completed issues
- Persist changes (sandbox mode uses `bd sync --flush-only`)
- Create follow-up tasks for incomplete work

### Multi-Agent Coordination
When using multiple agents, follow the rules in `003-multi-agent-coordination.md`:
- Never edit the same file from parallel agents
- Use sequential operations for overlapping work
- Document decision rationale

### Priority System
Issues use priorities 0-4:
- **P0**: Critical (security, data loss, broken builds)
- **P1**: High (major features, important bugs)
- **P2**: Medium (default for most work)
- **P3**: Low (polish, optimization)
- **P4**: Backlog (future ideas)

## Validation

A complete validation test is available in `docs/test-workflow-validation.md`. It walks through building a sample Python CLI (`pydo`) while exercising every workflow command.

## License

MIT - See [LICENSE](LICENSE) for details.

## Related

- [Beads](https://github.com/steveyegge/beads) - Distributed issue tracking for AI agents
- [Claude Code](https://claude.ai/claude-code) - AI coding assistant
