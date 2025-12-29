# Quickstart Guide

Get started with agentic workflow in 2 minutes.

## Prerequisites

- [Beads CLI](https://github.com/steveyegge/beads) v0.37.0+ (v0.39.1+ recommended)
  - Install: `go install github.com/steveyegge/beads/cmd/bd@latest`
  - Check version: `bd version`
- [Claude Code](https://claude.ai/claude-code) or compatible AI assistant
- Git

## Setup (2 minutes)

### Option A: Install Script (Recommended)

Add the workflow to any existing project:

```bash
cd your-project
curl -sL https://raw.githubusercontent.com/nightshift2k/claude-code-beads-workflow/main/install-workflow.sh | bash
```

Then in Claude Code:

```
/workflow-init
```

### Option B: Clone Template

Start a new project from the template:

```bash
git clone https://github.com/nightshift2k/claude-code-beads-workflow.git my-project
cd my-project
rm -rf .git && git init   # Fresh git history
```

Then in Claude Code:

```
/workflow-init
```

### Optional: Git Hooks

Auto-sync Beads state on commits and branch switches:

```bash
pip install pre-commit   # or: uv tool install pre-commit
pre-commit install --hook-type pre-commit --hook-type post-merge --hook-type post-checkout
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

| Problem                 | Solution                                                                        |
| ----------------------- | ------------------------------------------------------------------------------- |
| `bd: command not found` | Install Beads: `go install github.com/steveyegge/beads/cmd/bd@latest`           |
| Beads version too old   | Upgrade: `go install github.com/steveyegge/beads/cmd/bd@latest` (need v0.37.0+) |
| `no .beads directory`   | Run `/workflow-init`                                                            |
| `database out of sync`  | Run `bd import --force`                                                         |

## Monitoring & Configuration

### View Plan State

```
/workflow-overview [epic-id]           # Summary view
/workflow-overview [epic-id] --log     # Steering log only
/workflow-overview [epic-id] --full    # Complete details
```

### Manage Flags

```
/workflow-config --list                # Show current flags
/workflow-config team-mode on          # Enable team sync
/workflow-config strict-quality off    # Disable quality gate
```

### Check System Health

```
/workflow-health
```

## Learn More

- **Full workflow**: Read `CLAUDE.md.example` (copy to `CLAUDE.md` in your project)
- **Command details**: See `.claude/commands/`
- **Project principles**: See `.claude/rules/project-principles.md`
- **Beads docs**: https://github.com/steveyegge/beads
