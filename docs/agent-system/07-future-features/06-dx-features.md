# Developer Experience (DX) Features

## Feature 19: Interactive Mode (REPL Shell)

### Overview

An interactive shell (REPL) mode that provides persistent context, command auto-completion, command history navigation, and faster workflow by eliminating repetitive `agentflow` prefix and flag repetition.

### Why It Matters

- **Faster Workflow**: Type less, accomplish more
- **Context Awareness**: Project, agent, and other context persist across commands
- **Discoverability**: Auto-completion helps discover available commands
- **Better UX**: Similar to Python REPL, Django shell, Git REPL

### Implementation Complexity

**Moderate** - Requires:
- Interactive command loop (readline-based)
- Context management (state persistence)
- Auto-completion engine
- Command history (up/down arrow navigation)

**Phase**: Phase 1 (nice to have, not critical for MVP)

### How It Works

#### Starting Interactive Mode

```bash
# Start interactive shell
agentflow interactive

# Or short form
agentflow shell

# Output:
# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                    AgentFlow Interactive Shell                          ║
# ║                        Version 0.0.1 - Phase 0                          ║
# ╠══════════════════════════════════════════════════════════════════════════╣
# ║                                                                           ║
# ║  💡 Tips:                                                                ║
# ║    • Press TAB to auto-complete commands                               ║
# ║    • Press UP/DOWN to navigate command history                        ║
# ║    • Type 'help' for available commands                               ║
# ║    • Type 'exit' or Ctrl+D to quit                                     ║
# ║                                                                           ║
# ║  📋 Current Context:                                                    ║
# ║    Project: website-redesign (default)                               ║
# ║    Agent:   agent-dev-001 (Jean)                                     ║
# ║    Session: Not active                                               ║
# ║                                                                           ║
# ║  Ready! Type a command or 'help' to get started.                       ║
# ╚══════════════════════════════════════════════════════════════════════════╝
#
# agentflow>
```

#### Basic Usage in Interactive Mode

```bash
agentflow>

# Commands work WITHOUT 'agentflow' prefix

# View current context
> context

# Output:
# Current Context:
#   Project: website-redesign
#   Agent:   agent-dev-001 (Jean)
#   Session: None

# List tasks (context-aware - uses current project and agent)
> task list

# Output:
# Tasks for agent-dev-001 in project 'website-redesign':
#   • #123: Implement authentication (in_progress)
#   • #124: Fix login bug (backlog)

# View task details
> task view 123

# Output:
# Task: #123 - Implement authentication
# Status: in_progress
# Assigned to: Jean (agent-dev-001)
# ...

# Create new task
> task create --title "Add password reset" --priority P2

# Output:
# ✅ Task created
#    Task: #145 - Add password reset
#    Project: website-redesign (inherited from context)
#    Priority: P2
#    Agent: agent-dev-001 (inherited from context)

# Switch agent
> context set-agent agent-dev-002

# Output:
# Context updated: Agent changed to agent-dev-002 (Alice)

# Now commands use Alice as the agent
> task list

# Output:
# Tasks for agent-dev-002 in project 'website-redesign':
#   • #130: Design homepage (in_progress)
#   • #131: Create components (backlog)

# Switch project
> context set-project mobile-app

# Output:
# Context updated: Project changed to 'mobile-app'
# Agent: agent-dev-002 (preserved)

# Show all context
> context show

# Output:
# Current Context:
#   Project: mobile-app
#   Agent:   agent-dev-002 (Alice)
#   Session: None
#   Date:    2025-01-21

# Clear context
> context clear --project

# Output:
# Project context cleared
# Current: Agent only (agent-dev-002)
```

#### Auto-Completion

```bash
agentflow>

# Press TAB to see available commands
> [TAB]

# Output (shows all top-level commands):
# auth      agents     context    help       org        project    role       task
# exit       quit       status

# Continue typing
> task [TAB]

# Output (shows task subcommands):
# create     list       view       update     assign     delete     complete
# approve    reject     timeline

# Continue
> task view [TAB]

# Output (shows task IDs):
# #123      #124      #125      #130      #131

# Final command
> task view #123

# Auto-completion also works for:
# - Agent codes
> context set-agent [TAB]
# agent-dev-001  agent-dev-002  agent-qa-001

# - Project slugs
> context set-project [TAB]
# mobile-app  website-redesign  infrastructure

# - Role slugs
> role add-document [TAB]
# python-dev  react-dev  qa-engineer

# - Flags
> task list [TAB]
# --agent     --project   --status   --priority
```

