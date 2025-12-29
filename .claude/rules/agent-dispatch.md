# Agent Dispatch Rules

<agent_dispatch_critical>

## Critical: Always Dispatch Implementation Work

**NEVER implement code directly in the main conversation.** Always dispatch to specialized agents.

This ensures:

- Domain expertise drives implementation
- Code quality stays consistent
- Testing practices follow TDD
- Concerns remain separated
  </agent_dispatch_critical>

## Agent Selection

| Task Domain   | Agent                | Use For                                  |
| ------------- | -------------------- | ---------------------------------------- |
| Python        | `python-expert`      | Python code, pytest, CLI tools, pip/uv   |
| Go            | `golang-expert`      | Go implementations, testing              |
| TypeScript/JS | `frontend-architect` | Frontend, React/Vue, Node.js             |
| API Design    | `api-designer`       | REST/GraphQL endpoints                   |
| DevOps        | `devops-architect`   | CI/CD, infrastructure                    |
| Security      | `security-engineer`  | Auth, validation, vulnerabilities        |
| Backend       | `backend-architect`  | Server architecture, database, systems   |
| Refactoring   | `refactoring-expert` | Cleanup, restructure, tech debt          |
| Quality       | `quality-engineer`   | Testing strategies, edge cases, coverage |
| Documentation | `technical-writer`   | Technical docs, API docs, guides         |
| Debugging     | `root-cause-analyst` | Complex bugs, systematic investigation   |
| General       | `general-purpose`    | Research, multi-step exploration         |

> **Note:** Agent list is evolving. Check Task tool documentation for current available agents.

<agent_label_convention>

## Agent Label Convention

Beads issues can include an `agent:*` label to indicate which sub-agent should handle the work.

**Label format:** `agent:<agent-type>` (e.g., `agent:python-expert`)

**Dispatch Decision Framework:**

| Issue State                     | Action                             |
| ------------------------------- | ---------------------------------- |
| Has `agent:*` label             | Dispatch to labeled agent type     |
| No label, file types recognized | Use Auto-Detection Framework below |
| No label, keywords recognized   | Use Auto-Detection Framework below |
| No signals                      | Default to `general-purpose`       |

**When labels are assigned:**

- workflow-track auto-detects from file types and keywords
- Manual assignment via `--label agent:X` flag
- AI inference during issue creation

### Auto-Detection Framework

| Label                      | File Signals         | Keyword Signals                 |
| -------------------------- | -------------------- | ------------------------------- |
| `agent:python-expert`      | `.py`                | pytest, pip, uv, CLI            |
| `agent:golang-expert`      | `.go`                | Go modules, go test             |
| `agent:frontend-architect` | `.tsx`, `.vue`       | React, Vue, component           |
| `agent:backend-architect`  | -                    | server, database, system        |
| `agent:api-designer`       | -                    | API, endpoint, REST, GraphQL    |
| `agent:security-engineer`  | -                    | auth, validation, secrets       |
| `agent:devops-architect`   | `.yml`, `Dockerfile` | CI/CD, deploy, Docker           |
| `agent:refactoring-expert` | -                    | cleanup, restructure, tech debt |
| `agent:quality-engineer`   | `*_test.*`, `test_*` | coverage, edge case, QA         |
| `agent:technical-writer`   | `.md`, `.rst`        | documentation, README, guide    |
| `agent:root-cause-analyst` | -                    | debug, investigate, diagnose    |
| `agent:general-purpose`    | -                    | unclear scope, research         |

**Labels are hints, not mandates.** Override if the task clearly needs different expertise than labeled.
</agent_label_convention>

## Dispatch Pattern

Use the Task tool to dispatch work:

```
Use the Task tool with subagent_type="[agent-type]":

"Implement the following task from Beads issue [issue-id]:

[Full issue description from bd show output]

Requirements:
- Follow TDD: write test first, run to fail, implement, run to pass
- Update Beads status when complete: bd close [issue-id] --reason '[completion note]'
- Create follow-up issues for discoveries: bd create '[title]' --deps discovered-from:[issue-id]"
```

## Multi-Agent Coordination

When tasks require multiple agents:

- **Sequential only** - never dispatch multiple agents to the same file
- Complete one agent's work before starting the next on shared files
- See @.claude/rules/multi-agent-coordination.md for detailed rules

## When NOT to Dispatch

Some tasks need no specialized agent:

- Simple file reads/searches (use Glob, Grep, Read directly)
- Beads status updates (run bd commands directly)
- Git operations (run git commands directly)
- Quick documentation lookups

**Rule**: If the task involves writing or modifying code, dispatch to an agent.

## Agent Failure Recovery

| Failure Type         | Recovery Action                              |
| -------------------- | -------------------------------------------- |
| Agent unavailable    | Use `general-purpose` as fallback            |
| Agent times out      | Split task into smaller pieces, retry        |
| Agent returns error  | Check issue description clarity, add context |
| Wrong agent selected | Re-dispatch to correct agent type            |
| Partial completion   | Create follow-up issue for remaining work    |

**Recovery process:**

1. Document failure in issue notes: `bd update [id] --notes "Agent failure: [reason]"`
2. Adjust approach based on failure type
3. Re-dispatch or escalate to human

---

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/multi-agent-coordination.md - Multi-agent coordination rules
- @.claude/commands/workflow-work.md - Task execution workflow
- @.claude/commands/workflow-execute.md - Plan execution workflow
