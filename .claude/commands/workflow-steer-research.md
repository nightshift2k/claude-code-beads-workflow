---
argument-hint: "[research-id]"
description: Resolve research question and update blocked tasks with findings
---

## `/workflow-steer-research` - Resolve research question

Use this command when ready to resolve a research question and apply findings to blocked work.

This command integrates with `/workflow-question-ask` which creates research issues with full context stored in Beads.

**Usage:** `/workflow-steer-research [research-id]`

Example: `/workflow-steer-research pydo-r01`

### Environment Validation

**FIRST:** Run environment precheck before proceeding:
```bash
uv run python _claude/lib/workflow.py precheck --name workflow-steer-research
```

If precheck fails, follow the guidance to resolve environment issues before continuing.

---

### Agent Instructions

This command guides you through resolving a research question and applying findings. Follow these steps:

**1. Validate Research Issue Exists**

Get the research issue details:
```bash
uv run python _claude/lib/workflow.py show $RESEARCH_ID --json
```

Extract:
- Research title
- Research description (contains full context)
- Current status

If status is not "open" or "in_progress", warn the user and ask if they want to continue.

**2. Load Research Context**

Display the research context from the description:
```
Research Context:
────────────────────────────────────────
<description content>
```

This shows the full context captured during `/workflow-question-ask`.

**3. Execute Research**

Guide the research process with this prompt:
```
⏺ Research Phase

Based on the context above, please conduct research to answer this question.

Consider:
  - Web search for current best practices
  - Code analysis of existing patterns in the codebase
  - Official documentation for frameworks/libraries involved
  - Security and performance implications

When ready, provide your findings summary below.
```

*At this point, conduct research using available tools (WebSearch, Tavily, Code analysis, Context7, etc.) and return findings.*

**4. Capture Findings**

After research, capture findings:
```
Research Findings Summary:
────────────────────────────────────────

<Provide a concise summary of findings (2-5 paragraphs)>
```

Store the findings summary for later use.

**5. Find Blocked Tasks**

Find tasks blocked by this research issue:
```bash
uv run python _claude/lib/workflow.py find-affected $RESEARCH_ID --json
```

Count the blocked tasks. If zero:
```
No tasks are blocked by this research.

Close research issue anyway? (Y/n):
```

If user confirms, skip to step 10 (close research).

If blocked tasks exist, show impact:
```bash
uv run python _claude/lib/workflow.py find-affected $RESEARCH_ID
```
This displays a formatted impact table.

**6. Show Impact and Confirm**

Present the action plan:
```
Proposed action:
  1. Update <count> blocked task(s) with findings
  2. Add findings to task descriptions
  3. Remove blocking dependency (unblock tasks)
  4. Close research issue

Apply findings to blocked tasks? (Y/n):
```

Wait for confirmation. If not confirmed, exit with manual mode message.

**7. Gather Context for Plan Revision**

Extract the epic ID from the first blocked task (e.g., `pydo-abc.5` → `pydo-abc`):
```bash
# Get first task ID, extract epic portion before the dot
```

Get epic details for big picture context:
```bash
uv run python _claude/lib/workflow.py show $EPIC_ID --json
```

Extract:
- Epic title
- Epic description

For each blocked task, gather:
```bash
uv run python _claude/lib/workflow.py show $TASK_ID --json
```

Extract:
- Task title
- Task description (full implementation plan fragment)

Collect all task contexts into a structured format:
```
### <TASK_ID>: <TASK_TITLE>

<TASK_DESCRIPTION>

---
```

**8. Dispatch writing-plans Skill for Coherent Revision**

Use the writing-plans skill to revise implementation plans with findings:

```
Use the writing-plans skill to revise these implementation plan fragments.
Integrate the research findings into the relevant steps of each task.

EPIC CONTEXT:
<EPIC_TITLE>
<EPIC_DESCRIPTION>

RESEARCH FINDINGS:
<FINDINGS_SUMMARY>

AFFECTED TASKS TO REVISE:
<TASK_CONTEXTS>

INSTRUCTIONS:
1. For each task, integrate the research findings into the relevant implementation steps
2. Maintain the existing structure (step numbers, format)
3. Update specific steps where findings apply (don't just append)
4. Keep tasks coherent with each other (consistent approach across all)
5. Return ONLY the revised task descriptions, clearly labeled by task ID

Output format:
=== TASK_ID ===
[revised description]
=== END ===
```

*Dispatch writing-plans skill and receive revised descriptions.*

**9. Apply Revised Descriptions**

For each blocked task:
1. Extract the revised description from writing-plans output for that task
2. Update the task with the revised description:
```bash
uv run python _claude/lib/workflow.py update $TASK_ID --description="<revised_description>"
```

3. Remove the blocking dependency:
```bash
bd --sandbox dep remove $TASK_ID $RESEARCH_ID
```

Display progress as you update each task.

**10. Close Research Issue**

Close the research issue with resolution:
```bash
uv run python _claude/lib/workflow.py close $RESEARCH_ID "Research complete. Findings applied to <count> blocked task(s)."
```

**11. Display Summary**

Show completion summary:
```
✅ Steering complete
──────────────────────────────────
Updated:  <count> tasks
```

Display affected tasks that are now unblocked:
```bash
uv run python _claude/lib/workflow.py ready
```

---

### Before Using This Command

- Research issue must exist (created via `/workflow-question-ask`)
- Research context should be complete in issue description
- Understand which tasks are blocked by this research

### After Using This Command

- Research issue will be closed
- Blocked tasks will have **revised implementation plans** with findings integrated
- Plans are revised as a coherent unit (consistent across all affected tasks)
- Blocking dependencies will be removed
- Tasks will appear in ready work and can be claimed

### Workflow Integration

```
/workflow-question-ask "How should we implement auth?"
  └─> Creates research issue: pydo-r01
       └─> Blocks implementation task: pydo-abc.3

/workflow-steer-research pydo-r01
  ├─> Conduct research (web search, docs, code analysis)
  ├─> Gather epic context + all blocked task descriptions
  ├─> Dispatch writing-plans skill for coherent revision
  ├─> Apply revised descriptions to affected tasks
  ├─> Remove blocking dependencies
  └─> Close pydo-r01

/workflow-work
  └─> pydo-abc.3 now appears in ready work (unblocked)
```

### Troubleshooting

**If research issue not found:**
```bash
# List all research issues
uv run python _claude/lib/workflow.py list --json
# Filter for issues with "Research:" in title
```

**If no blocked tasks:**
- Research may have been exploratory (no blockers)
- Close research issue with findings documented
- Findings can still inform future work

**If findings are incomplete:**
- Continue research before applying
- Add additional notes to research issue
- Re-run command when ready

See @CLAUDE.md for comprehensive troubleshooting.

---

### Related Files

- @.claude/commands/workflow-question-ask.md - Creates research issues
- @CLAUDE.md - Main workflow instructions
- @.claude/rules/004-beads-json-patterns.md - Beads JSON patterns