---
argument-hint:
description: Track and resolve open questions systematically
---

## `/workflow-questions` - Track and resolve open questions

Use this command when needing to record or address open questions.

This command systematically tracks questions that need research or decisions.

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
source .claude/lib/workflow-precheck.sh
workflow_precheck "workflow-questions"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

### Process

**1. Record Questions**: Add to `.claude/rules/002-open-questions-template.md` with proper categorization

**2. Create Tracking Issues**: Create corresponding Beads issues for research tasks

**3. Assign Priorities**: Categorize questions by criticality (P0-P2)

**4. Track Resolution**: Monitor and update question status

---

### For New Questions

**Step 1:** Add to `.claude/rules/002-open-questions-template.md` with template:
```markdown
### [Question ID: QXXX]
**Question**: [What is the specific question?]
**Asks**: [Who asked this or why it's important]
**Status**: Open
**Owner**: [Person responsible for resolving]
**Due**: [Date when resolution is needed]
**Impact**: [What happens if this isn't resolved?]
```

**Step 2:** Create Beads issue to track research:
```bash
bd $BD_FLAGS create "Research: QXXX - [Question Topic]" \
  --description="Research to resolve question in .claude/rules/002-open-questions-template.md#QXXX. [Include specific research needs]" \
  -t task -p [appropriate priority] \
  --json
```

### For Resolving Questions

1. Update research Beads issue with findings
2. Close the Beads issue when research complete:
   ```bash
   bd $BD_FLAGS close [issue-id] --reason "Research complete: [summary]" --json
   ```
3. Update `.claude/rules/002-open-questions-template.md` with resolution
4. Mark question status as "Resolved"

### Question Prioritization

- **P0 (Critical)**: Must be resolved before implementation can proceed
- **P1 (High)**: Should be resolved soon to avoid delays
- **P2 (Medium)**: Good to resolve eventually

### Best Practices

- Always link Beads issues to entries in `.claude/rules/002-open-questions-template.md`
- Use `--deps discovered-from` to trace research back to original needs
- Update question status when research is complete
- Close Beads research issues when questions are answered

### Troubleshooting

If question tracking fails, see [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting) for common solutions.

**Example usage:**
```
/workflow-questions
# This will guide you through the process of recording a new question or addressing existing ones
```

This ensures that open questions don't become forgotten blockers.
