# pydo Design Document

> **Brainstorming Output:** This document captures the design decisions made during collaborative brainstorming for the pydo CLI task manager.

**Goal:** Build a Python CLI task manager to validate the agentic workflow.

**Status:** Design complete, ready for implementation planning.

**Tech Stack:** Python 3.9+, Click, pytest, uv (package management), JSON file storage

---

## Design Decisions

### Language Choice

**Decision:** Python
**Rationale:** Universal, fast to write, excellent testing ecosystem (pytest), accessible to the widest audience. Focus on validating the workflow, not fighting the language.

### Project Type

**Decision:** CLI Task Manager
**Rationale:**

- Natural epic structure (add/list/complete/delete/persist)
- Real dependencies between components
- Multi-file by design (triggers brainstorming gate)
- Clear error scenarios for testing recovery
- Meta validation: using task tracker (Beads) to build task tracker

### Feature Scope

**Decision:** Standard (not minimal, not extended)
**Features:**

- `pydo add "description" [-p 1-3]` - Add task with optional priority
- `pydo list [--all|--done|--pending]` - List tasks with filters
- `pydo show <id>` - Show task details
- `pydo complete <id>` - Mark task complete
- `pydo delete <id>` - Delete task

**Rationale:** 5-6 tasks with natural dependencies, enough files to trigger brainstorming gate (>3), completable in one focused session.

### Storage Approach

**Decision:** Single JSON file at `~/.pydo/tasks.json`
**Rationale:** Simple, human-readable, easy to test. Still exercises real edge cases (missing file, corrupted JSON, first-run initialization).

### Testing Strategy

**Decision:** pytest with fixtures (unit + integration tests)
**Rationale:** Validates TDD workflow, demonstrates proper test isolation, good coverage target.

---

## Architecture

### Project Structure

```
pydo/
├── pydo/
│   ├── __init__.py       # Package init, version
│   ├── cli.py            # Click-based CLI entry point
│   ├── models.py         # Task dataclass
│   ├── storage.py        # JSON file persistence
│   └── exceptions.py     # Custom exceptions
├── tests/
│   ├── conftest.py       # Shared fixtures
│   ├── test_models.py    # Task model tests
│   ├── test_storage.py   # Storage layer tests
│   └── test_cli.py       # CLI integration tests
├── pyproject.toml        # Modern Python packaging
├── README.md             # Usage documentation
└── .gitignore
```

### Architecture Layers

1. **CLI Layer** (`cli.py`): Parses commands, validates input, calls storage
2. **Storage Layer** (`storage.py`): Handles JSON read/write, file creation
3. **Model Layer** (`models.py`): Task dataclass with validation
4. **Exception Layer** (`exceptions.py`): TaskNotFound, StorageError, etc.

### Dependencies

- `click` - CLI framework (cleaner than argparse)
- `pytest` - Testing
- No other external dependencies

### Package Management

- Use `uv` for all Python operations (NOT pip directly)
- Project setup: `uv init` or `uv sync`
- Running tests: `uv run pytest`
- Running CLI: `uv run pydo <command>`

---

## Data Model

### Task Schema

```python
@dataclass
class Task:
    id: str              # Short ID (e.g., "a1b2c3")
    description: str     # Task text
    priority: int        # 1 (high), 2 (medium), 3 (low)
    status: str          # "pending" | "completed"
    created_at: str      # ISO timestamp
    completed_at: str    # ISO timestamp or None
```

### Storage Format

```json
{
  "version": 1,
  "tasks": [
    {
      "id": "a1b2c3",
      "description": "Write documentation",
      "priority": 1,
      "status": "pending",
      "created_at": "2025-12-14T23:45:00Z",
      "completed_at": null
    }
  ]
}
```

---

## CLI Interface

### Commands

```bash
# Add a task (priority defaults to 2)
pydo add "Write documentation" -p 1
# Output: Created task [a1b2c3]: Write documentation (priority: high)

# List tasks (default: pending only)
pydo list
pydo list --all        # Include completed
pydo list --done       # Only completed

# Show task details
pydo show a1b2c3

# Complete a task
pydo complete a1b2c3
# Output: Completed task [a1b2c3]: Write documentation

# Delete a task
pydo delete a1b2c3
# Output: Deleted task [a1b2c3]
```

---

## Error Handling

### Exception Hierarchy

```python
class PydoError(Exception): pass       # Base exception
class TaskNotFoundError(PydoError): pass
class StorageError(PydoError): pass
class InvalidTaskError(PydoError): pass
```

### Edge Cases

