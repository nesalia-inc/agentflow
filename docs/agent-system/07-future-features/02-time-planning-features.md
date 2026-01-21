# Time Tracking & Planning Features

## Feature 4: Time Tracking (Estimation vs Actual)

### Overview

A comprehensive time tracking system that compares task duration estimates with actual time spent across sessions, enabling better estimation accuracy and project planning.

### Why It Matters

- **Better Estimations**: Learn from historical data to improve future estimates
- **Identify Complexity**: Discover which task types consistently exceed estimates
- **Project Planning**: Predict completion dates with confidence intervals
- **Performance Insight**: Understand which agents are better at estimating

### How It Works

#### Creating Tasks with Estimates

```bash
# Create task with time estimate
agentflow task create \
  --title "Implement user authentication" \
  --type development \
  --priority P1 \
  --estimate 4h \
  --assign-to agent-dev-001 \
  --project website-redesign

# Output:
# ✅ Task created
#    Task: #123 - Implement user authentication
#    Estimate: 4h
#    Assigned to: Jean (agent-dev-001)
#
# 💡 Tip: Jean's historical accuracy for this task type is ±22%
#    Consider: Actual time may be 3h 10m - 4h 53m
```

#### Flexible Time Units

```bash
# Supported time formats
--estimate 30m     # 30 minutes
--estimate 2h      # 2 hours
--estimate 4h      # 4 hours
--estimate 1d      # 1 day (8 hours, configurable)
--estimate 0.5d    # 0.5 day (4 hours)
--estimate 3.5h    # 3.5 hours (3h 30m)

# All converted internally to hours (float)
```

#### Automatic Time Tracking

Time is **automatically calculated** from sessions - no manual timer needed:

```bash
# Session 1: Agent works on task
agentflow session start --agent agent-dev-001 --project my-project
# ... agent logs work on task #123 ...
agentflow session stop

# Output:
# ✅ Session stopped
#    Duration: 2h 15m
#    Task worked on: #123
#    Time added to task: +2h 15m

# Session 2: Continue work
agentflow session start --agent agent-dev-001 --project my-project
# ... more work on task #123 ...
agentflow session stop

# Output:
# ✅ Session stopped
#    Duration: 1h 30m
#    Task worked on: #123
#    Time added to task: +1h 30m

# Session 3: Final work
agentflow session start --agent agent-dev-001 --project my-project
# ... final work ...
agentflow session stop

# Output:
# ✅ Session stopped
#    Duration: 45m
#    Task worked on: #123
#    Time added to task: +45m
#
# 📊 Task #123 total time: 4h 30m
#    Estimate was: 4h
#    Variance: +30m (+12.5%)
```

#### Viewing Time Reports

```bash
# Time report for a specific task
agentflow task time 123

# Output:
# ⏱️  Time Report - Task #123
# ─────────────────────────────────
# Task: Implement user authentication
# Assigned to: Jean (agent-dev-001)
# Type: development
# Priority: P1
#
# Estimates:
#   Original: 4h
#   Actual:   4h 30m
#   Variance: +30m (+12.5%)
#
# Session Breakdown:
#   Session #1 (Jan 21, 09:00-11:15): 2h 15m
#   Session #2 (Jan 21, 14:00-15:30): 1h 30m
#   Session #3 (Jan 22, 10:00-10:45): 45m
#   ──────────────────────────────────
#   Total:                           4h 30m
#
# Status: completed
# Completed at: 2025-01-22 10:45
#
# 📊 Estimation Accuracy: Good (within 15%)
#    This task was reasonably well estimated.
```

#### Agent Estimation Accuracy

Track how well each agent estimates their work:

```bash
# View agent's estimation performance
agentflow agent time-accuracy agent-dev-001

# Output:
# 📈 Estimation Accuracy - Jean (agent-dev-001)
# ─────────────────────────────────────────
# Last 30 days | 15 tasks completed
#
# Overall accuracy: ±18% (Good)
#    Tasks are estimated within 18% on average
#
# By Task Type:
#   Feature development: ±22% (Fair)
#      → Tends to underestimate complexity
#   Bug fixes:           ±10% (Excellent)
#      → Very accurate estimates
#   Code reviews:        ±5%  (Excellent)
#      → Spot-on estimates
#   Documentation:       ±35% (Poor)
#      → Consistently underestimates
#
# Under-estimated Tasks (took longer):
#   • #123: Auth implementation
#     Est: 4h, Actual: 6h, Variance: +50%
#     Reason: "Forgot about token refresh logic"
#
#   • #127: API refactor
#     Est: 2h, Actual: 3h, Variance: +50%
#     Reason: "More complex than expected"
#
# Over-estimated Tasks (went faster):
#   • #124: Login bug fix
#     Est: 2h, Actual: 1h, Variance: -50%
#     Reason: "Simple configuration fix"
#
#   • #129: Update docs
#     Est: 1h, Actual: 30m, Variance: -50%
#     Reason: "Docs were mostly complete"
#
# 📊 Patterns Detected:
#   ⚠️  Tasks with "authentication" take 50% longer than estimated
#      → Recommendation: Add 50% buffer for auth-related work
#
#   ✅ Bug fixes are estimated accurately
#      → No adjustment needed
#
#   ⚠️  Documentation tasks consistently overestimated
#      → Recommendation: Reduce doc estimates by 30%
#
# 💡 Suggestions for Jean:
#   1. Break down "authentication" tasks into smaller subtasks
#   2. Add complexity buffer for feature work (+20%)
#   3. Be more aggressive with documentation estimates (-30%)
```

