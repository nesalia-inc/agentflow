# Feature Ideas - AgentFlow Agent System

**Status**: Ideas for future enhancements (post-Phase 0)
**Last Updated**: 2025-01-21

This document collects potential new features for the AgentFlow agent system, organized by category.

---

## Collaboration & Coordination

### 1. Mentions in Logs

Agents can mention other agents in logs to draw attention without sending formal messages.

**Use Case**:
- FYI notifications that don't require action
- Less formal than messages, more visible than plain logs
- Architectural decisions that need visibility

**Example**:
```bash
agentflow session log \
  --message "Used Redis for session storage - @agent-architect-001 might want to review this" \
  --type decision

# View mentions
agentflow mentions --agent agent-architect-001

# Output:
# 📭 Mentions for agent-architect-001
#
# 2 hours ago - agent-dev-001 (Jean)
#   "Used Redis for session storage - @agent-architect-001 might want to review this"
#   Context: Task #123, Session session-abc-123
```

**Difference from Messages**:
| Mention | Message |
|---------|---------|
| FYI, no response expected | Requests action/response |
| Visible in "mentions" timeline | Visible in inbox |
| Less formal | More formal |
| No priority level | Can be P0/P1/P2/P3 |

**Implementation Notes**:
- Parse `@agent-code` syntax in log messages
- Store mentions in `Event.mentions` array (already in data model)
- Create `agentflow mentions` command to view mentions
- Optional: send notification when mentioned

---

### 2. Session Resume (Draft Mode)

Auto-save session progress with ability to resume after crashes or for testing.

**Use Cases**:
- Recover from crashes without losing work
- Test/experiment before committing official logs
- Peace of mind for long sessions

**Example**:
```bash
# Session starts normally
agentflow session start --agent agent-dev-001 --project my-project

# Agent works, logs things...
agentflow session log --message "Starting implementation..."

# ⚠️ CRASH! Computer off, bug, etc.

# After restart:
agentflow session resume

# Output:
# 💾 Recovered draft session from 2025-01-21 14:32
#   Agent: agent-dev-001
#   Project: my-project
#   Logs since last save: 3
#   Unsaved work: "Starting implementation..."
#
# Options:
#   • Resume and continue
#   • Save as proper session
#   • Discard draft
```

**Draft Mode for Testing**:
```bash
agentflow session start --agent agent-dev-001 --draft
# Everything logged locally, not committed officially
# When ready: agentflow session finalize
```

**Implementation Notes**:
- Auto-save every N minutes (configurable)
- Draft sessions not counted in official stats
- Draft file: `~/.agentflow/drafts/<agent-id>-<timestamp>.json`
- On session stop: finalize or discard draft
- Useful for experimentation

---

### 3. Handoff Command

Transfer work in progress to another agent with context.

**Use Case**:
- Agent is blocked/busy, another agent can take over
- Preserves context and partial work
- Clear audit trail of who did what

**Example**:
```bash
agentflow task handoff \
  --task 123 \
  --from agent-dev-001 \
  --to agent-dev-002 \
  --message "JWT implementation partially done, testing phase needs completion"

# Creates:
# - Task reassignment: 123 → agent-dev-002
# - Handoff log with context
# - Message to new agent with summary
```

**Data Model Extension**:
```python
class TaskHandoff(BaseModel):
    id: str
    task_id: str
    from_agent_id: str
    to_agent_id: str
    message: str
    progress_snapshot: Dict[str, Any]  # State at handoff time
    created_at: datetime
```

---

## Task Management

### 4. Subtasks

Break down tasks into smaller, trackable units.

**Use Case**:
- Large tasks need to be broken down
- Track progress of complex features
- Better granularity for status updates

**Example**:
```bash
# Create task with subtasks
agentflow task create \
  --title "Implement authentication" \
  --type development \
  --subtasks "Create user model,Add JWT authentication,Write tests,Update docs"

# Or add subtasks later
agentflow task add-subtask --task 123 --title "Add rate limiting"

# View subtasks
agentflow task view 123

# Output:
# Task #123: Implement authentication
# Status: in_progress (2/4 subtasks complete)
#
# Subtasks:
#   ✅ Create user model
#   ✅ Add JWT authentication
#   ⏳ Write tests (in_progress)
#   ⏸️ Update docs (pending)
```

**Data Model**:
```python
class Subtask(BaseModel):
    id: str
    task_id: str
    title: str
    status: Literal["pending", "in_progress", "completed"]
    order: int
    assigned_agent_id: Optional[str]
```

---

### 5. Task Dependencies

Tasks can depend on other tasks. System blocks assignment if dependencies not met.

**Use Case**:
- "Frontend depends on API being ready"
- Automatic blocking of tasks that can't start yet
- Clear visualization of task dependencies

**Example**:
```bash
# Create tasks with dependencies
agentflow task create --title "Create API endpoint" --id 100
agentflow task create --title "Build frontend UI" --id 200 --depends-on 100

# Try to assign task 200 before 100 is complete
agentflow task assign --task 200 --to agent-dev-002

# Output:
# ❌ Cannot assign task #200
# Blocked by dependency: Task #100 "Create API endpoint" (status: in_progress)
#
# View dependency chain:
# Task #100 (in_progress) → Task #200 (blocked)

# Visualize dependencies
agentflow task dependencies --project my-project

# Output:
# Task Dependency Graph:
#   #100: Create API endpoint [in_progress]
#     └─ #200: Build frontend UI [blocked]
#   #101: Setup database [completed]
#     └─ #102: Migrate data [ready]
#       └─ #103: Test migrations [backlog]
```

