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
source .claude/lib/workflow-precheck.sh
workflow_precheck "workflow-work"
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

### Process

**1. Ready Work Detection**: Find unblocked issues available for work
```bash
bd $BD_FLAGS ready --json
```

**2. Work Selection**: Review available work with context and priority
   - Examine issue descriptions and priorities
   - Check dependencies with `bd $BD_FLAGS dep tree [issue-id]`
   - Select the most appropriate issue to work on

**3. Status Update**: Claim the selected issue by updating to "in_progress"
```bash
bd $BD_FLAGS update [issue-id] --status in_progress --json
```

**4. Context Setup**: Review any related documentation or specifications
   - Check issue description for links to specs or plans
   - Review project context in CLAUDE.md and project rules

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
- Make regular git commits with references to issue IDs in commit messages

### Troubleshooting

**If `bd ready` returns no issues:**
```bash
# Check for blocked issues
bd $BD_FLAGS blocked

# View all open issues
bd $BD_FLAGS list --status open

# Check for stale issues that need attention
bd $BD_FLAGS stale --days 7
```

See [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting) for more solutions.

**Example usage:**
```
/workflow-work
# This will show you available work and guide you through claiming a task
```

This ensures proper coordination and tracking of all development work.