#### Project Time Estimation

Predict completion time for remaining work:

```bash
# Estimate project completion
agentflow project estimate website-redesign

# Output:
# 📊 Project Estimate - website-redesign
# ─────────────────────────────────────
# Remaining tasks: 12
# Total estimate: 96h
#
# Completion Scenarios:
#   Optimistic: 80h (2 weeks @ 40h/week)
#   Realistic:  96h (2.4 weeks @ 40h/week)
#   Pessimistic: 120h (3 weeks @ 40h/week)
#
# By Agent:
#   ┌──────────────────────────────────────────┐
#   │ Agent      │ Load  │ Est. Completion      │
#   ├──────────────────────────────────────────┤
#   │ Jean       │ 28h   │ Jan 30 (7 days)      │
#   │ Alice      │ 16h   │ Jan 27 (4 days)      │
#   │ Bob        │ 32h   │ Feb 3 (11 days)      │
#   │ Charlie    │ 20h   │ Jan 29 (6 days)      │
#   └──────────────────────────────────────────┘
#
# Confidence: 75% (based on historical accuracy)
#    Historical variance: ±18%
#
# 🚧 Blockers & Risks:
#   • Task #135 blocked (waiting for #123)
#     → May delay completion by 1-2 days
#
#   • Bob has low accuracy on "integration" tasks (±40%)
#     → Actual time may be higher
#
# 📅 Milestone Predictions:
#   Sprint 1 goal: Jan 31
#     Current prediction: Feb 1 (1 day late)
#     Confidence: 65%
#
#   Project completion: Feb 14
#     Current prediction: Feb 14 (on track)
#     Confidence: 75%
```

#### Time Tracking Configuration

```bash
# Configure working hours
agentflow config set --key working_hours_per_day --value 8
agentflow config set --key working_days_per_week --value 5

# Configure default day length
agentflow config set --key hours_per_day --value 8

# Time is now calculated as:
# 1d = 8 hours
# 0.5d = 4 hours
```

### Data Model

```python
class Task(BaseModel):
    # ... existing fields ...
    estimated_hours: Optional[float] = None  # 4.0 = 4 hours
    actual_hours: float = 0.0  # Accumulated from sessions

    @property
    def time_variance_hours(self) -> Optional[float]:
        """Absolute difference in hours"""
        if not self.estimated_hours:
            return None
        return self.actual_hours - self.estimated_hours

    @property
    def time_variance_percentage(self) -> Optional[float]:
        """Percentage difference"""
        if not self.estimated_hours or self.estimated_hours == 0:
            return None
        return ((self.actual_hours - self.estimated_hours) / self.estimated_hours) * 100

class Session(BaseModel):
    # ... existing fields ...
    task_id: Optional[str] = None  # Working on specific task
    duration_seconds: int  # Already exists

    @property
    def duration_hours(self) -> float:
        """Duration in hours"""
        return self.duration_seconds / 3600

class AgentTimeStats(BaseModel):
    agent_id: str
    period_start: datetime
    period_end: datetime

    # Overall accuracy
    total_tasks: int
    avg_variance_percentage: float

    # By task type
    accuracy_by_type: Dict[str, float]  # {"development": 22.0, "bug": 10.0}

    # Under/over estimated
    under_estimated_tasks: List[Dict]
    over_estimated_tasks: List[Dict]

    # Patterns
    patterns: List[str]  # ["Auth tasks take 50% longer"]
```

### CLI Commands

```bash
# Task time
agentflow task time <task-id>
agentflow task time <task-id> --by-session  # Detailed breakdown

# Agent accuracy
agentflow agent time-accuracy <agent-code>
agentflow agent time-accuracy <agent-code> --period 30d
agentflow agent time-accuracy <agent-code> --by-type

# Project estimation
agentflow project estimate <project-slug>
agentflow project estimate <project-slug> --by-agent
agentflow project estimate <project-slug> --scenario optimistic

# Configuration
agentflow config set --key working_hours_per_day --value <hours>
```

