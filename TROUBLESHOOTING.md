# Troubleshooting

## Environment Validation

All workflow commands validate the environment automatically. The precheck system guides you through resolution when issues occur.

**Manual precheck** (if needed):

```bash
uv run python .claude/lib/workflow.py precheck --name manual-check
```

## Version Requirements

This workflow requires specific Beads CLI versions for full functionality:

| Version         | Status          | Notes                                             |
| --------------- | --------------- | ------------------------------------------------- |
| < 0.37.0        | **Unsupported** | Missing `--parent` flags, workflow will fail      |
| 0.37.0 - 0.39.0 | Supported       | Core features work, some new commands unavailable |
| >= 0.39.1       | **Recommended** | All documented features available                 |

**Check your version:**

```bash
bd version
```

**Upgrade to latest:**

```bash
go install github.com/steveyegge/beads/cmd/bd@latest
# Or: brew upgrade steveyegge/tap/beads
```

The precheck automatically validates version requirements and warns if outdated.

---

## Common Error Messages and Solutions

### "bd: command not found"

**Symptom:**

```
/workflow-start "New feature"
bash: bd: command not found
```

**Cause:** Beads CLI not installed or not in PATH

**Solutions:**

1. **Install via Go:**

   ```bash
   go install github.com/steveyegge/beads/cmd/bd@latest
   ```

2. **Install via Homebrew (macOS):**

   ```bash
   brew install steveyegge/tap/beads
   ```

3. **Verify installation:**

   ```bash
   bd version
   which bd
   ```

4. **Add to PATH if needed:**

   ```bash
   export PATH="$PATH:$(go env GOPATH)/bin"
   # Add to ~/.bashrc or ~/.zshrc for persistence
   ```

