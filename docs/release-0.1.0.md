# AgentFlow CLI v0.1.0

Git-like workflow management for AI agents.

## What is AgentFlow?

AgentFlow is a workflow management system designed to help AI agents track and manage their work sessions in a structured, version-controlled manner similar to how Git manages code.

## Features

- **Workspace Management** - Organize work into isolated workspaces for different projects
- **Session Tracking** - Track work sessions with start/end times and status
- **Action Logging** - Log detailed actions during active sessions
- **Commit System** - Create commits to summarize completed work with parent-child relationships
- **Multiple Databases** - Support for PostgreSQL and SQLite
- **ASCII-only Output** - Full Windows compatibility

## Installation

### Using pip
```bash
pip install agentflow-cli
```

### Using uv
```bash
uv pip install agentflow-cli
```

## Quick Start

### 1. Initialize
```bash
agentflow init
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

## Available Commands

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
- `agentflow session log <action>` - Log an action to the current session
- `agentflow session commit <message>` - Complete session with commit

### History
- `agentflow log [--limit N]` - Show commit history
- `agentflow show <commit-id>` - Show commit details

## Requirements

- Python >= 3.14
- PostgreSQL or SQLite

## Documentation

For full documentation, visit the [GitHub repository](https://github.com/Developers-Secrets-Inc/agentflow).

## Changelog

### [0.1.0] - 2025-01-16

#### Added
- Configuration system with interactive setup and direct database URL support
- Workspace management (create, list, switch, current)
- Session tracking (start, status, abort)
- Action logging during active sessions
- Session commit with parent-child relationship chain
- Commit history (log, show commands)
- Support for PostgreSQL and SQLite databases
- ASCII-only output for Windows compatibility
- Complete test suite (34 tests covering all entities)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Developers-Secrets-Inc/agentflow/blob/main/LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

- **Repository**: https://github.com/Developers-Secrets-Inc/agentflow
- **Issues**: https://github.com/Developers-Secrets-Inc/agentflow/issues

---

**PyPI**: https://pypi.org/project/agentflow-cli/
**Installation**: `pip install agentflow-cli`
