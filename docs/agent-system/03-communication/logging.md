# Agent Logging

## Agent Logging

### What is Agent Logging?

**Agent logging** is the mechanism by which agents record their activities, thoughts, progress, and observations during a work session. It's like:

- Developer commit messages
- Work diary / journal
- Activity stream
- Debug logs

### Log Types

Agents can log different types of events:

#### 1. Activity Logs
What the agent is doing:
```
"Working on user authentication module"
"Implementing JWT token validation"
"Refactoring database queries"
```

#### 2. Progress Logs
Status updates:
```
"Task #123: 50% complete - authentication flow implemented"
"Test coverage now at 75%"
"Identified performance bottleneck in user lookup"
```

#### 3. Problem Logs
Issues encountered:
```
"Error: Cannot connect to database - retrying..."
"Blocking issue: Missing API endpoint for user profile"
"Need clarification: Should password reset include security questions?"
```

#### 4. Decision Logs
Choices made and why:
```
"Chose bcrypt over SHA-256 for password hashing (security)"
"Decided to use Redis for session storage (performance)"
"Opted for PostgreSQL over MongoDB (relational data)"
```

#### 5. Escalation Logs
Messages to supervisor requiring attention:
```
"Blocking issue: Cannot continue task #123 without API documentation"
"Clarification needed: Task #124 specifies 'optimize' - which queries?"
"Proposal: Refactoring auth module would improve maintainability by 40%"
```

**Note**: These are logs FOR TRACKING. Actual communication with supervisor should use the message system (`agentflow agent send-message --to supervisor`).

### Log Structure

Each log entry is an `event` with type `session_log`:

```json
{
  "id": "uuid",
  "type": "session_log",
  "author_id": "agent-uuid",
  "session_id": "session-uuid",
  "project_id": "project-uuid",
  "content": {
    "message": "Implemented user authentication flow",
    "context": {
      "task_id": "task-uuid",
      "files": ["src/auth.py", "src/models/user.py"],
      "progress": 50,
      "status": "in_progress"
    },
    "tags": ["implementation", "authentication", "security"]
  },
  "mentions": [],
  "metadata": {
    "log_type": "activity",
    "confidence": 0.9,
    "blocker": false
  },
  "timestamp": "2025-01-21T10:15:00Z"
}
```

### Log Categories

Logs can be categorized for filtering:

**IMPORTANT: Log categories use domain-specific names, not classical logging levels**

Unlike traditional logging systems (DEBUG, INFO, WARNING, ERROR), AgentFlow uses semantic categories that describe the log's purpose:

1. **Status Updates**: Progress, milestones
2. **Code Changes**: Implementations, refactorings
3. **Issues/Blockers**: Problems, dependencies
4. **Questions**: Clarifications needed (logged for context, use messages for actual communication)
5. **Decisions**: Architectural choices
6. **Reviews**: Code reviews, feedback
7. **Escalations**: Issues requiring supervisor attention (logged for tracking)

**Why not DEBUG/INFO/WARNING/ERROR?**

| Traditional | AgentFlow Category | Why? |
|-------------|-------------------|------|
| DEBUG | Status Updates | "Debug" implies troubleshooting, agents log progress |
| INFO | All categories | Too generic, doesn't indicate log purpose |
| WARNING | Issues/Blockers | "Warning" is system-level, agents log domain issues |
| ERROR | Not applicable | Agents don't have "errors" - they log problems to solve |

**Log Category Examples**:

```bash
# Status update (not DEBUG or INFO)
agentflow session log --type status --message "Task #123: 50% complete"

# Code change (not INFO)
agentflow session log --type code-change --message "Refactored DB queries for 2.3x speedup"

# Issue/blocked (not WARNING)
agentflow session log --type issue --message "Missing API documentation for user profile"

# Question (not DEBUG)
agentflow session log --type question --message "Should we use bcrypt or argon2?"

# Decision (not INFO)
agentflow session log --type decision --message "Chose PostgreSQL over MongoDB (relational data needs)"

# Escalation (not ERROR)
agentflow session log --type escalation --message "Cannot proceed without external API access"
```

**Default Category for Auto-Generated Logs**:
- Session start/stop → "status"
- Task assigned → "status"
- Task completed → "status"
- Trust score change → "status"

**Filtering by Category**:
```bash
# Show all status updates
agentflow logs list --agent agent-dev-001 --category status

# Show all issues/blockers
agentflow logs list --agent agent-dev-001 --category issue

# Show multiple categories
agentflow logs list --agent agent-dev-001 --category status,decision,code-change
```

### Log Granularity

**Question**: How detailed should logs be?

**Too granular** (noise):
```
"Created variable 'x'"
"Added semicolon"
"Indented line 42"
```

**Too vague** (not useful):
```
"Working..."
"Did stuff"
"Made progress"
```

**Just right** (actionable):
```
"Implemented JWT token validation in src/auth/jwt.py (lines 45-89)"
"Refactored user lookup query - reduced from 3 queries to 1 (2.3x faster)"
"Encountering error with password reset email - SMTP connection timing out"
```

### Auto-Generated vs Manual Logs

**Auto-generated logs** (system-created):
- Session start/stop
- Task assigned/completed
- KPI updates
- Trust score changes

**Manual logs** (agent-created):
- Activity descriptions
- Progress updates
- Questions, decisions
- Escalations to supervisor

### Log Consumption

Who reads agent logs?

1. **Human users** (CEO)
   - Monitor progress
   - Understand what agents are doing
   - Debug issues

2. **Supervisors** (manager agents)
   - Review subordinate progress
   - Identify blockers needing intervention
   - Make task assignment decisions

3. **System analytics**
   - Generate reports
   - Calculate KPIs
   - Train models

### Log Storage & Retrieval

**Phase 0**: Local JSON array
```python
agent_events = [
  {
    "id": "uuid",
    "type": "session_log",
    "content": {...},
    "timestamp": "..."
  },
  ...
]
```

**Full system**: PostgreSQL `events` table with indexes on:
- `author_id` (agent's logs)
- `session_id` (session's logs)
- `timestamp` (chronological)
- `type` (filter by log type)
- `metadata` (tags, categories)

---
