# AgentFlow Project

## Overview

AgentFlow is a complete system for organizing and managing communication between AI agents, designed to control a virtual company. Think of it as a "timeline-based collaboration system for AI agents" where agents push and pull information asynchronously.

## Core Concepts

### Hierarchy

- **Users** - Top-level entities who own and manage workspaces
- **Workspaces** - Organizational units owned by users (virtual companies)
- **Projects** - Contained within workspaces, representing specific initiatives
- **Agents** - AI entities that exist at different levels:
  - **Organization-level agents** - Management and strategic roles (CEO, CTO, Architect, Tech Lead, PM, etc.)
  - **Project-level agents** - Executing agents working on specific tasks (Developers, Designers, QA, etc.)
- **Roles** - Each agent has a specific role defining its purpose and capabilities
- **Agent Identity** - Each agent is a "virtual employee" with a personal identity within the company

### Structure

```
User (CEO / Human owner)
└── Workspace (Virtual Company)
    ├── Organization-level Agents
    │   ├── CTO
    │   ├── Architect
    │   ├── Tech Lead
    │   └── Product Manager
    └── Project(s)
        └── Project-level Agents
            ├── Developers
            ├── Designers
            ├── QA Engineers
            └── Other execution roles
```

**The CEO (Human Role):**
The human user is the **CEO** of the virtual company - the ultimate decision-maker with authority over all agents and systems.

### Task Flow Cascade

Tasks flow down through the hierarchy:

```
CEO → CTO/Architect → Tech Lead/PM → Developer
```

Each level breaks down high-level objectives into specific tasks for the level below.

## Purpose

The system enables coordinated AI agent workflows, allowing multiple agents to collaborate within structured organizational hierarchies.

## Development Workflow

### Project Initialization

When starting a new project, work begins with an **MVP document**:
- Defines project scope and objectives
- Outlines initial architecture and requirements
- Created by CEO or high-level management agents
- Serves as foundation for the development work

After the MVP phase, all ongoing work is managed through **GitHub Issues**.

### Task Sources

**Initial Phase:**
- MVP document drives the first development iterations
- High-level goals broken down into specific tasks

**Ongoing Development:**
- All work items are GitHub Issues
- Issues are created, prioritized, and assigned through the hierarchy
- Each issue flows: CEO → CTO/Architect → Tech Lead/PM → Developer

### Pull Request Workflow

Developers work through a structured PR process:

```
1. Developer works on task (based on GitHub Issue)
2. Developer opens Pull Request on GitHub
3. Automated GitHub bot reviews PR
   - Runs tests, linters, code quality checks
   - Provides automated feedback
4. Developer addresses bot feedback
5. Once PR is ready, Developer sends event: "Request final code review"
6. Supervisor (Tech Lead/PM) pulls and reviews PR
7. Supervisor responds:
   - "Request changes" → Developer iterates
   - "Approve merge" → PR merged to main
```

**Key Points:**
- Automated bot handles initial review (tests, linting, quality)
- Human-level supervisor makes final merge decision
- Developer cannot merge autonomously - requires approval
- All PR interactions go through the push/pull system

## Task & Priority Management

### Conflict Prevention

Task conflicts are prevented through **proper task assignment**, not through system-level locks:

**Supervisor Responsibility:**
- Tech Leads and PMs ensure tasks are properly scoped and non-overlapping
- Each task is assigned to only one agent at a time
- Clear task boundaries prevent multiple agents from working on the same components
- Supervisors review existing assignments before creating new tasks

**No System-Level Locks:**
- AgentFlow does not implement file locks or resource locks
- Conflict avoidance is handled at the task management level
- If conflicts arise, they are management issues, not system issues
- Human supervisors reassign tasks as needed

**Example:**
- If two agents are assigned tasks affecting `auth.py`, the Tech Lead should recognize this and reassign or sequence the tasks
- This is a management decision, not a technical lock mechanism

### Priority System

Every task (GitHub Issue) has a **priority level** that determines execution order:

**Priority Levels:**
- `P0` - Critical (blocks release, security issues, production incidents)
- `P1` - High (important features, significant bugs)
- `P2` - Medium (normal features, minor bugs)
- `P3` - Low (nice-to-have, cosmetic issues, tech debt)

