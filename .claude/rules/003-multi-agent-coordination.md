# Multi-Agent Coordination Guidelines

This document establishes rules for coordinating multiple AI agents working on the same codebase to prevent conflicts, data loss, and merge issues.

<critical_rule>
## Critical Rule: Sequential File Operations

**NEVER dispatch multiple agents to modify the same file in parallel.**

This is the most common source of merge conflicts, lost work, and corrupted state. If two agents edit the same file simultaneously:
- Git conflicts are guaranteed
- One agent's work will be lost
- Recovery requires manual intervention
- Session state becomes corrupted

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

### Option 1: Separate Beads Prefixes (Recommended)

Each agent uses a unique issue prefix to avoid ID collisions:
```bash
# Agent A
bd create "Feature A" --prefix "agent-a-"

# Agent B
bd create "Feature B" --prefix "agent-b-"
```

### Option 2: Agent-Specific Branches

Each agent works on a dedicated branch:
```bash
# Agent A
git checkout -b agent-a/feature-auth
# All Beads operations scoped to this branch

# Agent B
git checkout -b agent-b/feature-api
# All Beads operations scoped to this branch
```

### Option 3: Coordinator Pattern

One agent acts as coordinator:
1. Coordinator breaks down work into non-overlapping tasks
2. Coordinator assigns tasks to worker agents
3. Worker agents report back to coordinator
4. Coordinator manages merging and conflict resolution

## File Coordination Protocol

Before modifying a file in multi-agent context:

1. **Check for locks**: Search for any in-progress issues touching the same file
   ```bash
   bd list --status in_progress --json | jq '.[] | select(.files // [] | contains(["target/file.go"]))'
   ```

2. **Claim the file**: Create or update issue with file list
   ```bash
   bd update [issue-id] --note "Claiming: target/file.go" --json
   ```

3. **Complete and release**: Mark complete when done
   ```bash
   bd close [issue-id] --reason "Completed: target/file.go changes" --json
   ```

## Conflict Resolution Workflow

When conflicts occur despite coordination:

1. **Identify the conflict source**
   ```bash
   git status
   git diff --name-only --diff-filter=U
   ```

2. **For Beads JSONL conflicts**
   ```bash
   bd merge merged.jsonl base.jsonl ours.jsonl theirs.jsonl
   ```

3. **For code conflicts**
   - Prefer the most complete implementation
   - Manually merge if both contain necessary changes
   - Test merged result before committing

4. **Document in Beads**
   ```bash
   bd create "Resolved merge conflict" --description="Merged Agent A and Agent B changes to [file]" -t task --json
   bd close [id] --reason "Conflict resolved" --json
   ```

## Session Scope Limits

### One Phase Per Session Rule

To prevent context overload and maintain quality:
- **DO**: Complete one implementation phase per session
- **DO**: Complete one feature epic per session
- **DON'T**: Combine planning with implementation in one session
- **DON'T**: Start a new feature before landing current work

### Session Scope Checklist

Before starting a session, verify:
- [ ] Clear, single objective defined
- [ ] No more than one feature/phase in scope
- [ ] All dependencies identified upfront
- [ ] Exit criteria defined

### Signs You Should Land the Session

Context-based indicators that a session is getting too long:

- **Re-reading earlier context** - If you're scrolling back to remember what was decided
- **Repeated clarification** - Asking the same questions you asked before
- **Scope creep** - Adding "just one more thing" repeatedly
- **Error accumulation** - Small mistakes piling up
- **Context confusion** - Mixing up which file does what

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

1. **In Beads issues**: Use `--note` to add decision context
2. **In design documents**: `docs/plans/` for architectural decisions
3. **In code comments**: Only for non-obvious implementation choices
4. **In CLAUDE.md**: For project-wide patterns and conventions

## Gotchas-First Research Pattern

Before implementing against external APIs or unfamiliar systems:

1. **Check existing gotchas**: Review CLAUDE.md and project docs
2. **Explore before implementing**: Use exploratory queries/calls
3. **Document discoveries**: Add new gotchas immediately
4. **Update for future sessions**: Ensure context persists

### Gotchas Documentation Format

```markdown
## Gotchas - [System Name]

### [Short Description]
**Discovered:** [Date]
**Impact:** [What breaks if ignored]
**Solution:** [How to handle correctly]
**Example:**
```code
// Correct approach
```
```

<brainstorming_gate>
## Brainstorming Gate

### When to Require Brainstorming

**Mandatory brainstorming** before coding when:
- Feature touches more than 3 files
- Multiple valid implementation approaches exist
- Unclear requirements or acceptance criteria
- Significant architectural decisions needed
- External API or system integration

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
</brainstorming_gate>

<verification_rules>
## Verification Before Completion

### Mandatory Checks

Before marking any task complete:
- [ ] `make test` or equivalent passes
- [ ] `make lint` or equivalent passes
- [ ] No regressions introduced
- [ ] Edge cases handled
- [ ] Documentation updated if needed

### Never Skip Verification

"I think it works" is not verification. Run the actual commands and confirm output before claiming completion.
</verification_rules>

## Summary of Multi-Agent Rules

| Rule | Description | Priority |
|------|-------------|----------|
| Sequential same-file | Never parallel edit same file | CRITICAL |
| Session scope | One phase/feature per session | HIGH |
| Decision context | Document WHY not just WHAT | HIGH |
| Brainstorming gate | Brainstorm before >3 file features | HIGH |
| Gotchas-first | Research before implementing | HIGH |
| Verification | Run tests before completion | CRITICAL |
