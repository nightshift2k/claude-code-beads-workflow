#!/usr/bin/env python3
"""
Agentic workflow utilities for Claude Code.

Single-file CLI tool for environment validation and health checks.
Runs via: uv run python .claude/lib/workflow.py <command>

stdlib only - no external dependencies.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

# Default timeout for subprocess calls (30 seconds)
SUBPROCESS_TIMEOUT = 30

# ============================================================================
# Beads CLI Helpers
# ============================================================================


def _bd_json_simple(*args: str) -> Any:
    """Run bd command and return parsed JSON.

    Simple helper for health checks - no sanitization needed.

    Args:
        *args: Command arguments (--json is appended automatically).

    Returns:
        Parsed JSON response, or empty list on error.
    """
    try:
        result = subprocess.run(
            ["bd", "--sandbox", *args, "--json"],
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
        if result.returncode != 0:
            return []
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return []


# ============================================================================
# Environment Validation
# ============================================================================


def check_command(cmd: str) -> tuple[bool, str]:
    """Check if a command exists in PATH.

    Args:
        cmd: Command name to check (e.g., 'bd', 'git', 'jq').

    Returns:
        Tuple of (exists: bool, version_or_error: str).
    """
    try:
        result = subprocess.run(
            [cmd, "--version"],
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
        if result.returncode != 0:
            return False, f"command failed (exit {result.returncode})"
        version = re.search(r"v?[\d.]+", result.stdout or result.stderr)
        return True, version.group() if version else "unknown"
    except FileNotFoundError:
        return False, "not found"
    except subprocess.TimeoutExpired:
        return False, "timeout"


def parse_beads_version(version_str: str) -> tuple[int, ...]:
    """Parse version string like '0.39.1' to tuple (0, 39, 1).

    Args:
        version_str: Version string (e.g., '0.39.1' or 'v0.39.1').

    Returns:
        Tuple of integers representing the version, or (0, 0, 0) on parse failure.
    """
    try:
        # Handle formats like "0.39.1" or "v0.39.1"
        cleaned = version_str.lstrip("v")
        parts = cleaned.split(".")
        return tuple(int(p) for p in parts[:3])
    except (ValueError, IndexError):
        return (0, 0, 0)


def check_beads_version() -> tuple[bool, bool, str]:
    """Check if Beads CLI version meets requirements.

    Minimum version: 0.37.0 (has --parent flags for epic scoping)
    Recommended version: 0.39.1 (all documented features available)

    Returns:
        Tuple of (meets_minimum, meets_recommended, message).
        - meets_minimum: False if < 0.37.0 (workflow will fail)
        - meets_recommended: False if < 0.39.1 (some features missing)
    """
    MIN_VERSION = (0, 37, 0)
    REC_VERSION = (0, 39, 1)

    try:
        result = subprocess.run(
            ["bd", "version"],
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
        # Parse "bd version 0.39.1 (commit_info)" - extract X.Y.Z pattern
        version_match = re.search(r"(\d+\.\d+\.\d+)", result.stdout)
        if not version_match:
            return True, True, "unknown (no version found)"
        version_str = version_match.group(1)
        version = parse_beads_version(version_str)

        if version < MIN_VERSION:
            return (
                False,
                False,
                f"Beads {version_str} too old (minimum: 0.37.0, recommended: 0.39.1+)",
            )
        if version < REC_VERSION:
            return (
                True,
                False,
                f"Beads {version_str} (recommended: 0.39.1+ for all features)",
            )
        return True, True, f"Beads {version_str}"
    except subprocess.TimeoutExpired:
        return True, True, "unknown (version check timed out)"
    except Exception:
        return True, True, "unknown (version check failed)"


def check_environment() -> list[str]:
    """Validate workflow environment prerequisites.

    Checks for required commands (bd, git, jq) and .beads directory.

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
    else:
        # Check bd version meets minimum requirements
        meets_min, meets_rec, version_msg = check_beads_version()
        if not meets_min:
            errors.append(
                f"{version_msg}\n   Upgrade: go install github.com/steveyegge/beads/cmd/bd@latest"
            )

    # Check git
    ok, _ = check_command("git")
    if not ok:
        errors.append("git not found. Install from https://git-scm.com/")

    # Check jq (required for JSON parsing in slash commands)
    ok, _ = check_command("jq")
    if not ok:
        errors.append("jq not found. Install from https://jqlang.github.io/jq/download/")

    # Check .beads directory
    if not Path(".beads").is_dir():
        errors.append("No .beads directory found.\n   Run: bd init -p <prefix>- --quiet")

    return errors


