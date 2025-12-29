---
argument-hint: "[research-id]"
description: Resolve research question and update blocked tasks with findings
---

## Intent

Resolve a research question, apply findings to blocked work, and update the epic's steering log.

## When to Use

- Research question answered
- Ready to apply findings to blocked tasks
- Research issue created via `/workflow-question-ask`

## When NOT to Use

- Research incomplete → continue research first
- No blocked tasks → close research issue directly
- Human course correction needed → use `/workflow-steer-correct`

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-steer-research
```

Gather before proceeding:

- Research issue ID and description (`bd show [research-id]`)
- Blocked task IDs (`bd dep tree [research-id]`)
- Epic ID (parent of blocked tasks)

## Decision Framework

| State                         | Action                  | Outcome           |
| ----------------------------- | ----------------------- | ----------------- |
| Research issue not found      | Error with guidance     | User corrects ID  |
| Research not open/in_progress | Warn, ask to continue   | User decides      |
| No blocked tasks              | Offer to close research | Clean closure     |
| Blocked tasks exist           | Show impact, confirm    | Apply findings    |
| Findings incomplete           | Continue research       | Defer application |
| User confirms                 | Dispatch writing-plans  | Coherent revision |

## Execution

1. Validate research issue exists and is open
2. Display research context from description
3. Conduct research (web search, docs, code analysis)
4. Capture findings summary (2-5 paragraphs)
5. Find blocked tasks (`bd dep tree`)
6. Show impact and confirm action plan
7. Gather epic context + all blocked task descriptions
8. Dispatch writing-plans skill for coherent revision
9. Update epic steering log with STEER entry
10. Apply revised descriptions to tasks (`--body-file`)
11. Remove blocking dependencies (`bd dep remove`)
12. Close research issue with resolution

## Success Criteria

- [ ] Research issue closed with documented findings
- [ ] All blocked tasks have revised descriptions
- [ ] Descriptions self-contained (no external references)
- [ ] Blocking dependencies removed
- [ ] Epic steering log updated with STEER entry
- [ ] Tasks appear in `bd ready` output

## Steering Log Entry (CRITICAL)

Every steering event MUST be logged in the epic description:

```markdown
### [YYYY-MM-DDTHH:MM:SSZ] STEER: Short Description

**Trigger:** Research issue [research-id]
**Decision:** What was decided
**Modified:** task-id-1, task-id-2
**Added:** task-id-3, task-id-4 (if any)
**Rationale:** Why this change was made
```

**Timestamp:** Use UTC (`date -u +"%Y-%m-%dT%H:%M:%SZ"`) for cross-timezone consistency.

## Self-Contained Descriptions (CRITICAL)

Each revised task description must be fully self-contained:

| Include           | Exclude                   |
| ----------------- | ------------------------- |
| All file paths    | "see above"               |
| All code examples | "see implementation plan" |
| All commands      | "as described earlier"    |
| Expected outcomes | External file references  |

## Edge Considerations

- **No blocked tasks**: Close research with documented findings; skip application
- **Circular dependencies**: Check with `bd dep cycles` after adding dependencies
- **Large revisions**: Use writing-plans skill for coherent multi-task updates
- **Incomplete findings**: Continue research before applying
- **User cancels**: Exit gracefully; research issue unchanged

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-steer-research

# Validate research issue
bd show $RESEARCH_ID --json | jq '.[0]'

# Find blocked tasks
bd dep tree $RESEARCH_ID

# Get epic context
bd show $EPIC_ID --json | jq '.[0].description'

# Get task context
bd show $TASK_ID --json | jq '.[0].description'

# Update task with revised description (MUST use --body-file)
cat > /tmp/task-update.md <<'EOF'
[revised description from writing-plans]
EOF
bd update $TASK_ID --body-file /tmp/task-update.md --json

# Remove blocking dependency
bd dep remove $TASK_ID $RESEARCH_ID

# Check for circular dependencies
bd dep cycles

# Update epic steering log (MUST use --body-file)
cat > /tmp/epic-update.md <<'EOF'
[full epic description with new STEER entry]
EOF
bd update $EPIC_ID --body-file /tmp/epic-update.md --json

# Close research issue
bd close $RESEARCH_ID --reason "Research complete. Findings applied to N task(s)." --json

# Check ready work (unblocked tasks should appear)
bd ready --json | jq -r '.[] | "[\(.id)] P\(.priority) \(.title)"'
```

## Workflow Integration

```
/workflow-question-ask "How should we implement auth?"
  └─> Creates research issue: pydo-r01
       └─> Blocks implementation task: pydo-abc.3

/workflow-steer-research pydo-r01
  ├─> Conduct research (web search, docs, code analysis)
  ├─> Gather epic context + all blocked task descriptions
  ├─> Dispatch writing-plans skill for coherent revision
  ├─> Update epic steering log with STEER entry
  ├─> Apply revised descriptions to affected tasks
  ├─> Remove blocking dependencies
  └─> Close pydo-r01

/workflow-work
  └─> pydo-abc.3 now appears in ready work (unblocked)
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - --body-file requirement
- @.claude/commands/workflow-question-ask.md - Create research questions
- @.claude/commands/workflow-overview.md - View steering log
