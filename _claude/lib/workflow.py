#!/usr/bin/env python3
"""
Agentic workflow utilities for Claude Code.

Single-file CLI tool replacing all bash scripts. Runs via: uv run python _claude/lib/workflow.py <command>

stdlib only - no external dependencies.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


# ============================================================================
# JSON Sanitization (Beads CLI bug workaround)
# See: https://github.com/steveyegge/beads/issues/599
# ============================================================================

def sanitize_json_string(s: str) -> str:
    """Escape string content using JSON encoding.
    
    Args:
        s: The string to escape.
        
    Returns:
        The escaped string with JSON-safe characters.
    """
    return json.dumps(s)[1:-1]


def sanitize_json(text: str) -> str:
    """Escape unescaped control characters inside JSON string values.
    
    Workaround for Beads CLI bug that outputs invalid JSON with unescaped
    control characters. See: https://github.com/steveyegge/beads/issues/599
    
    Args:
        text: Raw JSON text that may contain unescaped control characters.
        
    Returns:
        Sanitized JSON text safe for parsing.
    """
    result = []
    in_string = False
    escaped = False
    current_string = []

    for char in text:
        if char == '"' and not escaped:
            if in_string:
                sanitized = sanitize_json_string(''.join(current_string))
                result.append('"')
                result.append(sanitized)
                result.append('"')
                current_string = []
                in_string = False
            else:
                in_string = True
        elif in_string:
            current_string.append(char)
        else:
            result.append(char)

        escaped = (char == '\\' and not escaped)

    return ''.join(result)


# ============================================================================
# Beads CLI Wrapper
# ============================================================================

class BeadsError(Exception):
    """Raised when a Beads CLI command fails."""
    pass


def run_bd(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Execute bd command with --sandbox flag.
    
    Args:
        *args: Command arguments to pass to bd CLI.
        check: If True, raise BeadsError on non-zero exit code.
        
    Returns:
        CompletedProcess with stdout, stderr, and returncode.
        
    Raises:
        BeadsError: If check=True and command exits with non-zero status.
    """
    cmd = ["bd", "--sandbox", *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise BeadsError(f"bd {' '.join(args)} failed: {result.stderr}")
    return result


def bd_json(*args: str) -> Any:
    """Run bd command and return parsed JSON.
    
    Args:
        *args: Command arguments (--json is appended automatically).
        
    Returns:
        Parsed JSON response from bd command.
        
    Raises:
        BeadsError: If command fails or JSON is invalid.
    """
    result = run_bd(*args, "--json")
    sanitized = sanitize_json(result.stdout)
    try:
        return json.loads(sanitized)
    except json.JSONDecodeError as e:
        raise BeadsError(f"Invalid JSON from bd: {e}\nOutput: {result.stdout[:200]}")


def bd_show(issue_id: str) -> dict:
    """Get issue details by ID.
    
    Note: bd show returns an array; this returns the first element.
    
    Args:
        issue_id: The Beads issue ID (e.g., 'pydo-abc').
        
    Returns:
        Issue dictionary with id, title, status, description, etc.
        
    Raises:
        BeadsError: If issue not found.
    """
    results = bd_json("show", issue_id)
    if not results:
        raise BeadsError(f"Issue not found: {issue_id}")
    return results[0]


def bd_list(status: Optional[str] = None, limit: Optional[int] = None) -> list:
    """List issues with optional filters.
    
    Args:
        status: Filter by status ('open', 'in_progress', 'closed').
        limit: Maximum number of issues to return.
        
    Returns:
        List of issue dictionaries.
    """
    args = ["list"]
    if status:
        args.extend(["--status", status])
    if limit:
        args.extend(["--limit", str(limit)])
    return bd_json(*args)


def bd_ready() -> list:
    """Get ready (unblocked) issues available for work.
    
    Returns:
        List of issue dictionaries that have no blocking dependencies.
    """
    return bd_json("ready")


def bd_blocked() -> list:
    """Get blocked issues with their blockers.
    
    Returns:
        List of issue dictionaries including 'blocked_by' field.
    """
    return bd_json("blocked")


def bd_create(title: str, **kwargs) -> dict:
    """Create a new Beads issue.
    
    Note: bd create returns an object (not array like other commands).
    
    Args:
        title: Issue title/summary.
        **kwargs: Optional parameters:
            - type: Issue type ('epic', 'task', 'bug').
            - priority: Priority level (0-4).
            - parent: Parent issue ID for hierarchical issues.
            - description: Full issue description.
            
    Returns:
        Created issue dictionary with assigned ID.
        
    Raises:
        BeadsError: If creation fails.
    """
    args = ["create", title]
    if "type" in kwargs:
        args.extend(["-t", kwargs["type"]])
    if "priority" in kwargs:
        args.extend(["-p", str(kwargs["priority"])])
    if "parent" in kwargs:
        args.extend(["--parent", kwargs["parent"], "--force"])
    if "description" in kwargs:
        args.extend(["--description", kwargs["description"]])
    return bd_json(*args)


def bd_update(issue_id: str, **kwargs) -> list:
    """Update an existing issue.
    
    Args:
        issue_id: The issue ID to update.
        **kwargs: Fields to update:
            - status: New status ('open', 'in_progress', 'closed').
            - notes: Notes to append.
            - description: New description.
            
    Returns:
        List of affected issue dictionaries.
    """
    args = ["update", issue_id]
    if "status" in kwargs:
        args.extend(["--status", kwargs["status"]])
    if "notes" in kwargs:
        args.extend(["--notes", kwargs["notes"]])
    if "description" in kwargs:
        args.extend(["--description", kwargs["description"]])
    return bd_json(*args)


def bd_close(issue_id: str, reason: str) -> list:
    """Close an issue with a reason.
    
    Args:
        issue_id: The issue ID to close.
        reason: Closure reason (stored in issue history).
        
    Returns:
        List of affected issue dictionaries.
    """
    return bd_json("close", issue_id, "--reason", reason)


def bd_dep_add(blocked_id: str, blocking_id: str) -> None:
    """Add a blocking dependency between issues.
    
    Args:
        blocked_id: The issue that will be blocked.
        blocking_id: The issue that blocks completion.
    """
    run_bd("dep", "add", blocked_id, blocking_id)


def bd_dep_remove(blocked_id: str, blocking_id: str) -> None:
    """Remove a blocking dependency between issues.
    
    Args:
        blocked_id: The previously blocked issue.
        blocking_id: The issue that was blocking.
    """
    run_bd("dep", "remove", blocked_id, blocking_id, check=False)


def bd_stale(days: int = 7) -> list:
    """Get stale issues older than N days.
    
    Args:
        days: Number of days threshold for staleness.
        
    Returns:
        List of stale issue dictionaries.
    """
    return bd_json("stale", "--days", str(days))


# ============================================================================
# Environment Validation
# ============================================================================

def check_command(cmd: str) -> tuple[bool, str]:
    """Check if a command exists in PATH.
    
    Args:
        cmd: Command name to check (e.g., 'bd', 'git').
        
    Returns:
        Tuple of (exists: bool, version_or_error: str).
    """
    try:
        result = subprocess.run([cmd, "--version"], capture_output=True, text=True)
        version = re.search(r'v?[\d.]+', result.stdout or result.stderr)
        return True, version.group() if version else "unknown"
    except FileNotFoundError:
        return False, "not found"


def check_environment() -> list[str]:
    """Validate workflow environment prerequisites.
    
    Checks for required commands (bd, git) and .beads directory.
    
    Returns:
        List of error messages (empty if environment is valid).
    """
    errors = []

    # Check bd CLI
    ok, version = check_command("bd")
    if not ok:
        errors.append(
            "Beads CLI (bd) not found.\n"
            "   Install: go install github.com/steveyegge/beads/cmd/bd@latest\n"
            "   Or: brew install steveyegge/tap/beads"
        )

    # Check git
    ok, _ = check_command("git")
    if not ok:
        errors.append("git not found. Install from https://git-scm.com/")

    # Check .beads directory
    if not Path(".beads").is_dir():
        errors.append(
            "No .beads directory found.\n"
            "   Run: bd init -p <prefix>- --quiet"
        )

    return errors


def precheck(command_name: str, interactive: bool = False) -> bool:
    """Run environment validation before a workflow command.
    
    Args:
        command_name: Name of command for error messages.
        interactive: If True, prompt user to fix issues.
        
    Returns:
        True if environment is valid, False otherwise.
    """
    errors = check_environment()

    if not errors:
        print(f"Environment validation passed for {command_name}")
        return True

    print(f"Environment validation failed for {command_name}:", file=sys.stderr)
    for err in errors:
        print(f"  - {err}", file=sys.stderr)

    if interactive and ".beads" in str(errors):
        response = input("\nInitialize Beads now? (Y/n): ").strip().lower()
        if response != 'n':
            try:
                subprocess.run(["bd", "init", "--quiet"], check=True)
                print("Beads initialized successfully")
                return check_environment() == []
            except subprocess.CalledProcessError:
                print("Beads initialization failed", file=sys.stderr)

    return False


# ============================================================================
# Steering Utilities
# ============================================================================

def steering_show_tasks(epic_id_or_issues: str | list) -> None:
    """Display tasks in a formatted ASCII table.
    
    Args:
        epic_id_or_issues: Either an epic ID (str) to find children,
            or a list of issue dictionaries to display directly.
    """
    print("  ┌──────────────┬─────────────────────────────────┬──────────────┐")
    print("  │ Task         │ Title                           │ Status       │")
    print("  ├──────────────┼─────────────────────────────────┼──────────────┤")

    if isinstance(epic_id_or_issues, str):
        # Epic ID - find children
        issues = [i for i in bd_list() if i["id"].startswith(f"{epic_id_or_issues}.")]
    else:
        issues = epic_id_or_issues

    for issue in issues:
        print(f"  │ {issue['id'][:12]:<12} │ {issue['title'][:31]:<31} │ {issue['status'][:12]:<12} │")

    print("  └──────────────┴─────────────────────────────────┴──────────────┘")


def steering_find_affected(blocking_id: str) -> list:
    """Find tasks blocked by a given issue.
    
    Args:
        blocking_id: The issue ID that may be blocking others.
        
    Returns:
        List of issue dictionaries that are blocked by this issue.
    """
    return [
        issue for issue in bd_blocked()
        if blocking_id in issue.get("blocked_by", [])
    ]


def steering_show_impact(affected: list) -> None:
    """Display impact table for affected tasks.
    
    Args:
        affected: List of affected issue dictionaries.
    """
    print("  Affected tasks:")
    print("  ┌──────────────┬─────────────────────────────────┬──────────────┐")
    print("  │ Task         │ Impact                          │ Action       │")
    print("  ├──────────────┼─────────────────────────────────┼──────────────┤")

    for issue in affected:
        print(f"  │ {issue['id'][:12]:<12} │ {issue['title'][:31]:<31} │ UPDATE       │")

    print("  └──────────────┴─────────────────────────────────┴──────────────┘")


def steering_update_task(issue_id: str, additional_content: str) -> None:
    """Append a steering update to a task's description.
    
    Adds timestamped steering content separated by a horizontal rule.
    
    Args:
        issue_id: The issue ID to update.
        additional_content: Markdown content to append.
    """
    task = bd_show(issue_id)
    current_desc = task.get("description", "")

    new_desc = f"""{current_desc}

---

**Steering Update ({datetime.now().strftime('%Y-%m-%d')}):**

{additional_content}"""

    bd_update(issue_id, description=new_desc)


def steering_add_note(issue_id: str, note: str) -> None:
    """Add a note to an issue.
    
    Args:
        issue_id: The issue ID to update.
        note: Note text to add.
    """
    bd_update(issue_id, notes=note)


def steering_list_blocked(blocking_id: str) -> list:
    """List tasks blocked by a given issue.
    
    Args:
        blocking_id: The issue ID that may be blocking others.
        
    Returns:
        List of issue dictionaries blocked by this issue.
    """
    return [
        issue for issue in bd_blocked()
        if blocking_id in issue.get("blocked_by", [])
    ]


def steering_summary(updated: int, reopened: int = 0, created: int = 0) -> None:
    """Print steering completion summary.
    
    Args:
        updated: Count of updated tasks.
        reopened: Count of reopened tasks.
        created: Count of newly created tasks.
    """
    print()
    print("  ✅ Steering complete")
    print("  ──────────────────────────────")
    if updated > 0:
        print(f"  Updated:  {updated} tasks")
    if reopened > 0:
        print(f"  Reopened: {reopened} tasks")
    if created > 0:
        print(f"  Created:  {created} tasks")
    print()


# ============================================================================
# Health Check
# ============================================================================

def run_health_check() -> dict:
    """Run comprehensive workflow health diagnostics.
    
    Checks environment, Beads status, issue counts, and git state.
    
    Returns:
        Dictionary with keys: environment, beads, issues, git, overall.
        'overall' is one of: 'HEALTHY', 'DEGRADED', 'CRITICAL'.
    """
    results = {
        "environment": {},
        "beads": {},
        "issues": {},
        "git": {},
        "overall": "HEALTHY"
    }

    # Environment checks
    for cmd in ["bd", "git", "jq"]:
        ok, version = check_command(cmd)
        results["environment"][cmd] = {"ok": ok, "version": version}
        if not ok and cmd in ["bd", "git"]:
            results["overall"] = "CRITICAL"

    # Beads checks
    beads_dir = Path(".beads")
    results["beads"]["initialized"] = beads_dir.is_dir()

    if beads_dir.is_dir():
        db_path = beads_dir / "beads.db"
        results["beads"]["database_exists"] = db_path.exists()

        jsonl_path = beads_dir / "issues.jsonl"
        if jsonl_path.exists():
            results["beads"]["jsonl_entries"] = sum(1 for _ in open(jsonl_path))

        # Test bd commands
        try:
            bd_list(limit=1)
            results["beads"]["commands_working"] = True
        except BeadsError:
            results["beads"]["commands_working"] = False
            results["overall"] = "DEGRADED"
    else:
        results["overall"] = "CRITICAL"

    # Issue counts
    if results["beads"].get("commands_working"):
        try:
            results["issues"]["open"] = len(bd_list(status="open"))
            results["issues"]["in_progress"] = len(bd_list(status="in_progress"))
            results["issues"]["closed"] = len(bd_list(status="closed"))
            results["issues"]["ready"] = len(bd_ready())
            results["issues"]["blocked"] = len(bd_blocked())
            results["issues"]["stale"] = len(bd_stale(days=7))
        except BeadsError:
            pass

    # Git checks
    try:
        result = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True)
        results["git"]["is_repo"] = result.returncode == 0
        if results["git"]["is_repo"]:
            branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
            results["git"]["branch"] = branch.stdout.strip()
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            results["git"]["uncommitted"] = len(status.stdout.strip().split('\n')) if status.stdout.strip() else 0
    except FileNotFoundError:
        results["git"]["is_repo"] = False

    return results


