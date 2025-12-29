<p align="center">
  <h1 align="center">🚀 Agentic Development Workflow</h1>
  <p align="center">
    <strong>Supercharge your AI-assisted development with structured workflows and distributed issue tracking</strong>
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.2.0-green.svg" alt="Version"></a>
  <a href="https://github.com/steveyegge/beads"><img src="https://img.shields.io/badge/Beads_CLI-v0.37.0+-purple.svg" alt="Beads CLI"></a>
  <a href="https://github.com/nightshift2k/claude-code-beads-workflow/stargazers"><img src="https://img.shields.io/github/stars/nightshift2k/claude-code-beads-workflow?style=social" alt="GitHub Stars"></a>
  <a href="https://github.com/nightshift2k/claude-code-beads-workflow/issues"><img src="https://img.shields.io/github/issues/nightshift2k/claude-code-beads-workflow" alt="GitHub Issues"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-documentation">Docs</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

<div align="center">

| 🎯 **14 Slash Commands** | 🌿 **Git Branch Integration** | 👥 **Multi-Agent Coordination** |  🛡️ **Quality Gates**   |
| :----------------------: | :---------------------------: | :-----------------------------: | :---------------------: |
| Full workflow management |  Auto feature branches & PRs  |  Prevent conflicts & data loss  | Built-in best practices |

</div>

---

## 📋 Table of Contents

