# Quickstart Guide

Get started with agentic workflow in 5 minutes.

## Prerequisites

- [Beads CLI](https://github.com/steveyegge/beads) - `go install github.com/steveyegge/beads/cmd/bd@latest`
- [Claude Code](https://claude.ai/claude-code) or compatible AI assistant
- Git

## Setup (5 minutes)

```bash
# 1. Copy this template to your project
cp -r claude-code-beads-workflow my-project
cd my-project

# 2. Initialize Beads (use short prefix, max 8 chars)
bd init -p myproj- --quiet

# 3. Initialize workflow
# (In Claude Code)
/workflow-init
```

## Daily Workflow

### Start Work
```
/workflow-work
```
Finds available tasks and claims one.

### Complete Work
```
/workflow-land
```
Required before stopping. Closes issues, syncs state, commits changes.

## Feature Workflow

### Create Feature
```
/workflow-start "Feature name"
```
Creates epic. Save the returned ID (e.g., `myproj-abc`).

### Track Implementation Plan
```
/workflow-track path/to/plan.md
```
Converts plan tasks into Beads issues.

### Execute Plan
```
/workflow-execute path/to/plan.md
```
Runs plan with automated tracking.

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `bd: command not found` | Install Beads: `go install github.com/steveyegge/beads/cmd/bd@latest` |
| `no .beads directory` | Run `/workflow-init` |
| `database out of sync` | Run `bd import --force` |

## Learn More

- **Full workflow**: Read `CLAUDE.md.example` (copy to `CLAUDE.md` in your project)
- **Command details**: See `.claude/commands/`
- **Project principles**: See `.claude/rules/001-project-principles.md`
- **Beads docs**: https://github.com/steveyegge/beads