| Scenario                   | Behavior                                          |
| -------------------------- | ------------------------------------------------- |
| First run (no ~/.pydo/)    | Create directory and empty tasks.json             |
| Corrupted JSON             | Clear error message, suggest backup recovery      |
| Task ID not found          | `TaskNotFoundError` with helpful message          |
| Empty description          | `InvalidTaskError`: "Description cannot be empty" |
| Invalid priority           | `InvalidTaskError`: "Priority must be 1, 2, or 3" |
| Complete already-completed | Idempotent - no error, just confirm               |
| Delete completed task      | Allowed - warn but proceed                        |

### Error Output Format

```bash
$ pydo complete xyz123
Error: Task 'xyz123' not found

$ pydo add ""
Error: Description cannot be empty

$ pydo add "Task" -p 5
Error: Priority must be 1, 2, or 3
```

---

## Test Strategy

### Fixtures (`conftest.py`)

```python
@pytest.fixture
def temp_storage(tmp_path):
    """Provides isolated storage directory for each test."""
    storage_dir = tmp_path / ".pydo"
    storage_dir.mkdir()
    return Storage(storage_dir)

@pytest.fixture
def sample_tasks(temp_storage):
    """Pre-populated storage with test tasks."""
    # Creates 3 tasks with different states
```

### Test Categories

**Unit Tests (`test_models.py`):**

- Task creation with defaults
- Task validation (empty description, invalid priority)
- Task completion updates timestamp
- Task serialization to/from dict

**Storage Tests (`test_storage.py`):**

- Save and load roundtrip
- First-run initialization
- Handle missing file gracefully
- Handle corrupted JSON

**CLI Integration Tests (`test_cli.py`):**

- Add task success/failure
- List with filters
- Complete existing/nonexistent
- Delete existing/nonexistent

### Coverage Target

90%+ on core logic (models, storage)

---

## Implementation Phases

This project validates **all 14 workflow commands** through a structured implementation sequence. Each phase exercises specific commands with clear trigger conditions and success criteria.

### Phase 0: Environment Setup

**Commands:** `/workflow-init`, `/workflow-health`, `/workflow-config`

| Step | Command                         | Action                               |
| ---- | ------------------------------- | ------------------------------------ |
| 1    | `/workflow-init`                | Initialize Beads with `pydo-` prefix |
| 2    | `/workflow-health`              | Verify environment ready             |
| 3    | `/workflow-config team-mode on` | Enable team sync flag                |

**Success Criteria:**

- `.beads/` directory exists with `beads.db`
- Health check passes with no errors
- Flag file `.claude/ccbw-flag-team-mode` exists

---

### Phase 1: Epic Creation

**Commands:** `/workflow-start`, `/workflow-track`

| Step | Command                                     | Action                                  |
| ---- | ------------------------------------------- | --------------------------------------- |
| 1    | `/workflow-start "Build pydo CLI"`          | Create epic, save ID (e.g., `pydo-abc`) |
| 2    | `/workflow-track docs/plans/pydo-design.md` | Convert design to tracked issues        |

**Success Criteria:**

- Epic created with ID like `pydo-abc`
- 7 child tasks created with sequential IDs (`pydo-abc.1` through `pydo-abc.7`)
- `bd list --parent $EPIC_ID --json` returns 7 issues

---

### Phase 2: Core Implementation (Tasks 1-5)

**Commands:** `/workflow-work`, `/workflow-check`, `/workflow-overview`, `/workflow-execute`

**Task Dependency Graph:**

```
Task 1: Project structure (no deps)
├── Task 2: models.py
├── Task 3: exceptions.py
│   └── Task 4: storage.py (depends: 2, 3)
│       └── Task 5: cli.py (depends: 4)
```

**Execution Options:**

_Option A: Task-by-task with `/workflow-work`_
| Task | Files | Checkpoint |
|------|-------|------------|
| 1 | `pyproject.toml`, directory structure | — |
| 2 | `pydo/models.py` | — |
| 3 | `pydo/exceptions.py` | `/workflow-check` |
| 4 | `pydo/storage.py` | `/workflow-overview $EPIC_ID --current` |
| 5 | `pydo/cli.py` | — |

_Option B: Full plan with `/workflow-execute`_

- Execute entire implementation plan with automated tracking
- Progress checkpoints built into execution flow

**Success Criteria:**

- All 5 core modules implemented
- `bd list --status closed --parent $EPIC_ID --json | jq '. | length'` returns 5
- `uv run pydo --help` displays command usage

---

### Phase 3: Ad-Hoc Discovery

**Command:** `/workflow-do`

**Trigger:** After Task 5, attempting `python -m pydo` fails with module execution error.

**Scenario:**

```bash
$ python -m pydo
/usr/bin/python: No module named pydo.__main__; 'pydo' is a package and cannot be directly executed
```