#### Command History

```bash
agentflow>

# Navigate history with UP/DOWN arrows
> [UP ARROW]

# Shows previous command
> task list

# Press UP again
> [UP ARROW]

# Shows command before that
> context set-agent agent-dev-002

# Can search history with Ctrl+R
> [Ctrl+R]
(reverse-i-search)`task list':

# Found match (most recent)
# (press Enter to execute, Ctrl+C to cancel)

# Full history
> history

# Output:
# Command History (last 20):
#   20  task list
#   19  task view #123
#   18  context set-agent agent-dev-002
#   17  task list
#   16  context show
#   15  task create --title "Add password reset" --priority P2
#   14  context set-project website-redesign
#   13  ...
```

#### Helpful Features in Interactive Mode

```bash
# Multi-line commands
# Use backslash \ to continue on next line
> task create \
  --title "Very long task title that spans multiple lines" \
  --description "This is the description" \
  --priority P1

# Output:
# ✅ Task created successfully

# Shell commands (execute system commands)
> !ls -la

# Output:
# (runs system ls -la command)

# Pipe to external commands
> task list | grep "in_progress"

# Output:
#   #123: Implement authentication (in_progress)
#   #130: Design homepage (in_progress)

# Clear screen
> clear

# Output:
# (screen is cleared, shows fresh prompt)

# Get help
> help

# Output:
# AgentFlow Interactive Shell - Help
# ─────────────────────────────────────
#
# Context Commands:
#   context              Show current context
#   context show         Show detailed context
#   context set-agent    Set default agent
#   context set-project  Set default project
#   context clear        Clear context
#
# Task Commands:
#   task list            List tasks
#   task view <id>       View task details
#   task create          Create new task
#   task update          Update task status
#   ...
#
# Core Commands:
#   status               Show status
#   version              Show version
#   help                 Show this help
#   exit / quit          Exit shell
#
# Tips:
#   - TAB to auto-complete
#   - UP/DOWN for history
#   - Ctrl+R to search history
#   - !command to run shell command
#   - | to pipe to external commands
```

#### Configuration

```bash
# Set default context on shell start
agentflow config set interactive.default_project website-redesign
agentflow config set interactive.default_agent agent-dev-001

# Now shell starts with this context
agentflow interactive

# Output:
# Starting interactive shell...
# Context loaded:
#   Project: website-redesign (from config)
#   Agent:   agent-dev-001 (from config)
#
# agentflow>

# Custom prompt format
agentflow config set interactive.prompt "{agent}@{project} > "

# Output:
# jean@website-redesign > task list

# Enable syntax highlighting (if supported)
agentflow config set interactive.colors true

# Set history size
agentflow config set interactive.history_size 1000
```

#### Advanced Features

```bash
# Command chaining
> task create --title "Fix bug" && task list --status backlog

# Output:
# ✅ Task created
# Tasks in backlog:
#   • #146: Fix bug (backlog)

# Background commands
> task export --format json &

# Output:
# [Running in background...]
# Task ID: bg-1
#
# agentflow> jobs
#
# Background jobs:
#   bg-1: Running (task export)

# Check job status
> jobs --wait bg-1

# Output:
# Waiting for bg-1...
# ✅ Complete: Exported to tasks.json

# Macros (save command sequences)
> macro save "my-session"
> context set-agent agent-dev-001
> context set-project website-redesign
> session start
> macro end

# Run macro
> macro run "my-session"

# Output:
# Executing macro: my-session
# → context set-agent agent-dev-001
# → context set-project website-redesign
# → session start
```

### Data Model

```python
class InteractiveContext(BaseModel):
    project_id: Optional[str] = None
    project_slug: Optional[str] = None
    agent_id: Optional[str] = None
    agent_code: Optional[str] = None
    session_id: Optional[str] = None

    # History
    command_history: List[str] = []
    history_index: int = -1

class ShellConfig(BaseModel):
    default_project: Optional[str] = None
    default_agent: Optional[str] = None

    prompt_template: str = "{project}> "
    enable_completion: bool = True
    enable_history: bool = True
    history_size: int = 1000

    # Colors/Style
    enable_colors: bool = True
    show_context_in_prompt: bool = True
```

### CLI Commands

```bash
# Starting shell
agentflow interactive
agentflow shell
agentflow repl

