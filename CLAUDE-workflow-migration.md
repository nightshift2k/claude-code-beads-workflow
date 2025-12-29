# Migrating an Existing Project

Add agentic development workflow to any existing project in minutes.

## Quick Start

Run this command in your project directory:

```bash
curl -sL https://raw.githubusercontent.com/nightshift2k/claude-code-beads-workflow/main/install-workflow.sh | bash
```

The script:

1. Validates your git repository
2. Downloads workflow files
3. Configures CLAUDE.md
4. Provides next steps

## What Gets Installed

```
your-project/
├── CLAUDE.md                      # Created or updated with @reference
├── CLAUDE-workflow.md             # Complete workflow instructions
├── .claude/
│   ├── commands/                  # 14 workflow slash commands
│   │   ├── workflow-init.md
│   │   ├── workflow-start.md
│   │   ├── workflow-track.md
│   │   ├── workflow-execute.md
│   │   ├── workflow-work.md
│   │   ├── workflow-land.md
│   │   ├── workflow-check.md
│   │   ├── workflow-do.md
│   │   ├── workflow-question-ask.md
│   │   ├── workflow-steer-research.md
│   │   ├── workflow-steer-correct.md
│   │   ├── workflow-health.md
│   │   ├── workflow-overview.md
│   │   └── workflow-config.md
│   ├── lib/                       # Shared utilities
│   │   └── workflow.py            # Python utility library
│   └── rules/                     # 6 rule files
│       ├── project-principles.md
│       ├── ai-native-instructions.md
│       ├── multi-agent-coordination.md
│       ├── beads-patterns.md
│       ├── agent-dispatch.md
│       └── git-conventions.md
└── docs/
    └── plans/                     # Directory for implementation plans
```

**Total:** 22 files added

## After Installation

### 1. Install Beads CLI

If not already installed:

```bash
# Via Go
go install github.com/steveyegge/beads/cmd/bd@latest

# Or via Homebrew (macOS)
brew install steveyegge/tap/beads

# Verify installation
bd version
```

### 2. Run Workflow Initialization

Open your project in Claude Code and run:

```
/workflow-init
```

This command:

- Validates environment
- Initializes Beads with your project prefix
- Creates required directories
- Confirms the workflow is ready

### 3. Update Project Context

Edit CLAUDE.md to fill in your project details:

```markdown
<project_context>

## Project Information

Project: My Awesome App
Description: A REST API for task management
Tech Stack: Python, FastAPI, PostgreSQL
</project_context>
```

## Manual Installation

For users who prefer not to pipe curl to bash:

### 1. Clone the Template Repository

```bash
git clone https://github.com/nightshift2k/claude-code-beads-workflow.git /tmp/workflow-template
```

### 2. Copy Workflow Files

```bash
# Navigate to your project
cd /path/to/your/project

# Copy workflow files
cp /tmp/workflow-template/CLAUDE-workflow.md .
cp -r /tmp/workflow-template/.claude/commands .claude/
cp -r /tmp/workflow-template/.claude/rules .claude/
mkdir -p .claude/lib
cp /tmp/workflow-template/.claude/lib/workflow.py .claude/lib/
mkdir -p docs/plans
```

### 3. Configure CLAUDE.md

If CLAUDE.md exists, add at the top:

```markdown
@CLAUDE-workflow.md

# Your existing content below...
```

If no CLAUDE.md exists, create one:

```markdown
# Project Instructions

<project_context>

## Project Information

Project: [Your Project Name]
Description: [Brief description]
Tech Stack: [Languages, frameworks]
</project_context>

@CLAUDE-workflow.md
```

### 4. Clean Up

```bash
rm -rf /tmp/workflow-template
```

## Updating the Workflow

To update to the latest workflow version, run the install script again:

```bash
curl -sL https://raw.githubusercontent.com/nightshift2k/claude-code-beads-workflow/main/install-workflow.sh | bash
```

The script detects existing files and prompts before overwriting. Your CLAUDE.md content remains intact.

**What gets updated:**

- CLAUDE-workflow.md (workflow instructions)
- .claude/commands/\* (all 14 command files)
- .claude/rules/\* (all 6 rule files)
- \.claude/lib/workflow.py (utility library)

**What stays unchanged:**

- CLAUDE.md (your project context)
- .beads/\* (your issue tracking data)
- docs/plans/\* (your implementation plans)

## Troubleshooting Migration

### Script fails with "curl: command not found"

Install curl:

```bash
# macOS
brew install curl

# Ubuntu/Debian
sudo apt install curl
```

### Script fails with "No git repository found"

The workflow requires git. Initialize a repository:

```bash
git init
```

### CLAUDE.md backup created but reference not added

If you declined the prompt, manually add this line at the top of CLAUDE.md:

```markdown
@CLAUDE-workflow.md
```

### "bd: command not found" after installation

Beads CLI needs to be in your PATH:

```bash
export PATH="$PATH:$(go env GOPATH)/bin"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

### /workflow-init fails after migration

Run health check:

```
/workflow-health
```

Common issues:

- Beads CLI version too old (need v0.37.0+)
- Go not installed (needed for Beads)
- PATH not configured

## Uninstalling

To remove the workflow from your project:

```bash
# Remove workflow files
rm -f CLAUDE-workflow.md
rm -rf .claude/commands
rm -rf .claude/lib
rm -rf .claude/rules

# Optionally remove Beads tracking
# WARNING: This deletes all issue tracking data
rm -rf .beads

# Restore CLAUDE.md (remove @reference line)
# Edit CLAUDE.md manually
```

**Note:** This does not uninstall the Beads CLI. To uninstall Beads:

```bash
rm $(which bd)
```

## Preserving Existing Rules

If your project has custom rules in `.claude/rules/`:

1. **Before migration:** Back up custom rules

   ```bash
   cp -r .claude/rules .claude/rules.backup
   ```

2. **After migration:** Merge your customizations
   - Review workflow rules
   - Add project-specific rules to appropriate files
   - Or create new rule files (they won't be overwritten on update)

## Integration with Existing CLAUDE.md

The `@CLAUDE-workflow.md` reference uses Claude Code's file include syntax:

- Workflow instructions load automatically
- Your project context stays at the top
- Project-specific instructions can follow
- Order matters: @references process in sequence

**Example CLAUDE.md structure:**

```markdown
@CLAUDE-workflow.md

<project_context>

## Project Information

Project: My App
...
</project_context>

## Project-Specific Rules

Additional rules specific to this project...

## API Documentation

Links to external docs...
```

## Related Documentation

- [Quick Start Guide](QUICKSTART.md) - 5-minute introduction
- [Full Workflow Reference](CLAUDE-workflow.md) - Complete workflow documentation
- [Beads CLI Documentation](https://github.com/steveyegge/beads) - Issue tracking reference
