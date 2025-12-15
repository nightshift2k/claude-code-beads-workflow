---
argument-hint: "[path/to/implementation/plan.md]"
description: Execute an implementation plan with Beads tracking integration
---

## `/workflow-execute` - Execute implementation plan with Beads tracking

Use this command to execute an implementation plan with integrated Beads issue tracking.

This command acts as a wrapper for the executing-plans skill, ensuring proper tracking and coordination.

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
source .claude/lib/workflow-precheck.sh
workflow_precheck "workflow-execute"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

### Setup Interruption Handler

Set up cleanup trap to handle unexpected interruptions:
```bash
trap 'workflow_cleanup "workflow-execute"' EXIT INT TERM
```

### Validate Plan File Argument

```bash
PLAN_FILE="$1"

if [ -z "$PLAN_FILE" ]; then
  echo "ERROR: Usage: /workflow-execute [path/to/implementation/plan.md]"
  echo ""
  echo "   Example: /workflow-execute docs/plans/user-auth-plan.md"
  echo ""
  echo "   Looking for existing plans..."
  find . -name "*plan*.md" -type f -not -path "*/node_modules/*" -not -path "*/.git/*" | head -5
  exit 1
fi

if [ ! -f "$PLAN_FILE" ]; then
  echo "ERROR: Plan file not found: $PLAN_FILE"
  echo ""
  echo "   Searching for implementation plans..."
  find . -name "*plan*.md" -type f -not -path "*/node_modules/*" -not -path "*/.git/*" | head -5
  exit 1
fi

echo "Executing plan: $PLAN_FILE"
echo ""
```

---

**⚠️ Beads JSON:** All `bd` commands return arrays. See @.claude/rules/004-beads-json-patterns.md for correct jq usage.

### Process

**1. Plan Analysis**: Read the implementation plan file and identify individual tasks
   - Parse the plan markdown for task sections
   - Identify dependencies between tasks
   - Estimate scope and complexity

**2. Issue Sync**: Ensure Beads issues exist for tracking (via `/workflow-track` if not already done)
```bash
# Check if issues already exist for this plan
bd $BD_FLAGS list --json | grep -q "$PLAN_FILE" || echo "Consider running /workflow-track first"
```

**3. Invoke Executing-Plans Skill**: Use the superpowers skill for quality execution
```
Use the superpowers:executing-plans skill to execute the plan at: $PLAN_FILE

Additional instructions for execution:
- Dispatch appropriate sub-agents for specialized tasks (e.g., python-expert for Python)
- Follow TDD workflow: write test, run to fail, implement, run to pass
- Update Beads issue status as you progress through each task
- Create follow-up issues for any discoveries during implementation
```

**4. Beads Integration During Execution**: For each task in the plan:
   - Mark issue as in_progress: `bd $BD_FLAGS update [id] --status in_progress`
   - Execute the task using appropriate domain-specific agent
   - Create follow-up issues for discoveries: `bd $BD_FLAGS create "Discovered: [issue]" --deps discovered-from:[current-id]`
   - Mark issue as closed: `bd $BD_FLAGS close [id] --reason "[completion note]"`

**5. Version Control**: Ensure proper Git integration during execution
   - Commit after each major task completion
   - Reference issue IDs in commit messages

---

### Agent Dispatch

**⚠️ Agent Dispatch:** Never implement code directly. See @.claude/rules/005-agent-dispatch.md for agent selection and dispatch patterns.

For multi-agent coordination rules, see @.claude/rules/003-multi-agent-coordination.md

---

### Before Using This Command

- Ensure you have a completed implementation plan file (from writing-plans skill)
- Verify Beads has been initialized with `bd init --quiet`
- Confirm all project-specific rules in CLAUDE.md/AGENTS.md

### Execution Flow

- The command will parse your plan and create Beads issues for each major task
- Issues will be marked `in_progress` as they're executed
- Completed tasks will be marked `closed` with completion notes
- Dependencies will be properly managed based on plan sequence
- If interrupted, cleanup trap will save state and attempt sync

### Troubleshooting

If execution encounters issues:
- Use `bd $BD_FLAGS list --status in_progress` to see current work state
- Check `bd $BD_FLAGS blocked` for dependency issues
- See [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting) for common solutions

**Example usage:**
```
/workflow-execute path/to/implementation/plan.md
```

This ensures your implementation work is properly tracked while maintaining the detailed execution approach from your executing-plans skill.