# In-shell commands
context
context show
context set-agent <agent>
context set-project <project>
context clear
help
history
exit
quit
```

---

## Feature 20: Aliases & Custom Shortcuts

### Overview

Create custom shortcuts for frequently used or complex commands, reducing typing and simplifying workflows. Aliases can include parameters and be shared across team members.

### Why It Matters

- **Less Typing**: One word instead of long command chains
- **Complex Simplified**: Encapsulate complex workflows into simple commands
- **Consistency**: Team uses same commands for same operations
- **Personalization**: Each user can have their own aliases

### Implementation Complexity

**Low** - Requires:
- Alias storage (local config file)
- Command substitution engine
- Parameter expansion

**Phase**: Phase 1 (nice DX improvement)

### How It Works

#### Creating Aliases

```bash
# Simple alias - single command
agentflow alias create \
  --name "my-tasks" \
  --command "task list --agent agent-dev-001"

# Usage
agentflow my-tasks

# Equivalent to:
agentflow task list --agent agent-dev-001

# Alias with parameters
agentflow alias create \
  --name "new-task" \
  --command "task create --project website-redesign --priority P1"

# Usage with additional parameters
agentflow new-task --title "Fix bug" --assign-to agent-dev-002

# Equivalent to:
agentflow task create --title "Fix bug" --assign-to agent-dev-002 --project website-redesign --priority P1

# Chain multiple commands
agentflow alias create \
  --name "pull-start" \
  --command "agent pull && session start"

# Usage
agentflow pull-start

# Executes:
# 1. agentflow agent pull agent-dev-001
# 2. agentflow session start --agent agent-dev-001
```

#### Alias Parameters

```bash
# Aliases with placeholders
agentflow alias create \
  --name "create-for" \
  --command "task create --title \"{title}\" --project {project} --priority P{priority}"

# Usage with parameters
agentflow create-for --title "Fix auth" --project website-redesign --priority 0

# Placeholders:
# {title}   → Replaced by --title value
# {project} → Replaced by --project value
# {priority}→ Replaced by --priority value

# Alias with all parameters
agentflow alias create \
  --name "assign-task" \
  --command "task update --task {task_id} --assign-to {agent_code}"

# Usage
agentflow assign-task --task_id 123 --agent_code agent-dev-002

# Output:
# ✅ Task #123 reassigned to agent-dev-002
```

#### Managing Aliases

```bash
# List all aliases
agentflow alias list

# Output:
# Aliases (10):
#
# Personal Aliases:
#   my-tasks      → task list --agent agent-dev-001
#   pull-start    → agent pull && session start
#   new-task      → task create --project website-redesign --priority P1
#   quick-review  → task review --latest
#   standup       → agent standup {agent}
#   daily-report  → task report --period 1d --format markdown
#
# Shared Aliases:
#   review-me     → task review-queue --agent agent-lead-001
#   my-work       → task list --mine --status in_progress,backlog
#
# System Aliases (read-only):
#   status        → status show
#   version       → version show

# View alias details
agentflow alias view my-tasks

# Output:
# 🔧 Alias: my-tasks
# ─────────────────────────────────────
# Command: task list --agent agent-dev-001
#
# Created: 2025-01-21 by agent-dev-001
# Type: personal
# Usage: 23 times
# Last used: 2 hours ago

# Edit alias
agentflow alias update my-tasks \
  --command "task list --agent agent-dev-001 --status in_progress,backlog"

# Delete alias
agentflow alias delete my-tasks

# Output:
# Deleted alias: my-tasks
```

#### Shared Aliases

```bash
# Create shared alias (available to all team members)
agentflow alias create \
  --name "team-standup" \
  --command "task report --period 1d --all-agents --format markdown" \
  --shared

# Export alias to file for sharing
agentflow alias export team-standup --file team-standup.alias

# Team member can import
agentflow alias import --file team-standup.alias

# Or sync from shared location
agentflow alias sync --from https://config.company.com/aliases.json
```

#### Dynamic Aliases

```bash
# Alias with date
agentflow alias create \
  --name "today-report" \
  --command "task report --date {today} --format markdown"

# Usage
agentflow today-report

# {today} is automatically replaced with current date

# Alias with agent from context
agentflow alias create \
  --name "my-work" \
  --command "task list --agent {current_agent}"

# Usage
agentflow my-work

# {current_agent} uses currently configured agent

# Alias with weekday
agentflow alias create \
  --name "sprint-report" \
  --command "task report --period {week_start}..{today} --sprint"

# Usage on Friday
agentflow sprint-report

# {week_start} = Monday of current week
# {today} = today's date
```

#### Built-in System Aliases

```bash
# System aliases (always available, read-only)
agentflow alias list --system