**Data Model Extension**:
```python
class Task(BaseModel):
    # ... existing fields ...
    depends_on: List[str] = []  # Task IDs
    blocks: List[str] = []      # Computed: tasks that depend on this one

    @property
    def is_blocked(self) -> bool:
        """Check if task is blocked by incomplete dependencies"""
        return any(dep.status != "completed" for dep in self.dependencies)
```

---

### 6. Task Templates

Pre-defined templates for common task types.

**Use Case**:
- Standardize recurring tasks (code review, bug triage)
- Faster task creation with consistent structure
- Enforce best practices via templates

**Example**:
```bash
# Create a template
agentflow task template create \
  --name "feature-work" \
  --title-template "{{feature_name}} implementation" \
  --description-template "Implement {{feature_name}} with:
    - Unit tests (>80% coverage)
    - Documentation
    - Code review
  " \
  --default-type development \
  --default-priority P2

# Use template
agentflow task create \
  --template feature-work \
  --var feature_name="user authentication"

# Creates task with title: "user authentication implementation"
# and description filled in
```

**Pre-defined Templates**:
```yaml
# Bug Report Template
name: bug-report
title: "{{bug_type}}: {{title}}"
description: |
  **Bug Description**: {{description}}
  **Steps to Reproduce**: {{steps}}
  **Expected Behavior**: {{expected}}
  **Actual Behavior**: {{actual}}
  **Environment**: {{environment}}

# Code Review Template
name: code-review
title: "Review PR #{{pr_number}}: {{title}}"
type: review
checklist:
  - Code follows conventions
  - Tests added/updated
  - Documentation updated
  - No security issues
  - Performance acceptable
```

**Implementation**:
- Template storage: `~/.agentflow/templates/`
- Template variables: Jinja2-style `{{var}}`
- Required vs optional variables
- Per-project templates vs global templates

---

### 7. Time Tracking

Track estimated vs actual time for tasks.

**Use Case**:
- Improve estimation accuracy over time
- Identify tasks that consistently take longer than expected
- Track billable hours (for consulting)

**Example**:
```bash
# Create task with estimate
agentflow task create \
  --title "Implement auth" \
  --estimate 4h \
  --assign-to agent-dev-001

# Agent works on it, session tracks time automatically
agentflow session start --agent agent-dev-001 --task 123
# ... work ...
agentflow session stop
# Duration: 5h 30m

# View time tracking
agentflow task view 123

# Output:
# Task #123: Implement auth
# Estimated: 4h
# Actual: 5h 30m (138% of estimate)
# Sessions: 3
#
# Time breakdown:
#   Session 1: 2h 15m (Jan 21 09:00-11:15)
#   Session 2: 1h 45m (Jan 21 14:00-15:45)
#   Session 3: 1h 30m (Jan 22 10:00-11:30)

# Agent's estimation accuracy
agentflow agent estimation-accuracy agent-dev-001

# Output:
# Estimation Accuracy: agent-dev-001
# Average: 1.32x (tasks take 32% longer than estimated)
#
# By task type:
#   development: 1.45x
#   bug: 1.10x
#   review: 0.95x (underestimates)
```

**Data Model**:
```python
class Task(BaseModel):
    # ... existing fields ...
    estimate_minutes: Optional[int] = None
    actual_minutes: Optional[int] = None  # Sum of session durations

class TimeEntry(BaseModel):
    session_id: str
    task_id: str
    duration_minutes: int
    timestamp: datetime
```

---

### 8. Sprints / Milestones

Group tasks into sprints with burndown tracking.

**Use Case**:
- Agile project management
- Track velocity over time
- Plan capacity based on historical velocity

**Example**:
```bash
# Create sprint
agentflow sprint create \
  --name "Sprint 1" \
  --project my-project \
  --start-date 2025-01-21 \
  --duration 14d

# Add tasks to sprint
agentflow sprint add-tasks sprint-1 --tasks 123,124,125,126

# View sprint progress
agentflow sprint view sprint-1

# Output:
# 🏃 Sprint 1 (Jan 21 - Feb 3, 14 days)
# Status: In Progress (Day 5 of 14)
#
# Tasks: 8 total, 3 completed, 2 in_progress, 3 backlog
#
# Burndown:
#   Day 0: ████████████████████ 80 points (starting)
#   Day 5: ████████████░░░░░░░░ 50 points (current)
#   Day 14: ░░░░░░░░░░░░░░░░░░░  0 points (projected)
#
# Velocity: 16 points/week
# On track: ✅ Yes (will complete ~60 points, started with 80)

# Close sprint with retrospective
agentflow sprint close sprint-1

# Auto-generates:
# - Summary of completed work
# - Velocity metrics
# - Lessons learned
# - Suggestions for next sprint
```

**Data Model**:
```python
class Sprint(BaseModel):
    id: str
    name: str
    project_id: str
    start_date: date
    end_date: date
    status: Literal["planning", "active", "completed", "cancelled"]
    task_ids: List[str]
    retrospective: Optional[str]

class SprintMetrics(BaseModel):
    sprint_id: str
    total_points: int
    completed_points: int
    velocity: float  # points per week
    on_track: bool
```

---

## Communication

### 9. Message Threading

Group related messages into conversations.

**Use Case**:
- Avoid inbox flooding with many separate messages on same topic
- Keep conversation context together
- Easier to follow complex discussions

**Example**:
```bash
# First message starts a thread
agentflow agent send-message \
  --to supervisor \
  --type question \
  --message "Should we use JWT or OAuth for auth?"

# Supervisor replies (or agent follows up)
agentflow agent reply \
  --message-id 456 \
  --message "What are our security requirements?"

# View thread
agentflow message thread --id 456

# Output:
# 💬 Thread: Authentication approach (3 messages)
#
# Jean [10:00]: Should we use JWT or OAuth for auth?
# Tech Lead [10:15]: What are our security requirements?
# Jean [10:20]: Simple token-based auth, no external SSO needed
#
# Status: Awaiting response
```