- [Why This Workflow?](#-why-this-workflow)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Commands Reference](#-commands-reference)
- [Workflow Lifecycle](#-workflow-lifecycle)
- [Configuration](#️-configuration)
- [Project Structure](#️-project-structure)
- [Prerequisites](#-prerequisites)
- [Team Collaboration](#-team-collaboration)
- [Documentation](#-documentation)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 💡 Why This Workflow?

### The Problem

AI-assisted development is powerful, but without structure it leads to:

- ❌ **Lost context** between sessions - AI forgets what you were working on
- ❌ **Duplicate work** - Same tasks get redone without tracking
- ❌ **Merge conflicts** - Multiple agents editing the same files
- ❌ **Orphaned tasks** - Work started but never completed
- ❌ **No audit trail** - Can't trace decisions or changes

### The Solution

This workflow template provides:

- ✅ **Persistent tracking** - Beads tracks all work across sessions
- ✅ **Clear task ownership** - Issue IDs link code to decisions
- ✅ **Conflict prevention** - Multi-agent coordination rules
- ✅ **Session discipline** - Proper start/land workflow ensures nothing is lost
- ✅ **Full audit trail** - Every decision documented in issues

### Before & After

| Without Workflow               | With Workflow                                |
| ------------------------------ | -------------------------------------------- |
| "What was I working on?"       | `bd ready` shows all available tasks         |
| "Did anyone change this file?" | Agent coordination prevents conflicts        |
| "Why did we decide X?"         | Decision rationale in issue descriptions     |
| "Is this task done?"           | Clear status tracking with dependencies      |
| "How do I resume?"             | `/workflow-work` picks up where you left off |

---

## ✨ Features

### 🎯 Workflow Commands

14 powerful slash commands for complete workflow management:

| Category       | Commands                                                                        | Purpose                                |
| -------------- | ------------------------------------------------------------------------------- | -------------------------------------- |
| **Setup**      | `/workflow-init`                                                                | Initialize project with Beads tracking |
| **Planning**   | `/workflow-start`, `/workflow-track`                                            | Create epics, convert plans to issues  |
| **Execution**  | `/workflow-execute`, `/workflow-work`, `/workflow-do`                           | Run plans, claim tasks, quick fixes    |
| **Monitoring** | `/workflow-check`, `/workflow-health`, `/workflow-overview`                     | Status, diagnostics, plan views        |
| **Steering**   | `/workflow-question-ask`, `/workflow-steer-research`, `/workflow-steer-correct` | Research, course correction            |
| **Completion** | `/workflow-land`                                                                | Proper session closure (required!)     |
| **Config**     | `/workflow-config`                                                              | Manage workflow flags                  |

### 🌿 Git Branch Integration

- **Auto feature branches** - `/workflow-start` creates `feature/<epic-id>-<slug>`
- **Branch validation** - `/workflow-work` ensures you're on the right branch
- **Smart landing** - `/workflow-land` handles merge/PR decisions automatically
- **Draft PR support** - Incomplete epics create draft PRs with `protected-branch` flag
- **Conflict handling** - Auto-resolves Beads-only conflicts, guides manual for code

### 👥 Multi-Agent Coordination

Built-in rules prevent the chaos of multiple AI agents:

- **File locking convention** - Claim files via `--notes` before editing
- **Sequential enforcement** - Never parallel edit the same file
- **Agent dispatch** - Route tasks to specialized agents (`python-expert`, `golang-expert`, etc.)
- **Brainstorming gate** - Features touching 3+ files require design first

### 🛡️ Quality Gates

- **Session management** - Every session ends with `/workflow-land`
- **Verification rules** - Tests must pass before marking complete
- **Priority system** - P0-P4 for proper triage
- **Decision documentation** - WHY not just WHAT

### 🔧 Configuration Flags

| Flag               | Purpose                              |
| ------------------ | ------------------------------------ |
| `team-mode`        | Full git sync for team collaboration |
| `strict-quality`   | Require quality gate before closing  |
| `protected-branch` | Use PRs instead of direct merge      |
| `auto-cleanup`     | Clear stash + prune remotes on land  |

### 📊 Epic-Centric Management

- **Hierarchical IDs** - `epic-abc.1`, `epic-abc.2` for clear relationships
- **Steering logs** - INIT/STEER/CORRECT entries track plan evolution
- **Plan views** - Summary, log, full, current, or all modes

---

## 🚀 Quick Start

### 30-Second Setup (New Projects)

```bash
# 1. Clone the template
git clone https://github.com/nightshift2k/claude-code-beads-workflow.git my-project
cd my-project

# 2. Install Beads CLI
go install github.com/steveyegge/beads/cmd/bd@latest
# Or: brew install steveyegge/tap/beads

# 3. Initialize tracking
bd init -p myproj- --quiet

# 4. Open in Claude Code and run:
/workflow-init
```

### One-Command Install (Existing Projects)

```bash
curl -sL https://raw.githubusercontent.com/nightshift2k/claude-code-beads-workflow/main/install-workflow.sh | bash
```

The script:

- ✅ Validates your git repository
- ✅ Downloads all workflow files (22 files)
- ✅ Configures CLAUDE.md with `@CLAUDE-workflow.md` reference
- ✅ Provides next steps

See [CLAUDE-workflow-migration.md](CLAUDE-workflow-migration.md) for detailed migration instructions.

---

## 📖 Commands Reference

### Core Workflow

| Command             | Purpose                       | When to Use                 |
| ------------------- | ----------------------------- | --------------------------- |
| `/workflow-init`    | Initialize project            | First-time setup            |
| `/workflow-start`   | Create feature epic + branch  | Starting new feature        |
| `/workflow-track`   | Convert plan to Beads issues  | After planning complete     |
| `/workflow-execute` | Run full implementation plan  | Ready to implement          |
| `/workflow-work`    | Find and claim available task | Ready to work               |
| `/workflow-land`    | **Complete session properly** | **Always before stopping!** |

### Monitoring & Status

| Command              | Purpose                          | When to Use              |
| -------------------- | -------------------------------- | ------------------------ |
| `/workflow-check`    | Review current status            | Need overview            |
| `/workflow-health`   | Run diagnostics                  | Something seems wrong    |
| `/workflow-overview` | View plan state (multiple modes) | Detailed plan inspection |
| `/workflow-config`   | Manage workflow flags            | Configure behavior       |

### Steering & Research

| Command                    | Purpose                   | When to Use               |
| -------------------------- | ------------------------- | ------------------------- |
| `/workflow-do`             | Quick isolated task       | Small fix, no epic needed |
| `/workflow-question-ask`   | Capture research question | Need to investigate       |
| `/workflow-steer-research` | Apply research findings   | Research complete         |
| `/workflow-steer-correct`  | Course correction         | Human spots divergence    |

---

## 🔄 Workflow Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                      AGENTIC WORKFLOW LIFECYCLE                     │
└─────────────────────────────────────────────────────────────────────┘

   SETUP              PLANNING              TRACKING            EXECUTION
     │                   │                     │                    │
     ▼                   ▼                     ▼                    ▼
/workflow-init  →  /workflow-start  →  /workflow-track  →  /workflow-execute
                   (create epic)       (plan → issues)      (run full plan)
                        │                                          │
                        ▼                                    OR    ▼
                   brainstorm +                           /workflow-work ◄──┐
                   writing-plans                          (task by task)    │
                                                                │           │
                        MONITORING & STEERING                   │           │
                              │                                 │           │
            /workflow-check (status)                            │           │
            /workflow-health (diagnostics)                      │           │
            /workflow-overview (plan views)                     │           │
            /workflow-question-ask (research)                   │           │
            /workflow-steer-research (apply findings)           │           │
            /workflow-steer-correct (course correct)            │           │
            /workflow-do (quick isolated task)                  │           │
                                                                │           │
                                         SESSION END            │           │
                                              │                 │           │
                                              ▼                 │           │
                                       /workflow-land ◄─────────┘           │
                                              │                             │
                              ┌───────────────┴───────────────┐             │
                              │                               │             │
                        epic complete?                  epic incomplete     │
                              │                               │             │
                              ▼                               └─────────────┘
                       merge/PR + done                   (stay on branch,
                                                          next session)
```

---

## ⚙️ Configuration

### Workflow Flags

Flags control workflow behavior. Managed via `/workflow-config` or file presence in `.claude/`:

| Flag               | File                                 | Effect                              |
| ------------------ | ------------------------------------ | ----------------------------------- |
| `team-mode`        | `.claude/ccbw-flag-team-mode`        | Use `bd sync` for full git sync     |
| `strict-quality`   | `.claude/ccbw-flag-strict-quality`   | Require quality gate before close   |
| `protected-branch` | `.claude/ccbw-flag-protected-branch` | Use PRs instead of direct merge     |
| `auto-cleanup`     | `.claude/ccbw-flag-auto-cleanup`     | Clear stash + prune remotes on land |

**Managing flags:**

```bash
# Enable
/workflow-config team-mode on

# Disable
/workflow-config strict-quality off

# List all
/workflow-config --list

# Manual
touch .claude/ccbw-flag-team-mode   # Enable
rm .claude/ccbw-flag-team-mode      # Disable
```

### Team Setup

For team projects, commit flag files:

```bash
touch .claude/ccbw-flag-team-mode
git add .claude/ccbw-flag-team-mode
git commit -m "chore: enable team mode for workflow"
```

---

## 🏗️ Project Structure

```
your-project/
├── .claude/
│   ├── commands/           # 14 workflow slash commands
│   │   ├── workflow-init.md
│   │   ├── workflow-start.md
│   │   ├── workflow-track.md
│   │   ├── workflow-execute.md
│   │   ├── workflow-work.md
│   │   ├── workflow-land.md
│   │   ├── workflow-check.md
│   │   ├── workflow-do.md
│   │   ├── workflow-question-ask.md
│   │   ├── workflow-steer-research.md
│   │   ├── workflow-steer-correct.md
│   │   ├── workflow-health.md
│   │   ├── workflow-overview.md
│   │   └── workflow-config.md
│   ├── lib/                # Shared utilities
│   │   └── workflow.py     # Python workflow CLI (stdlib only)
│   └── rules/              # Project rules and principles
│       ├── project-principles.md
│       ├── ai-native-instructions.md
│       ├── multi-agent-coordination.md
│       ├── beads-patterns.md
│       ├── agent-dispatch.md
│       └── git-conventions.md
├── docs/
│   └── plans/              # Implementation plans
├── .beads/                 # Beads tracking database (created by bd init)
├── CLAUDE.md               # Your workflow instructions
├── CLAUDE.md.example       # Template to copy
├── CLAUDE-workflow.md      # Full workflow reference
├── QUICKSTART.md           # 2-minute introduction
└── README.md
```

---

## 📋 Prerequisites

### Required

| Dependency      | Version                         | Installation                                                                                  |
| --------------- | ------------------------------- | --------------------------------------------------------------------------------------------- |
| **Beads CLI**   | v0.37.0+ (v0.39.1+ recommended) | `go install github.com/steveyegge/beads/cmd/bd@latest` or `brew install steveyegge/tap/beads` |
| **Claude Code** | Latest                          | [claude.ai/claude-code](https://claude.ai/claude-code)                                        |
| **Git**         | Any recent                      | Pre-installed on most systems                                                                 |

**Check your Beads version:**

```bash
bd version
# Minimum: v0.37.0
# Recommended: v0.39.1+
```

### Optional (Enhanced Features)

| Feature                 | Dependency                                          | Fallback                                  |
| ----------------------- | --------------------------------------------------- | ----------------------------------------- |
| `/workflow-execute`     | `superpowers:executing-plans` skill                 | Manual task-by-task with `/workflow-work` |
| Brainstorming gate      | `superpowers:brainstorm` skill                      | Manual design documentation               |
| Implementation planning | `superpowers:writing-plans` skill                   | Manual plan creation in `docs/plans/`     |
| Specialized code tasks  | Sub-agents (`python-expert`, `golang-expert`, etc.) | Generic Claude Code capabilities          |

**Install superpowers skills:** See [superpowers](https://github.com/obra/superpowers) for installation.

> **Note:** All workflow commands function without skills - you just perform automated steps manually.

---

## 👥 Team Collaboration

### Solo Developer (Default)

```bash
# Export changes to JSONL only (no git operations)
bd sync --flush-only

# Handle git manually
git add . && git commit && git push
```

### Multi-Developer Team

Enable team mode for full git sync:

```bash
# Enable team mode
touch .claude/ccbw-flag-team-mode

# Full sync: export + commit + pull + import + push
bd sync
```

Run `bd sync` at task boundaries (start/end of each task).

### Protected Branch Workflow

For teams requiring code review:

```bash
# Setup (new project)
bd init -p myproj- --branch beads-metadata --quiet

# Setup (existing project)
bd migrate-sync beads-metadata

# Daily workflow
bd sync --flush-only  # Commits to beads-metadata branch
```

Human creates PR/MR to merge `beads-metadata` → `main` periodically.

### GitLab Enterprise

Works with any git remote:

```bash
git clone git@gitlab.company.com:team/project.git
cd project

# HTTPS with custom CA
git config http.sslCAInfo /path/to/company-ca.crt

# Initialize (same as GitHub)
bd init -p myproj- --quiet
```

Use Merge Requests (MR) instead of Pull Requests (PR).

---

## 📚 Documentation

| Document                                                        | Description                             |
| --------------------------------------------------------------- | --------------------------------------- |
| [QUICKSTART.md](QUICKSTART.md)                                  | 2-minute introduction                   |
| [CLAUDE-workflow.md](CLAUDE-workflow.md)                        | Complete workflow reference             |
| [CLAUDE-workflow-migration.md](CLAUDE-workflow-migration.md)    | Migration guide for existing projects   |
| [CLAUDE.md.example](CLAUDE.md.example)                          | Template to copy for your project       |
| [test-workflow-validation.md](docs/test-workflow-validation.md) | Full validation test (build sample CLI) |

### Rules Reference

| Rule File                     | Purpose                                    |
| ----------------------------- | ------------------------------------------ |
| `project-principles.md`       | Core development principles, quality gates |
| `ai-native-instructions.md`   | AI-optimized instruction design            |
| `multi-agent-coordination.md` | Prevent conflicts between agents           |
| `beads-patterns.md`           | Beads CLI patterns and gotchas             |
| `agent-dispatch.md`           | Route tasks to specialized agents          |
| `git-conventions.md`          | Commit conventions with Beads integration  |

---

## 🔧 Troubleshooting

### Quick Fixes

| Problem                 | Solution                                                              |
| ----------------------- | --------------------------------------------------------------------- |
| `bd: command not found` | Install Beads: `go install github.com/steveyegge/beads/cmd/bd@latest` |
| `no .beads directory`   | Run `/workflow-init`                                                  |
| `database out of sync`  | Run `bd import --force`                                               |
| Beads version too old   | Upgrade: `go install github.com/steveyegge/beads/cmd/bd@latest`       |
| No ready tasks          | Check `bd blocked` for dependencies                                   |

### Recovery Commands

```bash
# Auto-repair (v0.38.0+)
bd doctor --fix

# Rebuild from JSONL
bd import --force

# Full database reset
bd reset

# Find database location
bd where
```

### More Help

- Full troubleshooting in [CLAUDE.md.example](CLAUDE.md.example#troubleshooting)
- [Beads Troubleshooting](https://github.com/steveyegge/beads/blob/main/docs/TROUBLESHOOTING.md)
- [Open an issue](https://github.com/nightshift2k/claude-code-beads-workflow/issues)

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Test** your changes using `docs/test-workflow-validation.md`
4. **Commit** with conventional commits: `feat: add amazing feature`
5. **Push** to your fork: `git push origin feature/amazing-feature`
6. **Open** a Pull Request

### Development Notes

- This is a **meta-project** - the workflow template itself
- We do **NOT** use Beads to track work on this template (that would be circular)
- Test changes using the validation test which builds a sample Python CLI

### Code of Conduct

Be kind, be respectful, be constructive.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Beads](https://github.com/steveyegge/beads)** by Steve Yegge - The distributed issue tracking system that powers this workflow
- **[Claude Code](https://claude.ai/claude-code)** by Anthropic - The AI coding assistant this workflow is designed for
- **[superpowers](https://github.com/obra/superpowers)** by Jesse Vincent - Skills that enhance workflow automation
- **Community contributors** - Everyone who has tested, reported issues, and suggested improvements

---

## 🔗 Related Projects

| Project                                            | Description                              |
| -------------------------------------------------- | ---------------------------------------- |
| [Beads](https://github.com/steveyegge/beads)       | Distributed issue tracking for AI agents |
| [Claude Code](https://claude.ai/claude-code)       | AI coding assistant                      |
| [superpowers](https://github.com/obra/superpowers) | Skills for Claude Code automation        |

---

<p align="center">
  <sub>Built with ❤️ for the AI-assisted development community</sub>
</p>

<p align="center">
  <a href="#-agentic-development-workflow">⬆️ Back to Top</a>
</p>
