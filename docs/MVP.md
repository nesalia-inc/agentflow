# AgentFlow MVP - Minimal Viable Product

## Goal

Create a functional CLI that allows AI agents to track their work sessions in a "git-like" manner, storing data in a remote database.

---

## MVP Scope

The MVP enables agents to:

1. **Configure and connect** to a remote database
2. **Create/manage workspaces** to isolate different projects
3. **Start work sessions** and track them
4. **Log actions** during work
5. **Create commits** to end a session with a summary
6. **View history** of commits to resume context

---

## Features

### 1. Setup & Configuration

> **Important:** Configuration is done **once per user machine** and is shared across all workspaces. The config file is stored locally and reused for all `agentflow` commands.

- `pyproject.toml` with dependencies (typer, sqlalchemy, pydantic, alembic, asyncpg)
- Base Python package structure
- **Command:** `agentflow init` - Interactive database connection configuration
- **Command:** `agentflow init --db-url <url>` - Direct database URL configuration
- Local config file: `~/.agentflow/config.json`
- Database connection test

**Interactive setup flow:**

```bash
$ agentflow init

Welcome to AgentFlow! Let's configure your connection.

? Database type: (PostgreSQL / SQLite) [PostgreSQL]
? Host: [localhost]
? Port: [5432]
? Database name: [agentflow]
? Username: [postgres]
? Password: ********

? Connection test... ✅ Success!

? Workspace (optional, press enter to create new): [my-project]
? Your name: [Developer]

✅ Configuration saved to ~/.agentflow/config.json
✅ Database schema initialized
✅ Workspace 'my-project' created

You're ready! Use 'agentflow --help' to see available commands.
```

**Direct URL setup:**

```bash
$ agentflow init --db-url "postgresql+asyncpg://user:pass@host:port/dbname"
✅ Connection test... ✅ Success!
✅ Configuration saved to ~/.agentflow/config.json
✅ Database schema initialized
```

**Config file structure:**

```json
{
  "database": {
    "url": "postgresql+asyncpg://user:pass@host:port/dbname",
    "schema": "agentflow"
  },
  "current_workspace": "workspace-uuid",
  "user": {
    "id": "user-uuid",
    "name": "Developer"
  }
}
```

**Config management commands:**

```bash
# Show current configuration
agentflow config show

# Test database connection
agentflow config test

# Reconfigure (update database URL)
agentflow init --db-url "new-db-url"
```

---

### 2. Database & Entity Design

**Note:** The database layer uses SQLAlchemy with entity-centric design. Each entity (Workspace, Session, Commit, Action) encapsulates:
- Its own data model (SQLAlchemy schema)
- Business logic methods
- Database CRUD operations

See the **OOP Entity Design** section below for complete entity implementation examples.

**Technology stack:**
- SQLAlchemy 2.0 (async)
- Alembic for migrations
- PostgreSQL with asyncpg driver

---

### 3. Workspace Management

**Commands:**

```bash
# Create a new workspace
agentflow workspace create <name> [--description <desc>]

# List all workspaces
agentflow workspace list

# Switch to a workspace
agentflow workspace switch <id_or_name>

# Show current workspace
agentflow workspace current
```

**Examples:**

```bash
$ agentflow workspace create e-commerce --description "Online store project"
✅ Workspace created: e-commerce (id: ws-abc-123)

$ agentflow workspace list
e-commerce    (ws-abc-123)  Online store project
my-project    (ws-def-456)  Personal project

$ agentflow workspace switch e-commerce
✅ Switched to workspace: e-commerce

$ agentflow workspace current
Current workspace: e-commerce (ws-abc-123)
Description: Online store project
```

---

### 4. Session Management

**Local state file:** `~/.agentflow/state.json`

```json
{
  "current_session_id": "session-abc-123",
  "current_workspace_id": "ws-abc-123"
}
```

**Commands:**

```bash
# Start a new session
agentflow session start "<task description>"

# Show current session status
agentflow session status

# Log an action during work
agentflow session log "<description>" [--type <type>]

# End session with a commit
agentflow session commit "<commit message>" [--description "<desc>"]

# Abort current session
agentflow session abort
```

**Examples:**