**Data Model**:
```python
class Message(BaseModel):
    # ... existing fields ...
    thread_id: Optional[str] = None  # Group related messages
    parent_message_id: Optional[str] = None  # For replies
```

---

### 10. Broadcast Messages

Send a message to all agents in an organization or project.

**Use Case**:
- Important announcements (API outage, scheduled maintenance)
- Company-wide updates
- Emergency communications

**Example**:
```bash
# Broadcast to organization
agentflow agent broadcast \
  --from cto \
  --level org \
  --priority P1 \
  --message "API downtime scheduled for Sunday 2-4 AM UTC"

# Broadcast to project
agentflow agent broadcast \
  --from tech-lead \
  --project my-project \
  --message "Sprint planning tomorrow at 10 AM"

# All agents receive notification
# Messages appear in special "Broadcasts" section of inbox
```

**Data Model**:
```python
class Broadcast(BaseModel):
    id: str
    from_agent_id: str
    level: Literal["org", "project"]
    project_id: Optional[str]  # Required if level=project
    message: str
    priority: Literal["P0", "P1", "P2", "P3"]
    created_at: datetime
    read_by: List[str] = []  # Agent IDs who marked as read
```

---

### 11. Code Annotations

Agents can leave inline annotations in code files.

**Use Case**:
- TODO/FIXME comments tracked by AgentFlow
- Other agents see annotations when pulling
- Convert annotations to tasks

**Example**:
```bash
# Agent leaves annotation
agentflow annotate \
  --file src/auth.py \
  --line 45 \
  --message "TODO: Add rate limiting to this endpoint" \
  --type todo

# Other agents see annotations when working on file
agentflow annotations show --file src/auth.py

# Output:
# 📝 Annotations in src/auth.py
#
# Line 45 [TODO] - Jean (Jan 21):
#   "TODO: Add rate limiting to this endpoint"
#
# Line 89 [FIXME] - Alice (Jan 20):
#   "FIXME: This query has N+1 problem"

# Convert annotation to task
agentflow annotations create-task --annotation-id 123
# Creates task: "Add rate limiting to /auth endpoint"
```

**Storage**:
```json
{
  "file": "src/auth.py",
  "line": 45,
  "type": "todo",
  "message": "Add rate limiting",
  "author_agent_id": "agent-dev-001",
  "created_at": "2025-01-21T10:00:00Z",
  "resolved": false
}
```

---

## Quality & Review

### 12. Review Checklists

Define checklists for different task types.

**Use Case**:
- Standardize review process
- Ensure nothing is forgotten
- Train junior agents on review criteria

**Example**:
```bash
# Define checklist for feature tasks
agentflow checklist create \
  --name "feature-review" \
  --task-type development \
  --items "
    - [ ] Tests written (>80% coverage)
    - [ ] Documentation updated
    - [ ] No security vulnerabilities
    - [ ] Code follows conventions
    - [ ] Performance acceptable
    - [ ] Manual testing completed
  "

# When reviewer opens review task:
agentflow task view 456

# Output:
# Review Task #456: Review task #123 "Implement auth"
#
# Checklist:
#   [ ] Tests written (>80% coverage)
#   [ ] Documentation updated
#   [ ] No security vulnerabilities
#   [x] Code follows conventions
#   [ ] Performance acceptable
#   [ ] Manual testing completed
#
# Progress: 1/6 items checked
#
# Options:
#   • Check item: agentflow task check --item 3
#   • Approve (all items must be checked)
#   • Request changes
```

**Data Model**:
```python
class Checklist(BaseModel):
    id: str
    name: str
    task_type: Literal["development", "bug", "review", ...]
    items: List[str]

class ChecklistProgress(BaseModel):
    task_id: str
    checklist_id: str
    checked_items: List[int] = []  # Indices of checked items
```

---

### 13. Self-Review Suggestions**

Agent proposes their own review before submitting.

**Use Case**:
- Shows agent has self-checked their work
- Reduces reviewer workload
- Catches obvious issues early

**Example**:
```bash
# Agent marks task ready with self-review
agentflow task update \
  --task 123 \
  --status ready_review \
  --self-review "
    Checked:
    ✅ Tests pass (pytest: 45/45 passed)
    ✅ Coverage 85%
    ✅ No security issues (bandit: clean)
    ✅ Follows conventions (black: formatted)
    ⚠️  Performance: N+1 query in user lookup (acceptable for now)
    ❌ Documentation: Not yet updated (will do after review)
  "

# Reviewer sees:
agentflow task view 124  # Review task

# Output:
# Review Task #124: Review task #123
#
# Agent's Self-Review:
#   ✅ Tests pass (45/45)
#   ✅ Coverage 85%
#   ✅ No security issues
#   ✅ Code formatted
#   ⚠️  Performance: N+1 query (acceptable)
#   ❌ Documentation: Pending
#
# Your Review:
#   [ ] Approve
#   [ ] Request changes
```

---

### 14. TODO/FIXME Tracking

Track all TODOs and FIXMEs created by agents.

**Use Case**:
- Never forget a TODO
- Convert TODOs to tasks
- Track technical debt