# Output:
# System Aliases (read-only):
#
#   status    → status show
#   version   → version show
#   help      → help show
#   config    → config show
#   ctx       → context show
```

### Alias Examples

```bash
# Common workflow aliases
agentflow alias create \
  --name "daily-start" \
  --command "agent pull && session start && session log --message 'Starting work'"

agentflow alias create \
  --name "daily-end" \
  --command "session log --message 'Ending work' && session stop"

# Project-specific aliases
agentflow alias create \
  --name "website-tasks" \
  --command "task list --project website-redesign"

agentflow alias create \
  --name "mobile-tasks" \
  --command "task list --project mobile-app"

# Agent-specific aliases
agentflow alias create \
  --name "jean-work" \
  --command "task list --agent agent-dev-001 --status in_progress"

# Review workflow
agentflow alias create \
  --name "review-my-work" \
  --command "task create --type review --parent-task {latest_task} --for-supervisor"

# Reporting aliases
agentflow alias create \
  --name "weekly-summary" \
  --command "task report --period 1w --all-agents --format markdown --output weekly.md"

agentflow alias create \
  --name "agent-stats" \
  --command "agent timeline --agent {current_agent} --period 7d"
```

### Data Model

```python
class Alias(BaseModel):
    id: str
    name: str  # "my-tasks"
    command_template: str  # "task list --agent agent-dev-001"

    # Scope
    scope: Literal["personal", "shared", "system"]
    created_by: str  # Agent ID
    created_at: datetime

    # Usage stats
    usage_count: int = 0
    last_used_at: Optional[datetime] = None

    # Validation
    parameters: List[str] = []  # Required parameters: ["{title}", "{project}"]

class AliasParameter(BaseModel):
    name: str  # "title", "project", etc.
    placeholder: str  # "{title}", "{project}"
    required: bool = True
    default_value: Optional[str] = None
```

### CLI Commands

```bash
# Creating
agentflow alias create --name <name> --command "<cmd>"
agentflow alias create --name <name> --command "<cmd>" --shared

# Managing
agentflow alias list
agentflow alias list --personal
agentflow alias list --shared
agentflow alias list --system
agentflow alias view <name>
agentflow alias update <name> --command "<new-cmd>"
agentflow alias delete <name>

# Import/Export
agentflow alias export <name> --file <file>
agentflow alias import --file <file>
agentflow alias sync --from <url>
```

---

## Feature 21: Diff Viewer & VCS Integration

### Overview

Visualize differences between objects (role versions, task states, agent configurations, etc.) and integrate with version control systems (Git) to link work with code changes.

### Why It Matters

- **Change Tracking**: See what changed between versions
- **Review**: Visual review of modifications
- **Traceability**: Link agent work to code commits
- **Debugging**: Understand evolution of configurations

### Implementation Complexity

**Moderate** - Requires:
- Diff algorithm for structured data
- Git integration (log, show, blame)
- Change detection and visualization

**Phase**: Phase 1-2 (useful features)

### How It Works

#### Role Version Diff

```bash
# Compare two role versions
agentflow diff role python-dev --from v3 --to v4

# Output:
# 📊 Diff: python-dev (Role)
# ─────────────────────────────────────
# From: v3 (Jan 15, 2025 09:00)
# To:   v4 (Jan 21, 2025 14:30)
#
# Summary:
#   Documents: +1 added, 1 modified
#   Version: 3 → 4
#
# 📄 Description:
#   - "Senior Python developer with FastAPI expertise"
#   + "Senior Python developer with FastAPI and PostgreSQL expertise"
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Added PostgreSQL specialization
#
# 📄 Documents:
#
#   Added postgres-patterns.md (45 lines)
#   + # PostgreSQL Patterns
#   + ## Connection Management
#   + ...
#
# Modified testing-guidelines.md (from 67 to 89 lines):
#   +22 lines
#
#   ## Integration Tests (NEW)
#   + ### Testing with pg
#   + - Use pytest-asyncio and asyncpg for async tests
#   + - Create test database fixtures
#   + - Rollback transactions after each test
#   ...
#
# 📊 Impact:
#   Agents using this role: 3
#   Need to pull: YES (new content available)
#   Breaking changes: NO (additive only)
#
# 📋 Affected Agents:
#   • agent-dev-001 (Jean) - Last pulled: v2 (OUTDATED)
#   • agent-dev-002 (Alice) - Last pulled: v3 (OUTDATED)
#   • agent-dev-003 (Charlie) - Last pulled: v4 (CURRENT)
#
# 💡 Action: agentflow agent pull agent-dev-001,agent-dev-002

