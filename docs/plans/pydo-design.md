# pydo Design Document

> **Brainstorming Output:** This document captures the design decisions made during collaborative brainstorming for the pydo CLI task manager.

**Goal:** Build a Python CLI task manager to validate the agentic workflow.

**Status:** Design complete, ready for implementation planning.

**Tech Stack:** Python 3.9+, Click, pytest, uv (package management), JSON file storage

---

## Design Decisions

### Language Choice
**Decision:** Python
**Rationale:** Universal, fast to write, excellent testing ecosystem (pytest), accessible to widest audience. Lets us focus on validating the workflow rather than fighting the language.

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

| Scenario | Behavior |
|----------|----------|
| First run (no ~/.pydo/) | Create directory and empty tasks.json |
| Corrupted JSON | Clear error message, suggest backup recovery |
| Task ID not found | `TaskNotFoundError` with helpful message |
| Empty description | `InvalidTaskError`: "Description cannot be empty" |
| Invalid priority | `InvalidTaskError`: "Priority must be 1, 2, or 3" |
| Complete already-completed | Idempotent - no error, just confirm |
| Delete completed task | Allowed - warn but proceed |

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

## Task Dependencies (for Beads)

Natural implementation order with dependencies:

```
Epic: Build pydo CLI task manager
├── Task 1: Set up project structure
│   └── No dependencies (first task)
├── Task 2: Implement models.py
│   └── depends on: Task 1
├── Task 3: Implement exceptions.py
│   └── depends on: Task 1
├── Task 4: Implement storage.py
│   └── depends on: Task 2, Task 3
├── Task 5: Implement cli.py
│   └── depends on: Task 4
├── Task 6: Write test suite
│   └── depends on: Task 5
└── Task 7: Documentation and polish
    └── depends on: Task 6
```

---

## Workflow Validation Points

This project exercises these workflow commands:

| Command | How pydo validates it |
|---------|----------------------|
| `/workflow-init` | Initialize fresh project |
| `/workflow-start` | Create epic for pydo |
| `/workflow-track` | Convert this design to issues |
| `/workflow-work` | Claim and implement tasks |
| `/workflow-execute` | Execute implementation plan |
| `/workflow-land` | Close session properly |
| `/workflow-check` | Review status mid-work |
| `/workflow-health` | Diagnose issues |

---

## Next Steps

1. Use this design document as input for implementation planning
2. Create implementation plan with `superpowers:writing-plans` skill
3. Execute plan with Beads tracking
4. Validate all workflow commands function correctly
