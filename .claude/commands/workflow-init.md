---
argument-hint:
description: Initialize project for agentic workflow with Beads tracking
---

## `/workflow-init` - Initialize project for agentic workflow

Use this command to set up a new project for agentic development workflow with Beads tracking.

This command validates the environment and initializes all required components.

### Process

**1. Validate Environment**: Check all prerequisites
```bash
source .claude/lib/workflow-precheck.sh

echo "Checking workflow prerequisites..."
echo ""

# Check bd CLI
if ! command -v bd &> /dev/null; then
  echo "ERROR: bd CLI not found"
  echo ""
  echo "Installation options:"
  echo "1. Go: go install github.com/steveyegge/beads/cmd/bd@latest"
  echo "2. Homebrew (macOS): brew install steveyegge/tap/beads"
  echo ""
  exit 1
fi

BD_VERSION=$(bd version 2>&1 | grep -oE 'v?[0-9]+\.[0-9]+\.[0-9]+' | head -1)
echo "bd CLI: $BD_VERSION"

# Check git
if ! command -v git &> /dev/null; then
  echo "ERROR: git not found"
  exit 1
fi
echo "git: $(git --version | cut -d' ' -f3)"
```

**2. Determine Issue Prefix**: Select a short, meaningful prefix

<prefix_rules>
**CRITICAL: Beads prefix requirements:**
- **Maximum 8 characters** (including trailing hyphen)
- Must end with a hyphen (e.g., `pydo-`, `auth-`, `api-`)
- Lowercase letters, numbers, hyphens only
- Must start with a letter

**Good prefixes:** `pydo-`, `auth-`, `cli-`, `web-`, `api-`, `core-`
**Bad prefixes:** `agentic-workflow-test-` (too long), `MyProject-` (uppercase)
</prefix_rules>

```bash
# Derive short prefix from project name or ask user
PROJECT_NAME=$(basename "$(pwd)")

# Auto-generate short prefix: take first 4-6 chars, ensure valid
SHORT_PREFIX=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g' | cut -c1-6)

# If auto-generated is too generic or empty, prompt for input
if [ ${#SHORT_PREFIX} -lt 2 ]; then
  echo ""
  echo "Could not derive prefix from project name."
  echo "Please specify a short prefix (2-7 chars, e.g., 'pydo', 'auth'):"
  # In practice, Claude should ask the user via AskUserQuestion
fi

PREFIX="${SHORT_PREFIX}-"
echo ""
echo "Using issue prefix: $PREFIX"
```

**3. Initialize Beads**: Set up issue tracking with short prefix
```bash
if [ ! -d ".beads" ]; then
  echo ""
  echo "Initializing Beads tracking with prefix: $PREFIX"
  bd init -p "$PREFIX" --quiet
  echo "Beads initialized"

  # Verify prefix was set correctly
  ACTUAL_PREFIX=$(bd info --json 2>/dev/null | jq -r '.config.issue_prefix // empty')
  echo "Verified prefix: $ACTUAL_PREFIX"
else
  echo "Beads already initialized"
  ACTUAL_PREFIX=$(bd info --json 2>/dev/null | jq -r '.config.issue_prefix // empty')
  echo "Current prefix: $ACTUAL_PREFIX"

  # Warn if prefix is too long
  if [ ${#ACTUAL_PREFIX} -gt 8 ]; then
    echo ""
    echo "WARNING: Current prefix '$ACTUAL_PREFIX' exceeds 8 chars."
    echo "Consider running: bd rename-prefix <short>-"
    echo "Example: bd rename-prefix $(echo $ACTUAL_PREFIX | cut -c1-6)-"
  fi
fi
```

**4. Verify Directory Structure**: Ensure required directories exist
```bash
echo ""
echo "Verifying directory structure..."

# Ensure .claude directories exist
mkdir -p .claude/commands
mkdir -p .claude/rules
mkdir -p .claude/lib

echo ".claude/commands: OK"
echo ".claude/rules: OK"
echo ".claude/lib: OK"

# Ensure docs directory for plans
mkdir -p docs/plans
echo "docs/plans: OK"
```

**5. Validate Configuration Files**: Check required files exist
```bash
echo ""
echo "Checking configuration files..."

FILES=(
  "CLAUDE.md"
  ".claude/rules/001-project-principles.md"
  ".claude/lib/workflow-precheck.sh"
)

for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "$file: OK"
  else
    echo "WARNING: $file missing"
  fi
done
```

**6. Summary**: Report initialization status
```bash
echo ""
echo "================================"
echo "Workflow Initialization Complete"
echo "================================"
echo ""
echo "Issue prefix: $PREFIX"
echo ""
echo "Next steps:"
echo "1. Review CLAUDE.md for workflow instructions"
echo "2. Read .claude/rules/ for project guidelines"
echo "3. Start a feature with: /workflow-start [description]"
echo ""
echo "Quick reference:"
echo "  /workflow-start  - Begin new feature"
echo "  /workflow-work   - Find and claim work"
echo "  /workflow-land   - Complete session"
echo "  /workflow-check  - Review project status"
echo ""
```

---

### Prefix Selection Guidelines

When initializing a new project, choose a prefix that is:

| Guideline | Good | Bad |
|-----------|------|-----|
| Short (2-7 chars + hyphen) | `pydo-` | `python-todo-app-` |
| Meaningful | `auth-` | `aa-` |
| Lowercase | `api-` | `API-` |
| No special chars | `web-` | `web_app-` |

**Examples by project type:**
- CLI tool named "pydo" → `pydo-`
- Authentication service → `auth-`
- API gateway → `apigw-`
- Frontend app → `web-` or `ui-`

---

### When to Use

- Setting up a new project with the agentic workflow
- After cloning this repository
- When workflow commands fail with environment errors
- To verify project is properly configured

### Prerequisites

- `bd` CLI installed (Beads issue tracker)
- `git` installed and repository initialized
- Project directory is writable

### What Gets Created

| Component | Purpose |
|-----------|---------|
| `.beads/` | Beads issue tracking database and JSONL |
| `.claude/lib/` | Shared workflow scripts |
| `docs/plans/` | Implementation plan documents |

### Troubleshooting

If initialization fails:
1. Check `bd version` works
2. Verify write permissions to project directory
3. See [CLAUDE.md#troubleshooting](../../CLAUDE.md#troubleshooting)

**If prefix is too long:**
```bash
bd rename-prefix <short>- --dry-run   # Preview
bd rename-prefix <short>-             # Apply
```

**Example usage:**
```
/workflow-init
# Sets up all workflow components with short prefix
```
