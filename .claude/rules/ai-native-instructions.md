# AI-Native Instruction Design

**Purpose**: Guardrails for writing instructions that AI agents execute efficiently and correctly.

AI-native instructions state intent and outcomes. They replace procedural bash scripts with decision frameworks and observable success criteria, reducing tokens by 40-60% while improving reliability.

---

## Canonical Template

Every workflow instruction follows this 8-section structure:

### 1. Intent

State the purpose in one sentence. What does this accomplish?

### 2. When to Use

Define the trigger conditions. When should an agent execute this?

### 3. Context Required

List what the agent must know before executing:

- Files to read
- Commands to run first
- State to verify

### 4. Decision Framework

Provide decision logic as tables, not conditionals:

| Condition | Action | Reason      |
| --------- | ------ | ----------- |
| State A   | Do X   | Explanation |
| State B   | Do Y   | Explanation |

### 5. Execution

Describe the process at a high level. Avoid bash scripts:

- **Good**: "Create epic, save ID for tracking"
- **Bad**: `EPIC_ID=$(bd create "..." --json | jq -r '.id')`

### 6. Success Criteria

Define observable outcomes:

- What files exist?
- What commands return expected output?
- What state changed?

### 7. Edge Considerations

Document special cases, gotchas, recovery paths.

### 8. Reference Material

Preserve exact syntax, examples, error messages.

---

## Transformation Rules

### What Transforms

| Old Pattern           | New Pattern         | Reason                   |
| --------------------- | ------------------- | ------------------------ |
| Bash script           | High-level process  | AI infers implementation |
| If/else chains        | Decision tables     | Scannable, complete      |
| "Run this command"    | "Verify state X"    | Intent over procedure    |
| Multi-step procedures | Outcomes to achieve | Let AI sequence steps    |

### What Stays Unchanged

| Keep As-Is          | Why                   |
| ------------------- | --------------------- |
| `bd` command syntax | Reference material    |
| jq patterns         | Beads JSON gotchas    |
| Error messages      | Troubleshooting aid   |
| File paths          | Specific and concrete |
| Examples            | Demonstrate patterns  |

---

<anti_patterns_critical>

## Anti-Patterns

### ❌ Procedural Scripts

````markdown
**Bad:**

```bash
EPIC_ID=$(bd create "Feature" --json | jq -r '.id')
echo "Created: $EPIC_ID"
bd create "Task 1" --parent $EPIC_ID --force --json
```
````

````

**Why bad**: Agent must follow steps mechanically, cannot adapt.

### ❌ Nested Conditionals

```markdown
**Bad:**
If sandbox mode:
  If team mode:
    Run sync
  Else:
    Run flush-only
Else:
  Skip sync
````

**Why bad**: Hard to scan, error-prone parsing.

**Fix**: Use decision table.

### ❌ Implicit Context

```markdown
**Bad:**
"Update the issue with the result."
```

**Why bad**: Which issue? What result?

**Fix**: "Update issue [id] with test output status."

### ❌ Vague Success Criteria

```markdown
**Bad:**
"Ensure everything works."
```

**Why bad**: Not observable.

**Fix**: "Verify: `bd list --json` returns non-empty array."
</anti_patterns_critical>

---

## Execution Discipline

AI-native instructions describe outcomes. When gathering context:

| Anti-Pattern                         | Correct Pattern                     |
| ------------------------------------ | ----------------------------------- |
| Complex bash with jq conditionals    | Separate tool calls per query       |
| Retry same failed approach           | Switch approach after first failure |
| Inline command substitution `$(...)` | Store results, format in response   |
| Echo/printf for display              | Format output in response text      |

**Rule**: If a bash command fails, switch approaches immediately. Never retry similar syntax.

**Preferred**: Use `uv run python .claude/lib/workflow.py precheck --name [command]` for workflow state.

### Context Gathering Example

```bash
# WRONG - Complex bash that breaks in zsh
ACTIVE=$(bd list --status in_progress --json | jq -r 'if length == 0 then "None" else .[].title end')

# RIGHT - Separate queries, format in response
bd list --status in_progress --json
bd list --type epic --status open --json
# Then describe results in your response text
```

---

## Quality Checklist

Before merging instruction changes, verify:

- [ ] Intent stated in one sentence
- [ ] Trigger conditions explicit
- [ ] Context requirements listed
- [ ] Decision logic in tables (no if/else prose)
- [ ] Execution describes outcomes, not steps
- [ ] Success criteria observable
- [ ] Edge cases documented
- [ ] Reference material preserved
- [ ] Token count reduced 40-60% from bash version
- [ ] Active voice throughout
- [ ] No needless words
- [ ] Specific and concrete language

---

## Token Impact Guidance

### High Token Cost

| Pattern               | Tokens  | Alternative                |
| --------------------- | ------- | -------------------------- |
| Bash scripts          | 100-300 | Process description: 50-80 |
| If/else chains        | 80-150  | Decision table: 40-60      |
| Multi-step procedures | 200-400 | Outcomes list: 80-120      |

### Token Budget

| Section             | Target Tokens | Why             |
| ------------------- | ------------- | --------------- |
| Intent              | 10-20         | One sentence    |
| When to Use         | 20-40         | Trigger list    |
| Context Required    | 30-60         | File/state list |
| Decision Framework  | 60-120        | Tables compact  |
| Execution           | 80-150        | High-level only |
| Success Criteria    | 40-80         | Observable list |
| Edge Considerations | 60-120        | Gotchas only    |
| Reference Material  | Variable      | Keep complete   |

**Total target**: 300-600 tokens per instruction (excluding reference material)

---

## Example Transformation

### Before (Procedural)

```bash
# Initialize workflow
if [ ! -d ".beads" ]; then
  echo "Initializing Beads..."
  bd init -p myproj- --quiet
  if [ $? -ne 0 ]; then
    echo "Error: Failed to initialize"
    exit 1
  fi
fi

# Create epic
EPIC_ID=$(bd create "Feature name" -t epic -p 1 --json | jq -r '.id')
if [ -z "$EPIC_ID" ]; then
  echo "Error: Failed to create epic"
  exit 1
fi

echo "Epic created: $EPIC_ID"
echo "Save this ID for workflow-track"
```

**Tokens**: ~220

### After (AI-Native)

**Intent**: Initialize Beads tracking and create feature epic.

**When to Use**: Starting new feature work, no `.beads` directory exists.

**Context Required**:

- Verify `.beads/` existence
- Project prefix from `bd config` or initialize

**Decision Framework**:

| State            | Action                       | Outcome          |
| ---------------- | ---------------------------- | ---------------- |
| No `.beads/`     | Initialize with short prefix | Tracking enabled |
| `.beads/` exists | Skip initialization          | Use existing     |

**Execution**:

1. Initialize if needed (short prefix recommended)
2. Create epic (type: epic, priority: 1)
3. Return epic ID for tracking reference

**Success Criteria**:

- `.beads/beads.db` exists
- `bd list --type epic --json` returns new epic
- Epic ID available for child issues

**Edge Considerations**:

- Duplicate epic: Search `bd list --type epic` first
- Prefix requirements: See @.claude/rules/beads-patterns.md for format rules

**Reference Material**:

```bash
bd init -p myproj- --quiet
bd create "Feature name" -t epic -p 1 --json
# Returns: {"id": "myproj-abc", ...}
```

**Tokens**: ~280 (includes reference material)

---

## Related Files

- @.claude/rules/project-principles.md - Core development principles
- @.claude/rules/beads-patterns.md - Reference material (unchanged)
- @CLAUDE.md - Workflow instructions (transformation target)
