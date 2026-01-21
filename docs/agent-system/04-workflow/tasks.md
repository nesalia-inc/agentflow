# Tasks System

## Tasks System

### What are Tasks?

**Tasks** represent units of work that agents complete. They are the primary way agents contribute to projects.

**Task Lifecycle**:
```
backlog → assigned → in_progress → ready_review → completed
                ↓
              blocked
                ↓
              cancelled
```

### Task Types

For Phase 0, three task types are supported:

| Type | Description | Created By |
|------|-------------|------------|
| **development** | New features, implementations, enhancements | User, Manager Agents |
| **bug** | Bug fixes, error corrections | User, Manager Agents, System |
| **review** | Review and approval of work | System (automatic) |

**Future Types** (not in Phase 0):
- `feature` (large features)
- `refactor` (code refactoring)
- `documentation` (documentation work)
- `testing` (dedicated testing tasks)

### Task Structure

Each task contains:

```yaml
# Identity
id: uuid
type: development | bug | review
title: string
description: string

# Assignment
project_id: uuid
assigned_agent_id: uuid  # Who works on it
parent_task_id: uuid     # For reviews (points to original task)

# Status & Priority
status: backlog | assigned | in_progress | ready_review | completed | blocked | cancelled
priority: P0 | P1 | P2 | P3

# Metadata
tags: [string]           # ex: ["authentication", "security"]
deadline: datetime
github_issue_id: int     # For future GitHub sync
metadata: {}            # JSON for custom fields

# Timestamps
created_at: datetime
updated_at: datetime
started_at: datetime
completed_at: datetime
```

### Task Creation

Tasks can be created by:

**1. Human User**:
```bash
agentflow task create \
  --title "Implement user authentication" \
  --type development \
  --priority P1 \
  --project website-redesign \
  --assign-to agent-dev-001
```

**2. Manager Agents**:
```bash
# Tech Lead creating task for subordinate
agentflow task create \
  --title "Fix login bug" \
  --type bug \
  --priority P0 \
  --assign-to agent-dev-002 \
  --as agent-lead-001
```

**3. System (Automatic)**:
- Review tasks created when agent marks work "ready for review"

### Task Assignment

#### Task Assignment Scope

**IMPORTANT: Tasks are assigned at the PROJECT level, not globally**

Each task belongs to a specific project (`project_id` is required). Even if an agent works on multiple projects, their tasks are scoped to each project:

**Example:**
```
Agent: Alice (agent-dev-002)

Project A (website-redesign):
  Role: Senior Developer
  Tasks:
    • #123: Implement auth (in_progress)
    • #124: Fix login bug (backlog)

Project B (mobile-app):
  Role: Tech Lead
  Tasks:
    • #201: Review API design (in_progress)
    • #202: Plan sprint (backlog)
```

**Why Project-Level Assignment:**
1. **Clarity**: A task always belongs to one specific project
2. **Context**: When agent starts a session for Project A, they see only Project A tasks
3. **Isolation**: Project A tasks don't interfere with Project B tasks
4. **Role-specific**: Same agent may have different role/tasks in different projects

**Viewing Tasks (Filtered by Project):**
```bash
# List agent's tasks for a specific project
agentflow task list --agent agent-dev-002 --project website-redesign

# Output:
# Tasks for agent-dev-002 in project 'website-redesign':
#   #123: Implement authentication (in_progress)
#   #124: Fix login bug (backlog)

# When session is active, project is implied
agentflow session start --agent agent-dev-002 --project website-redesign
agentflow task list
# → Shows only tasks for 'website-redesign' (active session project)
```

**Creating Tasks (Project Required):**
```bash
# Project must be specified when creating task
agentflow task create \
  --title "Implement user authentication" \
  --project website-redesign \
  --assign-to agent-dev-002

# Error if project missing:
agentflow task create --title "Fix bug" --assign-to agent-dev-001
# Error: --project is required
```

**Multi-Agent, Multi-Project:**
```bash
# An agent can have different tasks in different projects
agentflow task list --agent agent-dev-002 --all-projects

# Output:
# agent-dev-002 tasks across all projects:
#
# Project: website-redesign (Role: Senior Dev)
#   • #123: Implement authentication (in_progress)
#   • #124: Fix login bug (backlog)
#
# Project: mobile-app (Role: Tech Lead)
#   • #201: Review API design (in_progress)
#   • #202: Plan sprint (backlog)
```

#### Manual Assignment
```bash
# Assign task to specific agent
agentflow task assign --task 123 --to agent-dev-001

# Reassign task
agentflow task reassign --task 123 --to agent-dev-002
```

**Self-Assignment** (future):
- Agents see available tasks and choose based on capabilities
- Priority-based queue
- Respects agent's current workload

### Task Status Transitions

**Workflow**:

```
1. Task Created (status: backlog)
                    ↓
2. Task Assigned (status: assigned)
                    ↓
3. Agent Starts Work (status: in_progress)
                    ↓
4a. Normal Path:
    Agent Completes → status: ready_review
                        ↓
                    Review Task Created for Supervisor
                        ↓
                    Supervisor Approves → status: completed

4b. Problem Path:
    Agent Encounters Issue → status: blocked
                            ↓
                        Logs problem
                            ↓
                        Issue Resolved → status: in_progress

4c. Cancellation:
    Task No Longer Needed → status: cancelled
```

**Status Change Permissions**:

| Status Change | Who Can Change |
|---------------|---------------|
| `backlog` → `assigned` | User, Manager Agent |
| `assigned` → `in_progress` | Assigned Agent |
| `in_progress` → `ready_review` | Assigned Agent (workers) |
| `ready_review` → `completed` | Reviewer (Manager) ONLY |
| Any → `blocked` | Assigned Agent |
| `blocked` → `in_progress` | Assigned Agent |
| Any → `cancelled` | User, Manager Agent |

**Key Rule**: Workers cannot mark tasks `completed` - only managers can approve.

### Task Priority System

**Priority Levels**:

| Priority | Description | Response Time | Example |
|----------|-------------|---------------|---------|
| **P0** | Critical, blocks release | Immediate | Production bug, security issue |
| **P1** | High, important | Same day | Feature block, major bug |
| **P2** | Medium | This week | Normal feature, bug |
| **P3** | Low | When possible | Enhancement, optimization |

**Priority Rules**:
- Agents work on highest priority tasks first
- P0 tasks preempt P1, P1 preempt P2, etc.
- Managers can reassign priorities
- Urgent tasks can "jump the queue"

### Task Metadata

**Tags**:
```bash
# Create task with tags
agentflow task create \
  --title "Fix authentication" \
  --tags "security,urgent,backend"
```

**Custom Metadata**:
```bash
# Create task with custom metadata
agentflow task create \
  --title "Implement feature" \
  --metadata '{"estimate": "4h", "complexity": "high"}'
```

**Linked Work**:
```bash
# Create review task (linked to original)
agentflow task create \
  --title "Review task #123" \
  --type review \
  --parent-task 123
```

### Task Dependencies (Future)

**Planned but not in Phase 0**:
```yaml
depends_on: [task-uuid-1, task-uuid-2]
blocks: [task-uuid-3]
```

Tasks can depend on other tasks or block other tasks.

---
