# Agent Dispatch Rules

<agent_dispatch_critical>
## Critical: Always Dispatch Implementation Work

**NEVER implement code directly in the main conversation.** Always dispatch to specialized agents.

This ensures:
- Domain expertise applied to implementation
- Consistent code quality
- Proper testing practices (TDD)
- Clean separation of concerns
</agent_dispatch_critical>

## Agent Selection

| Task Domain | Agent | Use For |
|-------------|-------|---------|
| Python | `python-expert` | Python code, pytest, CLI tools, pip/uv |
| Go | `golang-expert` | Go implementations, testing |
| TypeScript/JS | `frontend-architect` | Frontend, React/Vue, Node.js |
| API Design | `api-designer` | REST/GraphQL endpoints |
| DevOps | `devops-architect` | CI/CD, infrastructure |
| Security | `security-engineer` | Auth, validation, vulnerabilities |
| General | `general-purpose` | Research, multi-step exploration |

## Dispatch Pattern

Use the Task tool to dispatch work:

```
Use the Task tool with subagent_type="[agent-type]":

"Implement the following task from Beads issue [issue-id]:

[Full issue description from bd show output]

Requirements:
- Follow TDD: write test first, run to fail, implement, run to pass
- Update Beads status when complete: bd --sandbox close [issue-id] --reason '[completion note]'
- Create follow-up issues for discoveries: bd --sandbox create '[title]' --deps discovered-from:[issue-id]"
```

## Multi-Agent Coordination

When tasks require multiple agents:
- **Sequential only** - never dispatch multiple agents to the same file
- Complete one agent's work before starting the next on shared files
- See @.claude/rules/003-multi-agent-coordination.md for detailed rules

## When NOT to Dispatch

Some tasks don't require specialized agents:
- Simple file reads/searches (use Glob, Grep, Read directly)
- Beads status updates (run bd commands directly)
- Git operations (run git commands directly)
- Quick documentation lookups

**Rule of thumb:** If the task involves writing or modifying code, dispatch to an agent.

---

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/003-multi-agent-coordination.md - Multi-agent coordination rules
- @.claude/commands/workflow-work.md - Task execution workflow
- @.claude/commands/workflow-execute.md - Plan execution workflow