---

## Feature 5: Sprints & Milestones

### Overview

Organize work into time-boxed sprints with clear goals, track progress with burndown charts, and generate automatic retrospectives on completion.

### Why It Matters

- **Cadence**: Regular rhythm for planning and delivery
- **Focus**: Clear objectives for a defined period
- **Visibility**: Team progress visible via burndown charts
- **Improvement**: Retrospectives drive continuous improvement

### How It Works

#### Creating a Sprint

```bash
# Create a new sprint
agentflow sprint create \
  --project website-redesign \
  --name "Sprint 1 - Authentication" \
  --goal "Implement complete user authentication system with login, registration, and password recovery" \
  --start-date "2025-01-21" \
  --duration 2w \
  --agents agent-dev-001,agent-dev-002,agent-qa-001

# Output:
# ✅ Sprint created
#    Sprint: Sprint 1 - Authentication
#    Dates: Jan 21 - Feb 3 (10 working days)
#    Duration: 2 weeks
#    Team: 3 agents
#
# Next steps:
#   1. Add tasks: agentflow sprint add-tasks sprint-1 --tasks 123,124,125
#   2. Start sprint: agentflow sprint start sprint-1
```

#### Adding Tasks to Sprint

```bash
# Add individual tasks
agentflow sprint add-tasks sprint-1 --tasks 123,124,125,126,127

# Output:
# ✅ Added 5 tasks to sprint-1
#
# Sprint Overview:
#   Tasks: 5
#   Total estimate: 40h
#   Per day target: 4h/day (40h ÷ 10 days)

# Add tasks from backlog
agentflow sprint add-tasks sprint-1 --from-backlog --limit 10

# Auto-add tasks based on capacity
agentflow sprint add-tasks sprint-1 --auto-fill
# Adds tasks until sprint capacity is reached
```

#### Starting the Sprint

```bash
# Start the sprint
agentflow sprint start sprint-1

# Output:
# 🚀 Sprint started
#    Sprint: Sprint 1 - Authentication
#    Dates: Jan 21 - Feb 3, 2025
#    Status: Active
#
# Goal:
#   Implement complete user authentication system with login,
#   registration, and password recovery
#
# Team:
#   • Jean (agent-dev-001)
#   • Alice (agent-dev-002)
#   • Bob (agent-qa-001)
#
# Tasks: 5 (40h total, 4h/day target)
#
# Daily standup:
#   Time: 9:00 AM every day
#   Command: agentflow sprint standup sprint-1
```

#### Burndown Chart

```bash
# View burndown chart
agentflow sprint burndown sprint-1

# Output:
# 📉 Burndown Chart - Sprint 1
# ─────────────────────────────────
# Sprint: Sprint 1 - Authentication
# Dates: Jan 21 - Feb 3 (10 working days)
#
# Remaining Work:
#   Day 0 (Jan 21): ████████████████ 40h ← Baseline
#   Day 1 (Jan 22): ██████████████░░ 36h (-4h) ✅ On track
#   Day 2 (Jan 23): █████████████░░░ 33h (-3h) ✅ On track
#   Day 3 (Jan 24): ████████████░░░░ 33h (0h)   ⚠️  No progress
#   Day 4 (Jan 27): ███████████░░░░░ 30h (-3h) ✅ Back on track
#   Day 5 (Jan 28): ██████████░░░░░░ 26h (-4h) ✅ Good velocity
#   Day 6 (Jan 29): ██████████░░░░░░ 26h (0h)   ⚠️  Stalled
#   Day 7 (Jan 30): █████████░░░░░░░ 23h (-3h) ✅ Progress
#   Day 8 (Jan 31): ████████░░░░░░░░ 19h (-4h) ✅ Accelerating
#   Day 9 (Feb 3):  ████░░░░░░░░░░░░ 8h  (-11h) 🔥 Fast finish
#
# Statistics:
#   Velocity: 3.6h/day average
#   Target velocity: 4h/day
#   Efficiency: 90%
#
# Forecast:
#   Remaining work: 8h
#   At current velocity: 2.2 days remaining
#   Expected completion: Feb 3 ✅ On schedule
#
# 📊 ASCII Chart:
#  40h | █
#  35h | █ █
#  30h | █ █ █
#  25h | █ █ █ █
#  20h | █ █ █ █ █
#  15h | █ █ █ █ █ █
#  10h | █ █ █ █ █ █ █
#   5h | █ █ █ █ █ █ █ █
#   0h | └─────────────────────
#      D0 D1 D2 D3 D4 D5 D6 D7 D8 D9
#               ╱╲
#              ╱  ╲
#          Ideal   Actual
#
# ⚠️  Risks:
#   • Days 3 and 6 had no progress (weekends?)
#   • Task #126 blocked for 2 days
#   • Compensated by faster work on final day

# View as table
agentflow sprint burndown sprint-1 --format table

# Export as CSV
agentflow sprint burndown sprint-1 --export burndown.csv
```

