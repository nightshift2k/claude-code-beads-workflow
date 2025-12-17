---
argument-hint: "[rough question]"
description: Interactive command for capturing research questions with full context
---

## `/workflow-question-ask` - Interactive research question capture

Use this command when you need to capture a research question with proper context and tracking.

This command provides an interactive flow to gather complete information about a question before creating a Beads research issue.

**Usage:** `/workflow-question-ask [rough question]`

Example: `/workflow-question-ask How should we handle database migrations?`

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
uv run python .claude/lib/workflow.py precheck --name workflow-question-ask
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

### Agent Instructions

This command follows an interactive flow to capture complete question context. **ASK ONE QUESTION AT A TIME** and wait for user response before proceeding.

**Step 1: Initial Question**

Start with the rough question provided by the user. Display:
```
Capturing research question: <ROUGH_QUESTION>
```

**Step 2: Clarifying Questions (ONE AT A TIME)**

**Q1:** "Why is this important? What triggered it?"

Wait for user response. Store as `CONTEXT`.

**Q2:** "What's the impact if this isn't resolved?"

Wait for user response. Store as `IMPACT`.

**Q3:** "Who should own this research? (default: Agent)"

Wait for user response. Store as `OWNER`. If empty, default to "Agent".

**Q4:** "When do you need this resolved by?"

Wait for user response. Store as `DUE_DATE`.

**Q5:** "Any initial thoughts or research directions?"

Wait for user response. Store as `RESEARCH_NOTES`.

**IMPORTANT:** Do NOT ask all questions at once. This is a conversational flow.

**Step 3: Identify Blocked Issues**

List potentially blocked issues:
```bash
uv run python .claude/lib/workflow.py list --status open --json
```

For each issue, ask: "Should this block [issue-id] - [title]? (Y/n/skip)"

Collect the issue IDs that user confirms should be blocked.

**Step 4: Assess Priority**

Based on impact and due date, determine priority:

| Impact | Due Date | Priority |
|--------|----------|----------|
| Blocking implementation | Immediate | P0 (Critical) |
| Significant delay risk | Within week | P1 (High) |
| Minor delay or nice-to-know | Later | P2 (Medium) |

See @.claude/rules/001-project-principles.md for full priority guidelines.

**Step 5: Present Summary for Confirmation**

Display the summary:
```
Question Summary (before saving to Beads)
─────────────────────────────────────────
Question: <the question>
Context: <why important>
Impact: <consequence if unresolved>
Owner: <who resolves>
Due: <deadline>
Priority: <P0/P1/P2 based on assessment>
Blocks: <list of issue IDs>
Initial Research: <notes>

Does this look correct? (Y/n/edit)
```

Wait for confirmation:
- If "Y": proceed to create issue
- If "n": cancel and exit
- If "edit": ask which field to edit and loop back

**Step 6: Create Beads Research Issue**

After confirmation, create the issue with full description:

**Description template:**
```markdown
**Question**: <the question>

**Context/Asks**: <why important, what triggered it>

**Impact**: <consequence if unresolved>

**Owner**: <who resolves>

**Due**: <deadline>

**Initial Research**:
<notes>
```

Create the issue (note: bd create is wrapped by Python tool, not direct call):
```bash
# The Python workflow tool doesn't support all bd create features yet
# Fall back to direct bd command for research issue creation:

bd --sandbox create "Research: <short description>" \
  --description="<full description from template>" \
  -t task -p <priority> \
  --json
```

Extract the created issue ID from the output (bd create returns object `{...}`).

**Step 7: Add Blocking Dependencies**

For each issue ID collected in Step 3:
```bash
bd --sandbox dep add <blocked-id> <research-id>
```

Display:
```
Created research issue: <research-id>
Blocking dependencies added: <count> task(s)
```

**Step 8: Summary**

Display completion summary:
```
✅ Research question captured

Issue: <research-id>
Blocks: <count> task(s)

Next steps:
1. Conduct research when ready
2. Use /workflow-steer-research <research-id> to apply findings
```

---

### Critical: All Data in Beads Issue

<question_storage_critical>
**No external markdown file needed**

All question data is stored directly in the Beads issue description. This ensures:
- Self-contained issues that don't depend on external files
- Easy access from `bd show [research-id]`
- Token-efficient - read only what you need
- No file sync issues across sessions

