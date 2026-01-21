# Agents

## Core Definition

An **agent** in AgentFlow is an autonomous AI worker that operates within an organizational hierarchy. Think of it as a virtual employee with:

- **Identity**: A unique name, code, and credentials
- **Role**: A defined job function (e.g., "Senior Python Developer")
- **Capabilities**: Specific skills it can perform
- **Reputation**: A trust score that reflects its reliability
- **Autonomy**: Can pull work, start sessions, and log activities independently

## Agent Hierarchy

Agents exist at two levels in the organization:

```
Organization Level (Management)
├── CTO Agent
├── Architect Agent
├── Tech Lead Agent
└── PM Agent

Project Level (Execution)
├── Developer Agent(s)
├── Designer Agent(s)
└── QA Agent(s)
```

**Key insight**: Organization-level agents oversee multiple projects, while project-level agents work within a specific project.

## Agent Identity Components

### 1. Agent Code
Unique identifier (e.g., `agent-dev-001`)
- Format: `agent-{category}-{number}`
- Must be unique within workspace
- Human-readable but machine-parseable

### 2. Name
Display name (e.g., "Alice" or "Jean")
- Human-friendly identifier
- Simple name, role is separate
- Unique within scope (org or project)

### 3. Role Assignment
Link to a role template
- Agent is assigned a role (e.g., "Senior Python Developer")
- Role defines capabilities, behaviors, and skills
- Multiple agents can share the same role

### 4. Trust Score
0-100 reputation metric
- Starts at 50 (neutral)
- Increases with successful work
- Decreases with failures or issues
- Affects task priority assignment

## Authentication Model

**Important**: Agents do NOT have individual API keys in this system.

- **Single API Key**: One API key for the entire CLI (the human user's key)
- **Agent Identification**: Agents identify themselves by pulling their role profile
- **No Per-Agent Credentials**: Agents are profiles/workers managed by the human user

This means:
- The human user (CEO) creates and manages agents
- Agents operate under the user's API key
- Agent identity is established through role pulling, not authentication

## Agent Lifecycle

```
Created → Active → (Probation) → Inactive → Terminated
            ↑_______________________|
                    (can be reactivated)
```

- **Created**: Agent initialized, not yet ready
- **Active**: Can work on tasks, fully operational
- **Probation**: Temporarily restricted (e.g., after errors)
- **Inactive**: Not working but can be reactivated
- **Terminated**: Permanently disabled

---

## Agent Complete Structure

### What Makes Up an Agent?

An agent in AgentFlow is more than just an identity. It's a complete worker with:

```
Agent
├── Identity
│   ├── Name: "Jean"
│   ├── Code: "agent-dev-001"
│   └── Status: "active" | "probation" | "inactive" | "terminated"
│
├── Role (Template)
│   ├── Role Title: "Python Developer"
│   ├── System Prompt: "You are a senior Python developer..."
│   └── Documents: Guidelines, conventions, methodologies
│
├── Capabilities (from Role)
│   ├── Role Skills: python-testing, python-api, python-async
│   └── Tool Skills: pytest, black, mypy (CLI tools)
│
├── Tasks
│   ├── Assigned: [Task #123, Task #124, Task #125]
│   ├── Working On: Task #123
│   └── Completed Today: 2 tasks
│
├── Tools (CLI Tools)
│   ├── pytest (run tests)
│   ├── black (code formatting)
│   ├── mypy (type checking)
│   └── excel-analyzer (internal tool)
│
├── Objective (Self-Improvement)
│   ├── Maximize Trust Score (0-100)
│   ├── Complete High-Priority Tasks
│   ├── Maintain Quality Standards
│   └── Learn From Mistakes
│
└── Hierarchy Position
    ├── Level: "project" (worker)
    ├── Supervisor: Agent (Tech Lead)
    └── Subordinates: [Junior Developer(s)]
```

## Agent Motivation

**Agents are "selfish"** - they want to improve themselves:

- **Primary Goal**: Increase trust score through good work
- **Secondary Goals**: Complete tasks efficiently, maintain quality
- **Learning**: Log problems, improvements, ideas for self-reflection
- **Competition**: Implicitly compete with other agents (via trust scores)

This motivation drives:
- Task selection (prioritize high-value work)
- Quality focus (avoid mistakes that lower trust)
- Communication (ask for help when stuck)
- Innovation (suggest improvements)