**Example**:
```bash
# List all TODOs
agentflow todos list

# Output:
# 📋 TODOs (12 total)
#
# High Priority:
#   • [TODO] Add rate limiting to auth endpoint (src/auth.py:45)
#     Created by: Jean (2 days ago)
#     Task: #124
#
#   • [FIXME] Fix N+1 query in user lookup (src/db.py:89)
#     Created by: Alice (1 day ago)
#     No task linked
#
# Medium Priority:
#   • [TODO] Refactor authentication module (mentioned in logs)
#     Created by: Bob (5 days ago)
#
# Options:
#   • Create task from TODO: agentflow todos create-task --todo 456
#   • Mark as resolved: agentflow todos resolve --todo 456
#   • Dismiss: agentflow todos dismiss --todo 456

# Convert TODO to task
agentflow todos create-task --todo 456 \
  --title "Fix N+1 query in user lookup" \
  --priority P1
```

**Data Model**:
```python
class Todo(BaseModel):
    id: str
    type: Literal["TODO", "FIXME", "HACK", "XXX"]
    file: Optional[str] = None
    line: Optional[int] = None
    message: str
    author_agent_id: str
    task_id: Optional[str] = None  # If converted to task
    status: Literal["open", "resolved", "dismissed"]
    created_at: datetime
```

---

## Analytics & Insights

### 15. Agent Performance Comparison

Compare multiple agents with the same role.

**Use Case**:
- Identify top performers
- Understand performance differences
- Make better assignment decisions

**Example**:
```bash
agentflow agent compare --role python-dev --metric completion_rate

# Output:
# 📊 Performance Comparison: python-dev agents
#
# Completion Rate (last 30 days):
#   Alice (agent-dev-002): ████████████████████ 92%
#   Jean (agent-dev-001):  ████████████████░░░░ 85%
#   Bob (agent-dev-003):   ████████████░░░░░░░░ 76%
#
# Average Task Duration:
#   Alice: 4.2h per task
#   Jean:  5.1h per task
#   Bob:   6.3h per task
#
# Quality (rejection rate):
#   Alice: 2% (1 rejection in 50 tasks)
#   Jean:  8% (4 rejections in 50 tasks)
#   Bob:   12% (6 rejections in 50 tasks)
#
# Recommendation: Assign Alice to high-priority, complex tasks
```

**Metrics**:
- Completion rate
- Average duration per task
- Quality (rejection rate, bugs in production)
- Review speed (for managers)
- Communication frequency

---

### 16. Bottleneck Detection

Identify tasks/agents that are blocking progress.

**Use Case**:
- Find tasks stuck in review too long
- Identify overburdened reviewers
- Process optimization

**Example**:
```bash
agentflow bottlenecks show --project my-project

# Output:
# 🍾 Bottlenecks in my-project
#
# Tasks Waiting Too Long:
#   ⚠️  Task #123 "API design" waiting for review since 5 days
#       Assigned to: Tech Lead (agent-lead-001)
#       Reviewer workload: 7 tasks pending review
#
#   ⚠️  Task #127 "Frontend UI" blocked by dependency since 3 days
#       Waiting for: Task #125 (in_progress)
#
# Overburdened Reviewers:
#   Tech Lead (agent-lead-001):
#     7 tasks in review queue (avg wait: 4.2 days)
#     Suggestion: Assign reviews to Architect
#
# Recommendations:
#   • Reassign some reviews from Tech Lead to Architect
#   • Follow up on Task #125 (blocking 2 other tasks)
```

---

### 17. Workload Balancing

View and balance agent workloads.

**Use Case**:
- Avoid overloading some agents
- Identify underutilized agents
- Fair task distribution

**Example**:
```bash
agentflow workload show --project my-project

# Output:
# ⚖️  Workload: my-project
#
# Current Load (tasks in_progress):
#   Jean (agent-dev-001):  ████████████░░░░ 2 tasks
#   Alice (agent-dev-002): ████████████████ 3 tasks
#   Bob (agent-dev-003):   ████░░░░░░░░░░░░ 1 task
#
# Capacity (based on trust score & velocity):
#   Jean:  5 tasks max capacity (2 current, 3 available)
#   Alice: 5 tasks max capacity (3 current, 2 available)
#   Bob:   4 tasks max capacity (1 current, 3 available)
#
# Suggestions:
#   ✅ Balanced workload
#   • Bob has capacity for 2 more tasks
#   • Consider assigning next task to Bob

# Rebalance workload
agentflow workload rebalance --project my-project
# Automatically redistributes tasks to balance load
```

---

### 18. Velocity Tracking

Measure and predict team velocity.

**Use Case**:
- Sprint planning
- Predict completion dates
- Identify velocity trends

**Example**:
```bash
agentflow velocity show --agent agent-dev-001 --last 90days

# Output:
# 📈 Velocity: agent-dev-001 (Jean)
#
# Last 90 days:
#   Tasks completed: 45
#   Points completed: 180
#   Velocity: 20 points/week
#   Trend: ↗️ Increasing (+2 points/week vs last 90 days)
#
# Weekly breakdown:
#   Week 1: ████████████░░ 16 points
#   Week 2: ██████████████ 18 points
#   Week 3: ████████████████ 20 points
#   Week 4: ██████████████████ 22 points
#
# Prediction:
#   At current velocity, can complete ~80 points in 4-week sprint
#
# By task type:
#   development: 15 points/week
#   bug: 3 points/week
#   review: 2 points/week
```

**Use for Planning**:
```bash
agentflow sprint plan \
  --project my-project \
  --team agent-dev-001,agent-dev-002,agent-dev-003 \
  --duration 2weeks

# Output:
# Team velocity: 55 points/week (combined)
# 2-week capacity: ~110 points
#
# Current backlog: 130 points
# Recommendation: Plan 110 points for sprint, defer 20 points
```

---

## Skills & Roles

### 19. Skill Gaps Analysis

Compare agent skills with project needs.

**Use Case**:
- Identify missing skills in team
- Hire/train agents for specific skills
- Role composition planning

