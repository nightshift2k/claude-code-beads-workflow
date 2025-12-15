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

**IMPORTANT:** Do NOT specify a custom ID or prefix when creating issues. Beads automatically generates IDs using the project directory name as the prefix. Specifying a custom prefix will cause a "prefix mismatch" error.

**EFFICIENCY:** When creating multiple tasks from a plan, use batch mode to create all issues in a single command. This is faster and reduces API calls.

```bash
# BATCH MODE (recommended) - create multiple issues at once
bd $BD_FLAGS create "Task 1: Project Setup" -t task -p 2 --parent [epic-id] --json && \
bd $BD_FLAGS create "Task 2: Exceptions Module" -t task -p 2 --parent [epic-id] --json && \
bd $BD_FLAGS create "Task 3: Task Model" -t task -p 2 --parent [epic-id] --json
# ... continue for all tasks

# SINGLE MODE (slower) - only use for individual tasks
bd $BD_FLAGS create "[Task from plan]" \
  --description="[Context from implementation plan]" \
  -t [task|epic|bug|feature] \
  -p [priority] \
  --json
```

For child issues under an epic, use the `--parent` flag with the epic's auto-generated ID:
```bash
bd $BD_FLAGS create "[Child task]" --parent [epic-id] -t task -p 2 --json
```

### Mapping Guidelines

- Implementation plan → Beads epic (auto-generated ID like `project-name-abc`)
- Plan tasks → Beads child issues (auto-generated like `project-name-abc.1`, `project-name-abc.2`)
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