```bash
$ agentflow session start "Implement user authentication"
✅ Session started: session-abc-123
📝 Task: Implement user authentication
⏰ Started at: 2025-01-16 10:30:00

$ agentflow session status
Session: session-abc-123
Task: Implement user authentication
Status: active
Duration: 15m 23s

$ agentflow session log "Created User model with email and password" --type=model
✅ Action logged

$ agentflow session log "Added JWT authentication endpoints" --type=feature
✅ Action logged

$ agentflow session commit "feat: add user authentication with JWT" \
  --description="Implemented login, registration, and token refresh endpoints"
✅ Commit created: commit-xyz-789
📊 Session duration: 45m 23s
🔗 Previous commit: commit-def-456
```

**Error handling:**

```bash
$ agentflow session log "Some action"
❌ No active session. Use 'agentflow session start' first.
```

---

### 5. Commit History

**Commands:**

```bash
# View commit history (current workspace)
agentflow log

# View last N commits
agentflow log --last 5

# View commit details
agentflow show <commit-id>

# Show commit diff (future - simple version for MVP)
agentflow diff <from-commit> <to-commit>
```

**Examples:**

```bash
$ agentflow log
commit-xyz-789  feat: add user authentication with JWT     2 minutes ago
commit-def-456  feat: implement user model                1 hour ago
commit-abc-123  init: initial project setup               1 day ago

$ agentflow log --last 2
commit-xyz-789  feat: add user authentication with JWT     2 minutes ago
commit-def-456  feat: implement user model                1 hour ago

$ agentflow show commit-xyz-789

Commit: commit-xyz-789
Message: feat: add user authentication with JWT
Description: Implemented login, registration, and token refresh endpoints
Author: Developer
Date: 2025-01-16 11:15:23
Duration: 45m 23s
Parent: commit-def-456

Actions logged:
  - Created User model with email and password (model)
  - Added JWT authentication endpoints (feature)

Session: session-abc-123
Task: Implement user authentication
```

---

### 6. CLI Basics

- `--help` on all commands
- Error handling (DB connection, missing session, etc.)
- Clear success/error messages
- Structured output option: `--output=json`

**JSON output for agents:**

```bash
$ agentflow session status --output=json
{
  "session_id": "session-abc-123",
  "task": "Implement user authentication",
  "status": "active",
  "workspace_id": "ws-abc-123",
  "started_at": "2025-01-16T10:30:00Z",
  "duration_seconds": 923
}

$ agentflow log --output=json
{
  "commits": [
    {
      "id": "commit-xyz-789",
      "message": "feat: add user authentication with JWT",
      "created_at": "2025-01-16T11:15:23Z",
      "duration_seconds": 2723
    }
  ]
}
```

---

## Project Structure

> **Architecture:** Pure Object-Oriented Design with entity-centric approach. Each entity encapsulates its own data, behavior, and persistence logic.

```
agentflow/
├── agentflow/
│   ├── __init__.py
│   ├── cli.py                    # Main Typer app
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py           # Config loader/saver
│   │   └── database.py           # DB connection management
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── workspace.py          # Workspace entity (data + behavior)
│   │   ├── session.py            # Session entity (data + behavior)
│   │   ├── commit.py             # Commit entity (data + behavior)
│   │   └── action.py             # Action entity (logged actions)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py               # SQLAlchemy Base & engine
│   │   └── session.py            # DB session management
│   └── utils/
│       ├── __init__.py
│       ├── formatters.py         # Output formatting (tables, json)
│       └── state.py              # Local state management
├── alembic/
│   ├── versions/
│   │   └── 001_initial.py        # Initial schema migration
│   └── env.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures (DB session, test data)
│   ├── test_workspace.py
│   ├── test_session.py
│   ├── test_commit.py
│   └── test_action.py
├── pyproject.toml
├── README.md
└── .env.example
```

### OOP Entity Design

Each entity is responsible for its own:

1. **Data** - Attributes and state
2. **Behavior** - Business logic methods
3. **Persistence** - Database CRUD operations

**Example - Workspace Entity:**