**Example**:
```bash
agentflow skills analyze --project my-project

# Output:
# 🔍 Skill Gap Analysis: my-project
#
# Required Skills (from tasks and project type):
#   • FastAPI (high priority)
#   • PostgreSQL (high priority)
#   • React (medium priority)
#   • Docker (medium priority)
#   • AWS deployment (low priority)
#
# Current Team Skills:
#   Jean (agent-dev-001):
#     ✅ FastAPI, ✅ PostgreSQL, ❌ React, ⚠️  Docker (basic)
#
#   Alice (agent-dev-002):
#     ✅ FastAPI, ⚠️  PostgreSQL (intermediate), ✅ React, ❌ Docker
#
#   Bob (agent-dev-003):
#     ❌ FastAPI, ✅ PostgreSQL, ❌ React, ✅ Docker
#
# Gaps:
#   🔴 Missing: AWS deployment (no agent has this skill)
#      Suggestion: Create role "DevOps Engineer" or train existing agent
#
#   🟡 Underrepresented: React (only 1 agent proficient)
#      Suggestion: Assign Alice to all React tasks
#
#   🟢 Well-covered: FastAPI, PostgreSQL
```

---

### 20. Dynamic Skill Loading**

Load/unload skills without full pull.

**Use Case**:
- Quick skill testing
- Temporary skill for one-off task
- Reduce pull overhead

**Example**:
```bash
# Load specific skill
agentflow agent skill load \
  --agent agent-dev-001 \
  --skill python-testing

# Output:
# ✓ Loaded skill: python-testing
#   Path: ~/.claude/skills/python-testing/SKILL.md
#
# Note: This is a temporary load. Use 'agentflow agent pull' for permanent.

# Unload skill
agentflow agent skill unload \
  --agent agent-dev-001 \
  --skill python-testing

# List loaded skills
agentflow agent skills --agent agent-dev-001

# Output:
# Skills for agent-dev-001:
#   ✓ python-testing (loaded: temporary, expires in 24h)
#   ✓ python-api (loaded: permanent, via pull)
#   ✓ python-async (loaded: permanent, via pull)
```

---

### 21. Role Inheritance

Roles can extend other roles.

**Use Case**:
- Avoid duplication between similar roles
- Create role hierarchies
- Easier role maintenance

**Example**:
```bash
# Base role
agentflow role create \
  --name "Python Developer" \
  --slug python-dev \
  --description "Python developer..."

# Role that extends base role
agentflow role create \
  --name "Senior Python Developer" \
  --slug senior-python-dev \
  --extends python-dev \
  --description "Senior Python developer with architecture responsibilities" \
  --add-document "architecture-principles.md"

# senior-python-dev has all documents from python-dev plus its own
# Pull automatically includes all inherited documents

# View role lineage
agentflow role view senior-python-dev

# Output:
# Role: Senior Python Developer (senior-python-dev)
#
# Extends: Python Developer (python-dev)
#
# Documents (6 total):
#   Inherited from python-dev:
#     • testing-guidelines.md
#     • api-conventions.md
#     • async-patterns.md
#
#   Own documents:
#     • architecture-principles.md
#     • design-patterns.md
#     • mentoring.md
```

**Data Model**:
```python
class Role(BaseModel):
    # ... existing fields ...
    extends: Optional[str] = None  # Parent role slug
    all_documents: List[RoleDocument] = []  # Computed: inherited + own

    @property
    def inherited_documents(self) -> List[RoleDocument]:
        # Get from parent role
        pass
```

---

## Automation

### 22. Triggers

Automate actions based on events.

**Use Case**:
- Auto-assign review tasks
- Alert on trust score drops
- Remind about long-running sessions

**Example**:
```bash
# Define trigger
agentflow trigger create \
  --name "auto-review-assignment" \
  --on task.ready_review \
  --action "create_review_task_for_supervisor"

agentflow trigger create \
  --name "probation-alert" \
  --on agent.trust_score_below_30 \
  --action "send_alert_to_manager"

agentflow trigger create \
  --name "session-break-reminder" \
  --on session.duration_gt_4h \
  --action "log_break_reminder"

# List triggers
agentflow trigger list

# Output:
# Active Triggers (3):
#
#   auto-review-assignment
#     Event: task.ready_review
#     Action: Create review task for supervisor
#     Triggered: 12 times
#
#   probation-alert
#     Event: agent.trust_score_below_30
#     Action: Send alert to manager
#     Triggered: 1 time
#
#   session-break-reminder
#     Event: session.duration_gt_4h
#     Action: Log break reminder
#     Triggered: 3 times
```

**Trigger Events**:
- `task.created`, `task.assigned`, `task.ready_review`, `task.completed`, `task.rejected`
- `agent.status_changed`, `agent.trust_score_below_X`, `agent.trust_score_above_X`
- `session.started`, `session.stopped`, `session.duration_gt_X`
- `message.received`, `message.unread_gt_X`

**Actions**:
- `create_task`
- `send_message`
- `send_alert`
- `log_event`
- `run_command` (custom)

---

### 23. Scheduled Tasks

Create recurring tasks automatically.

**Use Case**:
- Regular maintenance tasks
- Weekly reports
- Periodic reviews

**Example**:
```bash
# Create scheduled task
agentflow task schedule \
  --name "Weekly database backup" \
  --type development \
  --every monday \
  --at 09:00 \
  --assign-to ops-agent \
  --priority P2 \
  --description "Perform weekly database backup and verify"

# Create with cron syntax
agentflow task schedule \
  --name "Daily log cleanup" \
  --cron "0 2 * * *" \
  --assign-to ops-agent

# List scheduled tasks
agentflow task schedule list

# Output:
# Scheduled Tasks (2):
#
#   Weekly database backup
#     Schedule: Every Monday at 09:00
#     Next run: 2025-01-27 09:00
#     Assign to: ops-agent
#     Last run: 2025-01-20 (completed)
#
#   Daily log cleanup
#     Schedule: 0 2 * * * (daily at 2 AM)
#     Next run: 2025-01-22 02:00
#     Assign to: ops-agent
#     Last run: 2025-01-21 02:00 (completed)

# Manually trigger scheduled task
agentflow task schedule run --name "Weekly database backup"
```