The old `/workflow-questions` command used an external markdown file. This new command stores everything in Beads.
</question_storage_critical>

---

### Blocking Dependencies

When research blocks existing work:
- Use `bd dep add [blocked-id] [research-id]` to establish dependency
- Blocked issues won't appear in ready work until research completes
- Track with `bd blocked` to see what's waiting on research

Example:
```bash
# Research issue created: test-r01
# It blocks implementation issue: test-abc

bd --sandbox dep add test-abc test-r01

# Now test-abc is blocked until test-r01 is resolved
uv run python .claude/lib/workflow.py list --blocked
# Shows: test-abc blocked by test-r01
```

---

### After Creating Research Issue

**Next steps:**
1. Research issue appears in ready work (if not blocked itself)
2. Claim with: `uv run python .claude/lib/workflow.py update [research-id] --status in_progress`
3. Document findings in issue notes: `uv run python .claude/lib/workflow.py update [research-id] --notes "Found: [discovery]"`
4. When complete, use `/workflow-steer-research [research-id]` to apply findings and unblock tasks

---

### Before Using This Command

- Understand what you need to research
- Consider if this truly needs tracking (use for non-trivial questions)
- Be ready to provide context about impact and urgency

### When to Use vs `/workflow-questions`

| Use `/workflow-question-ask` | Use old `/workflow-questions` |
|------------------------------|-------------------------------|
| Single question needing immediate tracking | Managing multiple existing questions |
| Interactive context gathering preferred | Batch question management |
| Self-contained Beads storage desired | External markdown file desired |
| NEW PROJECTS (recommended) | Legacy projects with existing questions.md |

---

### Troubleshooting

**If issue creation fails:**
```bash
# Check existing research issues
uv run python .claude/lib/workflow.py list --json
# Filter for issues with "Research:" in title
```

See @CLAUDE.md for comprehensive troubleshooting, or run `/workflow-health` for full diagnostics.

**Common issues:**
| Error | Cause | Solution |
|-------|-------|----------|
| "Cannot index object" | Using `.[0]` on `bd create` | Use `.id` instead (create returns object) |
| "Cannot index array" | Using `.id` on `bd list/show` | Use `.[0].id` (list/show return arrays) |
| Missing dependencies | Forgot to add blocking deps | Use `bd dep add [blocked] [research]` |
| Research not in ready | Has unresolved deps | Check with `bd dep tree [research-id]` |

See @.claude/rules/004-beads-json-patterns.md for Beads JSON patterns.

---

### Example Usage

**Scenario:** Unsure about authentication approach

```
/workflow-question-ask How should we implement user authentication?

# Agent asks (ONE AT A TIME):
# "Why is this important? What triggered it?"
# User: "Building user system, need to decide between JWT and sessions"

# "What's the impact if this isn't resolved?"
# User: "Can't implement login until we decide"

# "Who should own this research?"
# User: "Agent can research"

# "When do you need this resolved by?"
# User: "Within 2 days"

# "Any initial thoughts or research directions?"
# User: "Check industry best practices for SaaS apps"

# Agent shows open issues:
# [pydo-abc.3] Implement user login
# Should this block pydo-abc.3? Y

# Agent presents summary:
# Question Summary
# ─────────────────────────────────────────
# Question: How should we implement user authentication?
# Context: Building user system, need to decide between JWT and sessions
# Impact: Can't implement login until we decide
# Owner: Agent
# Due: 2024-12-17 (2 days)
# Priority: P0 (blocks implementation)
# Blocks: pydo-abc.3
# Initial Research: Check industry best practices for SaaS apps
#
# Does this look correct? Y

# Agent creates issue and sets dependency:
# bd create "Research: User authentication approach" ...
# Created: pydo-r01
# bd dep add pydo-abc.3 pydo-r01
# Dependency added: pydo-abc.3 blocked by pydo-r01
```

This ensures research questions are properly captured with full context and blocking relationships.

---

### Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/commands/workflow-steer-research.md - Resolve research and unblock tasks
- @.claude/rules/001-project-principles.md - Priority guidelines
- @.claude/rules/004-beads-json-patterns.md - Correct jq patterns for Beads JSON