#### Daily Standup

```bash
# Generate daily standup summary
agentflow sprint standup sprint-1

# Output:
# 📢 Daily Standup - Sprint 1
# ──────────────────────────────
# Date: Jan 27, 2025 (Day 4 of 10)
# Remaining: 30h / 40h (25% done)
#
# Team Updates:
#
#   Jean (agent-dev-001):
#     Yesterday: Completed user model implementation (4h)
#     Today: Starting JWT endpoints
#     Blockers: None
#
#   Alice (agent-dev-002):
#     Yesterday: Fixed login bug (2h)
#     Today: Continuing registration form
#     Blockers: Waiting for API spec (may impact tomorrow)
#
#   Bob (agent-qa-001):
#     Yesterday: Wrote tests for login (3h)
#     Today: Starting registration tests
#     Blockers: None
#
# Sprint Status:
#   Progress: 10h / 40h (25%)
#   Expected: 16h by now
#   Status: ⚠️  Behind by 6h
#
# Actions:
#   • Alice's blocker (API spec) needs attention today
#   • Consider adding resources to catch up
```

#### Sprint Status

```bash
# View current sprint status
agentflow sprint view sprint-1

# Output:
# 🎯 Sprint 1 - Authentication
# ──────────────────────────────
# Status: Active (Day 7 of 10)
# Dates: Jan 21 - Feb 3, 2025
#
# Goal:
#   Implement complete user authentication system with login,
#   registration, and password recovery
#
# Progress: 21h / 40h completed (52%)
#
# Tasks (5):
#   ✅ #123: User model (4h) - completed by Jean
#   ✅ #124: JWT endpoints (6h) - completed by Alice
#   ✅ #125: Login form (4h) - completed by Jean
#   🔄 #126: Registration (7h) - in progress (60%) by Alice
#   ⏳ #127: Password reset (5h) - backlog
#   ⏳ #128: Tests (8h) - backlog
#   ⏳ #129: Documentation (6h) - backlog
#
# Blockers:
#   ⚠️  #126 blocked: Waiting for API spec
#      Duration: 2 days
#      Impact: May delay completion
#
# Velocity:
#   Target: 4h/day
#   Actual: 3h/day (75%)
#   Required to finish: 5.7h/day
#   Status: ⚠️  Need to accelerate
#
# Forecast:
#   On current pace: Complete Feb 5 (2 days late)
#   On target pace: Complete Feb 3 (on time)
#
# 💡 Recommendations:
#   1. Resolve #126 blocker immediately
#   2. Consider adding Bob to help with tests
#   3. Reduce documentation scope if needed
```

#### Completing the Sprint

```bash
# Complete the sprint
agentflow sprint complete sprint-1

# Output:
# ✅ Sprint completed
#    Sprint: Sprint 1 - Authentication
#    Duration: Jan 21 - Feb 3 (10 working days)
#
# Results:
#   Tasks completed: 5/7 (71%)
#   Hours completed: 36h / 40h (90%)
#   Status: ✅ Mostly successful
#
# Goal Achievement:
#   ✅ Login: Completed
#   ✅ Registration: Completed
#   ✅ User model: Completed
#   ⚠️  Password reset: Carried over to Sprint 2
#   ⚠️  Tests: Partially completed, carried over
#
# 📊 Sprint Retrospective (Auto-Generated)
# ─────────────────────────────────────
#
# What Went Well ✅:
#   • Jean and Alice had good collaboration
#   • JWT implementation was smooth (no bugs)
#   • Zero production issues from this sprint
#   • Team adapted well when blocker occurred
#
# What Could Be Improved ⚠️:
#   • Task #126 blocked for 2 days (missing API spec)
#     Root cause: Spec wasn't ready before sprint
#     Solution: Create spec template, require approval before sprint
#
#   • Sprint finished with 2 tasks incomplete
#     Root cause: Estimates were optimistic
#     Solution: Add 20% buffer to estimates
#
#   • Documentation not started
#     Root cause: Ran out of time, focused on coding
#     Solution: Allocate dedicated doc time or separate doc sprint
#
# Action Items:
#   1. Create API spec template (assign to Tech Lead, due by Sprint 2 planning)
#   2. Add 20% buffer to all estimates (starting Sprint 2)
#   3. Consider "documentation sprint" or allocate 20% time to docs
#   4. Task #128 and #129 carried over to Sprint 2
#
# 📈 Velocity Metrics:
#   Planned velocity: 4h/day
#   Actual velocity: 3.6h/day (90%)
#   Recommendation: Plan 3.5h/day for next sprint
#
# 📄 Retrospective saved to: ~/.agentflow/sprints/sprint-1-retro.md
#    Share with team: agentflow sprint retro sprint-1 --share
```

