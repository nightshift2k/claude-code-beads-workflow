# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.0] - 2025-12-29

### Added

**Workflow Commands**

- `/workflow-overview` - View plan state (summary, log, full, current, all modes)
- `/workflow-config` - Manage flags (team-mode, strict-quality, protected-branch, auto-cleanup)
- `/workflow-question-ask` - Capture research questions with blocking dependencies
- `/workflow-steer-research` - Resolve research and update blocked tasks
- `/workflow-steer-correct` - Course-correct when human spots divergence

**Git Branch Integration**

- `/workflow-start` creates feature branch `feature/<epic-id>-<slug>` alongside epic
- `/workflow-work` validates branch matches claimed epic
- `/workflow-land` detects epic completion, handles merge/PR decisions, generates PR from Beads context
- Draft PR support for incomplete epics with `protected-branch` flag
- Tiered conflict handling: auto-resolves Beads-only, guides manual for code
- Stash warning with optional auto-cleanup

**Migration Support**

- `install-workflow.sh` - One-command installation for existing projects
- `CLAUDE-workflow.md` - Extracted workflow instructions for `@CLAUDE-workflow.md` reference
- `CLAUDE-workflow-migration.md` - Complete migration guide

**Configuration**

- Flag system: file-presence flags in `.claude/` control workflow behavior
- Epic-centric plan management with steering logs (INIT/STEER/CORRECT entries)
- Log validation warns when epic modifications lack steering entries
- Beads plan change reminder hook (conditional: checks bd + .beads exist)

**Infrastructure**

- Python workflow tool (`workflow.py`) replaces all bash scripts (stdlib only)
- Beads CLI version validation (minimum v0.37.0, recommended v0.39.1+)
- Prettier formatting hook (optional, skips if not installed)
- Beads git hooks via pre-commit (sync on commit, import on merge/checkout)
- Snippet testing quality gate (`docs/test-bd-commands.sh`)

**Documentation**

- `CLAUDE.md.example` - Template for users to copy
- `QUICKSTART.md` - 5-minute kickstart guide (root directory)
- `beads-patterns.md` - Beads CLI jq patterns and gotchas
- `agent-dispatch.md` - Agent selection rules
- `git-conventions.md` - Commit conventions with Beads integration
- Meta-project constraint in `CLAUDE.md` (template doesn't use its own workflow)
- bd vs TodoWrite decision framework
- Multi-developer collaboration patterns (team sync, sandbox mode, GitLab Enterprise, protected branches)

**Beads CLI v0.36-v0.39.1 Features**

- `bd ready --parent`, `bd blocked --parent` for epic scoping (v0.37.0+)
- `bd close --suggest-next` for dependency suggestions (v0.37.0+)
- `bd doctor --fix` for auto-repair (v0.38.0+)
- `bd where` for database location (v0.39.1+)
- `bd orphans` for finding orphaned issues (v0.39.0+)
- `bd update --parent` for reparenting (v0.39.1+)
- `bd list --pretty --watch` for live monitoring (v0.36.0+)
- `bd search` with filters (v0.36.0+)
- Removed `bd pin`/`bd unpin` references (commands removed in v0.39.0)
- Removed 8-character prefix limit (v0.39.1+)

### Changed

**Breaking**

- Moved `workflow.py` to `.claude/lib/` (consolidated from `_claude/lib/`)
  - Simplifies project structure: everything in `.claude/` now
  - Migration: `mv _claude/lib/workflow.py .claude/lib/ && rmdir _claude/lib _claude`
- Claude Code hooks migrated to JSON format
  - `.claude/settings.json` for shared hooks (committed)
  - `.claude/settings.local.json` for personal overrides (gitignored)
  - Deleted `.claude/hooks/` directory (YAML not supported)

**Architecture**

- Refactored all workflow utilities from bash to Python (no external dependencies)
- `workflow.py` reduced from 1090 to 378 lines (65% reduction)
  - Removed `bd_*` wrappers, `steering_*` utilities, unused `cmd_*` handlers
  - Contains only `precheck` and `health` commands
  - All slash commands call `bd` CLI directly
- AI-native instruction format: Intent/Decision Framework/Success Criteria sections

**Behavior**

- `/workflow-track` creates hierarchical child IDs (epic.1, epic.2)
- `/workflow-work` requires specialized agent dispatch
- Agent label convention (`agent:*`) enables automatic dispatch routing
- Expanded agent dispatch table (backend-architect, refactoring-expert, quality-engineer, technical-writer, root-cause-analyst)
- Markdownlint config tightened (re-enabled MD022, MD029, MD032, MD055; disabled MD001, MD058, MD060)

**Documentation**

- Rules files renamed: dropped numeric prefixes (e.g., `001-project-principles.md` → `project-principles.md`)
- Rules improvements: anti-patterns tag, agent failure recovery, file coordination via `--notes`, verification rules moved to project-principles.md
- All file references use `@path/to/file` syntax
- DRY refactors: jq warnings and agent dispatch consolidated into rules files
- Beads v0.29-v0.32.1 documentation: `--body-file`, `bd graph`, `bd reset`, `deferred` status

### Fixed

**Critical**

- `--description` heredoc silently loses data with code blocks - mandated `--body-file` for all complex content
- Self-contained descriptions rule - banned "see above" and external references in Beads descriptions

**Quality Reviews**

- Project-wide review (17 issues): sync checkpoint in workflow-track, bd graph requires issue-id, bd blocked structure documented, command count validation, rule files in Related Files, priority format standardized
- CLAUDE.md.example review (17 items): JSON format corrected, `--body-file` pattern, `/workflow-do` added, sandbox guidance updated, `-p PREFIX-` in examples, `bd import --force` fixes

**Bug Fixes**

- jq "Cannot index array with string" - all bd commands return arrays
- `/workflow-health` used `.issues` instead of array directly
- Missing `--force` flag with `--parent` caused "prefix mismatch" errors
- Random task IDs instead of sequential hierarchical IDs
- `/workflow-land` multi-line bash commands failed
- Bash variable persistence issues in Claude Code
- Precheck traceback in non-interactive environments
- Skill name consistency (`superpowers:brainstorm` without -ing)
- Beads version requirement in test-workflow-validation.md (0.2.0 → 0.37.0)

### Removed

- `.claude/lib/check_shell.py` - Obsolete after AI-native migration
- `.claude/hooks/` directory - YAML hook format not supported
- `/workflow-questions` - Replaced by `/workflow-question-ask`
- `open-questions-template.md` - No longer needed
- `.claude/lib/workflow-precheck.sh` - Replaced by Python
- `.claude/lib/steering-utils.sh` - Replaced by Python
- `.claude/lib/sanitize_beads_json.py` - Absorbed into workflow.py

## [0.1.0] - 2025-12-15

### Added

- Initial release of the Agentic Development Workflow
- 9 workflow slash commands:
  - `/workflow-init` - Initialize project for workflow
  - `/workflow-start` - Begin new feature with Beads epic
  - `/workflow-track` - Set up Beads tracking for planned work
  - `/workflow-execute` - Execute implementation plan with Beads tracking
  - `/workflow-work` - Find and claim available work
  - `/workflow-land` - Complete session properly (REQUIRED before stopping)
  - `/workflow-check` - Review project status
  - `/workflow-health` - Run diagnostics
- Beads integration for distributed issue tracking
- Multi-agent coordination rules
- Project principles and quality gates
- Session management workflows
- Environment validation precheck system
