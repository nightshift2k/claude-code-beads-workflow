# Project Constitution

Foundational principles and guidelines governing all development in this project.

<core_principles>

## Core Principles

### 1. Specification-First Development

- Base all implementation on approved specifications
- Define clear requirements and acceptance criteria before coding
- Treat specifications as the source of truth

### 2. Issue Tracking for All Work

- Track all development tasks in Beads
- Create issues before starting work
- Manage dependencies through Beads relationships

### 3. Quality and Testing

- Write tests before implementation
- Include appropriate test coverage for all features
- Maintain code quality standards

### 4. Documentation and Audit Trail

- Document all significant decisions
- Link specifications, implementations, and issues
- Keep comprehensive audit trail for changes

### 5. AI-Native Instruction Design

- State intent and outcomes, not procedural steps
- Provide decision frameworks using tables, not conditionals
- Maintain observable success criteria
- See @.claude/rules/ai-native-instructions.md for detailed guidelines
  </core_principles>

## Technical Guidelines

### Architecture

- Choose simple solutions over complex ones
- Trust framework defaults unless proven inadequate
- Use standard patterns; avoid unnecessary abstractions

### Implementation

- Write code for humans first, machines second
- Apply consistent coding standards across the codebase
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

### Multi-Agent Coordination

See @.claude/rules/multi-agent-coordination.md for detailed rules:

- **NEVER** edit same file from parallel agents
- Use sequential operations for overlapping work
- **Brainstorming gate**: Features touching >3 files require design first
- Document decision rationale (WHY, not just WHAT)
- Research gotchas before implementing against external APIs

### Code Review

- Review all changes before merging
- Verify specifications match implementation
- Confirm issue tracking completeness
  </workflow_requirements>

## Decision-Making Framework

### When to Create New Issues

- When discovering work during implementation
- When identifying technical debt
- When encountering blockers or problems

<priority_system>

### Priority Assignment

| Priority | Label    | Use For                            | Examples                                     |
| -------- | -------- | ---------------------------------- | -------------------------------------------- |
| 0        | Critical | Security, data loss, broken builds | CVE patches, production outages, CI failures |
| 1        | High     | Major features, important bugs     | Core functionality, user-blocking issues     |
| 2        | Medium   | Standard feature work (default)    | Most development tasks                       |
| 3        | Low      | Polish, optimization               | UX improvements, performance tweaks          |
| 4        | Backlog  | Future ideas, research             | Exploratory work, nice-to-haves              |

**Format Note:** Use numeric format in bash commands (`bd create -p 0`), while documentation and discussions use text labels (`P0`, `P1`, etc.) for readability.
</priority_system>

<quality_gates>

## Quality Gates

Before completing any feature:

- Close all Beads issues
- Implement all specifications as planned
- Pass all tests
- Meet code quality metrics
- Update documentation

**Note:** Define specific quality metrics (coverage thresholds, linting rules, acceptable warnings) per-project in CLAUDE.md.
</quality_gates>

<verification_rules_critical>

## Verification Before Completion

### Mandatory Checks

Before marking any task complete:

- [ ] `make test` or equivalent passes
- [ ] `make lint` or equivalent passes
- [ ] No regressions introduced
- [ ] Edge cases handled
- [ ] Documentation updated if needed

### Never Skip Verification

"I think it works" is not verification. Run the actual commands and confirm output before claiming completion.
</verification_rules_critical>

---

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - AI-native instruction design
- @.claude/rules/multi-agent-coordination.md - Multi-agent coordination rules
- @.claude/rules/git-conventions.md - Git commit conventions
- @.claude/commands/workflow-init.md - Project initialization
- @.claude/commands/workflow-start.md - Feature creation workflow
