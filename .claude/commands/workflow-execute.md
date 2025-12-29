---
argument-hint: "[path/to/implementation/plan.md]"
description: Execute an implementation plan with Beads tracking integration
---

## Intent

Execute an implementation plan with integrated Beads tracking, delegating to the executing-plans skill.

## When to Use

- Implementation plan tracked and ready
- Ready to implement all tasks in sequence
- Want automated tracking and agent dispatch

## When NOT to Use

- No plan exists → use `/workflow-start` + brainstorming first
- Plan not tracked → use `/workflow-track` first
- Want manual task-by-task control → use `/workflow-work`
- Quick isolated task → use `/workflow-do`

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-execute
```

Verify before proceeding:

- Plan file exists and is readable
- Beads issues created (from `/workflow-track`)
- No conflicting in-progress work

## Decision Framework

| State              | Action                          | Outcome             |
| ------------------ | ------------------------------- | ------------------- |
| Plan file provided | Validate and parse              | Tasks identified    |
| No plan file       | Search `docs/plans/`, prompt    | Plan selected       |
| Plan not tracked   | Suggest `/workflow-track` first | Proper tracking     |
| Issues exist       | Invoke executing-plans skill    | Automated execution |
| Task in progress   | Resume or reset                 | Clean state         |

## Execution Flow

| Phase       | Action                       | Beads Integration      |
| ----------- | ---------------------------- | ---------------------- |
| 1. Analyze  | Parse plan, identify tasks   | Verify issues exist    |
| 2. Dispatch | Invoke executing-plans skill | Mark issue in_progress |
| 3. Execute  | Agent implements task (TDD)  | Track progress         |
| 4. Commit   | Git commit after each task   | Include issue ID       |
| 5. Close    | Complete task                | Mark issue closed      |
| 6. Repeat   | Next task                    | Until plan complete    |

## Skill Integration

This command delegates to `superpowers:executing-plans` with additional context:

| Instruction                     | Purpose                                |
| ------------------------------- | -------------------------------------- |
| Dispatch appropriate sub-agents | Domain expertise (python-expert, etc.) |
| Follow TDD workflow             | Quality assurance                      |
| Update Beads status             | Track progress                         |
| Create follow-up issues         | Capture discoveries                    |
| Commit after each task          | Version control                        |

## Agent Dispatch

**Dispatch to specialized agents.** Never implement code directly.

See @.claude/rules/agent-dispatch.md for agent selection.

## Success Criteria

- [ ] All plan tasks executed
- [ ] Each task has corresponding Beads issue
- [ ] All issues closed with completion notes
- [ ] Git commits for each task with issue IDs
- [ ] Follow-up issues created for discoveries

## Edge Considerations

- **Skill not available**: Fall back to manual `/workflow-work` execution
- **Execution interrupted**: State saved in Beads, resume with `/workflow-work`
- **Task fails**: Document failure, create follow-up issue, continue
- **Multi-agent coordination**: Follow rules in multi-agent-coordination.md

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-execute

# Check if issues exist for plan
bd list --json

# Check current work state
bd list --status in_progress --json

# Check blocked dependencies
bd blocked --json

# Mark task in progress (during execution)
bd update [id] --status in_progress --json

# Close task (after completion) - --suggest-next shows newly unblocked
bd close [id] --reason "[completion note]" --suggest-next --json

# Create follow-up issue
bd create "Discovered: [issue]" --deps discovered-from:[current-id] --json

# Commit after task (see git-conventions.md)
git add .
git commit -m "type(scope): [issue-id] description"
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/multi-agent-coordination.md - Multi-agent rules
- @.claude/rules/agent-dispatch.md - Agent selection
- @.claude/rules/git-conventions.md - Commit format
- @.claude/commands/workflow-track.md - Plan tracking
