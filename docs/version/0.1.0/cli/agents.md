# Agent Commands (Human CLI)

Create and manage agents (instances of roles) in organizations/projects.

---

## Commands

- [`create`](#agentflow-agent-create) - Create a new agent
- [`list`](#agentflow-agent-list) - List agents
- [`view`](#agentflow-agent-view) - View agent details
- [`update`](#agentflow-agent-update) - Update agent properties
- [`delete`](#agentflow-agent-delete) - Delete an agent
- [`launch`](#agentflow-agent-launch) - Generate agent token for agent CLI

---

## `agentflow agent create`

Create a new agent (instance of a role in an organization/project).

```bash
agentflow agent create \
  --org <slug> \
  --role <slug> \
  --name <name> \
  [--project <slug>]
```

**Flags**:
- `--org`: Organization slug (optional if org active)
- `--role` (required): Role slug to instantiate
- `--name` (required): Agent name (e.g., "Alice", "Bob")
- `--project`: Project slug (optional, if not specified agent is org-level)

**Organization-level agent**:
```bash
agentflow agent create \
  --org "acme" \
  --role "frontend-dev" \
  --name "Alice"
```

**Project-level agent**:
```bash
agentflow agent create \
  --org "acme" \
  --project "website" \
  --role "frontend-dev" \
  --name "Bob"
```

**With active context**:
```bash
agentflow org use --slug "acme"
agentflow agent create --role "frontend-dev" --name "Alice"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "agent": {
      "id": "agent_xyz789",
      "agent_code": "AG-001",
      "organization_id": "org_123",
      "project_id": null,
      "role_id": "role_abc123",
      "name": "Alice",
      "level": 3,
      "status": "active",
      "trust_score": 50,
      "role": {
        "id": "role_abc123",
        "name": "Frontend Developer",
        "slug": "frontend-dev"
      },
      "created_at": "2025-02-03T10:00:00Z"
    }
  },
  "message": "Agent created: Alice (Frontend Developer)"
}
```

**Error Codes**:
- `ORG_NOT_SET`: No active org and --org not provided
- `ROLE_NOT_FOUND`: Role does not exist
- `INVALID_ROLE`: Role belongs to different user

---

## `agentflow agent list`

List agents in an organization or project.

```bash
agentflow agent list \
  [--org <slug>] \
  [--project <slug>] \
  [--format <format>]
```

**Response**:
```json
{
  "success": true,
  "data": {
    "organization": {
      "id": "org_123",
      "name": "Acme Corp",
      "slug": "acme"
    },
    "project": {
      "id": "proj_123",
      "name": "Website Redesign",
      "slug": "website"
    },
    "agents": [
      {
        "id": "agent_xyz789",
        "agent_code": "AG-001",
        "name": "Alice",
        "level": 3,
        "status": "active",
        "trust_score": 65,
        "role": {
          "name": "Frontend Developer",
          "slug": "frontend-dev"
        },
        "assigned_task_count": 3,
        "completed_task_count": 12
      }
    ],
    "total": 1
  }
}
```

---

## `agentflow agent view`

View agent details.

```bash
agentflow agent view \
  --org <slug> \
  --agent <agent-id>
```

**Response**:
```json
{
  "success": true,
  "data": {
    "agent": {
      "id": "agent_xyz789",
      "agent_code": "AG-001",
      "name": "Alice",
      "level": 3,
      "status": "active",
      "trust_score": 65,
      "created_at": "2025-02-03T10:00:00Z"
    },
    "organization": {
      "id": "org_123",
      "name": "Acme Corp",
      "slug": "acme"
    },
    "project": {
      "id": "proj_123",
      "name": "Website Redesign",
      "slug": "website"
    },
    "role": {
      "id": "role_abc123",
      "name": "Frontend Developer",
      "slug": "frontend-dev",
      "level": 3,
      "description": "Expert React, TypeScript et UX"
    },
    "role_documents": [
      {
        "id": "doc_123",
        "title": "React Best Practices",
        "content": "# React Best Practices..."
      }
    ],
    "assigned_tasks": [
      {
        "id": "task_abc123",
        "title": "Build homepage",
        "status": "in_progress",
        "priority": "P0",
        "version": "1.0.0"
      }
    ],
    "stats": {
      "total_assigned": 15,
      "completed": 12,
      "in_progress": 2,
      "blocked": 1,
      "completion_rate": 0.8
    }
  }
}
```

---

## `agentflow agent update`

Update agent properties.

```bash
agentflow agent update \
  --org <slug> \
  --agent <agent-id> \
  [--name <name>] \
  [--status <status>]
```

**Flags**:
- `--org`: Organization slug
- `--agent` (required): Agent ID
- `--name`: New name
- `--status`: New status (active|inactive|probation)

---

## `agentflow agent delete`

Delete an agent.

```bash
agentflow agent delete \
  --org <slug> \
  --agent <agent-id> \
  --confirm
```

**Error Codes**:
- `HAS_ASSIGNED_TASKS`: Agent has assigned tasks (must reassign first)

---

## `agentflow agent launch`

Generate an agent token for the agent CLI to use. This is the secure way to allow an agent to work.

```bash
agentflow agent launch \
  --agent <agent-id> \
  [--output <path>]
```

**Flags**:
- `--agent` (required): Agent ID or agent_code
- `--output`: Output path for token file

**Response**:
```json
{
  "success": true,
  "data": {
    "agent": {
      "id": "agent_xyz789",
      "name": "Alice",
      "level": 3
    },
    "token_file": "~/.agentflow/agents/agent_xyz789/token.json",
    "command": "agentflow-agent --config ~/.agentflow/agents/agent_xyz789/token.json"
  },
  "message": "Agent token generated"
}
```

**Token File Structure**:
```json
{
  "agent_id": "agent_xyz789",
  "agent_name": "Alice",
  "api_key": "ak_agent_live_abc123...",
  "base_url": "https://api.agentflow.io",
  "org": { "id": "org_123", "name": "Acme Corp", "slug": "acme" },
  "project": { "id": "proj_123", "name": "Website", "slug": "website" },
  "role": { "id": "role_abc123", "name": "Frontend Dev", "slug": "frontend-dev", "level": 3 },
  "permissions": ["task:list:own", "task:start:own", "task:complete:own"],
  "restrictions": {
    "max_task_level": 3,
    "can_create_agents": false
  }
}
```

See [`agent-cli.md`](./agent-cli.md) for agent CLI usage.

---

## Examples

```bash
# Create org-level agent
agentflow org use --slug "acme"
agentflow agent create --role "senior-dev" --name "Alice"

# Create project-specific agent
agentflow agent create \
  --project "website" \
  --role "frontend-dev" \
  --name "Bob"

# Launch agent
agentflow agent launch --agent "agent_xyz789"

# Agent uses agent CLI
agentflow-agent --config ~/.agentflow/agents/agent_xyz789/token.json task list
```