def print_health_report(results: dict) -> None:
    """Print formatted health check report to stdout.
    
    Args:
        results: Health check results from run_health_check().
    """
    print("=== Workflow Health Check ===")
    print()

    # Environment
    print("1. ENVIRONMENT")
    print("   ----------")
    for cmd, info in results["environment"].items():
        status = f"OK ({info['version']})" if info["ok"] else "MISSING"
        print(f"   {cmd}: {status}")

    # Beads
    print()
    print("2. BEADS TRACKING")
    print("   --------------")
    if results["beads"].get("initialized"):
        print("   .beads/: OK")
        db = "HEALTHY" if results["beads"].get("database_exists") else "MISSING"
        print(f"   Database: {db}")
        if "jsonl_entries" in results["beads"]:
            print(f"   JSONL: OK ({results['beads']['jsonl_entries']} entries)")
        cmds = "WORKING" if results["beads"].get("commands_working") else "FAILING"
        print(f"   bd commands: {cmds}")
    else:
        print("   .beads/: NOT INITIALIZED")

    # Issues
    print()
    print("3. ISSUE STATUS")
    print("   ------------")
    if results["issues"]:
        print(f"   Open: {results['issues'].get('open', '?')}")
        print(f"   In Progress: {results['issues'].get('in_progress', '?')}")
        print(f"   Closed: {results['issues'].get('closed', '?')}")
        print(f"   Ready to work: {results['issues'].get('ready', '?')}")
        if results["issues"].get("blocked", 0) > 0:
            print(f"   WARN: {results['issues']['blocked']} blocked issues")
        if results["issues"].get("stale", 0) > 0:
            print(f"   WARN: {results['issues']['stale']} stale issues (>7 days)")
    else:
        print("   (Beads not available)")

    # Git
    print()
    print("4. GIT STATUS")
    print("   ----------")
    if results["git"].get("is_repo"):
        print("   Repository: OK")
        print(f"   Branch: {results['git'].get('branch', 'unknown')}")
        uncommitted = results["git"].get("uncommitted", 0)
        print(f"   Working tree: {'CLEAN' if uncommitted == 0 else f'{uncommitted} uncommitted changes'}")
    else:
        print("   Repository: NOT INITIALIZED")

    # Summary
    print()
    print("=== SUMMARY ===")
    print()
    print(f"Overall: {results['overall']}")


