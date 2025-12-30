#!/usr/bin/env bash
# install-workflow.sh - Install or update the agentic development workflow
#
# Usage:
#   curl -sL https://raw.githubusercontent.com/nightshift2k/claude-code-beads-workflow/main/install-workflow.sh | bash
#
# Or download and run locally:
#   ./install-workflow.sh

set -euo pipefail

# Configuration
REPO_URL="https://raw.githubusercontent.com/nightshift2k/claude-code-beads-workflow/main"
WORKFLOW_VERSION="0.2.0"

# Colors for output (disabled if not a terminal)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Output helpers
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Files to download
COMMAND_FILES=(
    "workflow-check.md"
    "workflow-config.md"
    "workflow-do.md"
    "workflow-execute.md"
    "workflow-health.md"
    "workflow-init.md"
    "workflow-land.md"
    "workflow-overview.md"
    "workflow-question-ask.md"
    "workflow-start.md"
    "workflow-steer-correct.md"
    "workflow-steer-research.md"
    "workflow-track.md"
    "workflow-work.md"
)

RULE_FILES=(
    "agent-dispatch.md"
    "ai-native-instructions.md"
    "beads-patterns.md"
    "git-conventions.md"
    "multi-agent-coordination.md"
    "project-principles.md"
)

# Minimal CLAUDE.md template for new projects
MINIMAL_CLAUDE_MD='# Project Instructions

<project_context>
## Project Information
Project: [Your Project Name]
Description: [Brief description]
Tech Stack: [Languages, frameworks]
</project_context>

@CLAUDE-workflow.md
'

# Check if we have a required command
require_cmd() {
    if ! command -v "$1" &> /dev/null; then
        error "$1 is required but not installed."
        exit 1
    fi
}

# Download a file with progress indication
download_file() {
    local url="$1"
    local dest="$2"
    local name
    name=$(basename "$dest")

    if curl -sL --fail "$url" -o "$dest" 2>/dev/null; then
        echo -e "  ${GREEN}+${NC} $name"
        return 0
    else
        echo -e "  ${RED}x${NC} $name (failed)"
        return 1
    fi
}

# Prompt for yes/no with default
prompt_yn() {
    local prompt="$1"
    local default="${2:-y}"
    local yn

    if [[ "$default" == "y" ]]; then
        read -rp "$prompt [Y/n] " yn
        yn=${yn:-y}
    else
        read -rp "$prompt [y/N] " yn
        yn=${yn:-n}
    fi

    [[ "${yn,,}" == "y" || "${yn,,}" == "yes" ]]
}

# Phase 1: Validate environment
validate_environment() {
    info "Validating environment..."

    require_cmd "curl"
    require_cmd "git"

    # Check for git repository
    if [[ ! -d ".git" ]]; then
        warn "No git repository found in current directory."
        if prompt_yn "Initialize git repository?"; then
            git init
            success "Git repository initialized"
        else
            error "Git repository required. Run 'git init' first."
            exit 1
        fi
    else
        success "Git repository found"
    fi
}

# Phase 2: Check for existing workflow (update mode)
check_existing_workflow() {
    local workflow_exists=false

    if [[ -f "CLAUDE-workflow.md" ]] || [[ -d ".claude/commands" ]]; then
        workflow_exists=true
    fi

    if [[ "$workflow_exists" == "true" ]]; then
        warn "Workflow files already installed."
        if prompt_yn "Update to latest version?"; then
            info "Updating workflow files..."
            return 0
        else
            info "Installation cancelled."
            exit 0
        fi
    fi

    return 0
}

# Phase 3: Download workflow files
download_workflow_files() {
    local failed=0

    info "Downloading workflow files..."

    # Create directories
    mkdir -p .claude/commands
    mkdir -p .claude/rules
    mkdir -p .claude/lib
    mkdir -p docs/plans

    # Download root documentation files
    echo "Downloading main workflow files..."
    if ! download_file "$REPO_URL/CLAUDE-workflow.md" "CLAUDE-workflow.md"; then
        ((failed++))
    fi
    if ! download_file "$REPO_URL/TROUBLESHOOTING.md" "TROUBLESHOOTING.md"; then
        ((failed++))
    fi

    # Download command files
    echo "Downloading commands (14 files)..."
    for file in "${COMMAND_FILES[@]}"; do
        if ! download_file "$REPO_URL/.claude/commands/$file" ".claude/commands/$file"; then
            ((failed++))
        fi
    done

    # Download rule files
    echo "Downloading rules (6 files)..."
    for file in "${RULE_FILES[@]}"; do
        if ! download_file "$REPO_URL/.claude/rules/$file" ".claude/rules/$file"; then
            ((failed++))
        fi
    done

    # Download workflow.py
    echo "Downloading utility library..."
    if ! download_file "$REPO_URL/.claude/lib/workflow.py" ".claude/lib/workflow.py"; then
        ((failed++))
    fi

    # Download reference documentation
    echo "Downloading reference docs..."
    if ! download_file "$REPO_URL/docs/beads-reference.md" "docs/beads-reference.md"; then
        ((failed++))
    fi

    if [[ $failed -gt 0 ]]; then
        error "Failed to download $failed file(s). Check your network connection."
        exit 1
    fi

    success "Downloaded all workflow files"
}