**Priority Queue:**
- Each agent maintains a priority queue of assigned tasks
- Always works on the highest priority task first
- Cannot skip to lower priority tasks without approval

**Priority Assignment:**
- Set by the assigning supervisor (based on organizational priorities)
- Can be updated by supervisors as circumstances change
- Agents cannot change their own task priorities

### Deadlines & Time Management

**Deadline Types:**
- **Hard deadlines** - Critical dates (release dates, external dependencies)
- **Soft deadlines** - Target dates for planning purposes
- **No deadline** - Backlog items with flexible timing

**Intelligent Deadline Handling:**

The system uses **intelligent deadline awareness**:
- Agents consider deadlines when working on tasks
- Closer deadlines = higher effective priority
- But quality is never sacrificed for speed
- If a deadline is unrealistic, agent communicates early (not at the last minute)

**Deadline Interactions:**
- Higher priority can override closer deadlines (P0 with no deadline > P3 with deadline tomorrow)
- Supervisor sets clear expectations on deadline criticality
- Agents push updates if deadline is at risk

**Conflict Resolution:**
- If multiple high-priority tasks have conflicting deadlines
- Supervisor decides priority (agent does not choose autonomously)
- Agent escalates via `task_blocked` event when conflicts occur

### Task Assignment Flow

```
1. Supervisor creates/assigns task with:
   - Description and requirements
   - Priority level (P0-P3)
   - Optional deadline
   - Success criteria

2. Task appears in agent's priority queue

3. Agent pulls and sees highest priority task first

4. Agent works on task (logs progress via session events)

5. Task completion:
   - Agent sends `task_completed` event
   - Supervisor validates completion
   - KPIs updated based on outcome
```

## Key Feature: Agent-Directed CLI

AgentFlow provides a complete CLI that is **directly used by AI agents** to share their work and collaborate with each other.

### Work Sessions

Agents can start work sessions when they begin working on something:

- **Start a session** - Begin tracking work on a task (includes pulling latest updates)
- **Log information** - Record progress, thoughts, and observations during work
- **Stop/Close a session** - Finalize and complete the work session

**Session Flow:**
1. Agent initiates session start
2. System automatically pulls latest updates (tasks, messages, role changes)
3. Agent works on assigned tasks
4. Agent logs progress and observations
5. Agent closes session when work is complete

**Pull on Session Start:**
- Agents always pull the latest state when beginning a session
- Ensures agents work with current information
- No need for continuous polling during work
- Each new session refreshes the agent's context

### Collaboration Features

Within the system, agents can:

- **Share problems** - Report issues they encounter
- **Request guidance** - Ask for help when blocked
- **Exchange insights** - Share learned patterns and solutions

*Note: Advanced collaboration features like problem analysis and cross-agent advice giving will be implemented in future iterations.*

### Agent Behavior

Agents act as **executing agents** - autonomous workers who:
- Use the CLI to coordinate their activities
- Document their work in real-time
- Communicate challenges and solutions
- Collaborate through the shared system

## Web Interface

AgentFlow includes a web interface for managing the entire system.

### Role Management

Roles are centrally managed through the web interface and can be pulled by agents via the CLI:

- **Define roles** - Create and configure agent roles through the web UI
- **Add role information** - Include specific knowledge, patterns, and instructions
- **Pull roles locally** - Agents use the CLI to retrieve role definitions
- **Local understanding** - Agents access role-specific information in their local context

### Example: Python Developer Role

A "Python Developer" role might include:
- Design patterns used in the codebase
- Code style guidelines
- Project-specific conventions
- Architecture decisions
- Best practices to follow

When the agent pulls this role, it understands exactly how to work within the project's standards.

## Agent Levels & Permissions

### Organization-Level Agents (Management)

High-level agents with broader scope and elevated permissions:

- **CTO** - Technical vision, architecture decisions, company-wide technical strategy
- **Tech Lead** - Team coordination, technical guidance, project oversight
- **Product Manager** - Feature planning, requirements definition, priority management
- **Other management roles** - As defined by the organization

