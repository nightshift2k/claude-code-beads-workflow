# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- **BREAKING: Moved workflow.py from `.claude/lib/` to `_claude/lib/`** for Serena MCP compatibility ([#853](https://github.com/oraios/serena/issues/853))
  
  **Migration for existing users:**
  1. Move the file: `mv .claude/lib/workflow.py _claude/lib/workflow.py`
  2. Update command references from `.claude/lib/workflow.py` to `_claude/lib/workflow.py`
  3. Verify: Run `/workflow-health` to confirm
  
  **Why:** Serena MCP excludes dot-directories from symbol analysis. Using `_claude/lib/` enables code navigation while maintaining workflow functionality.

### Added
- `/workflow-question-ask` - Interactive research question capture with one-question-at-a-time UX
- `/workflow-steer-research` - Resolve research questions and update blocked tasks with findings
- `/workflow-steer-correct` - Course correction when human spots AI divergence mid-implementation
- `004-beads-json-patterns.md` - Centralized Beads CLI jq array handling patterns
- `005-agent-dispatch.md` - Centralized agent dispatch rules and patterns
- `006-git-conventions.md` - Centralized git commit conventions with Beads integration
- Agent dispatch requirement in `/workflow-work` - specialized agents now required for implementation
- Hierarchical issue ID documentation with `--parent --force` pattern
- **Checkpoint step in `/workflow-work`** - explicit "one task per invocation" rule with mandatory commit
- `docs/QUICKSTART.md` - Concise 5-minute kickstart guide for new users
- `CLAUDE.md.example` - Template for users to copy to their projects
- **Python workflow tool** - Single `workflow.py` CLI replacing all bash scripts (stdlib only)

### Changed
- **Refactored all workflow utilities from bash to Python** - Single `workflow.py` CLI with no external dependencies
- All internal file references now use `@path/to/file` syntax for Claude Code to read them
- DRY refactor: jq array warnings consolidated into single rules file
- DRY refactor: agent dispatch tables consolidated into single rules file
- Beads prefix enforcement: max 8 characters, validated during `/workflow-init`
- `/workflow-track` now creates hierarchical child IDs (e.g., `epic.1`, `epic.2`)
- `/workflow-start` emphasizes capturing epic ID for child issue creation
- `CLAUDE.md` refactored: meta-project version for template development, users copy `CLAUDE.md.example`
- All workflow commands now invoke Python tool via `uv run python _claude/lib/workflow.py <command>`

### Fixed
- jq "Cannot index array with string" errors - all `bd` commands return arrays `[{...}]`
- `/workflow-health` bug using `.issues` instead of array directly
- Missing `--force` flag with `--parent` causing "prefix mismatch" errors
- Random task IDs instead of sequential hierarchical IDs
- `/workflow-land` multi-line bash commands failing - added explicit `&&` chaining
- **Bash variable persistence issues in Claude Code** - eliminated by switching to Python

### Removed
- `/workflow-questions` - Legacy external file-based question tracking (replaced by `/workflow-question-ask`)
- `open-questions-template.md` - No longer needed with Beads-native question tracking
- **`.claude/lib/workflow-precheck.sh`** - Replaced by Python environment validation
- **`.claude/lib/steering-utils.sh`** - Replaced by Python steering utilities
- **`.claude/lib/sanitize_beads_json.py`** - Absorbed into `workflow.py`

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