```python
# entities/workspace.py
class Workspace(Base):
    """Represents a workspace for organizing work."""

    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    sessions: Mapped[List["Session"]] = relationship()
    commits: Mapped[List["Commit"]] = relationship()

    @classmethod
    def create(cls, db: DBSession, name: str, description: str | None = None) -> "Workspace":
        """Create a new workspace."""
        workspace = cls(id=generate_id(), name=name, description=description)
        db.add(workspace)
        db.commit()
        return workspace

    @classmethod
    def get_by_id(cls, db: DBSession, workspace_id: str) -> "Workspace | None":
        """Retrieve a workspace by ID."""
        return db.query(cls).filter(cls.id == workspace_id).first()

    @classmethod
    def get_by_name(cls, db: DBSession, name: str) -> "Workspace | None":
        """Retrieve a workspace by name."""
        return db.query(cls).filter(cls.name == name).first()

    @classmethod
    def list_all(cls, db: DBSession) -> list["Workspace"]:
        """List all workspaces."""
        return db.query(cls).order_by(cls.created_at.desc()).all()

    def add_session(self, task: str) -> "Session":
        """Create a new session in this workspace."""
        from .session import Session
        return Session.create(self.id, task)

    def get_commits(self, limit: int | None = None) -> list["Commit"]:
        """Get commits from this workspace."""
        from .commit import Commit
        query = Commit.query().filter(Commit.workspace_id == self.id)
        if limit:
            query = query.limit(limit)
        return query.all()

    def __repr__(self) -> str:
        return f"Workspace(id={self.id}, name={self.name})"
```

**Example - Session Entity:**

```python
# entities/session.py
class Session(Base):
    """Represents a work session for tracking agent activity."""

    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    workspace_id: Mapped[str] = mapped_column(String, ForeignKey("workspaces.id"))
    task: Mapped[str] = mapped_column(String, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String, default="active")

    # Relationships
    workspace: Mapped["Workspace"] = relationship()
    commit: Mapped["Commit | None"] = relationship()
    actions: Mapped[list["Action"]] = relationship()

    @classmethod
    def create(cls, workspace_id: str, task: str) -> "Session":
        """Create a new session."""
        db = get_db()
        session = cls(id=generate_id(), workspace_id=workspace_id, task=task)
        db.add(session)
        db.commit()
        return session

    @classmethod
    def get_active(cls, workspace_id: str) -> "Session | None":
        """Get the active session for a workspace."""
        db = get_db()
        return db.query(cls).filter(
            cls.workspace_id == workspace_id,
            cls.status == "active"
        ).first()

    def log_action(self, description: str, action_type: str) -> "Action":
        """Log an action during this session."""
        from .action import Action
        return Action.create(self.id, description, action_type)

    def complete(self, message: str, description: str | None = None) -> "Commit":
        """Complete the session and create a commit."""
        from .commit import Commit
        self.completed_at = datetime.utcnow()
        self.status = "completed"
        db = get_db()
        db.commit()

        return Commit.create(
            session_id=self.id,
            workspace_id=self.workspace_id,
            message=message,
            description=description
        )

    def abort(self) -> None:
        """Abort the current session."""
        self.completed_at = datetime.utcnow()
        self.status = "aborted"
        db = get_db()
        db.commit()

    @property
    def duration(self) -> int | None:
        """Get session duration in seconds."""
        if self.completed_at:
            return int((self.completed_at - self.started_at).total_seconds())
        return None

    def __repr__(self) -> str:
        return f"Session(id={self.id}, task={self.task}, status={self.status})"
```

**Example - Commit Entity:**

```python
# entities/commit.py
class Commit(Base):
    """Represents a commit summarizing a completed session."""

    __tablename__ = "commits"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("sessions.id"))
    workspace_id: Mapped[str] = mapped_column(String, ForeignKey("workspaces.id"))
    message: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    parent_id: Mapped[str | None] = mapped_column(String, ForeignKey("commits.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)

    # Relationships
    session: Mapped["Session"] = relationship()
    workspace: Mapped["Workspace"] = relationship()
    parent: Mapped["Commit | None"] = remote_side(id)
    children: Mapped[list["Commit"]] = relationship()

    @classmethod
    def create(
        cls,
        session_id: str,
        workspace_id: str,
        message: str,
        description: str | None = None
    ) -> "Commit":
        """Create a new commit from a session."""
        from .session import Session
        db = get_db()

        session = db.query(Session).filter(Session.id == session_id).first()
        duration = session.duration if session else None

        # Get previous commit for parent reference
        parent = db.query(cls).filter(
            cls.workspace_id == workspace_id
        ).order_by(cls.created_at.desc()).first()

        commit = cls(
            id=generate_id(),
            session_id=session_id,
            workspace_id=workspace_id,
            message=message,
            description=description,
            parent_id=parent.id if parent else None,
            duration_seconds=duration
        )
        db.add(commit)
        db.commit()
        return commit

    @classmethod
    def get_by_id(cls, commit_id: str) -> "Commit | None":
        """Get a commit by ID."""
        db = get_db()
        return db.query(cls).filter(cls.id == commit_id).first()

    @classmethod
    def list_for_workspace(cls, workspace_id: str, limit: int | None = None) -> list["Commit"]:
        """List commits for a workspace."""
        db = get_db()
        query = db.query(cls).filter(cls.workspace_id == workspace_id)
        if limit:
            query = query.limit(limit)
        return query.order_by(cls.created_at.desc()).all()

    @property
    def actions(self) -> list["Action"]:
        """Get actions from the session that created this commit."""
        from .action import Action
        db = get_db()
        return db.query(Action).filter(Action.session_id == self.session_id).all()

    def __repr__(self) -> str:
        return f"Commit(id={self.id}, message={self.message})"
```