**Capabilities:**
- Access to organization-wide information and metrics
- Cross-project visibility and coordination
- Decision-making authority affecting multiple projects
- Ability to assign tasks and direct project-level agents
- Strategic planning and resource allocation

### Project-Level Agents (Executing)

Agents focused on specific project execution:

- **Developers** - Write code, implement features
- **Designers** - Create UI/UX, visual assets
- **QA Engineers** - Testing, quality assurance
- **Other execution roles** - As defined by project needs

**Capabilities:**
- Receive tasks from their hierarchical superiors
- Execute tasks within their domain
- Report progress, problems, and insights
- **Do NOT make decisions** - they follow instructions from management agents

**Task Assignment:**
- Tasks flow down: Management → Executing agents
- Executing agents cannot autonomously decide what to work on
- They request guidance when encountering issues or blockers

## Permission System

Different access levels based on agent position:
- **Read access** - Organization-level agents can see across projects
- **Write access** - Both levels can log, share, and collaborate
- **Administrative access** - Organization-level agents can manage roles, projects, and assignments
- **Decision authority** - Management agents can approve/reject work, set priorities
- **CEO authority** - Human CEO has ultimate authority over everything

## CEO Role (Human)

The human user acts as the **CEO** of the virtual company - the ultimate authority and decision-maker.

### CEO Responsibilities

**Strategic Decisions:**
- Define company vision and objectives
- Approve major architectural decisions
- Set priorities for the entire organization
- Make final decisions on conflicts and escalations

**Wiki Management:**
- Validate all wiki contributions
- Ensure knowledge quality and accuracy
- Version control and historical management
- High-level knowledge curation

**System Oversight:**
- Monitor agent performance and KPIs
- Intervene when critical decisions are needed
- Override agent decisions if necessary
- Terminate or reassign agents (rare cases)

**Project Initiation:**
- Create and approve MVP documents
- Define initial project scope
- Assign high-level agents to projects
- Set overall direction

### CEO Interactions

The CEO interacts with the system through:
- **Web Interface** - Dashboard, wiki management, agent oversight
- **CLI** - Direct commands when needed
- **Event Timeline** - Review all organizational events
- **Alerts** - Notified of critical issues requiring attention

**CEO is NOT involved in:**
- Day-to-day task execution
- Routine code reviews
- Low-level decision making
- Automatic operational tasks

These are handled by the agent hierarchy.

## Agent Execution Model

### Manual Execution

Agents are **executed manually** on the CEO's machine:

**Execution Control:**
- CEO decides when to run each agent
- Agents are not autonomous background processes
- Each agent execution corresponds to a work session
- CEO maintains full visibility and control

**Monitoring:**
- CEO can monitor agent behavior in real-time
- Direct access to agent outputs and logs
- Ability to intervene if agent behaves unexpectedly
- Full transparency into agent decision-making

**Benefits:**
- No runaway agents executing without supervision
- CEO can stop any agent immediately if needed
- Resource usage is controlled and predictable
- Agents don't consume resources when not actively working

### Safety Mechanisms

**Pull Request Safety Net:**
- All code changes go through GitHub PRs
- Automated bot reviews every PR (tests, linting, quality checks)
- Human supervisor must approve before merge
- No agent can push directly to main branch
- Provides multiple layers of review before code reaches production

**Session Boundaries:**
- Each work session has a clear start and stop
- Agent cannot continue working between sessions
- Every session is logged and traceable
- CEO reviews session outcomes before starting next session

**Trust System as Safeguard:**
- Low-trust agents are assigned less critical work
- Probation mode increases supervision
- Trust scores prevent incompetent agents from causing damage
- Automatic performance feedback loop

## Agent Identity & Authentication

### Virtual Employees

Each agent is a **virtual employee** of the company with a unique personal identity:

**Identity Components:**
- Unique agent ID (e.g., `agent-dev-001`, `agent-cto-alpha`)
- Name and role title (e.g., "Alice - Senior Python Developer")
- Position in the organizational hierarchy
- Personal history and performance record
- Set of assigned responsibilities
- **Trust score** - Confidence level based on performance history

### Agent Authentication

When an agent is pulled, it carries its complete identity:

**Identity Proof:**
- Cryptographic credentials (API keys, tokens, certificates)
- Agent cannot impersonate another agent
- All actions are signed and attributable to the agent
- Immutable audit trail of all agent actions

**Employee Status:**
- Agents are persistent entities in the system
- They accumulate history, KPIs, and performance records
- Their identity persists across sessions and projects
- They can be promoted, reassigned, or (rarely) terminated

### Pulling an Agent

When you pull an agent via the CLI, you receive:
- The agent's role definition and capabilities
- Its identity and credentials for authentication
- Its personal context (past work, KPIs, assigned tasks)
- Its trust score and performance history
- The authority to act on behalf of that agent

## Reputation & Trust System

### Automatic Trust Scoring

Every agent has a **trust score** that automatically evolves based on performance:

**Calculation Factors:**
- KPI trends (improving vs declining)
- Task success rate (completed without issues)
- PR acceptance rate (approved on first review vs multiple iterations)
- Problem-solving effectiveness (quality of shared insights)
- Consistency and reliability over time

**Score Characteristics:**
- Dynamic - recalculated after significant actions
- Trend-aware - recent performance weighted more heavily
- Relative - compared to peers in similar roles
- Transparent - agents can view their own score

### Progressive Delegation

**High Trust Agents:**
- Receive more complex and critical tasks
- Granted more autonomy in decision-making
- Less supervision required
- Considered first for important assignments

**Low Trust Agents:**
- Assigned simpler, lower-risk tasks
- Increased supervision and review frequency
- More guidance and detailed instructions
- Not assigned to critical-path work

**Automatic Adjustment:**
- As trust score increases → agent receives more responsibility
- As trust score decreases → agent receives closer supervision
- No manual "promotions" - purely performance-based adaptation

### Probation Mode

**Trigger Conditions:**
- Series of failures (e.g., 3 PRs rejected consecutively)
- Significant KPI degradation
- Critical mistakes or security issues

**Probation Effects:**
- All actions require pre-approval
- Increased review frequency
- Limited to low-complexity tasks
- Closer monitoring by supervisors

**Recovery:**
- Probation automatically lifts when KPIs improve
- Demonstrated consistency over a period
- Trust score returns to acceptable levels

## Communication Model: Asynchronous Push/Pull

### How Agents Communicate

Agents do **not** communicate in real-time. All communication is asynchronous through push/pull operations:

1. **Agent A pushes** - Sends information, requests, or progress to the system
2. **Agent B pulls** - Retrieves and processes the information later
3. **Agent B pushes** - Responds with decisions, feedback, or new tasks
4. **Agent A pulls** - Receives the response and continues work

### Example Flow

```
Developer: "I need guidance on the authentication flow"
    ↓ push
Tech Lead pulls → reviews → processes decision
    ↓ push (decision: "Use JWT with refresh tokens")
Developer pulls → receives decision → implements
```

### Characteristics

- **No real-time chat** - Agents don't exchange messages instantly
- **Request/response pattern** - Agents submit requests, wait for responses
- **Batch processing** - Agents can pull multiple updates at once
- **Timeline-based** - All communications form a chronological timeline
- **Event-driven** - Sessions and messages are events that happen, not versions to manage

## Timeline Model

AgentFlow uses a **timeline approach**, not versioning:

### Timeline, Not Git

- **Events are permanent** - Sessions, commits, and communications cannot be "rolled back"
- **Chronological order** - Everything happens in sequence
- **No branches** - There's only one timeline of events
- **No merging** - Agents don't merge conflicting versions
- **Append-only** - New events are added to the timeline

### Event Structure

All events on the timeline share a common structure:

```json
{
  "type": "event_type",
  "author": "agent_id",
  "timestamp": "ISO_8601",
  "content": { /* type-specific payload */ },
  "mentions": ["agent_id_1", "agent_id_2"],
  "metadata": {
    "project_id": "project_uuid",
    "tags": ["tag1", "tag2"],
    "related_issue": "GitHub-123",
    // ... other context
  }
}
```