---

### 24. Webhooks

Call external URLs on events.

**Use Case**:
- Slack notifications
- Trigger CI/CD
- Integration with external tools

**Example**:
```bash
# Create webhook
agentflow webhook create \
  --name "slack-notify" \
  --url "https://hooks.slack.com/services/YOUR/WEBHOOK/URL" \
  --event task.completed \
  --filter "priority=P0" \
  --template "Task {{title}} (P0) completed by {{agent_name}}"

# Webhook with custom payload
agentflow webhook create \
  --name "ci-deploy" \
  --url "https://ci.example.com/deploy" \
  --event task.review_approved \
  --headers "Authorization=Bearer xxx"
  --body '{"project": "{{project_slug}}", "task": "{{task_id}}"}'

# Test webhook
agentflow webhook test --name slack-notify

# List webhooks
agentflow webhook list

# Output:
# Webhooks (2):
#
#   slack-notify
#     Event: task.completed
#     Filter: priority=P0 only
#     URL: https://hooks.slack.com/...
#     Triggered: 5 times
#     Last success: 2 hours ago
#
#   ci-deploy
#     Event: task.review_approved
#     URL: https://ci.example.com/deploy
#     Triggered: 3 times
#     Last success: 1 day ago
```

**Webhook Events**:
- All trigger events (task.*, agent.*, session.*, message.*)

**Security**:
- Secret signing for verification
- Retry logic on failure
- Dead letter queue for failed webhooks

---

## Security & Compliance

### 25. Approval Chains

Tasks can require multiple approvals.

**Use Case**:
- Production deployments need Tech Lead + CTO approval
- Security changes need Security review + Manager approval
- Financial decisions need multi-level approval

**Example**:
```bash
# Create task with approval chain
agentflow task create \
  --title "Deploy to production" \
  --type deployment \
  --approval-chain "tech-lead,cto"

# Or define in template
agentflow task template create \
  --name "production-deployment" \
  --approval-chain "tech-lead,cto,security-lead"

# When task is ready for review:
agentflow task view 123

# Output:
# Task #123: Deploy to production
# Status: ready_review
#
# Approval Chain (3 required):
#   ✅ Tech Lead (agent-lead-001) - Approved at 10:15
#   ⏳ CTO (agent-cto-001) - Pending
#   ⏸️ Security Lead (agent-sec-001) - Waiting (blocked by CTO)
#
# Note: All approvals must be obtained before task can complete

# Tech Lead approves
agentflow task approve --task 123 --as tech-lead

# CTO approves
agentflow task approve --task 123 --as cto

# Security Lead can now approve
```

**Data Model**:
```python
class ApprovalChain(BaseModel):
    task_id: str
    required_approvers: List[str]  # Agent IDs or role slugs
    approvals: List[Approval] = []

class Approval(BaseModel):
    agent_id: str
    approved_at: datetime
    comments: Optional[str]
```

---

### 26. Audit Trail Signing

Cryptographically sign critical events.

**Use Use**:
- Compliance requirements (SOX, SOC2)
- Non-repudiation
- Tamper evidence

**Example**:
```bash
# Enable audit signing
agentflow config set audit.signing.enabled true
agentflow config set audit.signing.private_key_path ~/.agentflow/key.pem

# Critical events are automatically signed
agentflow task approve --task 123

# Event is signed with private key
# Signature stored with event

# Verify audit trail
agentflow audit verify --agent agent-dev-001 --date 2025-01-21

# Output:
# ✓ Audit trail verified for agent-dev-001 on 2025-01-21
#   47 events, all signatures valid
#
# If tampered:
# ✗ Audit trail INVALID
#   Event #45 signature does not match
#   Possible tampering detected
```

**Signed Events**:
- Task approval/rejection
- Trust score changes
- Agent status changes (probation, termination)
- Role/document changes

---

### 27. Data Retention Policies

Auto-purge or archive old data.

**Use Case**:
- Compliance (GDPR right to be forgotten)
- Storage management
- Performance (smaller datasets)

**Example**:
```bash
# Create retention policy
agentflow retention create \
  --name "gdpr-compliance" \
  --sessions "keep 365days then archive"
  --logs "keep 90days then delete"
  --terminated-agents "keep 7years then delete"

# View retention status
agentflow retention status

# Output:
# Retention Policies:
#
#   Sessions:
#     Active: < 90 days
#     Archived: 90-365 days
#     Delete after: 365 days
#     Status: 45 sessions ready for archive
#
#   Logs:
#     Keep: 90 days
#     Delete after: 90 days
#     Status: 120 logs ready for deletion
#
#   Terminated Agents:
#     Keep: 7 years
#     Delete after: 7 years
#     Status: 2 agents ready for deletion

# Apply retention policies
agentflow retention apply

# Output:
# Archived 45 sessions to ~/.agentflow/archives/sessions-2025-01-21.tar.gz
# Deleted 120 logs
# No agents deleted (none older than 7 years)
```

**Policy Rules**:
- `keep X days then delete`
- `keep X days then archive`
- `archive to <path>`

---

## Developer Experience

### 28. Interactive Mode

Persistent shell with context.

**Use Case**:
- Faster workflow for power users
- Less repetition
- Better UX for extended sessions

