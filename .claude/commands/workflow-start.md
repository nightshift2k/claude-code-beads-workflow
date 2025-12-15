---
argument-hint: "[feature-description]"
description: Begin a new feature with Beads epic creation
---

## `/workflow-start` - Begin a new feature

Use this command when starting a new feature or capability.

This command creates a Beads epic to track the entire feature lifecycle.

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
source .claude/lib/workflow-precheck.sh
workflow_precheck "workflow-start"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

### Validate Feature Description

```bash
FEATURE_DESC="$1"

if [ -z "$FEATURE_DESC" ]; then
  echo "ERROR: Usage: /workflow-start [feature-description]"
  echo ""
  echo "   Example: /workflow-start User authentication system"
  exit 1
fi

echo "Starting new feature: $FEATURE_DESC"
echo ""
```

---

### Process

**1. Epic Creation**: Create a feature epic in Beads
```bash
bd $BD_FLAGS create "$FEATURE_DESC" --description="Feature epic: $FEATURE_DESC" -t epic -p 2 --json
```

**2. Context Linking**: Optionally link to any planning documents or specifications
   - Note any related documentation in the epic description
   - Reference project specifications if available

**3. Hierarchy Setup**: The epic serves as parent for all feature work
   - All related tasks should use `--deps discovered-from:[epic-id]`

---

### Result

- A new Beads epic that serves as the parent for all feature work
- Proper tracking hierarchy for the entire feature
- Foundation for breaking down work into sub-issues

### Before Using This Command, Ensure

- Beads has been initialized with `bd init --quiet`
- You understand the project principles in @.claude/rules/001-project-principles.md
- You have a clear understanding of the feature scope

### After Using This Command, Continue With

1. Create detailed implementation plan (using writing-plans skill)
2. Use `/workflow-track` to set up Beads tracking for the planned work
3. Use `/workflow-execute` to execute the plan with tracking

### Recommended: Brainstorming Gate

For features touching more than 3 files, consider using the brainstorming skill first:
- Define the problem statement clearly
- Explore data models and dependencies
- Make technology decisions with rationale documented
- Create design document before implementation

### Troubleshooting

If epic creation fails, see [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting) for common solutions.

**Example usage:**
```
/workflow-start User authentication system
```

This will create a Beads epic that properly tracks the entire feature.