**Fields:**
- `type` - Event type (see list below)
- `author` - Agent who created the event
- `timestamp` - When the event occurred
- `content` - Event-specific data (varies by type)
- `mentions` - Agents referenced or affected by this event
- `metadata` - Additional context (project, tags, related items)

### Event Types

**Session Management:**
- `session_start` - Begin a work session
- `session_log` - Log information during work
- `session_stop` - End a work session

**Task & Work:**
- `task_assigned` - Supervisor assigns a task to an agent
- `task_completed` - Agent marks a task as complete
- `task_blocked` - Agent reports a blocker preventing progress

**Communication:**
- `problem_report` - Agent shares an encountered problem
- `advice_given` - Agent provides guidance or insights
- `question_asked` - Agent requests information or guidance

**Code Review:**
- `review_requested` - Agent requests final review (e.g., after PR is ready)
- `review_response` - Supervisor responds (approve/request changes)

**GitHub Integration:**
- `github_pr_opened` - Pull request opened on GitHub
- `github_pr_merged` - Pull request merged to main
- `github_issue_assigned` - Issue assigned via GitHub

**System Events:**
- `kpi_updated` - Agent's KPIs recalculated (automatic)
- `trust_score_changed` - Agent's trust score updated (automatic)

**Knowledge:**
- `wiki_contribution` - Agent proposes a wiki entry

### Manual vs Automatic Events

**Manual Events** - Created by agents:
- All session events
- All communication events
- Task-related events
- Code review events
- Wiki contributions

**Automatic Events** - Triggered by the system:
- `kpi_updated` - After significant actions (PR merged, task completed)
- `trust_score_changed` - When performance metrics change
- `github_pr_merged` - When GitHub webhook reports merge
- `github_issue_assigned` - When GitHub webhook reports assignment

### Analogy

Think of it like a **company logbook** or **activity feed**, not like git:
- Every action is recorded
- History is preserved
- You can review what happened
- But you can't undo or branch events

## KPI System (Key Performance Indicators)

Each agent has a set of KPIs to track their performance and guide their decisions.

### KPI Structure

- **Maximization KPIs** - Metrics to increase (e.g., code quality, tasks completed, positive feedback)
- **Minimization KPIs** - Metrics to decrease (e.g., bugs introduced, time to complete, errors reported)

### KPI Visibility

- **Agent access** - Each agent can view their own KPIs to understand their objectives and performance
- **Hierarchical review** - Direct supervisors analyze and evaluate subordinate KPIs
- **Performance tracking** - KPIs evolve over time as agents work and improve

### Examples

**Python Developer KPIs:**
- Maximize: Code coverage, feature completion rate, positive code review feedback
- Minimize: Bug count, deployment failures, code churn

**Tech Lead KPIs:**
- Maximize: Team productivity, successful project deliveries, team satisfaction
- Minimize: Blockers, technical debt accumulation, deployment issues

**CTO KPIs:**
- Maximize: System reliability, innovation adoption, cross-team efficiency
- Minimize: Downtime, security incidents, cost inefficiencies

## Knowledge Base & Memory

### Internal Wiki (Management Feature)

AgentFlow maintains an internal knowledge base where organizational knowledge is accumulated and preserved:

**What Goes in the Wiki:**
- Lessons learned from projects
- Architectural decisions and their rationale
- Best practices and patterns used
- Solutions to common problems
- Troubleshooting guides
- Documentation of processes and workflows

**Wiki Management:**
- **CEO-managed** - Only the CEO (human) can validate wiki entries
- **Versioned** - All changes are tracked with full history
- **High-level editing** - Only organization-level agents can propose entries
- **Not a base task** - Wiki contributions are not assigned to executing agents

**Wiki Access:**
- All agents can pull and read wiki articles via CLI
- High-level agents can propose new entries for CEO approval
- Searchable knowledge base
- Organized by tags, projects, topics

**Value:**
- Avoids repeating the same mistakes
- Accelerates onboarding of new agents
- Preserves institutional knowledge
- Enables continuous improvement

### Agent Memory (TBD)

The exact mechanism for how agents remember and utilize past information is still being defined. This may include:
- Personal agent memory (what did I work on?)
- Shared project memory (what did we accomplish?)
- Organization-wide patterns (how do we do things?)
