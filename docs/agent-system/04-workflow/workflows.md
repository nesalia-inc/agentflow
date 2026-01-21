# Workflow Examples

## Workflow Examples

### Example 1: Creating a Role and Assigning to Agents

```bash
# 1. Create a role on the API
agentflow role create \
  --name "Python Developer" \
  --slug "python-dev" \
  --description "Senior Python developer specializing in FastAPI and PostgreSQL. Follow TDD, maintain >80% coverage." \
  --level project

# Output:
# ✓ Role created
#   Name:        Python Developer
#   Slug:        python-dev
#   Level:       project
#   Version:     1

# 2. Add documents to the role
agentflow role add-document python-dev \
  --name "testing-guidelines" \
  --file "./docs/testing-guidelines.md"

agentflow role add-document python-dev \
  --name "api-conventions" \
  --file "./docs/api-conventions.md"

agentflow role add-document python-dev \
  --name "async-patterns" \
  --file "./docs/async-patterns.md"

# Output:
# ✓ Document added to role python-dev
#   Name: testing-guidelines
#   File: testing-guidelines.md

# 3. View role details
agentflow role view python-dev

# Output:
# Role: Python Developer (python-dev)
#
# Level:       project
# Description: Senior Python developer specializing in FastAPI...
# Version:     1
# Documents:   3
#   • testing-guidelines
#   • api-conventions
#   • async-patterns

# 4. Create agents and assign the role
agentflow agent create \
  --name "Jean" \
  --code "agent-dev-001" \
  --role "python-dev" \
  --level project \
  --project website-redesign

agentflow agent create \
  --name "Alice" \
  --code "agent-dev-002" \
  --role "python-dev" \
  --level project \
  --project website-redesign

# Output:
# ✓ Agent created
#   Name:   Jean
#   Code:   agent-dev-001
#   Role:   python-dev (Python Developer)
#   Level:  project
#   Status: active
#   Trust Score: 50.0
#
# Next: Pull role to generate skills
#   agentflow agent pull agent-dev-001
```

### Example 2: Pulling Agent Role & Starting Work Session

```bash
# 1. Pull agent role (generates Claude Code skills)
agentflow agent pull agent-dev-001

# Output:
# ✓ Pulled role for agent-dev-001
#
# Role: Python Developer (python-dev)
# Version: 3
#
# Generated 3 Claude Code skills:
#   ✓ python-testing
#     → ~/.claude/skills/python-testing/SKILL.md
#     From: testing-guidelines.md
#
#   ✓ python-api
#     → ~/.claude/skills/python-api/SKILL.md
#     From: api-conventions.md
#
#   ✓ python-async
#     → ~/.claude/skills/python-async/SKILL.md
#     From: async-patterns.md
#
# Skills are now available in Claude Code!
# Use /python-testing to invoke, or Claude will auto-load when relevant.

# 2. Start work session
agentflow session start --agent agent-dev-001 --project website-redesign

# Output:
# ✓ Session started
#   Agent:   agent-dev-001 (Jean)
#   Project: website-redesign
#   Started: 2025-01-21 09:00:00 UTC
#
# Active Session: session-abc-123
#
# Note: Role pulled at 2025-01-21 08:55:00 UTC
#       Skills available: python-testing, python-api, python-async

# 3. Log activity
agentflow session log \
  --message "Starting work on task #123: user authentication" \
  --type activity

# Output:
# ✓ Logged activity
#   Session: session-abc-123
#   Time:    2025-01-21 09:05:00 UTC
#   Message: Starting work on task #123: user authentication

# 4. Log with context
agentflow session log \
  --message "Implemented JWT token validation in src/auth/jwt.py" \
  --context '{"file": "src/auth/jwt.py", "lines": "45-89", "progress": 50}' \
  --tags "implementation,authentication"

# Output:
# ✓ Logged activity
#   Message: Implemented JWT token validation in src/auth/jwt.py
#   Context: {"file": "src/auth/jwt.py", "lines": "45-89", "progress": 50}
#   Tags:    implementation, authentication

# 5. Log a problem
agentflow session log \
  --message "Blocking issue: Missing user model definition" \
  --type problem \
  --task 123

# Output:
# ✓ Logged problem
#   Message: Blocking issue: Missing user model definition
#   Task:    #123
#   Blocker: true

# 6. Stop session
agentflow session stop

# Output:
# ✓ Session stopped
#   Session:  session-abc-123
#   Duration: 2h 15m 30s
#   Tasks:    1 worked on
#   Logs:     7 events created
#
# Summary:
#   • Task #123: 50% complete
#   • Issue reported: Missing user model
```

### Example 3: Viewing Agent Activity

```bash
# 1. View agent timeline
agentflow agent timeline agent-dev-001 --limit 10

# Output:
# Timeline for agent-dev-001 (Jean)
# Role: Python Developer (python-dev)
#
# 2025-01-21 11:30:00 UTC
#   [session_stop] Session ended (duration: 2h 15m)
#
# 2025-01-21 11:25:00 UTC
#   [session_log] Implemented JWT token validation
#   Context: src/auth/jwt.py lines 45-89
#
# 2025-01-21 11:15:00 UTC
#   [session_log] Starting work on task #123
#   Task: User authentication
#
# 2025-01-21 09:00:00 UTC
#   [session_start] Session started
#   Skills available: python-testing, python-api, python-async

# 2. Search logs
agentflow logs search "authentication" --agent agent-dev-001

# Output:
# 5 logs found for 'authentication':
#
# 2025-01-21 11:15:00 UTC
#   Starting work on task #123: user authentication
#
# 2025-01-21 11:25:00 UTC
#   Implemented JWT token validation
#
# ...

# 3. View session details
agentflow session view session-abc-123

# Output:
# Session: session-abc-123
#
# Agent:    agent-dev-001 (Jean)
# Role:     Python Developer (python-dev)
# Project:  website-redesign
# Status:   Stopped
# Duration: 2h 15m 30s
#
# Tasks Worked On:
#   • #123: User authentication (50% complete)
#
# Events (7 total):
#   • 09:00 - Session started
#   • 09:05 - Starting work on task #123
#   • 09:30 - Implemented JWT token validation
#   • 10:15 - Blocking issue: Missing user model
#   • 10:30 - Question: Should we use bcrypt?
#   • 11:00 - Created user model
#   • 11:15 - Session stopped
```

---