# Side-by-side diff
agentflow diff role python-dev --from v3 --to v4 --format side-by-side

# Output:
# v3 (Old)                        |   v4 (New)
# --------------------------------|---------------------------------
# Senior Python developer      |   Senior Python developer
# with FastAPI expertise       |   with FastAPI and PostgreSQL
#                                 |   ^^^^^^^^^^^^^^^^ (added)
#
# Documents:                      |   Documents:
#   3 documents                   |   4 documents (+1)
#   • testing-guidelines          |   • testing-guidelines (modified)
#   • api-conventions             |   • api-conventions
#   • async-patterns              |   • async-patterns
#                                 |   • postgres-patterns (new)
```

#### Task State Diff

```bash
# Compare task state changes over time
agentflow diff task 123 --at "2025-01-21 09:00" --at "2025-01-21 17:00"

# Output:
# 📊 Diff: Task #123
# ─────────────────────────────────────
# Task: Implement user authentication
# Comparison: 09:00 → 17:00 (Jan 21, 2025)
#
# Changes:
#
# Status:
#   - backlog
#   + in_progress
#
# Progress:
#   - 0%
#   + 50%
#
# Session Logs (5 added):
#   + [09:05] Starting work on authentication
#   + [10:30] Implemented JWT token validation
#   + [11:45] Created user model with bcrypt
#   + [14:20] Added authentication endpoint
#   + [16:15] Testing login flow
#
# Trust Score:
#   - 70.0 (before session)
#   + 72.5 (after session)
#   ^ +2.5 points (session was productive)
#
# Estimated vs Actual:
#   Estimate: 4h
#   Actual so far: 2h (50% complete)
#   On track: YES
```

#### Agent Configuration Diff

```bash
# Compare agent state before and after
agentflow diff agent agent-dev-001 --before "2025-01-01" --after "2025-01-21"

# Output:
# 📊 Diff: agent-dev-001 (Jean)
# ─────────────────────────────────────
# Period: Jan 1 → Jan 21, 2025
#
# Trust Score:
#   - 65.0 (Jan 1)
#   + 72.5 (Jan 21)
#   ^ +7.5 points (+11.5%)
#
# Status:
#   Unchanged: active
#
# Role:
#   Unchanged: python-dev
#
# Skills:
#   - python-testing (v2)
#   + python-testing (v4) ← Pulled new version
#   - python-api (v2)
#   + python-api (v4) ← Pulled new version
#   - python-async (v2)
#   + python-async (v4) ← Pulled new version
#   + postgres-patterns (NEW) ← Added from role update
#
# Tasks Completed:
#   Tasks in period: 15
#   Completion rate: 93% (14/15 accepted, 1 rejected)
#
# Session Activity:
#   Sessions: 12
#   Total hours: 56h
#   Avg per session: 4.7h
```

#### Git Integration

```bash
# View Git commits for a specific task
agentflow git log --task 123

# Output:
# 📊 Git History - Task #123
# ─────────────────────────────────────
# Task: Implement user authentication
# Agent: Jean (agent-dev-001)
# Project: website-redesign
#
# Commits: 5
# Files changed: 12
# Lines added: 547
# Lines deleted: 23
#
# ┌──────────────────────────────────────────────────────────────────────────┐
# │ Commit    │ Date       │ Author │ Message                          │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ 1a2b3c4d  │ Jan 21     │ Jean   │ feat: implement JWT token       │
# │           │ 14:32      │        │   validation (45 lines)           │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ 2b3c4d5e  │ Jan 21     │ Jean   │ feat: add user model with        │
# │           │ 11:15      │        │   bcrypt hashing (78 lines)      │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ 3c4d5e6f  │ Jan 20     │ Jean   │ feat: create authentication     │
# │           │ 16:45      │        │   endpoint (102 lines)          │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ 4d5e6f7a  │ Jan 20     │ Jean   │ fix: resolve merge conflict      │
# │           │ 13:20      │        │   (23 lines)                     │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ 5e6f7a8b  │ Jan 20     │ Jean   │ chore: update dependencies       │
# │           │ 10:00      │        │   (pyproject.toml)                │
# └──────────────────────────────────────────────────────────────────────────┘

# Show detailed commit
agentflow git show 1a2b3c4d