#### Sprint Management

```bash
# List sprints
agentflow sprint list --project website-redesign

# Output:
# Sprints for website-redesign:
#
# Active:
#   sprint-3: Sprint 3 - UI (Jan 21 - Feb 3)
#
# Completed:
#   sprint-2: Sprint 2 - Database (Jan 7 - Jan 20) ✅
#   sprint-1: Sprint 1 - Auth (Dec 23 - Jan 6) ⚠️

# Create sprint from template
agentflow sprint create \
  --template "2-week-sprint" \
  --name "Sprint 4 - Testing" \
  --project website-redesign

# Recurring sprints
agentflow sprint create \
  --recurring \
  --interval 2w \
  --project website-redesign \
  --template "standard-sprint"
# Creates Sprint 5, 6, 7, ... automatically

# Export sprint data
agentflow sprint export sprint-1 --format json > sprint-1.json
agentflow sprint export sprint-1 --format csv > sprint-1.csv
```

### Data Model

```python
class Sprint(BaseModel):
    id: str  # UUID or "sprint-1"
    project_id: str
    name: str  # "Sprint 1 - Authentication"
    goal: str  # Detailed goal description
    status: Literal["planned", "active", "completed", "cancelled"]

    # Dates
    start_date: datetime
    end_date: datetime
    duration_days: int  # Working days (excludes weekends)

    # Team
    agent_ids: List[str]  # Team members
    task_ids: List[str]   # Tasks in sprint

    # Stats
    @property
    def total_estimate(self) -> float:
        """Sum of all task estimates"""
        pass

    @property
    def total_actual(self) -> float:
        """Sum of actual hours spent"""
        pass

    @property
    def completion_percentage(self) -> float:
        """% of tasks completed"""
        pass

    @property
    def velocity(self) -> float:
        """Average hours completed per day"""
        pass

    @property
    def expected_velocity(self) -> float:
        """Target velocity (total estimate / duration)"""
        pass

class DailyStandup(BaseModel):
    id: str
    sprint_id: str
    date: datetime
    agent_updates: List[Dict]  # [{"agent_id": ..., "yesterday": ..., "today": ...}]
    blockers: List[str]
    remaining_work: float  # Hours remaining
    created_at: datetime

class BurndownPoint(BaseModel):
    day: int  # 0, 1, 2, ...
    date: datetime
    remaining_work: float  # Hours
    ideal_remaining: float  # For comparison

class SprintRetrospective(BaseModel):
    sprint_id: str
    generated_at: datetime

    what_went_well: List[str]
    what_could_improve: List[str]
    action_items: List[str]

    velocity_metrics: Dict[str, float]
```

### CLI Commands

```bash
# Sprint management
agentflow sprint create --name <name> --project <project> --duration <2w>
agentflow sprint start <sprint-id>
agentflow sprint complete <sprint-id>
agentflow sprint cancel <sprint-id>

# Tasks
agentflow sprint add-tasks <sprint-id> --tasks <id1,id2,id3>
agentflow sprint remove-tasks <sprint-id> --tasks <id1,id2>
agentflow sprint list-tasks <sprint-id>

# Viewing
agentflow sprint view <sprint-id>
agentflow sprint list --project <project>
agentflow sprint burndown <sprint-id>
agentflow sprint standup <sprint-id>

# Retrospective
agentflow sprint retro <sprint-id>
agentflow sprint retro <sprint-id> --share

# Advanced
agentflow sprint create --recurring --interval <2w> --project <project>
agentflow sprint export <sprint-id> --format json
```

---

## Feature 6: Workload Balancing

### Overview

An intelligent workload distribution system that analyzes agent capacity, predicts availability, and suggests optimal task assignments to balance team load.

### Why It Matters

- **Prevent Burnout**: Avoid overloading some agents while others are idle
- **Optimize Utilization**: Make best use of team capacity
- **Predict Delays**: Identify bottlenecks before they impact deadlines
- **Smart Assignment**: Assign new tasks to agents with capacity

### How It Works

#### Team Workload Overview

