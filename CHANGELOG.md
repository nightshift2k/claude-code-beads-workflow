# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
