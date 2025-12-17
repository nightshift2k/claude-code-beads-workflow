---
argument-hint:
description: Find and claim available work from Beads issue tracking system
---

## `/workflow-work` - Find and claim available work

Use this command when ready to start working on tracked issues.

This command helps you find and properly claim work from the Beads issue tracking system.

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
workflow_precheck "workflow-work"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

**⚠️ Beads JSON:** All `bd` commands return arrays. See @.claude/rules/004-beads-json-patterns.md for correct jq usage.

### Process

**1. Ready Work Detection**: Find unblocked issues available for work
```bash
# Get all ready issues
bd  ready --json

# Parse with jq (note: returns array)
bd  ready --json | jq -r '.[] | "[\(.id)] P\(.priority) \(.title)"'
```

**2. Work Selection**: Review available work with context and priority
   - Examine issue descriptions and priorities
   - Check dependencies with `bd  dep tree [issue-id]`
   - Select the most appropriate issue to work on

**3. Status Update**: Claim the selected issue by updating to "in_progress"
```bash
# Update status (note: use .[0] for single result)
bd  update [issue-id] --status in_progress --json | jq -r '.[0] | "\(.id) now \(.status)"'
```

**4. Context Setup**: Review any related documentation or specifications
   - Check issue description for links to specs or plans
   - Review project context in @CLAUDE.md and project rules

**5. Execute with Specialized Agent**: Dispatch to appropriate agent
   - Read the full issue description with `bd  show [issue-id]`
   - **⚠️ Never implement directly** - dispatch via @.claude/rules/005-agent-dispatch.md

<task_checkpoint_critical>
**6. Checkpoint (CRITICAL)**: After task completion, STOP and return control to human

```bash
# 1. Commit changes (REQUIRED before closing)
git add .
git commit -m "type(scope): [issue-id] description"

# 2. Close the issue
bd  close [issue-id] --reason "Completed: [summary]" --json

# 3. STOP HERE - Do NOT continue to next task
```

**⚠️ ONE TASK PER INVOCATION**
- Human must run `/workflow-work` again for next task
- Or run `/workflow-land` to complete session
- Never automatically chain to next task

See @.claude/rules/006-git-conventions.md for commit message format.
</task_checkpoint_critical>

---

### Before Using This Command

- Ensure Beads database is synchronized (`bd sync`)
- Review any work in progress to avoid conflicts
- Verify your development environment is ready

### Best Practices

- Always use `bd ready` to find work instead of manually selecting issues
- Update your status to `in_progress` immediately when beginning work
- Include detailed descriptions when creating related issues from discoveries
- Use `--deps discovered-from:[current-issue-id]` when creating new issues during work

### During Work, Remember

- Create Beads issues for any discovered problems or tasks
- Keep issue descriptions detailed for future context
- Use appropriate priorities based on project guidelines
- Follow @.claude/rules/006-git-conventions.md for all commits

### Troubleshooting

**If `bd ready` returns no issues:**
```bash
# Check for blocked issues
bd  blocked

# View all open issues
bd  list --status open

# Check for stale issues that need attention
bd  stale --days 7
```

**If issues are blocked by research questions:**
- Use `/workflow-steer-research` to resolve research and unblock tasks

**If AI has diverged during implementation:**
- Use `/workflow-steer-correct` to create course correction task

See @CLAUDE.md for troubleshooting solutions.

**Example usage:**
```
/workflow-work
# This will show you available work and guide you through claiming a task
```

This ensures proper coordination and tracking of all development work.