def precheck(command_name: str, interactive: bool = False) -> bool:
    """Run environment validation before a workflow command.

    Args:
        command_name: Name of command for error messages.
        interactive: If True, display instructions to fix issues (no auto-init).

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
        print(
            "\nTo initialize Beads, run:\n"
            "   bd init -p <prefix>- --quiet\n"
            "\n"
            "Replace <prefix> with a short project identifier (e.g., 'myproj-').",
            file=sys.stderr,
        )

    return False


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
    results = {"environment": {}, "beads": {}, "issues": {}, "git": {}, "overall": "HEALTHY"}

    # Environment checks
    for cmd in ["bd", "git", "jq"]:
        ok, version = check_command(cmd)
        results["environment"][cmd] = {"ok": ok, "version": version}
        if not ok and cmd in ["bd", "git"]:
            results["overall"] = "CRITICAL"

    # Check Beads version requirements
    if results["environment"]["bd"]["ok"]:
        meets_min, meets_rec, version_msg = check_beads_version()
        results["environment"]["bd"]["version_status"] = version_msg
        results["environment"]["bd"]["meets_minimum"] = meets_min
        results["environment"]["bd"]["meets_recommended"] = meets_rec
        if not meets_min:
            results["overall"] = "CRITICAL"
        elif not meets_rec and results["overall"] == "HEALTHY":
            results["overall"] = "DEGRADED"

    # Beads checks
    beads_dir = Path(".beads")
    results["beads"]["initialized"] = beads_dir.is_dir()

    if beads_dir.is_dir():
        db_path = beads_dir / "beads.db"
        results["beads"]["database_exists"] = db_path.exists()

        jsonl_path = beads_dir / "issues.jsonl"
        if jsonl_path.exists():
            with open(jsonl_path) as f:
                results["beads"]["jsonl_entries"] = sum(1 for _ in f)

        # Test bd commands
        try:
            test_result = _bd_json_simple("list", "--limit", "1")
            results["beads"]["commands_working"] = isinstance(test_result, list)
        except Exception:
            results["beads"]["commands_working"] = False
            results["overall"] = "DEGRADED"
    else:
        results["overall"] = "CRITICAL"

    # Issue counts
    if results["beads"].get("commands_working"):
        try:
            results["issues"]["open"] = len(_bd_json_simple("list", "--status", "open"))
            results["issues"]["in_progress"] = len(
                _bd_json_simple("list", "--status", "in_progress")
            )
            results["issues"]["closed"] = len(_bd_json_simple("list", "--status", "closed"))
            results["issues"]["ready"] = len(_bd_json_simple("ready"))
            results["issues"]["blocked"] = len(_bd_json_simple("blocked"))
            results["issues"]["stale"] = len(_bd_json_simple("stale", "--days", "7"))
        except Exception:
            pass

    # Git checks
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
        results["git"]["is_repo"] = result.returncode == 0
        if results["git"]["is_repo"]:
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
            results["git"]["branch"] = branch.stdout.strip()
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=SUBPROCESS_TIMEOUT,
            )
            results["git"]["uncommitted"] = (
                len(status.stdout.strip().split("\n")) if status.stdout.strip() else 0
            )
    except (FileNotFoundError, subprocess.TimeoutExpired):
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
        # Show version status for bd
        if cmd == "bd" and info["ok"] and "version_status" in info:
            if not info.get("meets_minimum"):
                print(f"   CRITICAL: {info['version_status']}")
            elif not info.get("meets_recommended"):
                print(f"   WARN: {info['version_status']}")

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
        print(
            f"   Working tree: {'CLEAN' if uncommitted == 0 else f'{uncommitted} uncommitted changes'}"
        )
    else:
        print("   Repository: NOT INITIALIZED")

    # Summary
    print()
    print("=== SUMMARY ===")
    print()
    print(f"Overall: {results['overall']}")


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
        args: Parsed arguments with optional 'json' flag.

    Returns:
        Exit code (0 if healthy, 1 otherwise).
    """
    results = run_health_check()
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_health_report(results)
    return 0 if results["overall"] == "HEALTHY" else 1


def main() -> int:
    """CLI entry point for workflow utilities.

    Parses command-line arguments and dispatches to appropriate handler.

    Returns:
        Exit code from the executed subcommand.
    """
    parser = argparse.ArgumentParser(
        prog="workflow", description="Agentic workflow utilities for Claude Code"
    )
    parser.add_argument("--version", action="version", version="0.2.0")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Precheck command
    p_precheck = subparsers.add_parser("precheck", help="Validate environment")
    p_precheck.add_argument("--name", help="Command name for messages")
    p_precheck.set_defaults(func=cmd_precheck)

    # Health command
    p_health = subparsers.add_parser("health", help="Run health diagnostics")
    p_health.add_argument("--json", action="store_true", help="Output as JSON")
    p_health.set_defaults(func=cmd_health)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
