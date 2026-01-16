# AgentFlow - Architecture & Design Document

## Vision

AgentFlow is a **git-like workflow management system for AI agents**, enabling traceability, feedback loops, and continuous improvement across multi-agent workflows.

### Core Pillars

1. **Traceability** - Every agent action is tracked like a git commit
2. **Feedback Loop** - Agents can report issues and improvements internally
3. **Continuous Improvement** - Pattern analysis to optimize future agent performance

---

## Tech Stack

```
Language: Python 3.14+ with static typing (mypy)
CLI Framework: Typer (excellent type support, auto-completion)
Database: PostgreSQL (recommended) or MongoDB
ORM: SQLAlchemy 2.0 (async) or Beanie (for MongoDB)
Migrations: Alembic
Validation: Pydantic v2
Async: asyncio + httpx (for external API calls)
```

---

## Project Structure

```
agentflow/
├── agentflow/
│   ├── __init__.py
│   ├── cli.py                   # Typer entry point
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # Configuration & ENV vars
│   │   └── database.py          # DB connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── workspace.py
│   │   ├── session.py
│   │   ├── commit.py
│   │   ├── issue.py
│   │   └── personality.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── connection.py        # Session/Client DB
│   │   ├── repositories/        # Repository pattern
│   │   └── migrations/          # Alembic
│   ├── services/
│   │   ├── __init__.py
│   │   ├── session_service.py
│   │   ├── commit_service.py
│   │   ├── issue_service.py
│   │   └── analysis_service.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── interfaces.py        # Interfaces for external agents
│   └── utils/
│       ├── __init__.py
│       ├── formatters.py        # Output formatting
│       └── validators.py
├── tests/
├── pyproject.toml               # Poetry or uv
├── README.md
└── .env.example
```

---

## Core Concepts

### 1. Agent Session & Commit System

Every agent work session generates a "commit" containing:

- Actions performed
- Results obtained
- Decision context
- Created artifacts
- Metadata (duration, cost, model used)

**Data Schema:**

```python
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum

class SessionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABORTED = "aborted"

class CommitStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"

class AgentCommit(BaseModel):
    id: str
    session_id: str
    agent_id: str
    workspace_id: str

    # Commit content
    summary: str              # Commit message style summary
    description: str          # Detailed description
    actions: List[Action]     # List of actions
    artifacts: List[Artifact] # Created files/outputs

    # Metadata
    timestamp: datetime
    duration: int             # milliseconds
    token_usage: TokenUsage

    # Traceability
    parent_commit_id: Optional[str]  # Previous commit
    branch_name: Optional[str]       # For parallel work

    # Status
    status: CommitStatus
    errors: Optional[List[Error]]

class TokenUsage(BaseModel):
    input: int
    output: int
    cost: float  # USD

class Action(BaseModel):
    type: str  # "analysis", "code_change", "file_read", etc.
    description: str
    timestamp: datetime
    metadata: dict = {}

class Artifact(BaseModel):
    type: str  # "file", "document", "test_result", etc.
    path: Optional[str]
    content: Optional[str]
    metadata: dict = {}
```

**Workflow:**

1. Agent starts a session → `session:start`
2. Each significant action is logged
3. Agent finishes → Generates commit with summary
4. Next agent can read previous commits to resume context

---

### 2. Internal Issue System

Agents can create "issues" when encountering problems, similar to GitHub Issues but internal to the system.

**Data Schema:**

```python
from enum import Enum

class IssueCategory(str, Enum):
    BUG = "bug"
    IMPROVEMENT = "improvement"
    QUESTION = "question"
    PATTERN = "pattern"

class Priority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IssueStatus(str, Enum):
    OPEN = "open"
    REVIEWING = "reviewing"
    ADDRESSED = "addressed"
    DISMISSED = "dismissed"

class AgentIssue(BaseModel):
    id: str
    session_id: str
    agent_id: str
    workspace_id: str

    # Issue content
    title: str
    description: str
    category: IssueCategory

    # Context
    context: IssueContext

    # Auto-priorization
    priority: Priority
    estimated_cost: Optional[float]  # Estimated resolution cost

    # Status
    status: IssueStatus
    assigned_to: Optional[str]  # Agent or human

    # Resolution
    resolution: Optional[str]
    resolved_at: Optional[datetime]

class IssueContext(BaseModel):
    task: str
    steps: List[str]
    error: Optional[str]
    reproduction: Optional[str]
```

