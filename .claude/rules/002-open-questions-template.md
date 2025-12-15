# Open Questions & Research Items

This document tracks questions that need further investigation or decisions that need to be made.

## Critical (P0 - Must be resolved before implementation)

### [Question ID: Q001] 
**Question**: [What is the specific question?]
**Asks**: [Who asked this or why it's important]
**Status**: [Open | In Research | Resolved | Deferred]
**Owner**: [Person responsible for resolving]
**Due**: [Date when resolution is needed]
**Impact**: [What happens if this isn't resolved?]

**Research Notes**:
- [Note 1]
- [Note 2]

**Resolution**: [To be filled when resolved]

### [Question ID: Q002]
**Question**: [What is the specific question?]
**Asks**: [Who asked this or why it's important]
**Status**: [Open | In Research | Resolved | Deferred]
**Owner**: [Person responsible for resolving]
**Due**: [Date when resolution is needed]
**Impact**: [What happens if this isn't resolved?]

**Research Notes**:
- [Note 1]
- [Note 2]

**Resolution**: [To be filled when resolved]

## High Priority (P1 - Should be resolved soon)

### [Question ID: Q003]
**Question**: [What is the specific question?]
**Asks**: [Who asked this or why it's important]
**Status**: [Open | In Research | Resolved | Deferred]
**Owner**: [Person responsible for resolving]
**Due**: [Date when resolution is needed]
**Impact**: [What happens if this isn't resolved?]

**Research Notes**:
- [Note 1]
- [Note 2]

**Resolution**: [To be filled when resolved]

## Medium Priority (P2 - Good to resolve eventually)

### [Question ID: Q004]
**Question**: [What is the specific question?]
**Asks**: [Who asked this or why it's important]
**Status**: [Open | In Research | Resolved | Deferred]
**Owner**: [Person responsible for resolving]
**Due**: [Date when resolution is needed]
**Impact**: [What happens if this isn't resolved?]

**Research Notes**:
- [Note 1]
- [Note 2]

**Resolution**: [To be filled when resolved]

## How to Use This Document

1. **Add New Questions**: When you encounter uncertainty, create a new entry above
2. **Update Status**: Move questions through the priority tiers as needed
3. **Assign Owners**: Make sure every question has someone responsible for resolving it
4. **Track Research**: Document your research findings to avoid duplicate work
5. **Link to Beads**: Create Beads issues for research tasks and link back to questions
6. **Close Resolved**: Update the "Resolution" field when questions are answered

## Relationship to Beads Tracking

Each open research question should have a corresponding Beads issue:
- Use `bd create` to create tracking issues for research
- Use issue description to link to entries in this file
- Use `--deps discovered-from` to trace research back to original needs
- Use issue status to reflect the question status

Example Beads creation:
```bash
bd create "Research: Q001 - Database scaling approach" \
  --description="Research different approaches for database scaling. See @.claude/rules/002-open-questions-template.md#Q001" \
  -t task -p 1 \
  --json
```

---

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/commands/workflow-questions.md - Question tracking workflow
- @.claude/rules/001-project-principles.md - Priority system