```bash
# View workload distribution across team
agentflow workload show --project website-redesign

# Output:
# ⚖️  Workload Distribution - website-redesign
# ───────────────────────────────────────────
# As of: 2025-01-21 14:30
#
# Team Overview:
#   Active tasks: 12
#   Total estimated work: 96h
#   Team capacity: 80h/week (4 agents × 20h)
#   Utilization: 120% ⚠️  Over capacity
#
# ┌────────────────────────────────────────────────────┐
# │ Agent          │ Load  │ Capacity │ Utilization   │
# ├────────────────────────────────────────────────────┤
# │ Jean (dev)     │ 28h   │ 20h/week │ 140% 🔴 OVER   │
# │ Alice (dev)    │ 18h   │ 20h/week │  90% ✅ OK     │
# │ Bob (qa)       │ 32h   │ 20h/week │ 160% 🔴 OVER   │
# │ Charlie (dev)  │ 18h   │ 20h/week │  90% ✅ OK     │
# └────────────────────────────────────────────────────┘
#
# 🔴 Imbalance Detected:
#    Standard deviation: 6.5h (high)
#    Ideal distribution: ±2h per agent
#
# 💡 Reassignment Suggestions:
#   1. Task #136 (4h) - "API integration"
#      From: Bob (32h) → To: Charlie (18h)
#      Result: Bob 28h, Charlie 22h
#
#   2. Task #137 (2h) - "Write tests"
#      From: Bob (28h) → To: Alice (18h)
#      Result: Bob 26h, Alice 20h
#
#   3. Task #138 (3h) - "Update docs"
#      From: Jean (28h) → To: Charlie (22h)
#      Result: Jean 25h, Charlie 25h
#
# After rebalancing:
#   Jean: 25h (125%)
#   Alice: 20h (100%) ✅
#   Bob: 26h (130%)
#   Charlie: 25h (125%)
#
# Imbalance reduced from 6.5h → 2.5h ✅
#
# Apply these changes?
#   [1] Reassign #136 to Charlie
#   [2] Reassign #137 to Alice
#   [3] Reassign #138 to Charlie
#   [4] Apply all
#   [Enter] Skip

# Interactive mode
agentflow workload show --project website-redesign --interactive
# Allows selecting which suggestions to apply
```

#### Individual Agent Workload

```bash
# View detailed workload for an agent
agentflow workload agent agent-dev-001

# Output:
# 📊 Workload Detail - Jean (agent-dev-001)
# ───────────────────────────────────────
# Current Load: 28h (140% of capacity)
# Capacity: 20h/week
# Status: 🔴 Overloaded
#
# Tasks by Status:
#
#   🔴 In Progress (2 tasks) - 12h
#      • #123: Auth UI (6h)
#        Priority: P1
#        Due: Jan 23 (in 2 days)
#        Project: website-redesign
#        Session: Last worked 2h ago
#
#      • #124: Profile page (6h)
#        Priority: P2
#        Due: Jan 27 (in 5 days)
#        Project: website-redesign
#
#   ⏳ Backlog (3 tasks) - 16h
#      • #125: Password reset (4h)
#        Priority: P2
#        Due: Jan 30
#
#      • #126: Email verification (4h)
#        Priority: P3
#        Due: Feb 3
#
#      • #127: OAuth integration (8h)
#        Priority: P3
#        Due: Feb 10
#
# Timeline Analysis:
#   This Week (Jan 21-24): 20h capacity, 28h load
#   → Status: 🔴 Overloaded by 8h
#
#   Next Week (Jan 27-31): 20h capacity, 8h remaining
#   → Status: ✅ Underutilized (12h free)
#
# 📈 Historical Velocity:
#   Last 4 weeks average: 18h/week
#   Standard deviation: ±3h
#   Reliability: 90% (consistently 15-21h/week)
#
# ⚠️  Risks Identified:
#   1. Task #123 due in 2 days but Jean has no time today
#      → Action: Reassign or extend deadline
#
#   2. Load (28h) exceeds historical velocity (18h)
#      → Action: Reassign 10h to other agents
#
# 💡 Recommendations:
#   1. Reassign task #125 (4h) to Charlie
#   2. Negotiate deadline extension for #123
#   3. Defer task #127 to next week
```

#### Availability Forecast

```bash
# Predict when agent will be available
agentflow workload available --agent agent-dev-001

# Output:
# 📅 Availability Forecast - Jean (agent-dev-001)
# ─────────────────────────────────────────
# Current queue: 5 tasks (28h total)
#
# Assuming 18h/week velocity (historical):
#
# Week 1 (Jan 21-24):
#   Capacity: 18h
#   Load: 28h
#   Status: 🔴 Overloaded
#   → Will complete 18h, 10h carries over
#
# Week 2 (Jan 27-31):
#   Carryover: 10h
#   Capacity: 18h
#   Status: ✅ Available for 8h of new work
#
# Week 3 (Feb 3-7):
#   Status: ✅ Fully available (18h free)
#
# 🎯 Availability Windows:
#   • Today (Jan 21): ❌ No time (booked)
#   • Tomorrow (Jan 22): ❌ No time (booked)
#   • Next Monday (Jan 27): ✅ 4h available
#   • Next Tuesday (Jan 28): ✅ 8h available
#
# 💬 For task assignment:
#   "Jean can take new tasks starting Jan 27"
#   "Immediate availability: 0h (booked solid)"
#   "Next week availability: 8h"

# Compare multiple agents
agentflow workload available --agents agent-dev-001,agent-dev-002,agent-qa-001

# Output:
# 📅 Team Availability Comparison
# ───────────────────────────────────
# Agent           │ Today  │ This Week │ Next Week │ Full Availability
# ───────────────────────────────────────────────────────────────────
# Jean (dev)      │ ❌ 0h  │ ❌ 0h     │ ✅ 8h     │ Jan 27
# Alice (dev)     │ ✅ 2h  │ ✅ 6h     │ ✅ 18h    │ Jan 23
# Bob (qa)        │ ❌ 0h  │ ❌ 0h     │ ✅ 4h     │ Jan 28
# Charlie (dev)   │ ✅ 4h  │ ✅ 12h    │ ✅ 18h    │ Today
#
# 🎯 Best for new tasks:
#   Immediate: Charlie (4h available today)
#   This week: Alice (6h available)
#   Large task (>8h): Alice or Charlie next week
```