**Workflow:**

1. Agent detects a problem → Creates an issue
2. **Reviewer Agent** analyzes the issue:
   - Evaluates priority
   - Estimates resolution cost
   - Categorizes the problem
3. Issue is added to the backlog
4. A specialized agent or human can address it

---

### 3. Workspace Isolation

Different isolated work environments (e.g., e-commerce project vs medical project).

**Data Schema:**

```python
class Workspace(BaseModel):
    id: str
    name: str
    description: str

    # Isolation
    knowledge_base: List[str]      # Specific documentation
    agent_personalities: List[str] # Allowed personalities

    # Traceability
    commits: List[str]             # Commit history
    issues: List[str]              # Workspace issues

    # Configuration
    config: WorkspaceConfig

class WorkspaceConfig(BaseModel):
    max_cost_per_session: float
    allowed_models: List[str]
    require_human_approval: bool
```

**Benefits:**

- Separate knowledge per domain
- Different agent personalities per workspace
- Isolated costs and metrics
- Parallel work capability

---

### 4. A/B Testing for Agent Personalities

Test different agent configurations (prompt styles, temperature, tools) to identify the most effective.

**Data Schema:**

```python
from enum import Enum

class ReasoningStyle(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"
    CREATIVE = "creative"

class CommunicationStyle(str, Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    TECHNICAL = "technical"

class PersonalityVariant(BaseModel):
    id: str
    name: str
    base_personality: str

    # Configuration
    config: PersonalityConfig

    # Metrics
    metrics: PersonalityMetrics

    # Active A/B test
    active_experiment: Optional[Experiment]

class PersonalityConfig(BaseModel):
    system_prompt: str
    temperature: float
    tools: List[str]
    reasoning_style: ReasoningStyle
    communication_style: CommunicationStyle

class PersonalityMetrics(BaseModel):
    total_sessions: int
    success_rate: float
    avg_cost_per_task: float
    avg_duration: float  # milliseconds
    user_satisfaction: Optional[float]

class Experiment(BaseModel):
    name: str
    start_time: datetime
    comparison_variants: List[str]
```

**Workflow:**

1. Define a hypothesis (e.g., "concise agents are more efficient")
2. Create variants with different configs
3. Run parallel sessions with randomization
4. Collect metrics (success, cost, duration)
5. Analyze results → Promote the winner

---

### 5. Internal Knowledge Base (RAG)

A RAG (Retrieval-Augmented Generation) system where agents can ask questions about the domain and receive answers based on workspace documentation.

**Architecture:**

```
Documentation Sources
    ↓
Chunking + Embedding
    ↓
Vector Database (e.g., Pinecone, pgvector)
    ↓
Semantic Search when agent asks a question
    ↓
Context added to agent prompt
```

**Content Types:**

- Project README
- Technical documentation
- Identified patterns (resolved issues → documentation)
- Historical agent Q&A
- Code examples and solutions

---

### 6. Cost Analysis

Track and analyze all costs to optimize spending.

**Metrics:**

```python
class SessionCost(BaseModel):
    agent_id: str
    task_id: str
    tokens_used: int
    model_cost: float
    duration: int  # milliseconds
    timestamp: datetime

class CostAggregation(BaseModel):
    by_agent: Dict[str, TotalCost]
    by_task: Dict[str, TotalCost]
    by_workspace: Dict[str, TotalCost]
    by_model: Dict[str, TotalCost]

class TotalCost(BaseModel):
    total_tokens: int
    total_cost: float
    session_count: int

class CostRecommendation(BaseModel):
    type: str  # "use_cheaper_model", "cache_more", "reduce_context"
    description: str
    potential_savings: float
```

---

## CLI Design

### Main Commands

