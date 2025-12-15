---
argument-hint: "[path/to/questions.md]"
description: Track and resolve open questions systematically
---

## `/workflow-questions` - Track and resolve open questions

Use this command when needing to record or address open questions.

This command systematically tracks questions that need research or decisions.

**Usage:** `/workflow-questions [path/to/questions.md]`

Example: `/workflow-questions docs/open-questions.md`

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
source @.claude/lib/workflow-precheck.sh
workflow_precheck "workflow-questions"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

### Validate Questions File Path

```bash
QUESTIONS_FILE="$1"

if [ -z "$QUESTIONS_FILE" ]; then
  echo "ERROR: Usage: /workflow-questions [path/to/questions.md]"
  echo ""
  echo "   Example: /workflow-questions docs/open-questions.md"
  echo ""
  echo "   To create a new questions file from template:"
  echo "   cp @.claude/lib/open-questions-template.md docs/open-questions.md"
  echo "   # Then remove the warning header block from your copy"
  exit 1
fi

if [ ! -f "$QUESTIONS_FILE" ]; then
  echo "ERROR: Questions file not found at: $QUESTIONS_FILE"
  echo ""
  echo "To create a new questions file from template:"
  echo "   cp @.claude/lib/open-questions-template.md $QUESTIONS_FILE"
  echo "   # Then remove the warning header block from your copy"
  exit 1
fi

# Check if user forgot to remove the template warning header
if grep -q "TEMPLATE FILE - Do not edit directly" "$QUESTIONS_FILE"; then
  echo "WARNING: This appears to be the template file with the warning header still present."
  echo ""
  echo "Please remove the header block (lines 1-18) from $QUESTIONS_FILE before using."
  echo "The header is surrounded by <!-- --> comment markers."
  exit 1
fi

echo "Using questions file: $QUESTIONS_FILE"
```

---

### Process

**1. Record Questions**: Add new questions to your questions file

**2. Create Tracking Issues**: Create corresponding Beads issues for research tasks

**3. Assign Priorities**: Categorize questions by criticality (P0-P2)

**4. Track Resolution**: Monitor and update question status

---

### For New Questions

**Step 1:** Add to your questions file with template:
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
  --description="Research to resolve question in $QUESTIONS_FILE#QXXX. [Include specific research needs]" \
  -t task -p [appropriate priority] \
  --json
```

### For Resolving Questions

1. Update research Beads issue with findings
2. Close the Beads issue when research complete:
   ```bash
   bd $BD_FLAGS close [issue-id] --reason "Research complete: [summary]" --json
   ```
3. Update `$QUESTIONS_FILE` with resolution
4. Mark question status as "Resolved"

### Question Prioritization

- **P0 (Critical)**: Must be resolved before implementation can proceed
- **P1 (High)**: Should be resolved soon to avoid delays
- **P2 (Medium)**: Good to resolve eventually

### Best Practices

- Always link Beads issues to entries in your questions file
- Use `--deps discovered-from` to trace research back to original needs
- Update question status when research is complete
- Close Beads research issues when questions are answered

### Troubleshooting

**If question tracking fails:**
```bash
# Run quick diagnostics
source @.claude/lib/workflow-precheck.sh && workflow_quick_diagnose "questions"

# Check existing research issues
bd $BD_FLAGS list --json | jq -r '.[] | select(.title | contains("Research:")) | "[\(.id)] \(.title)"'
```

See @CLAUDE.md for comprehensive troubleshooting, or run `/workflow-health` for full diagnostics.

**Example usage:**
```
/workflow-questions docs/open-questions.md
# This will guide you through the process of recording a new question or addressing existing ones
```

This ensures that open questions don't become forgotten blockers.
