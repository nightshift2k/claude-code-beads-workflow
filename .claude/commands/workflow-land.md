---
argument-hint:
description: Complete a work session properly with local synchronization
---

## Intent

Close a work session with all state persisted and no orphaned work.

## When to Use

- Finishing any work session (required before stopping)
- Completed one or more tasks
- Pausing to resume later
- Switching to a different project

## When NOT to Use

- Mid-task (complete current task first)
- Want to continue working → use `/workflow-work`
- Just checking status → use `/workflow-check`

## Context Required

Run environment precheck first:

```bash
uv run python .claude/lib/workflow.py precheck --name workflow-land
```

## Decision Framework

| State                      | Action                             | Outcome              |
| -------------------------- | ---------------------------------- | -------------------- |
| Discovered follow-up work  | Create Beads issues first          | All work tracked     |
| Tasks completed            | Close with `--reason`              | Clean completion     |
| Tasks in progress          | Update with `--notes`              | Progress captured    |
| Code changes made          | Run quality gates                  | Tests/lint pass      |
| Task descriptions modified | Consider `/workflow-steer-correct` | Steering log updated |
| Team mode enabled          | Use `bd sync`                      | Full git sync        |
| Solo mode (default)        | Use `bd sync --flush-only`         | JSONL export only    |
| Uncommitted changes        | Git commit                         | State persisted      |

## Work Completion Detection

Determine whether current work is complete before closing a session.

### Context Required

| Query              | Command                                                                 | Purpose           |
| ------------------ | ----------------------------------------------------------------------- | ----------------- |
| In-progress epic   | `bd list --type epic --status in_progress --json`                       | Find active epic  |
| Epic children      | `bd list --json \| jq '[.[] \| select(.id \| startswith("EPIC_ID."))]'` | Count child tasks |
| Open issues        | `bd list --status open --json`                                          | Ad-hoc work check |
| In-progress issues | `bd list --status in_progress --json`                                   | Active work check |

### Completion Decision Framework

| Work Context                     | Completion Signal                 | Result     |
| -------------------------------- | --------------------------------- | ---------- |
| Epic exists, all children closed | Total children == Closed children | Complete   |
| Epic exists, children remain     | Total children > Closed children  | Incomplete |
| No epic, no open issues          | `open == 0 && in_progress == 0`   | Complete   |
| No epic, issues remain           | `open > 0 \|\| in_progress > 0`   | Incomplete |

### Routing by Result

| Result     | Next Action                                         |
| ---------- | --------------------------------------------------- |
| Complete   | Prompt: close epic, merge branch, create PR         |
| Incomplete | Show remaining work, confirm intentional early exit |

### Edge Considerations

- **Multiple in-progress epics**: Evaluate each, report mixed state
- **Blocked issues**: Count as incomplete (work remains)
- **Deferred issues**: Exclude from completion count (intentionally parked)
- **Pinned issues**: Exclude from completion count (persistent references)

## Environment Detection

Detect remote and branch state to guide persistence operations.

### Persistence Decision Framework

| Remote | Branch     | Work State | Persistence Action   |
| ------ | ---------- | ---------- | -------------------- |
| Yes    | main       | Complete   | Commit + push        |
| Yes    | main       | Incomplete | Commit + push + warn |
| Yes    | feature/\* | Complete   | Prompt: merge or PR  |
| Yes    | feature/\* | Incomplete | Commit + push branch |
| No     | any        | any        | Commit only (local)  |

### Edge Considerations

- **Multiple remotes**: Use `origin` as default
- **Detached HEAD**: Warn, skip branch-specific logic
- **Uncommitted changes**: Prompt before git operations

## Branch Handling

Handle branch operations based on work state, remote presence, and branch protection.

### Context Required

| Query            | Source                                      |
| ---------------- | ------------------------------------------- |
| Protected branch | `.claude/ccbw-flag-protected-branch` exists |
| Existing PR      | `gh pr list --head <branch> --state open`   |

### Branch Decision Framework

| Branch  | Remote | Work       | Protected | Action                           |
| ------- | ------ | ---------- | --------- | -------------------------------- |
| main    | No     | any        | -         | Commit only                      |
| main    | Yes    | any        | -         | Commit + push                    |
| feature | No     | Complete   | -         | Merge to main, delete branch     |
| feature | No     | Incomplete | -         | Commit, stay on branch           |
| feature | Yes    | Complete   | No        | Push, merge, delete local+remote |
| feature | Yes    | Complete   | Yes       | Push, mark PR ready (or create)  |
| feature | Yes    | Incomplete | No        | Push, stay on branch             |
| feature | Yes    | Incomplete | Yes       | Push, create/update draft PR     |

### Edge Considerations

- **Merge conflicts**: Abort merge, report to user, require manual resolution
- **PR creation fails**: Log error, continue with push (work not lost)
- **Fast-forward not possible**: Use merge commit
- **Branch already deleted**: Skip deletion step

## PR Generation from Beads

Generate PR title and body from Beads epic/issue context.

### PR Decision Framework