**Example**:
```bash
# Start interactive mode
agentflow interactive

# AgentFlow Interactive Shell v0.0.1
# Type 'help' for commands, 'exit' to quit
#
# Context: No active session
# Agent: Not set
# Project: Not set

# Set context once
> set agent agent-dev-001
✓ Agent set to agent-dev-001 (Jean)
> set project my-project
✓ Project set to my-project

# Now commands don't need --agent/--project
> session start
✓ Session started for agent-dev-001 in my-project

> log --message "Starting work"
✓ Logged activity

> tasks list
✓ Shows tasks for agent-dev-001 in my-project

# Autocompletion available
> task sta<tab>
> task start  task status  task stop

# Exit
> exit
✓ Session stopped (duration: 25m)
```

**Features**:
- Context persistence (agent, project)
- Command history
- Autocompletion
- Shorter commands (no need to repeat flags)

---

### 29. Aliases

Shortcuts for frequent commands.

**Use Case**:
- Faster workflow
- Personalized commands
- Team consistency (shared aliases)

**Example**:
```bash
# Create alias
agentflow alias create \
  --name pull-dev \
  --command "agentflow agent pull agent-dev-001 && agentflow session start --agent agent-dev-001"

# Use alias
agentflow pull-dev
# Runs the full command

# Create alias with parameters
agentflow alias create \
  --name start-session \
  --command "agentflow agent pull {{agent}} && agentflow session start --agent {{agent}}"

agentflow start-session --agent agent-dev-002

# List aliases
agentflow alias list

# Output:
# Aliases:
#
#   pull-dev
#     Command: agentflow agent pull agent-dev-001 && ...
#
#   start-session
#     Command: agentflow agent pull {{agent}} && ...
#     Parameters: agent

# Share alias with team (saved to project)
agentflow alias create \
  --name daily-standup \
  --command "agentflow standup --agent {{agent}} --project {{project}}" \
  --scope project
# Saved to .agentflow/project-aliases.yaml
# All team members can use it
```

---

### 30. Diff Viewer

View differences between role versions.

**Use Case**:
- Understand what changed in a role
- Decide whether to pull
- Debug skill issues

**Example**:
```bash
agentflow role diff python-dev v3 v4

# Output:
# Role Diff: python-dev (v3 → v4)
#
# Description changed:
#   - "Senior Python developer with FastAPI expertise"
#   + "Senior Python developer with FastAPI and async expertise"
#
# Documents added:
#   + async-best-practices.md (new)
#
# Documents modified:
#   testing-guidelines.md:
#     - "Coverage: Maintain >70% test coverage"
#     + "Coverage: Maintain >80% test coverage"
#     + Added section on pytest fixtures
#
# Documents removed:
#   - old-patterns.md (removed)
#
# Tools changed:
#   + Added: ruff (linter)
#
# Summary: 1 doc added, 1 modified, 1 removed, 1 tool added

# View specific document diff
agentflow role diff python-doc v3 v4 --document testing-guidelines
```

---

### 31. Dry-Run Mode

Preview actions without executing.

**Use Case**:
- Test dangerous commands
- Understand impact before running
- Debug command logic

**Example**:
```bash
# Dry-run task assignment
agentflow task assign \
  --task 123 \
  --to agent-dev-002 \
  --dry-run

# Output:
# 🧪 DRY RUN - No changes will be made
#
# Would assign:
#   Task #123: "Implement authentication"
#   To: agent-dev-002 (Alice)
#   From: agent-dev-001 (Jean)
#
# Consequences:
#   • Jean will have 1 less task (2 → 1)
#   • Alice will have 1 more task (2 → 3)
#   • Notification sent to Alice
#   • Logged in task history
#
# Run without --dry-run to execute

# Dry-run agent termination
agentflow agent terminate agent-dev-001 --dry-run

# Output:
# 🧪 DRY RUN - No changes will be made
#
# Would terminate:
#   Agent: agent-dev-001 (Jean)
#   Role: Python Developer
#   Trust Score: 67.5
#
# Data preserved:
#   • Tasks: 23 tasks completed
#   • Sessions: 45 sessions (120h total)
#   • Logs: 847 events
#   • Messages: 156 sent, 89 received
#
# Tasks affected:
#   • 2 in_progress tasks → reassigned to ? (unassigned)
#   • 3 backlog tasks → unassigned
#
# Run without --dry-run to execute
```

---

## Testing & Experimentation

### 32. A/B Testing for Workflows

Test different approaches with metrics.

**Use Case**:
- Compare two versions of a role
- Measure which approach performs better
- Data-driven process improvements

**Example**:
```bash
# Create experiment
agentflow experiment create \
  --name "async-vs-sync-patterns" \
  --description "Test async vs sync patterns for API development"

# Create two role variants
agentflow role copy \
  --source python-dev \
  --destination python-dev-async \
  --modify-document async-patterns.md

agentflow role copy \
  --source python-dev \
  --destination python-dev-sync \
  --modify-document sync-patterns.md

# Assign agents to variants
agentflow experiment assign \
  --experiment async-vs-sync-patterns \
  --variant-a python-dev-async \
  --variant-b python-dev-sync \
  --agents-a agent-dev-001,agent-dev-002 \
  --agents-b agent-dev-003,agent-dev-004

# Run experiment for 2 weeks...

# View results
agentflow experiment results async-vs-sync-patterns

# Output:
# 🧪 Experiment: async-vs-sync-patterns
# Duration: 14 days
# Status: Complete
#
# Variant A (async):
#   Agents: 2
#   Tasks completed: 24
#   Avg duration: 4.2h
#   Quality: 96% approval rate
#
# Variant B (sync):
#   Agents: 2
#   Tasks completed: 26
#   Avg duration: 3.8h
#   Quality: 92% approval rate
#
# Conclusion: Sync is 10% faster but async has 4% better quality
# Recommendation: Use async for critical tasks, sync for rapid prototyping
```

