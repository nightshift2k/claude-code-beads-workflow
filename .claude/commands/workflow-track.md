---
argument-hint: [path/to/implementation-plan.md]
description: Set up Beads issue tracking for planned work with proper hierarchy
---

## `/workflow-track` - Set up Beads tracking for planned work

**Usage:** `/workflow-track [path/to/implementation-plan.md]`

Use this command when ready to track planned work in Beads issue system.

This command converts your implementation plan tasks into Beads issues with proper hierarchy and tracking.

### Argument

- `path/to/implementation-plan.md` - Path to the implementation plan document to track
- If not provided, will prompt to select from available plans in `docs/plans/`

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
source .claude/lib/workflow-precheck.sh
workflow_precheck "workflow-track"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

### Process

**1. Task Analysis**: Reads tasks from your implementation plan document

**2. Issue Creation**: Creates corresponding Beads issues with proper mapping:
   - Feature epic → Beads epic
   - Plan tasks → Beads child issues

**3. Dependency Setup**: Establishes proper dependencies based on the plan sequence

**4. Context Linking**: Links issues back to the original implementation plan

---

### Before Using This Command

- Ensure you have a completed implementation plan (from writing-plans skill)
- Verify that Beads has been initialized with `bd init --quiet`
- Have your project's issue priorities and types clear

### After Using This Command

- Use `/workflow-work` to begin implementation
- Issues will be available via `bd ready` for tracking

### Proper Issue Creation Template

```bash
bd $BD_FLAGS create "[Task from plan]" \
  --description="[Context from implementation plan] - From [path/to/implementation/plan.md]" \
  -t [task|epic|bug|feature] \
  -p [priority] \
  --deps discovered-from:[feature-epic] \
  --json
```

### Mapping Guidelines

- Implementation plan → Beads epic (e.g., bd-a1b2)
- Plan tasks → Beads child issues (e.g., bd-a1b2.1, bd-a1b2.2)
- See [001-project-principles.md](../.claude/rules/001-project-principles.md#priority_system) for priority guidelines
- Default to Priority 2 (Medium) for most tasks

### Troubleshooting

If issue creation fails, see [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting) for common solutions.

**Example workflow:**
```
/workflow-track
# This will guide you to convert each task in your implementation plan to Beads issues
```

This ensures that your implementation work is properly tracked during execution.