**Action:**

```
/workflow-do "Add __main__.py for python -m pydo support"
```

**Implementation:** Create `pydo/__main__.py`:

```python
"""Enable python -m pydo execution."""
from pydo.cli import main

if __name__ == "__main__":
    main()
```

**Success Criteria:**

- Ad-hoc task created outside original plan
- `python -m pydo --help` works
- Task closed with completion note

---

### Phase 4: Research Scenario

**Commands:** `/workflow-question-ask`, `/workflow-steer-research`

**Trigger:** During Task 6 (test suite), discover storage path isolation problem.

**Problem Statement:**
CLI integration tests need isolated storage per test run. However, `storage.py` hardcodes `~/.pydo/`. Running tests would corrupt the user's real task data.

**Step 1: Capture Research Question**

```
/workflow-question-ask "Storage path isolation for tests"
```

Question context:

- **Impact:** Tests cannot run safely without corrupting real data
- **Blocking:** Task 6 (test suite)
- **Research needed:** Environment variable pattern for path override

**Step 2: Resolve Research**

```
/workflow-steer-research
```

**Resolution:** Add `PYDO_HOME` environment variable support.

**Files Modified:**
| File | Change |
|------|--------|
| `storage.py` | Add env var check, accept path parameter in constructor |
| `cli.py` | Pass configured path to Storage |
| `conftest.py` | Set `PYDO_HOME` to `tmp_path` in fixtures |

**Success Criteria:**

- Research issue created and closed
- Task 6 unblocked
- Tests use isolated storage via `PYDO_HOME`

---

### Phase 5: Completion

**Command:** `/workflow-land`

**Remaining Tasks:**
| Task | Description | Notes |
|------|-------------|-------|
| 6 | Test suite | Now includes `PYDO_HOME` support from research |
| 7 | Documentation | README.md with usage examples |

**Session Completion:**

```
/workflow-land
```

**Process:**

1. Close completed tasks with completion notes
2. Verify all epic children closed
3. Sync Beads state (`bd sync --flush-only`)
4. Commit changes with conventional commit message
5. Prompt for merge/PR decision (feature branch)

**Success Criteria:**

- All 7+ tasks closed (original 7 plus ad-hoc)
- `bd list --status open --parent $EPIC_ID --json` returns empty array
- Feature branch ready for merge or PR

---

## Course Correction

**Command:** `/workflow-steer-correct`

**Availability:** Throughout all phases as contingency.

**When to Use:**

- Implementation diverges from plan
- Human spots incorrect approach mid-task
- Requirements change during implementation

**Process:**

1. Human describes divergence
2. Command identifies affected tasks
3. Creates P0 correction task
4. Updates/reopens affected tasks with blocking dependency
5. Correction surfaces first in `/workflow-work`

**Note:** This command validates the workflow's ability to handle mid-implementation course corrections. Trigger it when any task implementation diverges from the approved design.

---

## Workflow Validation Summary

All 14 workflow commands validated through pydo implementation:

| Command                    | Phase | Scenario    | Validation Point                     |
| -------------------------- | ----- | ----------- | ------------------------------------ |
| `/workflow-init`           | 0     | Setup       | Initialize Beads tracking            |
| `/workflow-health`         | 0     | Setup       | Verify environment ready             |
| `/workflow-config`         | 0     | Setup       | Enable team-mode flag                |
| `/workflow-start`          | 1     | Happy path  | Create epic for pydo                 |
| `/workflow-track`          | 1     | Happy path  | Convert design to tracked issues     |
| `/workflow-work`           | 2     | Happy path  | Claim and implement each task        |
| `/workflow-execute`        | 2     | Happy path  | Alternative full-plan execution      |
| `/workflow-check`          | 2     | Happy path  | Review status mid-implementation     |
| `/workflow-overview`       | 2     | Happy path  | View plan state at checkpoint        |
| `/workflow-do`             | 3     | Ad-hoc      | Create `__main__.py` when discovered |
| `/workflow-question-ask`   | 4     | Research    | Capture storage isolation question   |
| `/workflow-steer-research` | 4     | Research    | Resolve with `PYDO_HOME` solution    |
| `/workflow-land`           | 5     | Happy path  | Complete session properly            |
| `/workflow-steer-correct`  | Any   | Contingency | Course correct if divergence         |

---

## Next Steps

1. **Create implementation plan** from this design using `superpowers:writing-plans` skill
2. **Execute Phase 0** to initialize environment
3. **Execute Phase 1** to create epic and track work
4. **Implement Phases 2-5** following the validation sequence
5. **Document results** for each workflow command validation
