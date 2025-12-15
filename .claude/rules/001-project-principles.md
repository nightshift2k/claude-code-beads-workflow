# Project Constitution

This document contains the foundational principles and guidelines that govern all development activities in this project.

<core_principles>
## Core Principles

### 1. Specification-First Development
- All implementation must be based on approved specifications
- No coding without clear requirements and acceptance criteria
- Specifications serve as the source of truth for implementation

### 2. Issue Tracking for All Work
- All development tasks must be tracked in Beads
- No work performed without corresponding issue tracking
- Proper dependency management through Beads relationships

### 3. Quality and Testing
- Test-first development approach
- All features must include appropriate test coverage
- Code quality standards must be maintained

### 4. Documentation and Audit Trail
- All significant decisions must be documented
- Maintain clear links between specifications, implementations, and issues
- Keep comprehensive audit trail for all changes
</core_principles>

## Technical Guidelines

### Architecture
- Prefer simple solutions over complex ones
- Trust framework defaults unless there's a proven need to diverge
- Use standard patterns and avoid unnecessary abstractions

### Implementation
- Write code for humans first, machines second
- Maintain consistent coding standards across the codebase
- Prioritize readability and maintainability

<workflow_requirements>
## Workflow Requirements

### Session Management
- **One phase per session**: Complete one feature/phase before starting another
- **Environment validation**: All workflow commands validate environment first
- **Proper session closure**: Always use `/workflow-land` before stopping

### Daily Development
- Check for ready work using `bd ready` before starting
- Update issue status when beginning and completing work
- Use `/workflow-land` to properly complete sessions
- Run `/workflow-health` when encountering issues

### Brainstorming Gate
For features touching more than 3 files:
- Complete brainstorming before implementation
- Document design decisions with rationale
- Create design document in `docs/plans/`

### Multi-Agent Coordination
See `.claude/rules/003-multi-agent-coordination.md` for detailed rules:
- **NEVER** edit same file from parallel agents
- Use sequential operations for overlapping work
- Document decision rationale (WHY, not just WHAT)
- Research gotchas before implementing against external APIs

### Code Review
- All changes must be reviewed before merging
- Ensure specifications are properly implemented
- Verify issue tracking completeness
</workflow_requirements>

## Decision-Making Framework

### When to Create New Issues
- When discovering work during implementation
- When identifying technical debt
- When encountering blockers or problems

<priority_system>
### Priority Assignment

| Priority | Label | Use For | Examples |
|----------|-------|---------|----------|
| 0 | Critical | Security, data loss, broken builds | CVE patches, production outages, CI failures |
| 1 | High | Major features, important bugs | Core functionality, user-blocking issues |
| 2 | Medium | Standard feature work (default) | Most development tasks |
| 3 | Low | Polish, optimization | UX improvements, performance tweaks |
| 4 | Backlog | Future ideas, research | Exploratory work, nice-to-haves |
</priority_system>

<quality_gates>
## Quality Gates

Before any feature completion:
- All Beads issues must be properly closed
- All specifications must be implemented as planned
- Tests must pass
- Code quality metrics must be met
- Documentation must be updated
</quality_gates>