```bash
# Configuration
agentflow init              # Initialize configuration
agentflow config set        # Modify configuration
agentflow config show       # Show current configuration
agentflow config test       # Test connection

# Workspace
agentflow workspace create      # Create a workspace
agentflow workspace list        # List workspaces
agentflow workspace switch      # Switch workspace
agentflow workspace current     # Show current workspace

# Session (Core system)
agentflow session start           # Start a new session
agentflow session status          # Current session status
agentflow session log             # Log an action
agentflow session commit          # End with a commit
agentflow session abort           # Cancel session

# Commits (History)
agentflow log                    # View commit history
agentflow show <commit-id>        # Commit details
agentflow diff <from> <to>        # Compare two commits

# Issues (Feedback)
agentflow issue create           # Create an issue
agentflow issue list             # List issues
agentflow issue show <id>        # Issue details
agentflow issue resolve <id>     # Resolve an issue

# Knowledge Base
agentflow docs add               # Add documentation
agentflow docs search            # Search documentation
agentflow docs ask               # Ask a question (RAG)

# Analytics
agentflow stats                  # Global statistics
agentflow cost                   # Cost analysis
agentflow report                 # Generate report
```

### Usage Examples

```bash
# Start a work session
$ agentflow session start "Implement user authentication"
✅ Session started: session-abc123
📝 Current task: Implement user authentication

# Agent works... can log actions
$ agentflow session log "Created User model" --type=model
✅ Action logged

$ agentflow session log "Added JWT authentication" --type=feature
✅ Action logged

# End with a commit
$ agentflow session commit "feat: add user authentication with JWT" \
  --message="Implemented login, registration, and token refresh" \
  --files="src/auth.py,src/models/user.py"

✅ Commit created: commit-xyz789
📊 Session duration: 45m 23s
💰 Token cost: $0.023
🔗 Parent commit: commit-def456
```

---

## Configuration System

### Local Configuration File

The CLI stores configuration in `~/.agentflow/config.json`:

```json
{
  "database": {
    "url": "postgresql+asyncpg://user:pass@host:port/dbname",
    "schema": "agentflow",
    "pool_size": 10,
    "max_overflow": 20
  },
  "current_workspace": "workspace-uuid",
  "user": {
    "id": "user-uuid",
    "name": "Developer"
  },
  "preferences": {
    "output_format": "rich",
    "auto_commit": true
  }
}
```

### Initialization Command

```bash
agentflow init
```

**Interactive workflow:**

```
$ agentflow init

Welcome to AgentFlow! Let's configure your connection.

? Database type: (PostgreSQL / MongoDB / SQLite) [PostgreSQL]
? Host: [db.example.com]
? Port: [5432]
? Database name: [agentflow]
? Username: [admin]
? Password: ********

? Connection test... ✅ Success!

? Workspace (optional, press enter to create new): [my-project]
? Your name: [Claude Dev]

✅ Configuration saved to ~/.agentflow/config.json
✅ Database schema initialized
✅ Workspace 'my-project' created

You're ready! Use 'agentflow --help' to see available commands.
```

### Environment Management

Support for multiple configurations (e.g., dev, staging, prod):

```bash
# Default config
~/.agentflow/config.json        # Default environment

# Named environments
~/.agentflow/configs/
  ├── dev.json
  ├── staging.json
  └── prod.json

# Usage
agentflow --env staging session start
```

---

## Database Connection

### Connection Architecture

```python
# config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    workspace_id: str | None = None
    user_id: str

    class Config:
        env_file = ".env"
        env_prefix = "AGENTFLOW_"

# db/connection.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(url, echo=False)
        self.async_session = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session

    async def connect(self) -> bool:
        """Test the connection"""
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

# Global singletons
_db: Database | None = None

def get_db() -> Database:
    """Get the DB instance (singleton)"""
    global _db
    if _db is None:
        config = load_config()
        _db = Database(config.database_url)
    return _db
```

### Usage in Typer Commands

```python
# cli.py
import typer
from .db.connection import get_db

app = typer.Typer()

@app.command()
def init(
    db_type: str = typer.Option("postgresql", prompt=True),
    host: str = typer.Option(..., prompt=True),
    # ...
):
    """Initialize configuration"""
    # Interactive setup

@app.command()
def session_start(task: str):
    """Start a new session"""
    db = get_db()

    with db.get_session() as session:
        session_service = SessionService(session)
        new_session = session_service.create(task)

    typer.echo(f"✅ Session started: {new_session.id}")
```

### Local State Management

To avoid re-connecting on every command, use a local state file:

```json
// ~/.agentflow/state.json
{
  "current_session_id": "session-abc123",
  "last_sync": "2025-01-16T10:30:00Z",
  "pending_actions": []
}
```

