# Work Sessions

## Work Sessions

### What is a Work Session?

A **work session** represents a continuous block of time where an agent is actively working on tasks. It's similar to:

- A workday for humans
- A git commit session
- A programming IDE session

### Session Lifecycle

```
          Pull Updates
                ↓
[START] → Started → Logging → [STOP] → Stopped
                ↓
           Log Events
```

#### States

1. **Started**: Session initiated
   - Agent has pulled latest updates
   - Ready to begin work
   - No activity yet

2. **Logging**: Active session
   - Agent is working
   - Logging events/activities
   - Can transition to 'stopped'

3. **Stopped**: Session ended
   - Final duration calculated
   - Tasks worked on recorded
   - Session immutable (read-only)

### Why Sessions Matter

Sessions provide:

1. **Temporal context**: When did work happen?
2. **Grouping**: What work was done together?
3. **Accountability**: Who worked on what, when?
4. **Metrics**: Session duration, tasks completed, logs count
5. **Continuity**: Resume work where you left off

### Session Metadata

Each session tracks:

```json
{
  "id": "uuid",
  "agent_id": "uuid",
  "project_id": "uuid",
  "status": "logging",
  "started_at": "2025-01-21T09:00:00Z",
  "stopped_at": null,
  "duration_seconds": null,
  "tasks_worked_on": ["task-uuid-1", "task-uuid-2"],
  "metadata": {
    "pull_summary": {
      "tasks_new": 2,
      "messages": 3
    },
    "environment": {
      "os": "linux",
      "tools": ["python", "git"]
    }
  }
}
```

### Session Rules

1. **One active session per agent**
   - Agent cannot start new session if one is already active
   - Must stop current session first

2. **Sessions belong to projects**
   - Each session is in context of a specific project
   - Switching projects = new session

3. **Auto-stop on error/crash**
   - If agent crashes, session is marked as stopped
   - Duration recorded up to crash point

4. **Immutable after stop**
   - Stopped sessions cannot be modified
   - Logs are part of permanent record

### Starting a Session

When an agent starts a session:

1. **Validate prerequisites**
   - Agent is authenticated
   - Agent has active status
   - Project context is set
   - No active session exists

2. **Pull updates automatically**
   - Get latest task assignments
   - Check for messages/mentions
   - Update agent context

3. **Create session record**
   - Set status to 'started'
   - Record start time
   - Link to agent and project

4. **Create session_start event**
   - Log in timeline
   - Include pull summary

### Stopping a Session

When an agent stops a session:

1. **Calculate duration**
   - `duration_seconds = stopped_at - started_at`

2. **Update session record**
   - Set status to 'stopped'
   - Record stop time
   - Save duration

3. **Create session_stop event**
   - Log in timeline
   - Include summary (tasks worked on, logs count)

4. **Make session immutable**
   - No further modifications allowed

### Session Auto-Stop (Future Enhancement)

**Question**: Should sessions auto-stop after inactivity?

**Options**:
1. **Timeout**: Auto-stop after N minutes of inactivity
2. **Manual only**: Only agent/user can stop
3. **Hybrid**: Auto-stop but allow resume within window

**Phase 0**: Manual stop only

---
