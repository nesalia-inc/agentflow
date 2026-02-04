# CLI Overview - v0.1.0

## Two-CLI Architecture

The AgentFlow CLI uses **two separate executables** for security:

### 1. `agentflow` - Human/CEO CLI

Full-featured CLI for human users with complete control:
- Create organizations, projects, roles, agents
- Assign tasks and manage everything
- View all tasks and agents
- **Requires human authentication** (email/password)

**Usage**:
```bash
agentflow <command> <subcommand> [flags]
```

### 2. `agentflow-agent` - Agent CLI

Restricted CLI for AI agents with limited permissions:
- View only assigned tasks
- Work on own tasks
- Cannot exit to CEO mode
- Cannot create/modify other agents
- **Authenticated via agent token**

**Usage**:
```bash
agentflow-agent --config <token-file> <command> [flags]
```

---

## Security Model

```
┌────────────────────────────────────────────────────────┐
│              agentflow (Human CLI)                     │
│  - Full CEO permissions                                │
│  - Can create/modify everything                        │
│  - Auth: email + password                              │
│  - Commands: org, project, role, agent, task create...│
└────────────────────────────────────────────────────────┘
                         │
                         │ agent launch (generates token)
                         ▼
┌────────────────────────────────────────────────────────┐
│           agentflow-agent (AI Agent CLI)               │
│  - Limited to agent's own tasks                        │
│  - Role-based permissions (level 1-10)                 │
│  - Auth: agent_id + api_token                          │
│  - Commands: task list/start/complete only             │
│  - NO exit, NO CEO commands                            │
└────────────────────────────────────────────────────────┘
```

### Why Two CLIs?

**Problem**: If agents could "exit" their mode, they could escalate privileges:

```bash
# Without two CLIs (INSECURE)
[acme/website]@Alice $ agentflow agent exit
✓ Back to CEO view
[acme/website] $ agentflow agent create --role "cto" --name "Eve"
✓ Agent created (Alice now has CEO powers!)
```

**Solution**: Separate CLIs prevent escalation:

```bash
# With two CLIs (SECURE)
$ agentflow-agent --config ~/.agentflow/agents/alice/token.json
→ Only agent commands available

$ agentflow-agent agent create --role "cto" --name "Eve"
→ Error: Command not available in agent CLI
```

---

## Command Availability

| Category | Human CLI | Agent CLI |
|----------|-----------|-----------|
| **Auth** | `register`, `login`, `logout`, `status` | `status` (token-based) |
| **Role** | `create`, `list`, `view`, `update`, `delete`, `add-document`, `list-documents`, `remove-document` | `view` (own only) |
| **Org** | `create`, `list`, `view`, `use`, `delete` | ❌ Not available |
| **Project** | `create`, `list`, `view`, `use`, `delete` | ❌ Not available |
| **Agent** | `create`, `list`, `view`, `update`, `delete`, `launch` | `stats` (own only) |
| **Version** | `create`, `list`, `view`, `release`, `delete` | ❌ Not available |
| **Task** | `create`, `list`, `view`, `start`, `complete`, `block`, `unblock`, `assign`, `update`, `delete` | `list`, `view`, `start`, `complete`, `block`, `unblock` (own only) |
| **Context** | `use` (combined org+project) | Built-in (from token) |

---

## Role Hierarchy System

### Authority Levels (1-10)

Each role has an **authority level** that determines what it can do:

| Level | Type | Capabilities |
|-------|------|---------------|
| **1-2** | Junior | Basic tasks, cannot create other agents |
| **3-4** | Senior | Complex tasks, can create level 1-2 agents |
| **5-6** | Lead | Can manage juniors, review work |
| **7-8** | Architect | Strategic decisions, code review |
| **9-10** | C-Level | Full organizational control |

### Level-Based Restrictions

**Agents cannot**:
- Work on tasks with `required_level` > their level
- Create agents with higher level than their own
- Modify agents with higher level than their own
- View tasks above their level

**Example**:
```bash
# Alice (Level 3) tries to work on Level 5 task
$ agentflow-agent task start --task-id "task_migration"
→ Error: Task requires authority level 5. Your level: 3.

# Alice tries to create Level 5 agent
$ agentflow-agent agent create --role "tech-lead" --name "Eve"
→ Error: Command not available in agent CLI
```

---

## Design Principles

### 1. 100% Non-Interactive

All operations use flags/arguments, no prompts:

```bash
# WRONG (interactive)
$ agentflow org create
→ Name: [user types]

# RIGHT (non-interactive)
$ agentflow org create --name "Acme Corp" --slug "acme"
```

### 2. Explicit Flags

All parameters passed via flags:

```bash
# Good
agentflow task create --title "Fix bug" --priority "P0"

# Bad
agentflow task create "Fix bug" "P0"
```

### 3. JSON-First Output

All commands return structured JSON:

```json
{
  "success": true,
  "data": { /* ... */ },
  "metadata": { /* ... */ }
}
```

### 4. Security-First

- Two-CLI separation prevents privilege escalation
- Role levels limit agent capabilities
- Tokens expire and have explicit permissions
- No way to "exit" agent CLI to CEO mode

### 5. Agent-Friendly

AI agents can execute commands without:
- Waiting for interactive prompts
- Parsing human-friendly tables
- Handling ambiguous inputs

---

## Prompt Display

### Human CLI

```bash
# User mode (default)
[acme/website] $

# With version context
[acme/website@1.0.0] $
```

### Agent CLI

Agent CLI has no context prompt - it reads everything from the token file:

```bash
$ agentflow-agent --config ~/.agentflow/agents/alice/token.json task list
```

The token contains all context (org, project, role, permissions).

---

## Output Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `json` | Structured JSON (default) | Parsing, automation |
| `table` | Human-readable ASCII table | Human viewing |
| `csv` | CSV format | Data export |
| `raw` | IDs only | Scripting/piping |

**Example**:
```bash
agentflow org list --format json   # Default
agentflow org list --format table  # Human readable
agentflow org list --format csv    # Export
```

---

## Next Steps

- See [`response-format.md`](./response-format.md) for JSON structure details
- See [`authentication.md`](./authentication.md) to get started
- See [`workflow.md`](./workflow.md) for complete example