**Workflow:**

```python
# CLI reads local state
state = load_local_state()
session_id = state.get("current_session_id")

# If no active session, error
if not session_id:
    typer.echo("❌ No active session. Use 'agentflow session start' first.")
    raise typer.Exit(1)

# Use session_id for operations
```

---

## How Agents Use the CLI

### Typical Agent Workflow

The agent (e.g., Claude, GPT-4) has terminal access and can call the CLI:

```bash
# 1. Agent starts a session
agentflow session start "Fix authentication bug in login flow"

# 2. Agent can read internal docs
agentflow docs search "authentication pattern"
# > Found 3 relevant documents...
# > - docs/auth-jwt-implementation.md (score: 0.95)
# > - docs/common-auth-pitfalls.md (score: 0.87)

# 3. Agent can see previous commits
agentflow log --last 5
# > commit-123: feat: initial auth implementation (2 days ago)
# > commit-124: fix: JWT expiration issue (1 day ago)

# 4. Agent works and can log actions
agentflow session log "Analyzed login controller, found race condition" --type=analysis

# 5. If agent finds a systemic problem
agentflow issue create \
  --title="Race condition in token refresh" \
  --category="bug" \
  --description="When multiple requests..."

# 6. Agent finishes with a commit
agentflow session commit \
  --title="fix: resolve race condition in token refresh" \
  --message="Added mutex lock to prevent concurrent token refresh" \
  --files="src/auth/token_manager.py" \
  --cost-tokens=12450 \
  --cost-usd=0.037
```

### Programmatic API (Optional)

For agents that cannot use the CLI, offer a Python API:

```python
# Agents can import directly
from agentflow import AgentFlowClient

client = AgentFlowClient()  # Uses local config

# Alternative: CLI can output JSON for parsing
$ agentflow session status --output=json
{"session_id": "abc", "task": "...", "status": "active"}
```

---

## Security & Authentication

### Security Options

**1. Credentials in config** (simple, less secure)
```json
{
  "database": {
    "url": "postgresql://user:password@host/db"
  }
}
```

**2. Environment variables** (recommended)
```bash
export AGENTFLOW_DB_URL="postgresql://..."
agentflow session start
```

**3. Secrets management** (for production)
- Integration with AWS Secrets Manager, Vault, etc.
- CLI retrieves secrets at runtime

**4. Database-level authentication**
- Row Level Security (PostgreSQL)
- Each workspace = separate DB user
- Complete data isolation

---

## Database Models (SQLAlchemy)

```python
# models/workspace.py
from sqlalchemy import String, DateTime, ForeignKey, Integer, Float, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relations
    sessions: Mapped[List["Session"]] = relationship(back_populates="workspace")
    commits: Mapped[List["Commit"]] = relationship(back_populates="workspace")

# models/session.py
class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    workspace_id: Mapped[str] = mapped_column(String, ForeignKey("workspaces.id"))
    task: Mapped[str] = mapped_column(String, nullable=False)

    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)

    status: Mapped[SessionStatus] = mapped_column(SQLEnum(SessionStatus), default="active")

    # Relations
    workspace: Mapped["Workspace"] = relationship(back_populates="sessions")
    commit: Mapped["Commit | None"] = relationship(back_populates="session")
    actions: Mapped[List["SessionAction"]] = relationship(back_populates="session")

# models/commit.py
class Commit(Base):
    __tablename__ = "commits"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    session_id: Mapped[str] = mapped_column(String, ForeignKey("sessions.id"))
    workspace_id: Mapped[str] = mapped_column(String, ForeignKey("workspaces.id"))

    # Git-like
    message: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String)
    parent_id: Mapped[str | None] = mapped_column(String, ForeignKey("commits.id"))
    branch: Mapped[str | None] = mapped_column(String)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)

    # Costs
    token_usage_input: Mapped[int] = mapped_column(Integer, default=0)
    token_usage_output: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)

    # Artifacts
    artifacts: Mapped[List["CommitArtifact"]] = relationship(back_populates="commit")

    # Relations
    session: Mapped["Session"] = relationship(back_populates="commit")
    workspace: Mapped["Workspace"] = relationship(back_populates="commits")
    parent: Mapped["Commit | None"] = remote_side(id)
    children: Mapped[List["Commit"]] = relationship

# models/issue.py
class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    session_id: Mapped[str | None] = mapped_column(String, ForeignKey("sessions.id"))
    workspace_id: Mapped[str] = mapped_column(String, ForeignKey("workspaces.id"))

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[IssueCategory] = mapped_column(SQLEnum(IssueCategory), nullable=False)

    priority: Mapped[Priority] = mapped_column(SQLEnum(Priority), default="medium")
    status: Mapped[IssueStatus] = mapped_column(SQLEnum(IssueStatus), default="open")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Auto-generated by reviewer agent
    estimated_cost: Mapped[float | None] = mapped_column(Float)
    resolution_notes: Mapped[str | None] = mapped_column(Text)
```

