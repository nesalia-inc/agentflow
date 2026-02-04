# Quick Reference

## Human CLI (`agentflow`)

```bash
# Auth
agentflow auth register --email <email> --password <pass> --name <name>
agentflow auth login --email <email> --password <pass>
agentflow auth status
agentflow auth logout

# Role (with levels)
agentflow role create --name <name> --slug <slug> --level <level>
agentflow role list [--format table]
agentflow role view --slug <slug>
agentflow role update --slug <slug> [--name <name>]
agentflow role add-document --role <slug> --title <title> --content <content>
agentflow role add-document --role <slug> --title <title> --file <path>
agentflow role delete --slug <slug> --confirm

# Org
agentflow org create --name <name> --slug <slug>
agentflow org list [--format table]
agentflow org view --slug <slug>
agentflow org use --slug <slug>
agentflow org delete --slug <slug> --confirm

# Project
agentflow project create --name <name> --slug <slug> [--github-url <url>]
agentflow project list [--format table]
agentflow project view --slug <slug>
agentflow project use --slug <slug>
agentflow project delete --slug <slug> --confirm

# Agent
agentflow agent create --role <slug> --name <name> [--project <slug>]
agentflow agent list [--format table]
agentflow agent view --agent <id>
agentflow agent update --agent <id> [--name <name>]
agentflow agent delete --agent <id> --confirm
agentflow agent launch --agent <id>

# Context shortcut
agentflow use --org <slug> --project <slug>

# Version
agentflow version create --version <version> [--name <name>]
agentflow version list [--format table]
agentflow version view --version <version>
agentflow version release --version <version> [--release-notes <notes>]
agentflow version delete --version <version> --confirm

# Task
agentflow task create --title <title> [--priority <priority>] [--required-level <level>]
agentflow task list [--version <version>] [--status <status>]
agentflow task view --task-id <id>
agentflow task start --task-id <id>
agentflow task complete --task-id <id> [--success <notes>]
agentflow task block --task-id <id> --reason <reason>
agentflow task unblock --task-id <id>
agentflow task assign --task-id <id> --agent <agent-id>
agentflow task add-relation --task-id <id> --related-to <id> --type <type>
agentflow task remove-relation --task-id <id> --related-to <id>
agentflow task relations --task-id <id>
agentflow task delete --task-id <id> --confirm
```

## Agent CLI (`agentflow-agent`)

```bash
# Usage
agentflow-agent --config <token-file> <command> [flags]

# Status
agentflow-agent status

# Task (own tasks only)
agentflow-agent task list
agentflow-agent task view --task-id <id>
agentflow-agent task start --task-id <id>
agentflow-agent task complete --task-id <id> [--success <notes>]
agentflow-agent task block --task-id <id> --reason <reason>
agentflow-agent task unblock --task-id <id>

# Role (own role only)
agentflow-agent role view --slug <slug>

# Stats
agentflow-agent agent stats
```

## Quick Start

```bash
# 1. Setup
agentflow auth register --email "you@example.com" --password "..." --name "Your Name"

# 2. Create org
agentflow org create --name "My Startup" --slug "mystartup"
agentflow org use --slug "mystartup"

# 3. Create project
agentflow project create --name "My App" --slug "myapp"
agentflow project use --slug "myapp"

# 4. Create role with level
agentflow role create --name "Developer" --slug "dev" --level 3

# 5. Create agent
agentflow agent create --role "dev" --name "Alice"

# 6. Launch agent
agentflow agent launch --agent "agent_alice"

# 7. Agent works
agentflow-agent --config ~/.agentflow/agents/agent_alice/token.json task list
```