# Phase 4: Handle CLAUDE.md
handle_claude_md() {
    info "Configuring CLAUDE.md..."

    if [[ -f "CLAUDE.md" ]]; then
        # Check if @reference already exists
        if grep -q "@CLAUDE-workflow.md" "CLAUDE.md"; then
            success "CLAUDE.md already references workflow"
            return 0
        fi

        # Show current content
        echo ""
        echo "Current CLAUDE.md starts with:"
        echo "---"
        head -5 "CLAUDE.md"
        echo "---"
        echo ""

        if prompt_yn "Add @CLAUDE-workflow.md reference at top of CLAUDE.md?"; then
            # Create backup
            cp "CLAUDE.md" "CLAUDE.md.backup"

            # Add reference at top
            {
                echo "@CLAUDE-workflow.md"
                echo ""
                cat "CLAUDE.md.backup"
            } > "CLAUDE.md"

            success "Added workflow reference to CLAUDE.md (backup: CLAUDE.md.backup)"
        else
            warn "Skipped CLAUDE.md modification"
            echo "  Add this line at the top of your CLAUDE.md:"
            echo "    @CLAUDE-workflow.md"
        fi
    else
        # Create minimal CLAUDE.md
        echo "$MINIMAL_CLAUDE_MD" > "CLAUDE.md"
        success "Created CLAUDE.md with workflow reference"
        echo ""
        warn "Update CLAUDE.md with your project details:"
        echo "  - Project name"
        echo "  - Description"
        echo "  - Tech stack"
    fi
}

# Phase 5: Report installation
report_installation() {
    echo ""
    echo "=========================================="
    echo -e "${GREEN}Workflow Installation Complete (v${WORKFLOW_VERSION})${NC}"
    echo "=========================================="
    echo ""
    echo "Installed files:"
    echo "  CLAUDE-workflow.md          - Workflow instructions"
    echo "  TROUBLESHOOTING.md          - Error recovery guide"
    echo "  .claude/commands/           - 14 workflow commands"
    echo "  .claude/rules/              - 6 rule files"
    echo "  .claude/lib/workflow.py     - Utility library"
    echo "  docs/beads-reference.md     - Beads CLI reference"
    echo "  docs/plans/                 - Directory for implementation plans"
    echo ""
}

# Phase 6: Next steps
show_next_steps() {
    echo "Next steps:"
    echo ""
    echo "  1. Open your project in Claude Code"
    echo "  2. Run: /workflow-init"
    echo ""

    # Check for Beads
    if ! command -v bd &> /dev/null; then
        warn "Beads CLI not found. Install before running /workflow-init:"
        echo "    go install github.com/steveyegge/beads/cmd/bd@latest"
        echo "  Or:"
        echo "    brew install steveyegge/tap/beads"
        echo ""
    fi

    if [[ ! -d ".beads" ]]; then
        info "No Beads database found. /workflow-init will help you set it up."
        echo ""
    fi

    echo "Documentation:"
    echo "  - Quick start: https://github.com/nightshift2k/claude-code-beads-workflow/blob/main/QUICKSTART.md"
    echo "  - Migration guide: https://github.com/nightshift2k/claude-code-beads-workflow/blob/main/CLAUDE-workflow-migration.md"
    echo ""
}

# Main installation flow
main() {
    echo ""
    echo "=========================================="
    echo "  Agentic Development Workflow Installer"
    echo "  Version: $WORKFLOW_VERSION"
    echo "=========================================="
    echo ""

    # Run installation phases
    validate_environment
    check_existing_workflow
    download_workflow_files
    handle_claude_md
    report_installation
    show_next_steps
}

# Handle --version flag
if [[ "${1:-}" == "--version" ]] || [[ "${1:-}" == "-v" ]]; then
    echo "Agentic Development Workflow Installer v${WORKFLOW_VERSION}"
    exit 0
fi

# Handle --help flag
if [[ "${1:-}" == "--help" ]] || [[ "${1:-}" == "-h" ]]; then
    echo "Usage: install-workflow.sh [OPTIONS]"
    echo ""
    echo "Install or update the agentic development workflow in the current directory."
    echo ""
    echo "Options:"
    echo "  -v, --version    Show version and exit"
    echo "  -h, --help       Show this help message and exit"
    echo ""
    echo "Quick install:"
    echo "  curl -sL https://raw.githubusercontent.com/nightshift2k/claude-code-beads-workflow/main/install-workflow.sh | bash"
    exit 0
fi

# Run main
main "$@"