---

## Connection Flow

### Startup Sequence

```
1. User runs: agentflow session start "..."
   ↓
2. CLI loads config (~/.agentflow/config.json)
   ↓
3. If no config → Error or run 'agentflow init'
   ↓
4. DB connection test (async)
   ↓
5. Retrieve current workspace from config
   ↓
6. Create new session in DB
   ↓
7. Save session_id in local state (~/.agentflow/state.json)
   ↓
8. Display confirmation to user
```

### Connection Error Handling

```python
try:
    db = get_db()
    await db.connect()
except ConnectionRefusedError:
    typer.echo("❌ Cannot connect to database.")
    typer.echo("💡 Run 'agentflow config test' to diagnose.")
    raise typer.Exit(1)
except AuthenticationError:
    typer.echo("❌ Authentication failed. Check your credentials.")
    typer.echo("💡 Run 'agentflow init' to reconfigure.")
    raise typer.Exit(1)
```

---

## Key Considerations

### Performance & Connection Pooling

- Use SQLAlchemy connection pool
- Client-side connection pooling (don't reconnect on every command)
- Async I/O to avoid blocking the CLI

### Concurrency

- If multiple agents work in parallel in the same workspace:
  - Locks at session level
  - DB transactions to avoid inconsistencies
  - Eventual consistency for commits

### Offline Mode

- Allow working offline and sync later
- Local command queue
- `agentflow sync` to push data to DB

### Extensibility

- Plugin architecture to add custom commands
- Hooks to execute code before/after commands
- Custom output formatters

---

## Implementation Plan

### Phase 1 - Setup & Configuration
1. Initialize Python project (pyproject.toml, uv)
2. Base package structure
3. Data models with SQLAlchemy
4. Local configuration system
5. `agentflow init` command

### Phase 2 - CLI Core
1. Workspace management commands
2. Session commands (start, log, commit, abort)
3. Local state for tracking active session
4. `agentflow log` command (history)

### Phase 3 - Issues & Feedback
1. Issue system
2. `agentflow issue` commands (create, list, resolve)
3. Basic reviewer agent

### Phase 4 - Knowledge Base
1. Documentation storage
2. Simple search (keyword)
3. `agentflow docs` commands

### Phase 5 - Intelligence
1. A/B testing framework for personalities
2. Pattern detection (offline)
3. Cost tracking

### Phase 6 - Polish
1. Output formatting (tables, rich text)
2. Command auto-completion
3. Tests and documentation

---

## Complete Workflow Example

```
1. Human creates a task in a Workspace
   ↓
2. Orchestrator selects an agent (based on A/B tested personality)
   ↓
3. Agent reads internal documentation (RAG) to understand context
   ↓
4. Agent reads previous commits to resume where work stopped
   ↓
5. Agent works on the task
   ↓
6. If problem → Agent creates an Issue
   ↓
7. Agent Reviewer prioritizes the issue
   ↓
8. Agent finishes session → Creates a Commit with summary
   ↓
9. Agent Pattern Analyzer analyzes the commit:
    - Identifies patterns
    - Suggests improvements
    - Updates documentation
   ↓
10. Costs are tracked and analyzed
   ↓
11. Next agent can resume with full context
```

---

## Success Criteria

- ✅ Agents can seamlessly track work sessions
- ✅ Historical context is easily accessible
- ✅ Issues are systematically captured and prioritized
- ✅ Knowledge base grows organically from agent interactions
- ✅ Costs are transparent and optimized
- ✅ System is agent-friendly (simple CLI commands)
- ✅ Workspaces provide proper isolation
- ✅ A/B testing continuously improves agent effectiveness
