# Commands Outline

## Human CLI (`agentflow`)

```
auth
  ├── register --email <email> --password <password> --name <name>
  ├── login --email <email> --password <password>
  ├── status
  └── logout

role
  ├── create --name <name> --slug <slug> --level <level>
  ├── list [--format <format>]
  ├── view --slug <slug>
  ├── update --slug <slug> [--name <name>]
  ├── add-document --role <slug> --title <title> (--content <content> | --file <path>)
  └── delete --slug <slug> --confirm

org
  ├── create --name <name> --slug <slug>
  ├── list [--format <format>]
  ├── view --slug <slug>
  ├── use --slug <slug>
  └── delete --slug <slug> --confirm

project
  ├── create --name <name> --slug <slug> [--github-url <url>]
  ├── list [--format <format>]
  ├── view --slug <slug>
  ├── use --slug <slug>
  └── delete --slug <slug> --confirm

agent
  ├── create --role <slug> --name <name> [--project <slug>]
  ├── list [--format <format>]
  ├── view --agent <id>
  ├── update --agent <id> [--name <name>]
  ├── delete --agent <id> --confirm
  └── launch --agent <id>

version
  ├── create --version <version> [--name <name>]
  ├── list [--format <format>]
  ├── view --version <version>
  ├── release --version <version> [--release-notes <notes>]
  └── delete --version <version> --confirm

task
  ├── create --title <title> [--priority <priority>] [--required-level <level>]
  ├── list [--version <version>] [--status <status>]
  ├── view --task-id <id>
  ├── start --task-id <id>
  ├── complete --task-id <id> [--success <notes>]
  ├── block --task-id <id> --reason <reason>
  ├── unblock --task-id <id>
  ├── assign --task-id <id> --agent <agent-id>
  ├── add-relation --task-id <id> --related-to <id> --type <type>
  ├── remove-relation --task-id <id> --related-to <id>
  ├── relations --task-id <id>
  └── delete --task-id <id> --confirm

use
  └── --org <slug> --project <slug>
```

## Agent CLI (`agentflow-agent`)

```
status

task
  ├── list
  ├── view --task-id <id>
  ├── start --task-id <id>
  ├── complete --task-id <id> [--success <notes>]
  ├── block --task-id <id> --reason <reason>
  └── unblock --task-id <id>

role
  └── view --slug <slug>

agent
  └── stats
```
