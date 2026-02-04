# Agent CLI (`agentflow-agent`)

The agent CLI is a separate, restricted executable that agents use to perform their tasks. It has no CEO commands and cannot "exit" to a higher privilege level.

---

## Usage

```bash
agentflow-agent --config <token-file> <command> [flags]
```

Or with environment variable:
```bash
export AGENTFLOW_TOKEN_FILE=~/.agentflow/agents/agent_xyz789/token.json
agentflow-agent <command> [flags]
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `status` | Show agent status and permissions |
| `task list` | List own tasks only |
| `task view` | View task details |
| `task start` | Start working on a task |
| `task complete` | Complete a task |
| `task block` | Report a blocker |
| `task unblock` | Remove blocker |
| `role view` | View own role and documents |
| `agent stats` | View own performance stats |

---

## Commands

### `agentflow-agent status`

```bash
$ agentflow-agent status
```

**Response**:
```json
{
  "success": true,
  "data": {
    "agent": {
      "id": "agent_xyz789",
      "name": "Alice",
      "level": 3,
      "trust_score": 65
    },
    "role": {
      "name": "Frontend Developer",
      "slug": "frontend-dev"
    },
    "permissions": ["task:list:own", "task:start:own", "task:complete:own"],
    "restrictions": {
      "max_task_level": 3,
      "can_create_agents": false
    }
  }
}
```

### `agentflow-agent task list`

```bash
$ agentflow-agent task list
```

**Security**: Only shows tasks assigned to this agent

### `agentflow-agent task start`

```bash
$ agentflow-agent task start --task-id <task-id>
```

**Security Checks**:
- Task must be assigned to this agent OR unassigned
- Task `required_level` must be ≤ agent's level
- Cannot start tasks assigned to other agents

**Error Codes**:
- `TASK_LEVEL_TOO_HIGH`: Task requires higher authority level
- `ASSIGNED_TO_OTHER`: Task is assigned to another agent

### `agentflow-agent task complete`

```bash
$ agentflow-agent task complete --task-id <task-id> [--success <notes>]
```

### `agentflow-agent role view`

```bash
$ agentflow-agent role view --slug <slug>
```

**Security**: Can only view own role

---

## Unavailable Commands

These commands are **intentionally not available** in the agent CLI:

```bash
agentflow-agent agent create   # ❌ Not available
agentflow-agent org delete     # ❌ Not available
agentflow-agent task list --all  # ❌ Not available
agentflow-agent task assign    # ❌ Not available
```

---

## Examples

```bash
# Agent starts session
$ agentflow-agent --config ~/.agentflow/agents/alice/token.json

# Check status
$ agentflow-agent status

# List own tasks
$ agentflow-agent task list

# Start a task
$ agentflow-agent task start --task-id "task_123"

# Complete a task
$ agentflow-agent task complete --task-id "task_123" --success "Done"

# Exit
$ exit
```

---

## Security Model

The agent CLI enforces:

1. **No privilege escalation** - Cannot exit to CEO mode
2. **Level-based restrictions** - Cannot work on tasks above level
3. **Task ownership** - Only see/modify own tasks
4. **No CEO commands** - Cannot create orgs, projects, or other agents

This prevents agents from ever gaining full control, even if compromised.