#### Smart Assignment Suggestions

```bash
# System suggests best assignee for new task
agentflow task create \
  --title "Implement search feature" \
  --estimate 6h \
  --priority P2 \
  --project website-redesign \
  --suggest-assignment

# Output:
# 🤖 Assignment Suggestion
# ──────────────────────────────
# Task: Implement search feature
# Estimate: 6h
# Priority: P2
# Due: Jan 30
#
# 🎯 Recommended: Charlie (agent-dev-003)
#
# Why Charlie?
#   ✅ Current load: 18h (90% capacity)
#   ✅ Can take 2h today, 4h this week
#   ✅ Has relevant experience:
#      • #110: Implemented search API (4.8★ satisfaction)
#      • #115: Optimized search queries
#   ✅ Trust score: 72 (Very Good)
#   ✅ Estimation accuracy: ±15% (Good)
#
# Fit Score: 9.2/10 ⭐
#
# Alternatives:
#
#   2. Alice (agent-dev-002)
#      Load: 18h (90%)
#      Can take: 2h today
#      Experience: No prior search tasks
#      Fit score: 6.5/10
#
#   3. Jean (agent-dev-001)
#      Load: 28h (140%) ⚠️
#      Can take: 0h (fully booked)
#      Experience: Moderate
#      Fit score: 4.0/10 ⚠️ Not recommended
#
#   4. Bob (agent-qa-001)
#      Load: 32h (160%) ❌
#      Can take: 0h
#      Fit score: 2.0/10 ❌ Not available
#
# 💡 Recommendation:
#   Assign to Charlie for best balance and expertise match
#
# Create task with Charlie assigned? [Y/n]
```

#### Automatic Workload Balancing

```bash
# Auto-balance workload across team
agentflow workload balance --project website-redesign --auto

# Output:
# ⚖️  Auto-Balancing
# ─────────────────────────────────────
# Analyzing workload distribution...
#
# Current State:
#   Imbalance score: 42% (high)
#   Standard deviation: 6.5h
#   Target: Everyone within 80-100% capacity (±2h)
#
# Proposed Changes (3 reassignments):
#
#   1. Task #136 (4h) - "API integration"
#      From: Bob (32h, 160%)
#      To:   Charlie (18h, 90%)
#
#      Bob's new load:   28h (140%)
#      Charlie's load:   22h (110%)
#      Impact: Bob -4h, Charlie +4h
#      Risk: LOW (Charlie has capacity)
#
#   2. Task #137 (2h) - "Write tests"
#      From: Bob (28h, 140%)
#      To:   Alice (18h, 90%)
#
#      Bob's new load:   26h (130%)
#      Alice's new load: 20h (100%)
#      Impact: Bob -2h, Alice +2h
#      Risk: LOW (Alice at perfect capacity)
#
#   3. Task #138 (3h) - "Update docs"
#      From: Jean (28h, 140%)
#      To:   Charlie (22h, 110%)
#
#      Jean's new load:  25h (125%)
#      Charlie's load:  25h (125%)
#      Impact: Jean -3h, Charlie +3h
#      Risk: LOW (balanced)
#
# Final State:
#   ┌────────────────────────────────────────────────┐
#   │ Agent    │ Before │ After  │ Change │ Util     │
#   ├────────────────────────────────────────────────┤
#   │ Jean     │ 28h    │ 25h    │ -3h    │ 125%     │
#   │ Alice    │ 18h    │ 20h    │ +2h    │ 100% ✅  │
#   │ Bob      │ 32h    │ 26h    │ -6h    │ 130%     │
#   │ Charlie  │ 18h    │ 25h    │ +7h    │ 125%     │
#   └────────────────────────────────────────────────┘
#
# Results:
#   Imbalance reduced: 42% → 15% ✅
#   Std deviation: 6.5h → 2.5h ✅
#   Agents at 100%: 1 (Alice) ✅
#   Overloaded agents (>130%): 1 (Bob) ⚠️
#
# ⚠️  Notes:
#   • Bob is still at 130% but much better than 160%
#   • Further reassignments may risk quality
#   • Consider extending deadlines for Bob's tasks
#
# Apply these changes?
#   [1] Apply all
#   [2] Apply selectively (interactive)
#   [3] Show detailed plan
#   [4] Cancel

# Dry-run mode (preview without applying)
agentflow workload balance --project website-redesign --dry-run

# Set custom target
agentflow workload balance --project website-redesign --target 90%
# Tries to bring everyone to 90% capacity

# Limit number of reassignments
agentflow workload balance --project website-redesign --max-changes 2
# Maximum 2 tasks will be reassigned
```