---

### 33. Canary Deployment

Gradually roll out new roles.

**Use Case**:
- Test new role with small group first
- Reduce risk of role-wide issues
- Easy rollback if problems

**Example**:
```bash
# Create canary deployment
agentflow role canary start \
  --role python-dev \
  --version v4 \
  --percentage 10

# Output:
# 🐤 Canary deployment started
# Role: python-dev v3 → v4
# Canary: 10% of agents
#
# Selected for canary:
#   ✅ agent-dev-001 (Jean)
#
# Remaining on v3:
#   • agent-dev-002 (Alice)
#   • agent-dev-003 (Bob)
#   • ... (90% of agents)
#
# Monitor for 48 hours before full rollout

# Monitor canary
agentflow role canary status --role python-dev

# Output:
# Canary Status: python-dev v4
# Duration: 26h of 48h monitoring
#
# Canary agents (1):
#   agent-dev-001: ✅ No issues, 3 tasks completed, 100% approval
#
# Comparison:
#   v4 (canary): 4.1h avg duration, 100% approval
#   v3 (stable): 4.3h avg duration, 97% approval
#
# Status: ✅ Looking good, no issues detected
#
# Options:
#   • Roll out to remaining: agentflow role canary rollout python-dev
#   • Rollback: agentflow role canary rollback python-dev
#   • Extend monitoring: agentflow role canary extend python-dev --24h

# Rollout to everyone
agentflow role canary rollout python-dev
# All agents now use v4
```

---

### 34. Shadow Mode

Agent observes another agent's work.

**Use Case**:
- Learning by observation
- Train new agents
- Audit and oversight

**Example**:
```bash
# Start shadow mode
agentflow shadow start \
  --observer agent-dev-003 \
  --shadow agent-dev-001

# Output:
# 👥 Shadow mode started
# Observer: agent-dev-003 (Bob - learning)
# Shadowing: agent-dev-001 (Jean - senior)
#
# Bob will see all of Jean's:
#   • Session logs
#   • Decisions made
#   • Code written
#
# But cannot:
#   • Modify Jean's work
#   • Send messages as Jean
#   • Complete Jean's tasks

# View shadow activity
agentflow shadow activity --observer agent-dev-003

# Output:
# Shadow Activity: Bob shadowing Jean
#
# Session learned from:
#   Session #456 (Jan 21, 2h 30m)
#
# Key learnings:
#   • Used pytest fixtures for test isolation
#   • Applied builder pattern for complex objects
#   • Handled edge case with empty input
#
# Suggestions for Bob:
#   • Practice pytest fixtures in next task
#   • Review builder pattern documentation
#
# Stop shadowing
agentflow shadow stop --observer agent-dev-003
```

**Use Cases**:
- **Mentoring**: Junior agents shadow seniors
- **Onboarding**: New agents learn workflows
- **Cross-training**: Agent learns different role

---

## Advanced Features

### 35. Task Dependencies Visualization

Graph view of task dependencies.

**Example**:
```bash
agentflow task graph --project my-project --output graphviz

# Generates visual graph showing dependencies
# Can output as: graphviz, mermaid, ASCII
```

---

### 36. Agent Performance Predictions

ML-based predictions for task completion.

**Example**:
```bash
agentflow predict completion --task 123

# Output:
# 📊 Prediction for Task #123
#
# Estimated completion: Jan 25, 2025
# Confidence: 87%
#
# Based on:
#   • Similar tasks: 4.5h average
#   • Agent velocity: 1.2x faster than average
#   • Current workload: 1 other task
#
# Factors:
#   ✅ Agent experienced with this type
#   ✅ Agent's trust score is high (87)
#   ⚠️  Agent has 1 other task (may delay)
```

---

### 37. Cross-Project Task Sync

Sync related tasks across projects.

**Example**:
```bash
# Link tasks across projects
agentflow task link \
  --task project-a:123 \
  --with project-b:456 \
  --type "shared-dependency"

# When one task updates, notify linked tasks
```

---

## Priority Assessment

### High Priority (Post-Phase 0)

1. **Mentions in Logs** - High value, relatively simple
2. **Session Resume/Draft Mode** - Safety critical
3. **Task Dependencies** - Fundamental for complex projects
4. **Time Tracking** - Important for planning
5. **Triggers** - Enables automation
6. **Workload Balancing** - Important for team management
7. **Interactive Mode** - Major UX improvement

### Medium Priority

8. **Subtasks** - Useful but not critical
9. **Review Checklists** - Quality improvement
10. **Agent Performance Comparison** - Analytics
11. **Role Inheritance** - Reduces duplication
12. **Scheduled Tasks** - Automation
13. **Approval Chains** - Compliance
14. **Aliases** - UX improvement

### Low Priority (Nice to Have)

15. **Message Threading** - UX improvement
16. **Broadcast Messages** - Rare use case
17. **Code Annotations** - Can use existing code comments
18. **A/B Testing** - Advanced experimentation
19. **Canary Deployment** - Advanced rollout
20. **Shadow Mode** - Learning feature
21. **Predictions** - Requires ML

---

**Implementation Notes**:

- Start with **High Priority** items that provide immediate value
- Many features build on each other (e.g., triggers need events)
- Consider data model implications for each feature
- Some features may require API changes for full implementation
- Phase 0 should focus on core features; advanced features can come later

---

**Document Version**: 1.0
**Last Updated**: 2025-01-21
**Total Ideas**: 37 features organized into 10 categories
