# Multi-Agent Coordination Guidelines

Rules for coordinating multiple AI agents on the same codebase. These prevent conflicts, data loss, and merge issues.

<critical_rule>

## Critical Rule: Sequential File Operations

**NEVER dispatch multiple agents to modify the same file in parallel.**

Parallel file edits cause merge conflicts, lost work, and corrupted state. When two agents edit the same file simultaneously:

- Git conflicts result
- One agent loses work
- Recovery requires manual intervention
- Session state corrupts

### What to Do Instead

1. **Sequential Operations**: When multiple tasks touch the same file, execute them sequentially
2. **Agent-Specific Branches**: Create separate branches for each agent's work
3. **File Locking**: Claim files by updating a coordination issue before editing
   </critical_rule>

## Parallel Agent Patterns

### Safe: Different Files

```
Agent A: src/auth/login.go
Agent B: src/api/users.go
Agent C: tests/auth_test.go
```

These can run in parallel safely.

### Unsafe: Same File

```
Agent A: src/auth/login.go (adding feature)
Agent B: src/auth/login.go (fixing bug)
```

These MUST run sequentially.

### Unsafe: Shared Dependencies

```
Agent A: src/models/user.go (adding field)
Agent B: src/api/users.go (using same model)
```

These SHOULD run sequentially to avoid interface mismatches.

## Multi-Agent Session Setup

### Multi-Agent Session Decision Framework

| Pattern             | When to Use                            | Setup                             |
| ------------------- | -------------------------------------- | --------------------------------- |
| Separate prefixes   | Independent work, minimal coordination | Each agent uses unique prefix     |
| Separate branches   | Feature isolation, code review         | Each agent on dedicated branch    |
| Coordinator pattern | Complex dependencies, shared state     | One coordinator, multiple workers |

### Reference Commands

#### Option 1: Separate Beads Prefixes (Recommended)

Each agent uses a unique issue prefix to avoid ID collisions:

```bash
# Agent A
bd create "Feature A" --prefix "agent-a-"

# Agent B
bd create "Feature B" --prefix "agent-b-"
```

#### Option 2: Agent-Specific Branches

Each agent works on a dedicated branch:

```bash
# Agent A
git checkout -b agent-a/feature-auth
# All Beads operations scoped to this branch

# Agent B
git checkout -b agent-b/feature-api
# All Beads operations scoped to this branch
```

#### Option 3: Coordinator Pattern

One agent acts as coordinator:

1. Coordinator breaks down work into non-overlapping tasks
2. Coordinator assigns tasks to worker agents
3. Worker agents report back to coordinator
4. Coordinator manages merging and conflict resolution

## File Coordination Protocol

### File Coordination Decision Framework

| Before Modifying  | Check                                | Action if Conflict                  |
| ----------------- | ------------------------------------ | ----------------------------------- |
| Any file          | In-progress issues on same file?     | Wait or coordinate with other agent |
| Shared dependency | Other agent working on related code? | Sequential execution required       |
| New file          | None                                 | Proceed with claim and update       |

### File Coordination Process

| Phase         | Outcome                       |
| ------------- | ----------------------------- |
| Check locks   | Identify any conflicting work |
| Claim file    | Update issue with file list   |
| Execute work  | Modify file as needed         |
| Release claim | Close issue with outcome      |

### File Claim Convention

**Convention:** Use `--notes` to record file claims. Format: `FILES: path1, path2, ...`

```bash
# Claim files when starting work
bd update [issue-id] --notes "FILES: src/auth.py, src/login.py" --json

# Check for conflicts (search notes for file mentions)
bd list --status in_progress --json | jq -r '.[].notes // ""' | grep -i "target/file"

# Release on completion
bd close [issue-id] --reason "Completed changes" --json
```

**Note:** This convention relies on agent cooperation; Beads does not enforce it.

## Conflict Resolution Workflow

### Conflict Resolution Decision Framework

| Conflict Type              | Resolution Strategy                                              | Outcome                      |
| -------------------------- | ---------------------------------------------------------------- | ---------------------------- |
| Beads JSONL                | Use `bd merge` tool                                              | Merged issue state           |
| Code (complete vs partial) | Prefer most complete implementation                              | Single authoritative version |
| Code (both necessary)      | Manual merge with testing                                        | Combined implementation      |
| Circular dependencies      | Visualize with `bd graph [issue-id]`, break with `bd dep remove` | Resolved dependency chain    |

### Resolution Process

| Phase                     | Success Indicator                |
| ------------------------- | -------------------------------- |
| Identify conflict source  | Know which files/issues affected |
| Apply resolution strategy | Changes merged or selected       |
| Validate result           | Tests pass, no regressions       |
| Document in Beads         | Conflict recorded for audit      |