#### Workload Alerts

```bash
# Configure workload alerts
agentflow config set --key workload_alert_threshold --value 120

# Now get alerts when agents exceed 120% capacity
agentflow workload check --project website-redesign

# Output:
# 🚨 Workload Alerts
# ───────────────────────
# 2 agents exceed threshold (120%):
#
#   🔴 Bob (agent-qa-001)
#      Load: 32h (160%)
#      Threshold: 120%
#      Exceeded by: 40%
#      Action: Reassign 12h of work
#
#   🔴 Jean (agent-dev-001)
#      Load: 28h (140%)
#      Threshold: 120%
#      Exceeded by: 20%
#      Action: Reassign 8h of work
#
# Run: agentflow workload balance --project website-redesign
```

### Data Model

```python
class WorkloadReport(BaseModel):
    project_id: str
    generated_at: datetime
    agents: List["AgentWorkload"]
    total_hours: float
    total_capacity: float
    utilization_percentage: float
    imbalance_score: float  # 0% = perfect, 100% = terrible

class AgentWorkload(BaseModel):
    agent_id: str
    current_load_hours: float  # Sum of task estimates
    capacity_hours_per_week: float
    utilization_percentage: float

    # Task breakdown
    tasks_by_status: Dict[str, List[str]]  # {"in_progress": ["#123"], "backlog": ["#124"]}

    # Velocity
    velocity_hours_per_week: float  # Historical average
    velocity_reliability: float  # Consistency (0-1)

    # Availability
    availability_today: float  # Hours available today
    availability_this_week: float  # Hours available this week
    fully_available_date: Optional[datetime]  # When completely free

    # Risk assessment
    is_overloaded: bool
    risk_level: Literal["low", "medium", "high"]

class AssignmentSuggestion(BaseModel):
    task_id: Optional[str]  # None if task not created yet
    task_title: str
    task_estimate: float

    recommended_agent_id: str
    fit_score: float  # 0-10

    alternatives: List["AssignmentAlternative"]

    reasoning: List[str]  # ["Has capacity", "Relevant experience"]

class AssignmentAlternative(BaseModel):
    agent_id: str
    fit_score: float
    pros: List[str]
    cons: List[str]

class ReassignmentProposal(BaseModel):
    task_id: str
    from_agent_id: str
    to_agent_id: str
    reason: str
    estimated_improvement: float  # Reduction in imbalance score
    risk_level: Literal["low", "medium", "high"]
```

### CLI Commands

```bash
# Viewing workload
agentflow workload show --project <project>
agentflow workload agent <agent-code>
agentflow workload available --agent <agent-code>
agentflow workload available --agents <agent1,agent2,agent3>

# Smart assignment
agentflow task create --suggest-assignment
agentflow task reassign --task <id> --suggest

# Balancing
agentflow workload balance --project <project>
agentflow workload balance --project <project> --dry-run
agentflow workload balance --project <project> --auto
agentflow workload balance --project <project> --max-changes <3>

# Alerts
agentflow workload check --project <project>
agentflow config set --key workload_alert_threshold --value <120>
```

---

## Implementation Notes

### Dependencies

- **Feature 4 (Time Tracking)**: Requires sessions, tasks
- **Feature 5 (Sprints)**: Requires tasks, time tracking
- **Feature 6 (Workload)**: Requires agents, tasks, time tracking

### Priority

1. **Feature 4 (Time Tracking)** - Foundation for planning
2. **Feature 6 (Workload)** - High value for team management
3. **Feature 5 (Sprints)** - Cadence and structure

### Phasing

- **Phase 1**: Basic time tracking (session → task accumulation)
- **Phase 2**: Workload balancing (analysis and suggestions)
- **Phase 3**: Sprints (burndown, standups, retros)

---

**Document Version**: 1.0
**Created**: 2025-01-21
**Status**: 🎨 Design proposal - Ready for review