**Reference:** [Beads Installation Guide](https://github.com/steveyegge/beads/blob/main/docs/INSTALLING.md)

---

### "no .beads directory found"

**Symptom:**

```
bd ready
Error: no .beads directory found
```

**Cause:** Project not initialized with Beads tracking

**Solutions:**

1. **Initialize automatically (workflow commands do this):**

   ```
   /workflow-start "First feature"
   # Will prompt to initialize
   ```

2. **Initialize manually:**

   ```bash
   bd init -p myproj- --quiet
   ```

3. **Verify initialization:**

   ```bash
   ls -la .beads/
   # Should show: beads.db, issues.jsonl, README.md, etc.
   ```

---

### "database out of sync with JSONL"

**Symptom:**

```
bd ready
Error: database out of sync with JSONL
```

**Cause:** Sandbox mode defaults to on for Claude Code compatibility.

**Solution:** Sandbox mode is enabled. If you see this error:

```bash
bd import --force
```

**Reference:** [Beads Troubleshooting - Sandboxed Environments](https://github.com/steveyegge/beads/blob/main/docs/TROUBLESHOOTING.md#sandboxed-environments)

---

### "merge conflict in .beads/issues.jsonl"

**Symptom:**

```
bd sync
Error: merge conflict in .beads/issues.jsonl
```

**Cause:** Same issue modified on different branches

**Solutions:**

1. **Use bd merge tool:**

   ```bash
   git show :1:.beads/issues.jsonl > base.jsonl
   git show :2:.beads/issues.jsonl > ours.jsonl
   git show :3:.beads/issues.jsonl > theirs.jsonl

   bd merge merged.jsonl base.jsonl ours.jsonl theirs.jsonl

   cp merged.jsonl .beads/issues.jsonl
   git add .beads/issues.jsonl
   git merge --continue
   ```

2. **Simple conflicts (different fields):**

   ```bash
   # Keep both changes (manual edit)
   # OR prefer one side:
   git checkout --ours .beads/issues.jsonl   # Keep your changes
   git checkout --theirs .beads/issues.jsonl # Keep their changes

   bd import --force
   git add .beads/issues.jsonl
   git merge --continue
   ```

**Reference:** [Beads Conflict Resolution](https://github.com/steveyegge/beads/blob/main/.agent/workflows/resolve-beads-conflict.md)

---

### "bd ready" returns no issues

**Symptom:**

```
/workflow-work
bd ready --json
[]
```

**Cause:** No unblocked work available

**Diagnostic Commands:**

```bash
# Check for blocked issues
bd blocked

# View all open issues
bd list --status open

# Check for stale issues
bd stale --days 7

# Visualize dependency graph for specific issue (requires issue-id)
bd graph [issue-id]

# Check dependency tree for specific issue
bd dep tree [issue-id]

# Detect circular dependencies
bd dep cycles
```

**Solutions:**

1. **If issues are blocked:**
   - Resolve blocking issues first
   - Or remove blocking dependencies: `bd dep remove [from-id] [to-id]`

2. **If no open issues:**
   - All work complete!
   - Create new work: `/workflow-start "Next feature"`

3. **If blocked by circular dependencies:**

   ```bash
   bd dep cycles  # Detect cycles
   bd dep remove [from-id] [to-id]  # Break cycle
   ```

---

### "Plan file not found after tracking"

**Expected behavior.** After `/workflow-track`, plan files are deleted.

**To view plan:**

```bash
/workflow-overview [epic-id] --full
```

---

### "Steering log is empty"

**Symptom:**

```
/workflow-overview myproj-abc --log
# Shows only INIT entry, no STEER/CORRECT
```

**Cause:** No steering events have occurred yet.

**If steering DID happen but isn't logged:**

- Use `/workflow-steer-correct` to add a CORRECT entry documenting the change

---

## Recovery Decision Tree

When something goes wrong, try these in order:

```
1. FIRST: bd doctor --fix (v0.38.0+)
   └─ Auto-repair common issues (recommended first step)

2. IF doctor fails: bd import --force
   └─ Rebuilds database from JSONL (fixes most sync issues)

3. IF import fails: bd reset
   └─ Complete database reset (keeps JSONL, faster than manual recovery)

4. IF still broken: Database Corruption Recovery (below)
   └─ Manual backup, reinitialize, reimport from JSONL

5. IF context issues: Session State Recovery (below)
   └─ Check in-progress issues, resume or reset status

6. LAST RESORT: Full Reset (below)
   └─ Backup everything, delete DB, start fresh
```

**Rule:** Never jump to Full Reset without trying simpler fixes first.

---

## Emergency Recovery Procedures

### Auto-Repair (v0.38.0+ - Recommended First)

```bash
# Automatically diagnose and fix common issues
bd doctor --fix

# Verify recovery
bd list --json | jq '. | length'
```

### Quick Reset (If Auto-Repair Fails)

```bash
# Reset database completely (keeps JSONL)
bd reset

# Verify recovery
bd list --json | jq '. | length'
```

Rebuilds the database from JSONL without manual steps.

### Database Corruption Recovery (Manual Method)

Use this if `bd doctor --fix` and `bd reset` both fail:

```bash
# 1. Verify corruption
sqlite3 .beads/*.db "PRAGMA integrity_check;"

# 2. Backup corrupted database
mkdir -p .beads/backup
mv .beads/*.db .beads/backup/

# 3. Recover from JSONL (use your project's prefix)
bd init -p myproj- --quiet
bd import --force

# 4. Verify recovery
bd list --json | jq '. | length'
```

### Session State Recovery After Interruption

```bash
# 1. Check for in-progress issues
bd list --status in_progress

# 2. Review state
bd show [issue-id]

# 3. Resume work
/workflow-work
# Select the in-progress issue

# 4. Or mark as open and re-prioritize
bd update [issue-id] --status open
```

### Full Reset (Nuclear Option)

Only use when other recovery methods fail:

```bash
# 1. Backup everything
cp -r .beads .beads.backup-$(date +%s)

# 2. Remove database
rm .beads/*.db

# 3. Reinitialize (use your project's prefix)
bd init -p myproj- --quiet

# 4. Reimport from JSONL
bd import --force

# 5. Verify
bd list --json | jq '. | length'
```

---

## Quick Reference

| Problem                  | Solution                                                                       |
| ------------------------ | ------------------------------------------------------------------------------ |
| Lost work (sandbox)      | `bd sync --flush-only` then check .beads/issues.jsonl                          |
| JSONL conflicts          | Use `bd merge` tool                                                            |
| Database out of sync     | `bd import --force` then `bd reset` if needed                                  |
| Multi-machine sync       | `bd sync` (full git sync)                                                      |
| Confusing dependencies   | `bd graph [issue-id]` for visualization, `bd dep tree [id]` for specific issue |
| Circular dependencies    | `bd dep cycles` to detect, `bd dep remove` to break                            |
| Stale issues             | `bd stale --days 7`                                                            |
| Database corruption      | `bd doctor --fix` (auto-repair) or `bd reset` (full rebuild)                   |
| Sandbox mode issues      | Auto-detected since v0.21.1; use `bd import --force` if sync issues            |
| Find database location   | `bd where`                                                                     |
| Orphaned issues          | `bd orphans`                                                                   |
| Move issue to new parent | `bd update [id] --parent [new-parent-id]`                                      |

### New Statuses

| Status     | Purpose                     | Usage                              |
| ---------- | --------------------------- | ---------------------------------- |
| `deferred` | Icebox (not ready for work) | `bd update [id] --status deferred` |

---

## Getting Additional Help

**Beads Documentation:**

- [Beads Troubleshooting](https://github.com/steveyegge/beads/blob/main/docs/TROUBLESHOOTING.md)
- [Beads Error Handling](https://github.com/steveyegge/beads/blob/main/docs/ERROR_HANDLING.md)
