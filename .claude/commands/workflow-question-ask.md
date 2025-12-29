---
argument-hint: "[rough question]"
description: Interactive command for capturing research questions with full context
---

## Intent

Capture a research question with full context and blocking relationships through interactive dialogue.

## When to Use

- Track a non-trivial research question
- Question blocks implementation work
- Full context needed for future reference
- Research spans multiple sessions or requires external investigation

## When NOT to Use

- Simple question with quick answer → answer it directly
- Findings already exist → use `/workflow-steer-research`
- Does not block work → consider regular task instead

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-question-ask
```

## Interactive Flow (CRITICAL)

**Ask ONE question at a time. Wait for response before proceeding.**

| Step | Question                                         | Captures       |
| ---- | ------------------------------------------------ | -------------- |
| 1    | "Why is this important? What triggered it?"      | Context        |
| 2    | "What's the impact if this isn't resolved?"      | Impact         |
| 3    | "Who should own this research? (default: Agent)" | Owner          |
| 4    | "When do you need this resolved by?"             | Due date       |
| 5    | "Any initial thoughts or research directions?"   | Research notes |

After gathering answers, present summary for confirmation before creating issue.

## Priority Assessment

| Impact                      | Timeline    | Priority     |
| --------------------------- | ----------- | ------------ |
| Blocking implementation     | Immediate   | 0 (Critical) |
| Significant delay risk      | Within week | 1 (High)     |
| Minor delay or nice-to-know | Later       | 2 (Medium)   |

## Decision Framework

| State                        | Action                        | Outcome          |
| ---------------------------- | ----------------------------- | ---------------- |
| User provides rough question | Start interactive flow        | Context gathered |
| All questions answered       | Show summary for confirmation | User validates   |
| User confirms                | Create Beads issue            | Research tracked |
| User says "edit"             | Ask which field to change     | Loop back        |
| User says "n"                | Cancel                        | No issue created |
| Open issues exist            | Ask which should be blocked   | Dependencies set |

## Execution

1. Display rough question, start interactive flow
2. Ask clarifying questions ONE AT A TIME
3. List open issues, ask which this blocks
4. Assess priority from impact + timeline
5. Present summary for confirmation (Y/n/edit)
6. Create Beads issue with full description (use `--body-file`)
7. Add blocking dependencies
8. Display completion summary with next steps

## Blocking Dependencies

After creating the research issue, establish blocking relationships to affected tasks:

```bash
# List open issues to identify which tasks are blocked by this research
bd list --status open --type task --json | jq -r '.[] | "[\(.id)] \(.title)"'

# Add dependency: task is blocked BY research issue
bd dep add <blocked-task-id> <research-issue-id>

# Example: If task "api-xyz.2" needs research from "api-abc" to proceed
bd dep add api-xyz.2 api-abc
```

**Purpose**: Marking dependencies when a task cannot proceed ensures:

- Task shows as "blocked" in `bd ready` output
- Research issue appears in dependency visualizations (`bd graph`, `bd dep tree`)
- Audit trail links work to its blocking research

**When to establish dependencies**:

- Task awaits this research decision
- Feature requires research completion before implementation
- Research affects multiple tasks (add dependency for each)

**Multiple blockers**: If a task is blocked by multiple research issues, add each:

```bash
bd dep add myproj-def.3 research-issue-1
bd dep add myproj-def.3 research-issue-2
```

## Success Criteria

- [ ] All context captured (question, context, impact, owner, due, notes)
- [ ] User confirmed summary
- [ ] Beads issue created with complete description
- [ ] Blocking dependencies added for affected issues
- [ ] Next steps displayed

## All Data in Beads Issue (CRITICAL)

No external markdown file needed. The Beads issue description stores all question data:

| Benefit          | Why                                     |
| ---------------- | --------------------------------------- |
| Self-contained   | No external file dependencies           |
| Token-efficient  | Read only what you need with `bd show`  |
| Session-portable | Works across sessions without file sync |

## Summary Template

```
Question Summary (before saving to Beads)
─────────────────────────────────────────
Question: [the question]
Context: [why important]
Impact: [consequence if unresolved]
Owner: [who resolves]
Due: [deadline]
Priority: [0-4; text labels P0-P4 also work]
Blocks: [list of issue IDs]
Initial Research: [notes]

Does this look correct? (Y/n/edit)
```

## Edge Considerations

- **No blocking issues**: Skip dependency step; create issue only
- **User cancels mid-flow**: Exit gracefully; create nothing
- **Research blocks research**: Valid scenario; use `bd dep add`
- **bd create returns object**: Use `.id` not `.[0].id`

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-question-ask

# List open issues to check for blocking
bd list --status open --json

# Write description to temp file (REQUIRED for complex content)
cat > /tmp/research-issue.md <<'EOF'
**Question**: [the question]

**Context/Asks**: [why important]

**Impact**: [consequence if unresolved]

**Owner**: [who resolves]

**Due**: [deadline]

**Initial Research**:
[notes]
EOF

# Create issue with --body-file (safe for all content)
bd create "Research: [short description]" --body-file /tmp/research-issue.md -t task -p 1 --json
# Returns: {"id": "prefix-xxx", ...}
# Extract: jq -r '.id'

# Add blocking dependencies
bd dep add [blocked-id] [research-id]

# Check blocked issues
bd blocked --json
```

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - bd create returns object
- @.claude/rules/project-principles.md - Priority guidelines
- @.claude/commands/workflow-steer-research.md - Resolve research questions
- @.claude/commands/workflow-work.md - Find available work