# ============================================================================
# Utility Functions
# ============================================================================

def derive_prefix(project_name: str) -> str:
    """Derive a short Beads prefix from project name.
    
    Args:
        project_name: Project directory name.
        
    Returns:
        Sanitized prefix (6 chars max + hyphen), or empty string if invalid.
    """
    clean = re.sub(r'[^a-z0-9]', '', project_name.lower())
    return clean[:6] + "-" if len(clean) >= 2 else ""


# ============================================================================
# Command Handlers
# ============================================================================

def cmd_precheck(args: argparse.Namespace) -> int:
    """CLI handler: Run environment precheck.
    
    Args:
        args: Parsed arguments with optional 'name' field.
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if precheck(args.name or "manual-check", interactive=True):
        return 0
    return 1


def cmd_health(args: argparse.Namespace) -> int:
    """CLI handler: Run health diagnostics.
    
    Args:
        args: Parsed arguments (unused).
        
    Returns:
        Exit code (0 if healthy, 1 otherwise).
    """
    results = run_health_check()
    print_health_report(results)
    return 0 if results["overall"] == "HEALTHY" else 1


def cmd_init(args: argparse.Namespace) -> int:
    """CLI handler: Initialize project for workflow.
    
    Args:
        args: Parsed arguments with optional 'prefix' field.
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    print("=== Workflow Initialization ===")
    print()

    # Check bd CLI
    ok, version = check_command("bd")
    if not ok:
        print("ERROR: bd CLI not found", file=sys.stderr)
        print("Install: go install github.com/steveyegge/beads/cmd/bd@latest")
        return 1
    print(f"bd CLI: {version}")

    # Check/derive prefix
    project_name = Path.cwd().name
    prefix = args.prefix or derive_prefix(project_name)

    if not prefix or len(prefix) > 8:
        print(f"ERROR: Invalid prefix '{prefix}'. Must be 2-7 chars + hyphen.")
        return 1

    if not prefix.endswith("-"):
        prefix = prefix + "-"

    print(f"Using prefix: {prefix}")

    # Initialize Beads if needed
    if not Path(".beads").is_dir():
        print()
        print("Initializing Beads...")
        try:
            subprocess.run(["bd", "init", "-p", prefix, "--quiet"], check=True)
            print("Beads initialized")
        except subprocess.CalledProcessError:
            print("ERROR: Beads initialization failed", file=sys.stderr)
            return 1
    else:
        print(".beads directory exists")

    # Ensure directories
    for d in [".claude/commands", ".claude/rules", "_claude/lib", "docs/plans"]:
        Path(d).mkdir(parents=True, exist_ok=True)
    print("Directories verified")

    # Summary
    print()
    print("================================")
    print("Workflow Initialization Complete")
    print("================================")
    print()
    print(f"Issue prefix: {prefix}")
    print()
    print("Next steps:")
    print("1. /workflow-start [description] - Begin new feature")
    print("2. /workflow-work - Find and claim work")
    print()
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    """CLI handler: Start new feature with epic creation.
    
    Args:
        args: Parsed arguments with 'description' field.
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if not precheck("start"):
        return 1

    if not args.description:
        print("ERROR: Usage: workflow start <feature-description>", file=sys.stderr)
        return 1

    description = " ".join(args.description)
    print(f"Starting new feature: {description}")
    print()

    try:
        epic = bd_create(
            description,
            type="epic",
            priority=1,
            description=f"Feature epic: {description}"
        )

        epic_id = epic["id"]
        print()
        print("==========================================")
        print(f"EPIC CREATED: {epic_id}")
        print("==========================================")
        print()
        print("IMPORTANT: Save this epic ID for /workflow-track")
        print()
        print("Next steps:")
        print("1. Create implementation plan (use writing-plans skill)")
        print(f"2. Track with: /workflow-track [plan-path]")
        print(f"   Use --parent {epic_id} --force for child issues")
        print()
        return 0

    except BeadsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_ready(args: argparse.Namespace) -> int:
    """CLI handler: Show ready (unblocked) issues.
    
    Args:
        args: Parsed arguments (unused).
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if not precheck("ready"):
        return 1

    try:
        issues = bd_ready()
        if not issues:
            print("No ready issues found.")
            print()
            print("Check blocked issues: uv run python _claude/lib/workflow.py list --blocked")
            return 0

        print("Ready issues:")
        print()
        for issue in issues:
            print(f"[{issue['id']}] P{issue.get('priority', '?')} {issue['title']}")
        print()
        print(f"Total: {len(issues)} issue(s) ready for work")
        return 0

    except BeadsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_list(args: argparse.Namespace) -> int:
    """CLI handler: List issues with optional filters.
    
    Args:
        args: Parsed arguments with optional 'status' and 'blocked' fields.
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if not precheck("list"):
        return 1

    try:
        if args.blocked:
            issues = bd_blocked()
            label = "Blocked issues"
        elif args.status:
            issues = bd_list(status=args.status)
            label = f"Issues ({args.status})"
        else:
            issues = bd_list()
            label = "All issues"

        if not issues:
            print(f"No {label.lower()} found.")
            return 0

        print(f"{label}:")
        print()
        for issue in issues:
            blocked_by = issue.get("blocked_by", [])
            suffix = f" [blocked by: {', '.join(blocked_by)}]" if blocked_by else ""
            print(f"[{issue['id']}] {issue['status']:<12} {issue['title']}{suffix}")
        print()
        print(f"Total: {len(issues)}")
        return 0

    except BeadsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_find_affected(args: argparse.Namespace) -> int:
    """CLI handler: Find tasks blocked by an issue.
    
    Args:
        args: Parsed arguments with 'issue_id' and optional 'json' fields.
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if not precheck("find-affected"):
        return 1

    try:
        affected = steering_find_affected(args.issue_id)
        if args.json:
            print(json.dumps(affected, indent=2))
        else:
            if not affected:
                print(f"No tasks blocked by {args.issue_id}")
            else:
                steering_show_impact(affected)
        return 0

    except BeadsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_show(args: argparse.Namespace) -> int:
    """CLI handler: Show issue details.
    
    Args:
        args: Parsed arguments with 'issue_id' and optional 'json' fields.
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if not precheck("show"):
        return 1

    try:
        issue = bd_show(args.issue_id)

        if args.json:
            print(json.dumps(issue, indent=2))
        else:
            print(f"ID: {issue['id']}")
            print(f"Title: {issue['title']}")
            print(f"Status: {issue['status']}")
            print(f"Type: {issue.get('type', 'task')}")
            print(f"Priority: P{issue.get('priority', '?')}")
            if issue.get("blocked_by"):
                print(f"Blocked by: {', '.join(issue['blocked_by'])}")
            print()
            print("Description:")
            print("-" * 40)
            print(issue.get("description", "(no description)"))
        return 0

    except BeadsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_close(args: argparse.Namespace) -> int:
    """CLI handler: Close an issue with reason.
    
    Args:
        args: Parsed arguments with 'issue_id' and 'reason' fields.
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if not precheck("close"):
        return 1

    try:
        bd_close(args.issue_id, args.reason)
        print(f"Closed: {args.issue_id}")
        print(f"Reason: {args.reason}")
        return 0

    except BeadsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_update(args: argparse.Namespace) -> int:
    """CLI handler: Update an issue.
    
    Args:
        args: Parsed arguments with 'issue_id' and optional
            'status', 'notes', 'description' fields.
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if not precheck("update"):
        return 1

    kwargs = {}
    if args.status:
        kwargs["status"] = args.status
    if args.notes:
        kwargs["notes"] = args.notes
    if args.description:
        kwargs["description"] = args.description

    if not kwargs:
        print("ERROR: Specify at least one of --status, --notes, --description", file=sys.stderr)
        return 1

    try:
        bd_update(args.issue_id, **kwargs)
        print(f"Updated: {args.issue_id}")
        for key, val in kwargs.items():
            print(f"  {key}: {val[:50]}{'...' if len(val) > 50 else ''}")
        return 0

    except BeadsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


def cmd_show_tasks(args: argparse.Namespace) -> int:
    """CLI handler: Show tasks for an epic.
    
    Args:
        args: Parsed arguments with 'epic_id' field.
        
    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if not precheck("show-tasks"):
        return 1
    steering_show_tasks(args.epic_id)
    return 0