### Reference Commands

```bash
# Identify conflict source
git status
git diff --name-only --diff-filter=U

# Beads JSONL conflicts
bd merge merged.jsonl base.jsonl ours.jsonl theirs.jsonl

# Visualize circular dependencies (requires issue-id)
bd graph [issue-id]
bd dep cycles

# Document resolution
bd create "Resolved merge conflict" --description="Merged Agent A and Agent B changes to [file]" -t task --json
bd close [id] --reason "Conflict resolved" --json
```

## Session Scope Limits

### One Phase Per Session Rule

Prevent context overload and maintain quality:

- **DO**: Complete one implementation phase per session
- **DO**: Complete one feature epic per session
- **AVOID**: Combining planning with implementation in one session
- **AVOID**: Starting new features before landing current work

### Session Scope Checklist

Before starting a session, verify:

- [ ] Clear, single objective defined
- [ ] No more than one feature/phase in scope
- [ ] All dependencies identified upfront
- [ ] Exit criteria defined

### Signs You Should Land the Session

Indicators that a session has grown too long:

- **Re-reading earlier context** - Scrolling back to remember decisions
- **Repeated clarification** - Asking questions you asked before
- **Scope creep** - Adding "just one more thing" repeatedly
- **Error accumulation** - Small mistakes piling up
- **Context confusion** - Mixing up file purposes

When you notice these signs:

1. Stop current task at a clean checkpoint
2. Run `/workflow-land` to save state
3. Start fresh session with `/workflow-work`

## Decision Documentation

### Record WHY, Not Just WHAT

Every significant decision must include rationale:

**Bad:**

```
Use DuckDB for analytics.
```

**Good:**

```
Decision: Use DuckDB for analytics
Rationale:
- Embedded database (no external dependencies)
- Excellent performance for analytical queries
- Parquet file support for data exchange
- Considered alternatives: SQLite (slower analytics), PostgreSQL (requires server)
```

### Where to Document Decisions

1. **In Beads issues**: Use `--notes` to add decision context
2. **In design documents**: `docs/plans/` for architectural decisions
3. **In code comments**: Only for non-obvious implementation choices
4. **In @CLAUDE.md**: For project-wide patterns and conventions

## Gotchas-First Research Pattern

Before implementing against external APIs or unfamiliar systems:

1. **Check existing gotchas**: Review @CLAUDE.md and project docs
2. **Explore before implementing**: Run exploratory queries/calls
3. **Document discoveries**: Add new gotchas immediately
4. **Persist for future sessions**: Ensure context survives

### Gotchas Documentation Format

````markdown
## Gotchas - [System Name]

### [Short Description]

**Discovered:** [Date]
**Impact:** [What breaks if ignored]
**Solution:** [How to handle correctly]
**Example:**

```code
// Correct approach
```
````

```

<brainstorming_gate_critical>
## Brainstorming Gate

### When to Require Brainstorming

**Brainstorm before coding** when:
- Feature touches more than 3 files
- Multiple valid implementation approaches exist
- Requirements or acceptance criteria remain unclear
- Significant architectural decisions arise
- External API or system integration required

### Brainstorming Checklist

Before coding, ensure you have:
- [ ] Clear problem statement
- [ ] Data model understanding
- [ ] Technology decisions with rationale
- [ ] Edge cases identified
- [ ] Design document created (for >3 file features)

### Using the Brainstorming Skill

```

# Before implementation

/superpowers:brainstorm [feature description]

# Results in:

# - Refined requirements

# - Design document in docs/plans/

# - Clear implementation path

```
</brainstorming_gate_critical>

## Summary of Multi-Agent Rules

**Note:** Verification rules are defined in @.claude/rules/project-principles.md under "Verification Before Completion".

| Rule | Description | Priority |
|------|-------------|----------|
| Sequential same-file | Never parallel edit same file | CRITICAL |
| Session scope | One phase/feature per session | HIGH |
| Decision context | Document WHY not just WHAT | HIGH |
| Brainstorming gate | Brainstorm before >3 file features | HIGH |
| Gotchas-first | Research before implementing | HIGH |
| Verification | Run tests before completion | CRITICAL |

---

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/project-principles.md - Project principles and quality gates
- @.claude/rules/agent-dispatch.md - Agent selection and dispatch patterns
- @.claude/rules/git-conventions.md - Commit timing and conventions
- @.claude/commands/workflow-work.md - Task execution workflow
- @.claude/commands/workflow-land.md - Session completion workflow
```
