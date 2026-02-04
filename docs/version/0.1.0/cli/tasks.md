# Task Commands

Create and manage tasks within project versions.

---

## Commands

- [`create`](#agentflow-task-create) - Create a new task
- [`list`](#agentflow-task-list) - List tasks
- [`view`](#agentflow-task-view) - View task details
- [`start`](#agentflow-task-start) - Mark task as in progress
- [`complete`](#agentflow-task-complete) - Mark task as completed
- [`block`](#agentflow-task-block) - Report a blocker
- [`unblock`](#agentflow-task-unblock) - Remove blocker
- [`assign`](#agentflow-task-assign) - Assign task to agent
- [`add-relation`](#agentflow-task-add-relation) - Add relationship between tasks
- [`remove-relation`](#agentflow-task-remove-relation) - Remove relationship
- [`relations`](#agentflow-task-relations) - View task relationships
- [`update`](#agentflow-task-update) - Update task properties
- [`delete`](#agentflow-task-delete) - Delete a task

---

## `agentflow task create`

Create a new task.

```bash
agentflow task create \
  --org <slug> \
  --project <slug> \
  --version <version> \
  --title <title> \
  [--description <description>] \
  [--type <type>] \
  [--priority <priority>] \
  [--required-level <level>] \
  [--tags <tags>] \
  [--agent <agent-id>]
```

**Flags**:
- `--version`: Version number
- `--title` (required): Task title
- `--description`: Task description
- `--type`: development|bug|review|testing
- `--priority`: P0|P1|P2|P3
- `--required-level`: Authority level required (1-10)
- `--tags`: Comma-separated tags
- `--agent`: Agent ID to assign

**With active context**:
```bash
agentflow task create \
  --title "Fix navigation bug" \
  --priority "P0" \
  --required-level 2
```

---

## `agentflow task list`

```bash
agentflow task list \
  [--org <slug>] \
  [--project <slug>] \
  [--version <version>] \
  [--status <status>] \
  [--priority <priority>] \
  [--agent <agent-id>]
```

---

## `agentflow task assign`

```bash
agentflow task assign \
  --task-id <task-id> \
  --agent <agent-id>
```

---

## Examples

```bash
# Create level 1 task (anyone can do)
agentflow task create \
  --title "Fix typo" \
  --priority "P3" \
  --required-level 1

# Create level 5 task (leads only)
agentflow task create \
  --title "Database migration" \
  --priority "P0" \
  --required-level 5

# Assign to agent
agentflow task assign --task-id "task_123" --agent "agent_alice"
```

---

## `agentflow task add-relation`

Add a relationship between two tasks.

```bash
agentflow task add-relation \
  --task-id <task-id> \
  --related-to <related-task-id> \
  --type <type>
```

**Flags**:
- `--task-id` (required): Source task ID
- `--related-to` (required): Target task ID
- `--type` (required): Relationship type

**Relationship Types**:
| Type | Description |
|------|-------------|
| `blocks` | This task blocks the other task |
| `blocked_by` | This task is blocked by the other task |
| `depends_on` | This task depends on the other task |
| `depended_on_by` | The other task depends on this task |
| `relates_to` | General relationship between tasks |
| `duplicates` | This task duplicates the other task |
| `is_duplicated_by` | This task is duplicated by the other task |
| `parent_of` | This task is a parent of the other (subtask) |
| `child_of` | This task is a subtask of the other |

**Examples**:
```bash
# Task A blocks Task B
agentflow task add-relation \
  --task-id "task_a" \
  --related-to "task_b" \
  --type "blocks"

# Task C depends on Task D
agentflow task add-relation \
  --task-id "task_c" \
  --related-to "task_d" \
  --type "depends_on"

# Link related tasks
agentflow task add-relation \
  --task-id "task_frontend" \
  --related-to "task_backend" \
  --type "relates_to"
```

---

## `agentflow task remove-relation`

Remove a relationship between two tasks.

```bash
agentflow task remove-relation \
  --task-id <task-id> \
  --related-to <related-task-id>
```

**Example**:
```bash
agentflow task remove-relation \
  --task-id "task_a" \
  --related-to "task_b"
```

---

## `agentflow task relations`

View all relationships for a task.

```bash
agentflow task relations --task-id <task-id>
```

**Response**:
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "task_a",
      "title": "Build homepage"
    },
    "relations": [
      {
        "type": "blocks",
        "related_task": {
          "id": "task_b",
          "title": "Deploy to production"
        }
      },
      {
        "type": "depends_on",
        "related_task": {
          "id": "task_c",
          "title": "Design mockups"
        }
      }
    ]
  }
}
```
