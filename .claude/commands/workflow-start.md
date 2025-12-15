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
# Create epic and capture the ID
EPIC_OUTPUT=$(bd $BD_FLAGS create "$FEATURE_DESC" --description="Feature epic: $FEATURE_DESC" -t epic -p 1 --json)
echo "$EPIC_OUTPUT"

# Extract epic ID for use in /workflow-track
EPIC_ID=$(echo "$EPIC_OUTPUT" | jq -r '.id')
echo ""
echo "=========================================="
echo "EPIC CREATED: $EPIC_ID"
echo "=========================================="
echo ""
echo "IMPORTANT: Save this epic ID for /workflow-track"
echo "You will need it to create child issues with hierarchical IDs"
```

**2. Verify Prefix**: Check the prefix is appropriate
```bash
# Verify prefix length
PREFIX=$(bd info --json 2>/dev/null | jq -r '.config.issue_prefix // empty')
if [ ${#PREFIX} -gt 8 ]; then
  echo ""
  echo "WARNING: Issue prefix '$PREFIX' exceeds 8 characters."
  echo "Consider running: bd rename-prefix <short>-"
  echo "Short prefixes create cleaner issue IDs."
fi
```

**3. Context Linking**: Optionally link to any planning documents or specifications
   - Note any related documentation in the epic description
   - Reference project specifications if available

**4. Hierarchy Setup**: The epic serves as parent for all feature work
   - All related tasks should use `--parent $EPIC_ID --force`
   - This creates hierarchical IDs like `pydo-abc.1`, `pydo-abc.2`

---

### Result

- A new Beads epic with ID (e.g., `pydo-abc`)
- Proper tracking hierarchy for the entire feature
- Foundation for breaking down work into child issues with `.1`, `.2` suffixes

<important_output>
**CRITICAL: Note the epic ID in the output!**

The epic ID (e.g., `pydo-abc`) is required for `/workflow-track` to create
child issues with hierarchical IDs. Without it, tasks get random independent IDs.

Example output:
```
{
  "id": "pydo-abc",
  "title": "Build pydo CLI",
  ...
}

==========================================
EPIC CREATED: pydo-abc
==========================================

IMPORTANT: Save this epic ID for /workflow-track
```

Use this ID when running `/workflow-track`:
- Pass to `--parent pydo-abc --force` for each child issue
- Results in clean IDs: `pydo-abc.1`, `pydo-abc.2`, `pydo-abc.3`
</important_output>

---

### Before Using This Command, Ensure

- Beads has been initialized with short prefix (`bd init -p <short>-`)
- You understand the project principles in @.claude/rules/001-project-principles.md
- You have a clear understanding of the feature scope

### After Using This Command, Continue With

1. **Save the epic ID** from the output (e.g., `pydo-abc`)
2. Create detailed implementation plan (using writing-plans skill)
3. Use `/workflow-track [plan-path]` to set up Beads tracking
   - Use the epic ID with `--parent $EPIC_ID --force` for hierarchical child IDs
4. Use `/workflow-execute` to execute the plan with tracking

### Recommended: Brainstorming Gate

For features touching more than 3 files, consider using the brainstorming skill first:
- Define the problem statement clearly
- Explore data models and dependencies
- Make technology decisions with rationale documented
- Create design document before implementation

### Troubleshooting

If epic creation fails, see [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting) for common solutions.

**If prefix is too long:**
```bash
bd rename-prefix <short>- --dry-run   # Preview
bd rename-prefix <short>-             # Apply
```

**Example usage:**
```
/workflow-start User authentication system

# Output includes:
# EPIC CREATED: auth-abc
# Save this ID for /workflow-track
```

This will create a Beads epic that properly tracks the entire feature with a clean, short ID.