---

## Dependencies & Project Management

**Project Manager:** uv (fast Python package manager)

### Installation

```bash
# Install uv
pip install uv

# Or with curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Project Setup

```bash
# Create project with uv
uv init --name agentflow

# Install dependencies
uv sync

# Run with uv
uv run agentflow --help
```

### pyproject.toml

```toml
[project]
name = "agentflow"
version = "0.1.0"
description = "Git-like workflow management for AI agents"
requires-python = ">=3.14"
dependencies = [
    "typer>=0.12.0",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.29.0",           # PostgreSQL async driver
    "alembic>=1.13.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "rich>=13.0.0",              # Beautiful CLI output
    "python-dateutil>=2.8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[project.scripts]
agentflow = "agentflow.cli:app"

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 100
target-version = "py314"

[tool.mypy]
python_version = "3.14"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### Development Workflow

```bash
# Add a new dependency
uv add <package-name>

# Add dev dependency
uv add --dev <package-name>

# Run tests
uv run pytest

# Run type checking
uv run mypy agentflow/

# Run linting
uv run ruff check agentflow/

# Format code
uv run ruff format agentflow/
```

---

## Success Criteria

An agent can successfully complete this workflow:

```bash
# 1. Initial setup
$ agentflow init
✅ Connected to database

# 2. Create a workspace
$ agentflow workspace create my-project
✅ Workspace created

# 3. Start a session
$ agentflow session start "Fix authentication bug"
✅ Session started: abc-123

# 4. Log actions
$ agentflow session log "Analyzed login code" --type=analysis
✅ Action logged

$ agentflow session log "Fixed race condition" --type=fix
✅ Action logged

# 5. End with commit
$ agentflow session commit "fix: race condition in token refresh"
✅ Commit created: xyz-789

# 6. View history
$ agentflow log
xyz-789  fix: race condition in token refresh  2 minutes ago
def-456  feat: initial auth implementation     1 day ago

# 7. Next agent can resume
$ agentflow show def-456
# View previous commit details to understand context
```

---

## Out of Scope (Future Phases)

### Phase 2 - Feedback Loop
- Issue system (`agentflow issue create/list/resolve`)
- Agent reviewer for automatic prioritization
- Issue backlog management

### Phase 3 - Knowledge Base
- Documentation storage
- Search functionality (`agentflow docs search`)
- RAG system with embeddings

### Phase 4 - Intelligence
- A/B testing for agent personalities
- Advanced cost tracking
- Pattern detection

### Phase 5 - Advanced Features
- Offline mode with sync
- Collaborative multi-agent sessions
- Analytics dashboard
- Workspace export/import

---

## Implementation Order

1. **Project setup** - Initialize with `uv`, create pyproject.toml, directory structure
2. **Database foundation** - SQLAlchemy Base, engine, and session management
3. **Entity models** - Implement Workspace, Session, Commit, Action entities with data models
4. **Entity behaviors** - Add class methods and instance methods to each entity (CRUD, business logic)
5. **Config system** - Local config (~/.agentflow/config.json), `agentflow init` with interactive and `--db-url` modes
6. **Workspace commands** - create, list, switch, current (using Workspace entity methods)
7. **Session commands** - start, status, abort (using Session entity methods)
8. **Session logging** - log action storage (using Action entity and Session.log_action())
9. **Commit commands** - commit creation, parent tracking (using Session.complete() and Commit entity)
10. **History commands** - log, show (using Commit entity methods)
11. **Polish** - Error handling, JSON output, formatting