| Context     | PR Type | Title Source                 | Body Content                       |
| ----------- | ------- | ---------------------------- | ---------------------------------- |
| Epic exists | Ready   | Epic title                   | Summary + task checklist (all [x]) |
| Epic exists | Draft   | "WIP: " + epic title         | Progress checklist + X/Y status    |
| No epic     | Ready   | "Bug fixes and improvements" | Closed issue list                  |
| No epic     | Draft   | N/A (no draft for ad-hoc)    | -                                  |

### PR Body Templates

**Ready PR (epic complete):**

```markdown
## Summary

[Epic description]

## Changes

- [x] Task 1 (epic-abc.1)
- [x] Task 2 (epic-abc.2)

## Beads Tracking

Epic: epic-abc
```

**Draft PR (epic in progress):**

```markdown
## WIP: Work in Progress

### Progress

- [x] Completed task (epic-abc.1)
- [ ] Pending task (epic-abc.2)

### Status

1/2 tasks complete. Work continues next session.

### Beads Tracking

Epic: epic-abc
```

### Edge Considerations

- **Empty epic description**: Use "No description"
- **No closed tasks in draft**: Show all as pending
- **gh CLI not available**: Skip PR, report error, push succeeds

**Implementation**: See [Reference Commands](#reference-commands) for jq patterns to extract epic description and generate task checklists.

## Conflict Handling

Handle merge conflicts with automatic resolution for Beads, manual guidance for code.

### Conflict Decision Framework

| Conflict Type | Detection            | Resolution                | Outcome                |
| ------------- | -------------------- | ------------------------- | ---------------------- |
| None          | Exit 0               | Continue                  | Proceed with push      |
| Beads only    | Only `.beads/` files | Auto-merge via `bd merge` | Continue after resolve |
| Code only     | Non-Beads files      | Stop, show instructions   | User resolves manually |
| Mixed         | Both Beads + code    | Stop, show instructions   | User resolves all      |

### Execution

1. Attempt `git pull --rebase`
2. On conflict, classify files by path
3. If Beads-only: auto-resolve with `bd merge`
4. If code involved: stop with clear instructions

### Edge Considerations

- **`bd merge` fails**: Fall back to manual resolution
- **Partial Beads conflict**: Treat as mixed (user intervention required)
- **Rebase already in progress**: Detect with `git status`, guide completion

## Stash Warning

Warn about stash entries. The auto-cleanup flag clears them automatically.

### Stash Decision Framework

| Stash       | Auto-cleanup Flag | Action                     |
| ----------- | ----------------- | -------------------------- |
| Empty       | any               | Skip (nothing to report)   |
| Has entries | Off (default)     | Warn with count and list   |
| Has entries | On                | Clear stash, prune remotes |

### Context Required

| Query             | Source                                  |
| ----------------- | --------------------------------------- |
| Stash count       | `git stash list \| wc -l`               |
| Auto-cleanup flag | `.claude/ccbw-flag-auto-cleanup` exists |

### Edge Considerations

- **Large stash**: Show first 5 entries, summarize rest
- **Stash clear fails**: Log warning, continue (not blocking)

## Completion Checklist (MANDATORY)

| Step | Requirement                 | Why                       |
| ---- | --------------------------- | ------------------------- |
| 1    | File follow-up work         | No orphaned discoveries   |
| 2    | Review issue status         | Know what to close/update |
| 3    | Close completed issues      | Clean tracking state      |
| 4    | Update in-progress issues   | Progress documented       |
| 5    | Run quality gates (if code) | No broken builds          |
| 6    | Persist changes             | State survives session    |
| 7    | Git commit                  | Local history preserved   |

## Execution

1. Create Beads issues for any discovered follow-up work
2. Review current status (closed, in-progress, open)
3. Close completed issues with specific reasons
4. Update in-progress issues with progress notes
5. Run quality gates if code was changed
6. Check team-mode flag, run appropriate sync
7. Commit Beads state and any code changes
8. Identify next available work (optional)

## Success Criteria

- [ ] All follow-up work filed as issues
- [ ] Completed issues closed with reasons
- [ ] In-progress issues have status notes
- [ ] Quality gates pass (if code changed)
- [ ] `.beads/issues.jsonl` updated
- [ ] Git commit created
- [ ] No orphaned or untracked work

## Edge Considerations

- **Log validation**: If task descriptions modified without steering commands, add CORRECT entry
- **Sync verification**: If DB count ≠ JSONL count, run `bd import --force` first
- **Sandbox mode**: Claude Code sandboxed environments require `bd sync --flush-only`
- **Team override**: Solo user on team project can run `bd sync` manually
- **Sync failure**: Check `.beads/` permissions, use `bd export` as backup

## Reference Commands

```bash
# Environment precheck
uv run python .claude/lib/workflow.py precheck --name workflow-land

# Work completion detection
# Find in-progress epic
bd list --type epic --status in_progress --json | jq -r '.[0].id // empty'

# Count child tasks for epic (replace EPIC_ID with actual ID)
bd list --json | jq --arg epic "EPIC_ID" '[.[] | select(.id | startswith($epic + "."))] | length'

# Count closed children
bd list --status closed --json | jq --arg epic "EPIC_ID" '[.[] | select(.id | startswith($epic + "."))] | length'

# Ad-hoc work check (no epic context)
bd list --status open --json | jq 'length'
bd list --status in_progress --json | jq 'length'

# Environment detection
# Check for git remote
git remote -v | grep -q . && echo "Remote exists" || echo "No remote"

# Get current branch
git branch --show-current

# Check for detached HEAD
git symbolic-ref -q HEAD || echo "Detached HEAD"

# Branch handling
# Check for protected branch flag
test -f .claude/ccbw-flag-protected-branch && echo "Protected" || echo "Not protected"

# Check for existing PR
gh pr list --head "$(git branch --show-current)" --state open --json number --jq '.[0].number // empty'

# Merge patterns
git merge "$BRANCH" --ff-only || git merge "$BRANCH" -m "Merge $BRANCH"

# PR operations
gh pr ready "$PR_NUMBER"                          # Mark draft as ready
gh pr create --draft --title "..." --body "..."   # Create draft PR

# Branch cleanup (after merge)
git branch -d "$BRANCH"                           # Delete local
git push origin --delete "$BRANCH" 2>/dev/null || true  # Delete remote

# PR generation from Beads
# Get epic description
bd show "$EPIC_ID" --json | jq -r '.[0].description // "No description"'

# Generate task checklist with status
bd list --json | jq --arg epic "$EPIC_ID" -r '
  .[] | select(.id | startswith($epic + ".")) |
  "- \(if .status == "closed" then "[x]" else "[ ]" end) \(.title) (\(.id))"'

# Create ready PR
gh pr create --title "$TITLE" --body "$BODY" --base main

# Create draft PR
gh pr create --draft --title "WIP: $TITLE" --body "$BODY" --base main

# Conflict handling
# Detect conflicted files
git diff --name-only --diff-filter=U

# Check if only Beads files conflicted
git diff --name-only --diff-filter=U | grep -v '^\.beads/' && echo "Code conflicts" || echo "Beads only"

# Auto-resolve Beads JSONL
git show :1:.beads/issues.jsonl > /tmp/base.jsonl
git show :2:.beads/issues.jsonl > /tmp/ours.jsonl
git show :3:.beads/issues.jsonl > /tmp/theirs.jsonl
bd merge .beads/issues.jsonl /tmp/base.jsonl /tmp/ours.jsonl /tmp/theirs.jsonl
git add .beads/issues.jsonl
git rebase --continue

# Stash warning
# Count and list stash
git stash list | wc -l
git stash list --oneline | head -5

# Check auto-cleanup flag
test -f .claude/ccbw-flag-auto-cleanup && echo "Auto-cleanup enabled" || echo "Manual mode"

# Clear stash (with flag only)
git stash clear

# Prune remotes (with flag only)
git remote prune origin

# File follow-up work (simple)
bd create "Follow-up task" --description="Brief context" -t task -p [priority] --json

# File follow-up work (complex content - REQUIRED for code blocks)
cat > /tmp/followup.md <<'EOF'
[Full task content with code examples]
EOF
bd create "Follow-up task" --body-file /tmp/followup.md -t task -p [priority] --json

# Review status (run separately, not chained)
bd list --status closed --json | jq -r '.[] | "[\(.id)] \(.title)"'
bd list --status in_progress --json | jq -r '.[] | "[\(.id)] \(.title)"'
bd list --status open --json | jq -r '.[] | "[\(.id)] \(.title)"'

# Close completed work (--suggest-next shows newly unblocked)
bd close [issue-id] --reason "Completed: [specific reason]" --suggest-next --json

# Update in-progress issues
bd update [issue-id] --notes "[progress update]" --json

# Sync verification
bd list --json | jq '. | length'
jq -s 'length' .beads/issues.jsonl

# Sync (team mode)
bd sync

# Sync (solo mode - default)
bd sync --flush-only

# Git commit (Beads state only)
git add .beads/issues.jsonl && git commit -m "chore(workflow): sync Beads state"

# Git commit (with code changes)
git add . && git commit -m "chore(workflow): sync session - [summary]"

# Next work
bd ready --json | jq -r '.[] | "[\(.id)] P\(.priority) \(.title)"'

# Troubleshooting: sync fails
ls -la .beads/
test -w .beads/issues.jsonl && echo "Writable" || echo "Not writable"
bd export > .beads/issues.jsonl.backup
```

## Team Mode Configuration

| Flag File                            | Behavior          | Sync Command           |
| ------------------------------------ | ----------------- | ---------------------- |
| `.claude/ccbw-flag-team-mode` exists | Full git sync     | `bd sync`              |
| Flag absent (default)                | JSONL export only | `bd sync --flush-only` |

## Related Files

- @CLAUDE.md - Main workflow instructions
- @.claude/rules/ai-native-instructions.md - Execution principles
- @.claude/rules/beads-patterns.md - --body-file requirement
- @.claude/rules/git-conventions.md - Commit message format
- @.claude/commands/workflow-work.md - Task execution
- @.claude/commands/workflow-check.md - Status review