def main() -> int:
    """CLI entry point for workflow utilities.
    
    Parses command-line arguments and dispatches to appropriate handler.
    
    Returns:
        Exit code from the executed subcommand.
    """
    parser = argparse.ArgumentParser(
        prog="workflow",
        description="Agentic workflow utilities for Claude Code"
    )
    parser.add_argument("--version", action="version", version="1.0.0")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Precheck command
    p_precheck = subparsers.add_parser("precheck", help="Validate environment")
    p_precheck.add_argument("--name", help="Command name for messages")
    p_precheck.set_defaults(func=cmd_precheck)

    # Health command
    p_health = subparsers.add_parser("health", help="Run health diagnostics")
    p_health.set_defaults(func=cmd_health)

    # Init command
    p_init = subparsers.add_parser("init", help="Initialize project for workflow")
    p_init.add_argument("--prefix", help="Issue prefix (2-7 chars, auto-derived if omitted)")
    p_init.set_defaults(func=cmd_init)

    # Start command
    p_start = subparsers.add_parser("start", help="Start new feature")
    p_start.add_argument("description", nargs="*", help="Feature description")
    p_start.set_defaults(func=cmd_start)

    # Ready command
    p_ready = subparsers.add_parser("ready", help="Show ready issues")
    p_ready.set_defaults(func=cmd_ready)

    # List command
    p_list = subparsers.add_parser("list", help="List issues")
    p_list.add_argument("--status", help="Filter by status (open, in_progress, closed)")
    p_list.add_argument("--blocked", action="store_true", help="Show only blocked issues")
    p_list.set_defaults(func=cmd_list)

    # Find-affected command
    p_find = subparsers.add_parser("find-affected", help="Find tasks blocked by an issue")
    p_find.add_argument("issue_id", help="Blocking issue ID")
    p_find.add_argument("--json", action="store_true", help="Output as JSON")
    p_find.set_defaults(func=cmd_find_affected)

    # Show command
    p_show = subparsers.add_parser("show", help="Show issue details")
    p_show.add_argument("issue_id", help="Issue ID")
    p_show.add_argument("--json", action="store_true", help="Output as JSON")
    p_show.set_defaults(func=cmd_show)

    # Close command
    p_close = subparsers.add_parser("close", help="Close an issue")
    p_close.add_argument("issue_id", help="Issue ID")
    p_close.add_argument("reason", help="Closure reason")
    p_close.set_defaults(func=cmd_close)

    # Update command
    p_update = subparsers.add_parser("update", help="Update an issue")
    p_update.add_argument("issue_id", help="Issue ID")
    p_update.add_argument("--status", help="New status")
    p_update.add_argument("--notes", help="Add notes")
    p_update.add_argument("--description", help="New description")
    p_update.set_defaults(func=cmd_update)

    # Show-tasks command
    p_show_tasks = subparsers.add_parser("show-tasks", help="Show tasks for an epic")
    p_show_tasks.add_argument("epic_id", help="Epic ID")
    p_show_tasks.set_defaults(func=cmd_show_tasks)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())