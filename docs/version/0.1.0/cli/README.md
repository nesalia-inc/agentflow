# CLI Specification - v0.1.0

**Version**: 0.1.0-pre
**Date**: 2025-02-03
**Status**: Draft
**Author**: AgentFlow Team

---

## Overview

This specification describes the **agent-first CLI interface** for AgentFlow v0.1.0. The system uses **two separate CLIs** for security:

- **`agentflow`** - Human/CEO CLI with full control
- **`agentflow-agent`** - Agent CLI with restricted permissions

## Documentation Structure

This documentation is organized into the following sections:

### Getting Started
- [`overview.md`](./overview.md) - Architecture, security model, and design principles
- [`response-format.md`](./response-format.md) - JSON response structure and output formats

### Human CLI (`agentflow`)
- [`authentication.md`](./authentication.md) - User registration, login, logout
- [`roles.md`](./roles.md) - Creating and managing role templates with authority levels
- [`organizations.md`](./organizations.md) - Organization management
- [`projects.md`](./projects.md) - Project management
- [`agents.md`](./agents.md) - Creating agents and generating agent tokens
- [`versions.md`](./versions.md) - Version management
- [`tasks.md`](./tasks.md) - Task creation and management
- [`context.md`](./context.md) - Context management and the `use` command

### Agent CLI (`agentflow-agent`)
- [`agent-cli.md`](./agent-cli.md) - Restricted agent CLI for AI agents

### Reference
- [`workflow.md`](./workflow.md) - Complete workflow example
- [`errors.md`](./errors.md) - Error codes reference
- [`quick-reference.md`](./quick-reference.md) - Command quick reference

## Quick Start

```bash
# 1. Install and authenticate
npm install -g agentflow
agentflow auth register --email "you@example.com" --password "..." --name "Your Name"

# 2. Create your organization and project
agentflow org create --name "My Startup" --slug "mystartup"
agentflow org use --slug "mystartup"
agentflow project create --name "My App" --slug "myapp"
agentflow project use --slug "myapp"

# 3. Create roles with authority levels
agentflow role create --name "Developer" --slug "dev" --level 3

# 4. Create and launch an agent
agentflow agent create --role "dev" --name "Alice"
agentflow agent launch --agent "agent_alice"

# 5. Agent works via agent CLI
agentflow-agent --config ~/.agentflow/agents/agent_alice/token.json task list
```

## Security Model

```
┌────────────────────────────────────────────────────────┐
│              agentflow (Human CLI)                     │
│  - Full CEO permissions                                │
│  - Auth: email + password                              │
└────────────────────────────────────────────────────────┘
                         │
                         │ agent launch (generates token)
                         ▼
┌────────────────────────────────────────────────────────┐
│           agentflow-agent (AI Agent CLI)               │
│  - Limited to agent's own tasks                        │
│  - Role-based permissions (level 1-10)                 │
│  - Auth: agent_id + api_token                          │
│  - NO exit, NO CEO commands                            │
└────────────────────────────────────────────────────────┘
```

## Design Principles

- **100% non-interactive**: All operations use flags/arguments, no prompts
- **Agent-friendly**: AI agents can execute commands without blocking
- **JSON-first**: All commands return structured JSON output
- **Security-first**: Two-CLI system prevents privilege escalation
- **Role hierarchy**: Level-based permissions (1-10) prevent abuse

---

**Status**: Ready for implementation
**Next steps**: See [`overview.md`](./overview.md) for detailed architecture
