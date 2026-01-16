# AgentFlow

Git-like workflow management for AI agents.

## Overview

AgentFlow is a workflow management system designed to help AI agents track and manage their work sessions in a structured, version-controlled manner similar to how Git manages code.

## Features

- **Workspace Management** - Organize work into isolated workspaces for different projects
- **Session Tracking** - Track work sessions with start/end times, duration, and status
- **Action Logging** - Log detailed actions during active sessions with optional types
- **Commit System** - Create commits to summarize completed work with parent-child relationships
- **Commit History** - View commit history with detailed information and logged actions
- **Multiple Databases** - Support for PostgreSQL and SQLite
- **ASCII Output** - Windows-compatible output (no special characters)

## Installation

```bash
pip install agentflow-cli
```

Or using [uv](https://github.com/astral-sh/uv):

```bash
uv pip install agentflow-cli
```

## Quick Start

### 1. Initialize

Interactive setup:
```bash
agentflow init
```

Or with a direct database URL:
```bash
agentflow init --db-url "postgresql://user:pass@localhost/agentflow"
```

For SQLite:
```bash
agentflow init --db-url "sqlite:///agentflow.db"
```

### 2. Create a Workspace

```bash
agentflow workspace create my-project
agentflow workspace switch my-project
```

### 3. Start a Session

```bash
agentflow session start "Implement user authentication"
```

### 4. Log Actions

```bash
agentflow session log "Created User model"
agentflow session log "Added login endpoint"
```

### 5. Check Status

```bash
agentflow session status
```

### 6. Complete Session

```bash
agentflow session commit "feat: implement authentication" --description "Added login and registration with JWT tokens"
```

### 7. View History

```bash
agentflow log
agentflow show <commit-id>
```

## Commands

### Configuration
- `agentflow init` - Initialize configuration
- `agentflow config show` - Show current configuration
- `agentflow config test` - Test database connection

### Workspace
- `agentflow workspace create <name>` - Create a new workspace
- `agentflow workspace list` - List all workspaces
- `agentflow workspace switch <name>` - Switch to a workspace
- `agentflow workspace current` - Show current workspace

### Session
- `agentflow session start <task>` - Start a new session
- `agentflow session status` - Show current session status
- `agentflow session abort` - Abort the current session
- `agentflow session log <action> [-t <type>]` - Log an action to the current session
- `agentflow session commit <message> [-d <description>]` - Complete session and create commit

### History
- `agentflow log [-n N]` - Show commit history (default 10 commits)
- `agentflow show <commit-id>` - Show commit details with actions

## Requirements

- Python >= 3.14
- PostgreSQL or SQLite

## Development

Install development dependencies:

```bash
uv pip install -e ".[dev]"
```

Run tests:

```bash
uv run pytest
```

Lint:

```bash
uv run ruff check
```

Type check:

```bash
uv run mypy
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Roadmap

For planned features and future development, see the [ROADMAP](docs/ROADMAP.md).

## Links

- [PyPI](https://pypi.org/project/agentflow-cli/)
- [GitHub Repository](https://github.com/Developers-Secrets-Inc/agentflow)
- [Issue Tracker](https://github.com/Developers-Secrets-Inc/agentflow/issues)
- [Release Notes](CHANGELOG.md)