# Output:
# commit 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9
# Author: Jean <jean@company.com>
# Date:   Mon Jan 21 14:32:45 2025 +0000
#
#     feat: implement JWT token validation
#
#     Added JWT token validation logic with:
#     - Token generation with HS256
#     - Token validation middleware
#     - Refresh token support
#
# Refs: #123
#
# diff --git a/src/auth/jwt.py b/src/auth/jwt.py
# index abc123..def456 100644
# --- a/src/auth/jwt.py
# +++ b/src/auth/jwt.py
# @@ -45,6 +45,12 @@
#  def validate_token(token: str) -> bool:
#      """Validate JWT token"""
# -    return jwt.decode(token, SECRET)
# +    try:
# +        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
# +        return payload.get("exp", 0) > time.time()
# +    except jwt.DecodeError:
# +        return False
#
#  def generate_token(user_id: str) -> str:
#      """Generate JWT token for user"""
# -    return jwt.encode({"user_id": user_id}, SECRET)
# +    payload = {
# +        "user_id": user_id,
# +        "exp": time.time() + 3600,  # 1 hour
# +        "iat": time.time()
# +    }
# +    return jwt.encode(payload, SECRET, algorithms=["HS256"])

# View files changed by task
agentflow git files --task 123

# Output:
# Files changed by task #123:
#
# Modified:
#   src/auth/jwt.py         (+45 lines)
#   src/models/user.py       (+78 lines)
#   src/api/auth.py         (+102 lines)
#   pyproject.toml          (+3 dependencies)
#
# Added:
#   tests/test_auth.py      (+67 lines)
#
# Total: 4 files modified, 1 file added, 295 lines changed

# Git blame - see who changed what
agentflow git blame src/auth/jwt.py --line 50

# Output:
# src/auth/jwt.py line 50:
#   "return jwt.decode(token, SECRET)"
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Authored by: Jean (agent-dev-001)
#   Date: Jan 21, 2025 14:32
#   Commit: 1a2b3c4d - "feat: implement JWT token validation"
#   Task: #123
```

#### Pull Request Integration (Future)

```bash
# Create PR for task completion
agentflow git create-pr --task 123

# Output:
# ✅ Pull request created
#    Task: #123 - Implement user authentication
#    Branch: feature/task-123-auth
#    Base: main
#    PR: #47
#
# PR includes:
#   • Commits: 5
#   • Files: 4
#   • Lines: +295, -23
#
# Link: https://github.com/org/repo/pull/47
#
# Ready for review by: Tech Lead

# Update task when PR is merged
agentflow git watch-pr --pr 47 --task 123
# When PR is merged → Task marked completed automatically
```

### Data Model

```python
class DiffResult(BaseModel):
    diff_type: Literal["role", "task", "agent", "config"]
    from_id: str  # Version ID, timestamp, etc.
    to_id: str
    changes: List["ChangeItem"]

    summary: str  # Human-readable summary
    impact: str  # "Need to pull", "Breaking changes", etc.

class ChangeItem(BaseModel):
    type: Literal["added", "removed", "modified"]
    section: str  # "description", "documents", "trust_score"
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    description: Optional[str] = None

class GitIntegration(BaseModel):
    task_id: Optional[str] = None
    commit_hash: str
    author: str
    timestamp: datetime
    message: str
    files_changed: List[str]
    diff: Optional[str] = None
```

### CLI Commands

```bash
# Diff
agentflow diff role <role> --from <v3> --to <v4>
agentflow diff task <id> --at <date1> --at <date2>
agentflow diff agent <agent> --before <date> --after <date>

# Git
agentflow git log --task <id>
agentflow git show <commit-hash>
agentflow git files --task <id>
agentflow git blame <file> --line <number>

# PR (Future)
agentflow git create-pr --task <id>
agentflow git watch-pr --pr <number> --task <id>
```

---

## Implementation Notes

### Dependencies

- **Feature 19 (Interactive Mode)**: Requires readline/repl library, command history
- **Feature 20 (Aliases)**: Requires config storage, command substitution
- **Feature 21 (Diff/VCS)**: Requires diff algorithm, Git integration

### Priority

1. **Feature 20 (Aliases)** - Low complexity, high value
2. **Feature 19 (Interactive)** - Moderate complexity, high value
3. **Feature 21 (Diff/VCS)** - Moderate complexity, medium value

### Phasing

- **Phase 1**: Basic aliases, simple diff (role versions)
- **Phase 2**: Interactive shell, Git log integration
- **Phase 3**: Advanced diff visualization, PR integration

---

**Document Version**: 1.0
**Created**: 2025-01-21
**Status**: 🎨 Design proposal - Developer Experience improvements
