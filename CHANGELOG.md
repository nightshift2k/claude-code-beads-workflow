# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `004-beads-json-patterns.md` - Centralized Beads CLI jq array handling patterns
- `005-agent-dispatch.md` - Centralized agent dispatch rules and patterns
- `006-git-conventions.md` - Centralized git commit conventions with Beads integration
- Agent dispatch requirement in `/workflow-work` - specialized agents now required for implementation
- Hierarchical issue ID documentation with `--parent --force` pattern
- **Checkpoint step in `/workflow-work`** - explicit "one task per invocation" rule with mandatory commit

### Changed
- All internal file references now use `@path/to/file` syntax for Claude Code to read them
- DRY refactor: jq array warnings consolidated into single rules file
- DRY refactor: agent dispatch tables consolidated into single rules file
- Beads prefix enforcement: max 8 characters, validated during `/workflow-init`
- `/workflow-track` now creates hierarchical child IDs (e.g., `epic.1`, `epic.2`)
- `/workflow-start` emphasizes capturing epic ID for child issue creation

### Fixed
- jq "Cannot index array with string" errors - all `bd` commands return arrays `[{...}]`
- `/workflow-health` bug using `.issues` instead of array directly
- Missing `--force` flag with `--parent` causing "prefix mismatch" errors
- Random task IDs instead of sequential hierarchical IDs
- `/workflow-land` multi-line bash commands failing - added explicit `&&` chaining

## [0.1.0] - 2025-12-15

### Added
- Initial release of the Agentic Development Workflow
- 9 workflow slash commands:
  - `/workflow-init` - Initialize project for workflow
  - `/workflow-start` - Begin new feature with Beads epic
  - `/workflow-track` - Set up Beads tracking for planned work
  - `/workflow-execute` - Execute implementation plan with tracking
  - `/workflow-work` - Find and claim available work
  - `/workflow-land` - Complete work session properly
  - `/workflow-check` - Review project status
  - `/workflow-questions` - Track open questions
  - `/workflow-health` - Diagnose workflow issues
- Project rules and principles:
  - `001-project-principles.md` - Core principles and priority system
  - `002-open-questions-template.md` - Question tracking template
  - `003-multi-agent-coordination.md` - Multi-agent coordination guidelines
- Environment precheck library (`workflow-precheck.sh`)
- Comprehensive troubleshooting documentation
- Validation test document with pydo CLI example project
- Sandbox mode enabled by default for Claude Code compatibility
