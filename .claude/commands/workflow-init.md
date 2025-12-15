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

**2. Initialize Beads**: Set up issue tracking
```bash
if [ ! -d ".beads" ]; then
  echo ""
  echo "Initializing Beads tracking..."
  bd init --quiet
  echo "Beads initialized"
else
  echo "Beads already initialized"
fi
```

**3. Verify Directory Structure**: Ensure required directories exist
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

**4. Validate Configuration Files**: Check required files exist
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

**5. Summary**: Report initialization status
```bash
echo ""
echo "================================"
echo "Workflow Initialization Complete"
echo "================================"
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

**Example usage:**
```
/workflow-init
# Sets up all workflow components
```
