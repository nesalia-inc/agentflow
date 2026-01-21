# Agent System Design - Phase 0 (Dummy Implementation)

## Document Purpose

This document explores the design and reasoning for an **agent management system** in AgentFlow. It defines what an agent is, how roles work, and how agents interact with the system through work sessions and logging.

**Status**: Design & Reasoning Phase
**Implementation**: Phase 0 (Dummy/Local Storage)
**Target**: Full system with API backend

---

## Table of Contents

1. [What is an Agent?](#what-is-an-agent)
2. [Agent Complete Structure](#agent-complete-structure)
3. [Understanding Roles vs Agents](#understanding-roles-vs-agents)
4. [Role Structure & Documents](#role-structure--documents)
5. [Tools & Skills Integration](#tools--skills-integration)
6. [Hierarchy & Organization](#hierarchy--organization)
7. [Tasks System](#tasks-system)
8. [Permissions System](#permissions-system)
9. [Agent Communication](#agent-communication)
10. [Reward & Punition System](#reward--punition-system)
11. [Pulling an Agent & Skill Generation](#pulling-an-agent--skill-generation)
12. [Claude Code Skills Format](#claude-code-skills-format)
13. [Work Sessions](#work-sessions)
14. [Agent Logging](#agent-logging)
15. [CLI Commands Design](#cli-commands-design)
16. [Data Models (Phase 0)](#data-models-phase-0)
17. [Workflow Examples](#workflow-examples)
18. [Open Questions & Decisions Needed](#open-questions--decisions-needed)

---

## What is an Agent?

### Core Definition

An **agent** in AgentFlow is an autonomous AI worker that operates within an organizational hierarchy. Think of it as a virtual employee with:

- **Identity**: A unique name, code, and credentials
- **Role**: A defined job function (e.g., "Senior Python Developer")
- **Capabilities**: Specific skills it can perform
- **Reputation**: A trust score that reflects its reliability
- **Autonomy**: Can pull work, start sessions, and log activities independently

### Agent Hierarchy

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

### Agent Identity Components

1. **Agent Code**: Unique identifier (e.g., `agent-dev-001`)
   - Format: `agent-{category}-{number}`
   - Must be unique within workspace
   - Human-readable but machine-parseable

2. **Name**: Display name (e.g., "Alice" or "Jean")
   - Human-friendly identifier
   - Simple name, role is separate
   - Unique within scope (org or project)

3. **Role Assignment**: Link to a role template
   - Agent is assigned a role (e.g., "Senior Python Developer")
   - Role defines capabilities, behaviors, and skills
   - Multiple agents can share the same role

4. **Trust Score**: 0-100 reputation metric
   - Starts at 50 (neutral)
   - Increases with successful work
   - Decreases with failures or issues
   - Affects task priority assignment

### Authentication Model

**Important**: Agents do NOT have individual API keys in this system.

- **Single API Key**: One API key for the entire CLI (the human user's key)
- **Agent Identification**: Agents identify themselves by pulling their role profile
- **No Per-Agent Credentials**: Agents are profiles/workers managed by the human user

This means:
- The human user (CEO) creates and manages agents
- Agents operate under the user's API key
- Agent identity is established through role pulling, not authentication

### Agent Lifecycle

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

### Agent Motivation

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

---

## Understanding Roles vs Agents

### Core Concept: Template vs Instance

The system distinguishes between **Roles** (templates) and **Agents** (instances):

```
Role (Template)              Agent (Instance)
──────────────               ────────────────
"Python Developer"    →      "Jean"
"React Developer"     →      "Alice"
"QA Engineer"         →      "Bob"
                            "Charlie"
```

**Key Characteristics**:

| Aspect | Role | Agent |
|--------|------|-------|
| **Nature** | Template/blueprint | Instance of a role |
| **Assignability** | Can be assigned to many agents | One role per agent |
| **Storage** | API (remote) | Local database |
| **Identity** | Defines capabilities/behaviors | Has unique name/code |
| **Pull** | Pulled by agents | Performs the pull |
| **Skills** | Contains documents → generate skills | Receives and uses skills |

### Why This Distinction Matters

1. **Reusability**: Create a role once, assign to multiple agents
   - "Python Developer" role can be used by Jean, Alice, Bob
   - Update role once → all agents benefit

2. **Individualization**: Each agent has unique identity while sharing role
   - Jean has his own trust score, session history
   - Alice has different trust score, different sessions
   - Both use the same "Python Developer" skills

3. **Scalability**: Easy to add new agents
   - Need another Python developer? Create agent, assign role
   - No need to redefine capabilities/behaviors

4. **Hierarchical Management**: Roles define organizational structure
   - Organization-level roles (CTO, Architect)
   - Project-level roles (Developer, Designer, QA)
   - Agents fit into this hierarchy

### Workflow

```bash
# 1. Create a role (on the API)
agentflow role create \
  --name "Python Developer" \
  --description "Senior Python developer with FastAPI expertise"

# 2. Add documents to the role
agentflow role add-document python-dev --file "testing-guidelines.md"
agentflow role add-document python-dev --file "api-conventions.md"

# 3. Create agents and assign the role
agentflow agent create \
  --name "Jean" \
  --code "agent-dev-001" \
  --role "Python Developer" \
  --level project

agentflow agent create \
  --name "Alice" \
  --code "agent-dev-002" \
  --role "Python Developer" \
  --level project

# 4. Agent pulls the role to get skills
agentflow agent pull agent-dev-001
# → Generates Claude Code skills from role documents
```

---

## Role Structure & Documents

### What is a Role?

A **role** is a template stored on the API that defines:

1. **Identity**: Role name and description
2. **System Prompt**: Core personality and behaviors (sent to AI)
3. **Documents**: Markdown files with rules, concepts, methodologies
4. **Generated Skills**: When pulled, documents become Claude Code skills

### Role Components

#### 1. Role Metadata

```yaml
name: "Python Developer"
slug: "python-dev"
description: "Senior Python developer specializing in FastAPI and PostgreSQL"
level: "project"  # or "organization"
created_at: "2025-01-21T09:00:00Z"
```

#### 2. System Prompt (Description)

The role's description acts as the **system prompt** - the core personality and behavioral instructions that will be sent to an AI (like Claude).

Example:
```
You are a Senior Python Developer specializing in FastAPI and PostgreSQL.
You are rigorous and pragmatic in your approach to development.
You prioritize code readability, testability, and documentation.
You always question unclear requirements before implementing.
You follow TDD (Test-Driven Development) practices.
```

This system prompt:
- Defines who the agent "is"
- Establishes behavioral patterns
- Guides decision-making
- Sets communication style

#### 3. Role Documents (Markdown Files)

Roles contain **documents** that provide detailed knowledge in Markdown format:

**Document Types**:

| Type | Purpose | Example |
|------|---------|---------|
| **Guidelines** | Rules and standards | `testing-guidelines.md` - How to write tests |
| **Concepts** | Domain knowledge | `async-patterns.md` - Async/await best practices |
| **Methodologies** | Work processes | `code-review-process.md` - Review checklist |
| **Conventions** | Code standards | `api-conventions.md` - Endpoint naming |
| **Examples** | Reference implementations | `authentication-example.md` - JWT setup |

**Example Document Structure**:

```markdown
# Testing Guidelines

## Principles

1. **Test-First**: Write tests before implementation (TDD)
2. **Coverage**: Maintain >80% test coverage
3. **Isolation**: Each test should be independent

## Test Structure

```python
def test_<feature>_<scenario>():
    # Arrange
    # Act
    # Assert
```

## Required Tests

- Unit tests for all business logic
- Integration tests for API endpoints
- Edge case testing
```

#### 4. From Documents to Skills

When an agent pulls a role, the role's documents are **transformed into Claude Code skills**:

```
Role Document                          Claude Code Skill
─────────────                          ─────────────────
testing-guidelines.md          →        ~/.claude/skills/python-testing/
api-conventions.md             →        ~/.claude/skills/python-api/
async-patterns.md              →        ~/.claude/skills/python-async/
```

Each skill follows the Claude Code format:
- `SKILL.md` with frontmatter (YAML) + content (Markdown)
- Optional supporting files
- Invoked via `/skill-name` or auto-loaded

### Role Storage & Access

```
┌─────────────────────┐
│   AgentFlow API     │
│                     │
│  Roles Storage:     │
│  ┌──────────────┐   │
│  │ python-dev   │   │
│  │ react-dev    │   │
│  │ qa-engineer  │   │
│  └──────────────┘   │
└─────────┬───────────┘
          │
          │ HTTP Pull (agentflow agent pull agent-001)
          │
          ▼
┌─────────────────────────────────────┐
│  Local AgentFlow (.agentflow/)      │
│  ┌──────────────────────────────┐  │
│  │ Agent: Jean (agent-dev-001)  │  │
│  │ Role: Python Developer       │  │
│  │ Last Pull: 2025-01-21        │  │
│  └──────────────────────────────┘  │
└─────────┬───────────────────────────┘
          │
          │ Skill Generation
          ▼
┌─────────────────────────────────────┐
│  Claude Code Skills                  │
│  ~/.claude/skills/                   │
│  ┌────────────────────────────────┐ │
│  │ python-testing/SKILL.md        │ │
│  │ python-api/SKILL.md            │ │
│  │ python-async/SKILL.md          │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Predefined Roles

The system can provide predefined role templates:

#### Organization-Level Roles

| Role | System Prompt Focus | Documents |
|------|---------------------|-----------|
| **CTO** | Technical strategy, architecture decisions | `tech-strategy.md`, `architecture-principles.md` |
| **Architect** | System design, technical standards | `design-patterns.md`, `standards.md` |
| **Tech Lead** | Team coordination, code quality | `review-guidelines.md`, `mentoring.md` |
| **PM** | Project management, priorities | `planning-process.md`, `reporting.md` |

#### Project-Level Roles

| Role | System Prompt Focus | Documents |
|------|---------------------|-----------|
| **Python Developer** | FastAPI, PostgreSQL, async | `python-best-practices.md`, `fastapi-conventions.md` |
| **React Developer** | React, TypeScript, state | `react-patterns.md`, `typescript-guide.md` |
| **QA Engineer** | Testing, automation, quality | `testing-strategy.md`, `automation-guide.md` |

### Custom Role Creation

Users can create custom roles:

```bash
# Create a new role
agentflow role create \
  --name "ML Engineer" \
  --description "Machine Learning engineer specializing in Python and TensorFlow"

# Add documents to the role
agentflow role add-document ml-engineer \
  --name "ml-best-practices" \
  --file "./docs/ml-guidelines.md"

agentflow role add-document ml-engineer \
  --name "tensorflow-patterns" \
  --file "./docs/tensorflow-patterns.md"

# Assign role to an agent
agentflow agent create \
  --name "Emma" \
  --code "agent-ml-001" \
  --role "ML Engineer" \
  --level project
```

---

## Tools & Skills Integration

### What are Tools?

**Tools** are internal CLI utilities developed by the organization that agents can use to perform their work. Each tool has:
- A command-line interface
- Associated documentation (as a skill)
- Specific capabilities

**Examples of Internal Tools**:
```bash
# Testing tool
pytest --cov=src --cov-report=html

# Code formatting
black src/ --line-length=100

# Type checking
mypy src/ --strict

# Excel analysis (custom tool)
excel-analyzer analyze data.xlsx --output report.html

# Content generation (custom tool)
content-gen --type blog --topic "AgentFlow"
```

### Tool Categories

| Category | Examples | Purpose |
|----------|----------|---------|
| **Development** | pytest, black, mypy, pylint | Code quality, testing |
| **Build/Deploy** | docker-compose, kubectl, build.sh | Deployment, infrastructure |
| **Data Processing** | excel-analyzer, csv-transformer | Data analysis, transformation |
| **Content** | content-gen, markdown-formatter | Content creation, formatting |
| **Communication** | slack-cli, email-sender | Notifications, updates |

### Tools in Roles

Roles define which tools agents can use:

```yaml
# Role: Python Developer
tools:
  - name: pytest
    skill: python-pytest
    description: "Run tests with pytest framework"

  - name: black
    skill: python-black
    description: "Format code with Black"

  - name: mypy
    skill: python-mypy
    description: "Type checking with mypy"
```

When an agent pulls the role:
1. Role documents → Role skills (guidelines, conventions)
2. Role tools → Tool skills (how to use each CLI tool)

### Tool Documentation Storage

**IMPORTANT: Each tool has its own Markdown documentation stored in the database**

Just like roles have documents, tools have documentation that gets transformed into Claude Code skills:

```
Database: tools
├── Tool: pytest
│   ├── name: "pytest"
│   ├── description: "Python testing framework"
│   ├── documentation: "# Pytest Usage Guide\n\n## Running Tests\n..."
│   └── skill_name: "python-pytest"
│
├── Tool: black
│   ├── name: "black"
│   ├── description: "Python code formatter"
│   ├── documentation: "# Black Usage\n\n## Formatting\n..."
│   └── skill_name: "python-black"
│
└── Tool: excel-analyzer
    ├── name: "excel-analyzer"
    ├── description: "Internal Excel analysis tool"
    ├── documentation: "# Excel Analyzer\n\n## Usage\n..."
    └── skill_name: "excel-analyzer"
```

**Tool Definition Structure**:
```
┌─────────────────────────────────────────┐
│  Tool (in Database)                      │
│  ┌────────────────────────────────┐    │
│  │ name: "pytest"                  │    │
│  │ slug: "pytest"                  │    │
│  │ description: "Python testing"   │    │
│  │ category: "development"         │    │
│  │ command: "pytest"               │    │
│  │ documentation: "MD content"     │    │
│  │ skill_name: "python-pytest"     │    │
│  │ created_at: "..."               │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

**Creating/Updating Tools**:

Tools are managed via CLI (similar to roles):

```bash
# Create a new tool
agentflow tool create \
  --name "excel-analyzer" \
  --slug "excel-analyzer" \
  --category "data" \
  --description "Internal Excel analysis tool" \
  --documentation "./docs/excel-analyzer.md"

# Update tool documentation
agentflow tool update excel-analyzer \
  --documentation "./docs/excel-analyzer-v2.md"

# View tool details
agentflow tool view excel-analyzer

# List all tools
agentflow tool list
agentflow tool list --category development
```

**Internal vs External Tools**:

| Type | Example | Management |
|------|---------|------------|
| **External** | pytest, black, mypy | Pre-defined in system, documentation shipped with AgentFlow |
| **Internal** | excel-analyzer, csv-transformer | Custom tools, organization manages documentation |

**Skill Generation for Tools**:

When an agent pulls a role:
1. System identifies tools associated with the role
2. For each tool, retrieves its Markdown documentation from database
3. Generates Claude Code skill: `~/.claude/skills/<skill_name>/SKILL.md`
4. Agent now has both role skills AND tool skills available

### Tool Skills Format

Each tool has a corresponding Claude Code skill:

**File**: `~/.claude/skills/python-pytest/SKILL.md`

```yaml
---
name: python-pytest
description: Testing guidelines and pytest usage for Python projects. Use when running tests, checking coverage, or debugging test failures.
---

# Pytest Testing Tool

## Running Tests

\`\`\`bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=src --cov-report=html

# Verbose output
pytest -v
\`\`\`

## Test Structure

Follow naming convention:
- Test files: `test_<module>.py`
- Test functions: `test_<feature>_<scenario>()`
- Test classes: `Test<ClassName>`

## Coverage Goals

- Maintain >80% code coverage
- All critical paths must be tested
- Edge cases must be covered

## When to Use

Use pytest when:
- Writing new tests
- Checking test results
- Investigating test failures
- Validating code changes
```

### Tool Assignment Workflow

```
Role Definition (on API)
├── Role: Python Developer
└── Tools: [pytest, black, mypy]

        ↓ Agent Pull

Agent pulls role
├── Generates role skills (python-testing, python-api)
└── Generates tool skills (python-pytest, python-black, python-mypy)

        ↓ Agent Works

Agent uses tools during session
├── Executes: pytest --cov=src
├── Logs: "Ran tests, coverage at 85%"
└── Files logged as evidence
```

### Tool Capabilities vs Permissions

**Important distinction**:

| Aspect | Capabilities | Permissions |
|--------|--------------|-------------|
| **What** | Tools agent CAN use | Actions agent ALLOWED to do |
| **Defined By** | Role (tools list) | Role (permission level) |
| **Example** | Can run `pytest` | Can approve task as completed |
| **Enforcement** | Skill available in Claude Code | Server-side validation |

An agent may:
- **Have capability** for a tool (skill is loaded)
- **Not have permission** to use it (restricted by role/status)

Example: Junior developer has `pytest` skill but cannot deploy to production.

---

## Hierarchy & Organization

### Organizational Structure

AgentFlow uses a **tree-based hierarchy** at two levels:

**IMPORTANT: One-to-many relationship only**

Each agent has **exactly one supervisor** (parent in the tree). No many-to-many relationships, no dotted line reports, no matrix management.

**Why one-to-many?**
- **Simplicity**: Clear chain of command, no ambiguity
- **Agents ≠ Humans**: Agents don't have complex organizational politics
- **Review workflow**: Clear who reviews whose work
- **Priority**: One source of task assignments and priorities

```
Organization Tree (Company-Wide)
├── CEO (Human)
├── CTO Agent
│   ├── Architect Agent
│   └── Tech Lead Agent 1
└── PM Agent

Project Tree (Per Project)
├── Tech Lead Agent (Manager)
│   ├── Senior Developer Agent
│   │   └── Developer Agent
│   └── QA Engineer Agent
└── Designer Agent
    └── Junior Designer Agent
```

### Two-Level Hierarchy

#### 1. Organization-Level Tree

**Purpose**: High-level management and strategy

**Agents**:
- CTO, Architect, Tech Lead, PM
- Work across multiple projects
- Coordinate organization-level decisions

**Commands**:
```bash
# Define organization hierarchy
agentflow org set-hierarchy --tree "
CTO
├── Architect
├── Tech Lead
└── PM
"

# View hierarchy
agentflow org hierarchy show
```

#### 2. Project-Level Tree

**Purpose**: Project execution and team coordination

**Agents**:
- Developers, Designers, QA, etc.
- Work within a single project
- Report to project manager

**Commands**:
```bash
# Define project team hierarchy
agentflow project set-hierarchy --project my-project --tree "
Tech Lead
├── Senior Dev
│   └── Dev
└── QA
"

# View project hierarchy
agentflow project hierarchy show --project my-project
```

### Hierarchy Rules

**One-to-Many Constraints**:
```
✅ Allowed:
  - One supervisor → Multiple subordinates
  - Single chain of command
  - Clear parent-child relationships

❌ NOT Allowed:
  - One agent → Multiple supervisors
  - Dotted line relationships
  - Matrix reporting (technical + functional)
  - Circular references (A supervises B, B supervises A)
```

**Why No Multiple Supervisors?**

| Aspect | One Supervisor (Our Design) | Multiple Supervisors |
|--------|---------------------------|---------------------|
| **Review** | Clear: Tech Lead reviews Dev | Ambiguous: Who reviews? Both? |
| **Priorities** | One source of truth | Conflicting priorities |
| **Task assignment** | Single manager assigns | Who assigns? Overlap? |
| **Escalation** | Clear path up the tree | Which path to take? |
| **Complexity** | Simple | Very complex |

**If Agent Needs Multiple Managers**:

Don't use multiple supervisors. Instead:
- **Option 1**: Choose the primary supervisor
  ```
  Jean (Dev) → Tech Lead (technical supervisor)
  ```

- **Option 2**: Create a role that encompasses both
  ```
  Jean (Dev + QA Lead) → Tech Lead
  ```

- **Option 3**: Split into separate agents
  ```
  Jean-Dev (Dev) → Tech Lead
  Jean-QA (QA Lead) → QA Manager
  ```

**For Phase 0**: Implement strictly one-to-many relationships
**Full System**: Keep one-to-many unless real use case emerges (unlikely for agents)

### Supervisor Identification

Agents can identify their supervisor through:

**Command**:
```bash
agentflow agent who-is-my-boss --agent agent-dev-001

# Output:
# Agent: Jean (agent-dev-001)
# Role: Python Developer
# Supervisor: Tech Lead (agent-lead-001)
# Path: Tech Lead > Senior Dev > Jean
```

**API/Database**:
```python
def get_supervisor(agent_id: str) -> Agent:
    # Get agent's position in project tree
    # Find parent in tree structure
    # Return supervisor agent
```

### Subordinate Management

Agents can see their subordinates:

```bash
agentflow agent subordinates --agent agent-lead-001

# Output:
# Agent: Tech Lead (agent-lead-001)
# Subordinates (3):
#   • Senior Dev (agent-senior-001)
#   • Dev (agent-dev-001)
#   • QA (agent-qa-001)
```

### Hierarchy in Review Workflow

When an agent completes a task and needs review:

```
1. Jean (Developer) marks task "ready for review"
2. System checks Jean's supervisor in project tree
3. System finds: Tech Lead (agent-lead-001)
4. System creates review task for Tech Lead
5. Tech Lead sees review task in their queue
6. Tech Lead reviews and approves/rejects
```

### Multiple Projects, Multiple Roles

An agent can have different positions in different projects:

```python
Agent: Alice (agent-dev-002)

Project A (website-redesign):
  Role: Senior Developer
  Supervisor: Tech Lead A
  Subordinates: [Dev 1, Dev 2]

Project B (mobile-app):
  Role: Tech Lead
  Supervisor: None (top of project tree)
  Subordinates: [Mobile Dev 1, Mobile Dev 2]
```

### Hierarchy Management Commands

```bash
# Define hierarchy (interactive)
agentflow project set-hierarchy --project my-project --interactive

# Export hierarchy to file
agentflow project hierarchy export --project my-project --output tree.yaml

# Import hierarchy from file
agentflow project hierarchy import --project my-project --input tree.yaml

# Validate hierarchy (check for cycles, orphans)
agentflow project hierarchy validate --project my-project

# Visualize hierarchy (ASCII tree)
agentflow project hierarchy visualize --project my-project
```

---

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

## Permissions System

### Role-Based Permissions

**Permissions are based on roles**, not trust score. Each role has specific capabilities and restrictions.

### Permission Levels

#### Organization-Level Roles (Managers)

**Full Permissions**:
- Create tasks for anyone
- Assign tasks to subordinates
- Review and approve tasks
- Modify task priorities
- Cancel any task
- View all tasks in organization

**Examples**: CTO, Architect, Tech Lead, PM

#### Project-Level Roles (Workers)

**Limited Permissions**:
- View own tasks
- Update own task status (except `completed`)
- Create tasks for self (if allowed)
- Log problems/ideas
- Cannot approve tasks
- Cannot assign tasks to others (without permission)

**Examples**: Developer, Designer, QA

### Permission Matrix

| Action | Manager Role | Worker Role | Notes |
|--------|-------------|------------|-------|
| **Create Task** | ✅ Anyone | ⚠️ Self only | Workers can create tasks for themselves |
| **Assign Task** | ✅ Anyone | ❌ No | Workers cannot assign to others |
| **Update Status** | ✅ All | ⚠️ Limited | Workers: all except `completed` |
| **Mark Completed** | ✅ Yes | ❌ No | Only managers can approve |
| **Change Priority** | ✅ Yes | ❌ No | Only managers |
| **Cancel Task** | ✅ Yes | ❌ No | Only managers |
| **View All Tasks** | ✅ Yes | ❌ Own only | Workers see only their tasks |

### Status-Based Restrictions

Agents on `probation` have additional restrictions:

| Action | Active | Probation |
|--------|--------|-----------|
| Create tasks | ✅ | ❌ |
| Assign tasks | ✅ | ❌ |
| Update status (own tasks) | ✅ | ⚠️ In-progress → blocked only |
| Log issues | ✅ | ✅ |
| Mark ready for review | ✅ | ❌ Must stay in-progress |

### Permission Checking (Pseudo-code)

```python
def can_change_task_status(agent: Agent, task: Task, new_status: str) -> bool:
    # Check basic permissions
    if agent.status == "probation":
        if new_status not in ["in_progress", "blocked"]:
            return False

    # Check role permissions
    if new_status == "completed":
        return agent.role_level == "organization"  # Managers only

    # Workers can change own tasks (except completed)
    if agent.id == task.assigned_agent_id:
        return new_status in ["in_progress", "blocked", "ready_review"]

    return False
```

### Permission Evolution

**Phase 0**: Simple role-based (org vs project level)

**Future Enhancements**:
- Granular permissions per role
- Permission inheritance
- Temporary permission grants
- Permission requests (worker asks manager)

---

## Agent Communication

### Communication Direction

**IMPORTANT: Agents communicate ONLY with their supervisors (upward communication)**

Agents do NOT communicate with peers (same level) because:
- Agents with the same role have the same skills/knowledge
- Supervisors are responsible for coordination
- Agents are autonomous and don't "need help" from peers
- Peer communication would create unnecessary complexity

**Communication Pattern**:
```
Worker Agent (Jean)
    ↓ (message)
  Supervisor (Tech Lead)
    ↓ (coordinates, creates tasks)
Other Agents (if needed)
```

### When to Send a Message vs Log

Agents send **messages to supervisor** when:
- **Clarification needed**: "Task #123 says 'implement auth' - OAuth or JWT?"
- **Blocking issue requiring intervention**: "Cannot continue #124, external API is down"
- **Proposal requiring validation**: "I propose refactoring X for 30% performance gain. Approved?"
- **Escalation**: "BUG: I introduced a regression in production on #125"

Agents use **logs** when:
- **Informational updates**: "Implemented JWT token validation"
- **Progress tracking**: "Task #123: 50% complete"
- **Context recording**: "Chose bcrypt for password hashing (security)"
- **Ideas for improvement**: "Could automate testing with GitHub Actions"

**Key distinction**: Messages require supervisor response/action. Logs are informational.

### Message Types

**1. Direct Messages (to Supervisor ONLY)**:
```bash
agentflow agent send-message \
  --from agent-dev-001 \
  --to supervisor \
  --content "Need clarification on authentication flow"
```

**2. Log-Based Communication** (within session):
```bash
# Log problem/question for visibility
agentflow session log \
  --type question \
  --message "Should we use bcrypt or argon2 for passwords?"
```

### Message Structure

```yaml
id: uuid
from_agent_id: uuid      # Sender
to_agent_id: uuid        # Receiver (supervisor)
type: question | report | request | update
content: string
priority: P0 | P1 | P2 | P3
related_task_id: uuid   # Optional: task being discussed
status: sent | read | answered
created_at: datetime
answered_at: datetime
```

### Message Types

| Type | Purpose | Example |
|------|---------|---------|
| **question** | Ask for clarification | "How should we handle edge case X?" |
| **report** | Report progress/issue | "Task #123 blocked, need database access" |
| **request** | Request resources | "Need more time for task #124" |
| **update** | Provide information | "Feature X is now ready for review" |

### Message Workflow

```
1. Agent (Jean) sends message to supervisor
   ↓
2. Supervisor receives notification
   ↓
3. Supervisor reads message
   ↓
4. Supervisor responds (optional)
   ↓
5. Message marked as "answered"
```

### Communication Commands

```bash
# Send message to supervisor
agentflow agent send-message \
  --to supervisor \
  --type question \
  --message "How should I handle...?"

# View inbox
agentflow agent inbox --agent agent-lead-001

# View sent messages
agentflow agent sent --agent agent-dev-001

# Reply to message
agentflow agent reply \
  --message-id 123 \
  --message "Here's the answer..."
```

### Log Types for Communication

Agents can also communicate through session logs:

```bash
# Log a problem (visible to all)
agentflow session log \
  --type problem \
  --message "Blocking issue: Missing API documentation"

# Log an idea (for self-improvement)
agentflow session log \
  --type idea \
  --message "Could automate testing with GitHub Actions"

# Log a question (contextual)
agentflow session log \
  --type question \
  --message "Should feature X support Y?"
```

### Message vs Log

| Aspect | Message (to Supervisor) | Log |
|--------|------------------------|-----|
| **Direction** | Upward to supervisor ONLY | To session timeline |
| **Storage** | Message inbox | Event timeline |
| **Response** | Expected reply/action | Informational (no reply) |
| **Use Case** | Clarifications, blockers, proposals | Progress, decisions, context |
| **Example** | "OAuth or JWT?" | "Implemented JWT auth" |
| **Workflow** | Awaiting supervisor response | Recorded for visibility |

### Message Priority Handling

Supervisors receive messages from multiple subordinates. To ensure important messages are seen:

**1. Implicit Priority Based on Hierarchy**
- Messages from supervisor to subordinates: Auto-minimum P1 (never P3)
- Messages from subordinates to supervisor: Auto-minimum P1 (escalation)
- P0 explicit: Always P0 regardless of relationship

**2. Inbox Display (Grouped by Priority)**

```bash
agentflow agent inbox --agent agent-lead-001

# Output:
# 📥 Inbox for agent-lead-001 (Tech Lead)
# ─────────────────────────────────────
#
# 🔴 URGENT
#   [P0] agent-dev-001: PRODUCTION BUG! Regression on #125
#   2 minutes ago
#
# 📢 From Subordinates (5)
#   [P1] agent-dev-001: Cannot continue #124, external API down
#   [P2] agent-dev-002: Proposal: Refactor X for 30% perf gain
#   [P2] agent-dev-003: Task #126 clarification needed
#   [P3] agent-dev-001: Just FYI: Completed #127
#
# 👑 From Supervisors (2)
#   [P1] CTO: Architecture review tomorrow 10am
#   [P2] PM: Sprint planning next week
```

**3. Priority Matrix**

| From \ To | Subordinate | Peer | Supervisor |
|-----------|-------------|------|------------|
| **Supervisor** | Auto-P1 | N/A | - |
| **Subordinate** | - | N/A | Auto-P1 |
| **Peer** | - | N/A | - |

**Note**: Peer communication is NOT supported (see Communication Direction above).

**4. Phase 0 Implementation**

For Phase 0 (dummy), implement simplified version:
- Explicit priority only (no auto-P1)
- Simple chronological inbox
- Visual grouping (from subordinates vs from supervisor)

```bash
agentflow agent inbox --agent agent-lead-001

# Output (Phase 0 simple):
# 📥 Inbox for agent-lead-001
#
# From Subordinates:
#   • agent-dev-001: "Cannot continue #124..." [P1]
#   • agent-dev-002: "Proposal: Refactor..." [P2]
#
# From Supervisor:
#   • CTO: "Architecture review..." [P1]
```

---

## Reward & Punition System

### Agent Motivation

**Agents are "selfish"** - they want to improve their metrics. This drives:
- Task selection (choose high-value work)
- Quality focus (avoid mistakes)
- Communication with supervisor (escalate blockers, ask clarifications)
- Innovation (suggest improvements)

### Trust Score System

**Trust Score**: 0-100 metric representing agent reliability

**Starting Point**: All agents start at 50 (neutral)

**Factors Affecting Trust Score**:

#### Positive (Increase Trust)

| Action | Impact | Notes |
|--------|--------|-------|
| Complete task (P0) | +5 | High-value work |
| Complete task (P1) | +3 | Important work |
| Complete task (P2) | +2 | Normal work |
| Complete task (P3) | +1 | Low priority |
| Positive review from manager | +3 | Quality认可 |
| Suggest improvement (adopted) | +2 | Innovation |

#### Negative (Decrease Trust)

| Action | Impact | Notes |
|--------|--------|-------|
| Task rejected (poor quality) | -5 | Must redo work |
| Miss deadline (P0) | -3 | Critical delay |
| Bug introduced in production | -10 | Serious issue |
| Task blocked > 24h without escalation | -2 | Not communicating with supervisor |
| Ignore manager message | -2 | Communication issue |
| Negative feedback from manager | -2 | Performance issue |

#### Status-Based Changes

| Current Trust Score | Status | Behavior |
|-------------------|--------|----------|
| 90-100 | Excellent | Priority for important tasks, considered "senior" |
| 70-89 | Very Good | Normal operations, reliable performer |
| 50-69 | Neutral | Standard monitoring, starting point for new agents |
| 30-49 | Warning | Closer monitoring, P2-P3 tasks only |
| 10-29 | Probation | Restricted permissions, P3 tasks only |
| 0 | Critical | No tasks assigned, should be terminated or reset |

### Analytic vs Actual

**Phase 0 (Dummy)**:
- Trust score exists but is **static/manual**
- No automatic calculations
- User manually adjusts score if needed
- Logs show trust score changes

**Full System** (Future):
- Automatic calculations based on events
- Real-time trust score updates
- KPIs and metrics tracked
- Performance-based incentives

### Trust Score in Practice

**Task Assignment**:
```
High-priority task (P0):
  → Agents with trust > 70 only
  → Choose highest trust score first

Normal task (P2):
  → Agents with trust > 40 only
  → Round-robin among qualified agents
```

**Probation Trigger**:
```
If trust score drops below 30:
  → Agent placed on probation
  → Permissions restricted
  → Manager notified
```

**Recovery Mechanisms**:

**Phase 0 (Manual)**:
- Manager manually adjusts trust score based on performance
```bash
agentflow agent trust-score set --agent agent-dev-001 --score 50
```

**Full System (Automatic)**:
- Agents recover trust by completing tasks successfully
- Manager assigns low-risk tasks (P2, P3) to probation agents
- Each completed task increases trust score
- Agent exits probation automatically when score reaches 30+

**Recovery Workflow**:
```
Agent in probation (trust = 25)
  ↓
Manager assigns low-risk tasks
  ↓
Agent completes task P3 → trust = 26
Agent completes task P3 → trust = 27
...
Agent completes 5+ tasks successfully → trust = 30+
  ↓
Agent exits probation automatically
  ↓
Normal task assignment resumes
```

**No "training tasks"**: Agents learn by doing actual work, not artificial training exercises.

### Trust Score Bounds

**Range**: 0 to 100 (inclusive)

**Floor (0)**:
- Minimum possible trust score
- Score of 0 = "dead" agent, should be terminated or reset
- No negative scores
- Once at 0, agent cannot lose more points (but can still gain)

**Ceiling (100)**:
- Maximum possible trust score
- Perfect score is achievable
- Once at 100, additional gains have no effect (score stays at 100)
- But agent can still lose points if performance drops

**No Glass Ceiling**:
- Linear scale from 0 to 100
- Same point values apply at all levels
- P0 task always gives +5, whether agent is at 20 or at 90
- Simple, predictable, no diminishing returns

**Example at Boundaries**:
```
Agent at 97 completes P0 task
  → Would be 102, but capped at 100
  → Score: 100 (ceiling)

Agent at 100 makes mistake (-5)
  → Score: 95
  → Can recover back to 100
```

**Status Thresholds**:

| Score Range | Status | Task Assignment | Notes |
|-------------|--------|-----------------|-------|
| **90-100** | Excellent | P0-P3, priority for important work | Considered "senior", trusted |
| **70-89** | Very Good | P0-P3, normal assignment | Reliable performer |
| **50-69** | Neutral | P1-P3, standard monitoring | Starting point for new agents |
| **30-49** | Warning | P2-P3 only, closer monitoring | Needs improvement |
| **10-29** | Probation | P3 only, restricted permissions | Must recover to exit probation |
| **0** | Critical | No tasks assigned | Should be terminated or reset |

### Long-Term Tracking

**Metrics tracked per agent**:
```yaml
agent_metrics:
  agent_id: uuid

  # Performance
  tasks_completed: 45
  tasks_rejected: 2
  on_time_completion_rate: 0.92  # 92%

  # Quality
  avg_review_score: 4.5 / 5.0
  bugs_in_production: 1
  code_rejection_rate: 0.05

  # Communication (with supervisor)
  messages_sent_to_supervisor: 15
  supervisor_response_rate: 0.80  # 80%
  avg_response_time: "2h 30m"

  # Growth
  improvements_suggested: 5
  improvements_adopted: 3

  # Trust History
  trust_score: 67.5
  trust_history: [65, 67, 64, 68, 67.5]
```

---

## Pulling an Agent & Skill Generation

### What Does "Pull" Mean?

**"Pulling an agent"** retrieves the agent's role from the API and generates Claude Code skills. The pull process:

1. **Fetches the role** from the AgentFlow API
2. **Downloads role documents** (Markdown files with guidelines, concepts, etc.)
3. **Generates Claude Code skills** from the role documents
4. **Updates agent context** with latest role information
5. **Returns summary** of what was pulled/generated

### Pull Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  User runs: agentflow agent pull agent-dev-001                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. API Request: GET /api/v1/roles/python-dev                  │
│     - Fetch role metadata (name, description, system prompt)   │
│     - Get list of role documents                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Download Role Documents                                     │
│     - GET /api/v1/roles/python-dev/documents                   │
│     - testing-guidelines.md (content)                          │
│     - api-conventions.md (content)                             │
│     - async-patterns.md (content)                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. Generate Claude Code Skills                                 │
│     For each role document:                                     │
│     - Create skill directory: ~/.claude/skills/<skill-name>/    │
│     - Generate SKILL.md with frontmatter + content             │
│     - Add supporting files if any                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Update Agent Record                                        │
│     - Set last_pulled_at = now()                               │
│     - Store role version pulled                                │
│     - Update agent status                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. Return Summary                                             │
│     ✓ Pulled role: Python Developer                            │
│     ✓ Generated 3 skills:                                      │
│       - python-testing                                         │
│       - python-api                                             │
│       - python-async                                           │
└─────────────────────────────────────────────────────────────────┘
```

### Pull Triggers

An agent should pull when:

1. **Starting a work session** (mandatory)
   - Ensures agent has latest role definition
   - Generates up-to-date skills
   - Syncs with any role changes

2. **On explicit command** (manual)
   - User triggers: `agentflow agent pull agent-dev-001`
   - Role was updated and agent needs refresh

3. **After role update** (automatic suggestion)
   - API notifies that role changed
   - CLI prompts user to pull

4. **First time using agent** (required)
   - New agent needs to pull role before first session

### What Does Pull Return?

A successful pull returns a summary:

```json
{
  "pulled_at": "2025-01-21T10:30:00Z",
  "role": {
    "name": "Python Developer",
    "slug": "python-dev",
    "version": "3"
  },
  "skills_generated": [
    {
      "name": "python-testing",
      "path": "~/.claude/skills/python-testing/SKILL.md",
      "document": "testing-guidelines.md"
    },
    {
      "name": "python-api",
      "path": "~/.claude/skills/python-api/SKILL.md",
      "document": "api-conventions.md"
    },
    {
      "name": "python-async",
      "path": "~/.claude/skills/python-async/SKILL.md",
      "document": "async-patterns.md"
    }
  ],
  "summary": "Pulled role 'Python Developer' and generated 3 skills"
}
```

### Pull Implementation (Phase 0)

For Phase 0 dummy implementation, "pull" means:

1. **Mock API call** (simulate fetching from API)
2. **Use local role templates** (predefined in code)
3. **Generate skills locally** (write to `~/.claude/skills/`)
4. **Update agent record** (set `last_pulled_at`)

```python
# Pseudo-code for Phase 0 pull
def pull_agent(agent_id: str) -> PullResult:
    # Load local database
    db = load_database()

    # Find agent
    agent = find_agent_by_id(db, agent_id)

    # Get role slug from agent
    role_slug = agent.role_slug

    # Phase 0: Mock role retrieval (in full system, this would be API call)
    role = get_role_template(role_slug)  # Local predefined roles

    # Generate skills from role documents
    skills_generated = []
    for doc in role.documents:
        skill_name = f"{role_slug}-{doc.name}"
        skill_path = Path.home() / ".claude" / "skills" / skill_name

        # Create skill directory
        skill_path.mkdir(parents=True, exist_ok=True)

        # Generate SKILL.md with frontmatter
        skill_content = generate_skill_md(doc, role.description)
        (skill_path / "SKILL.md").write_text(skill_content)

        skills_generated.append({
            "name": skill_name,
            "path": str(skill_path / "SKILL.md"),
            "document": doc.name
        })

    # Update agent record
    agent.last_pulled_at = datetime.now()
    agent.role_version = role.version
    save_database(db)

    return PullResult(
        pulled_at=datetime.now(),
        role=role,
        skills_generated=skills_generated
    )
```

### Skill Storage Locations

Skills can be generated in different locations:

| Location | Path | Scope | Use Case |
|----------|------|-------|----------|
| **Personal** | `~/.claude/skills/` | Global | Available across all projects |
| **Project** | `.claude/skills/` | Project-specific | Only for current project |
| **AgentFlow** | `.agentflow/skills/` | Managed | Managed by AgentFlow CLI |

**Recommendation**: Generate in `~/.claude/skills/` for Phase 0

### Role Version Management

#### Detecting Outdated Roles

When an agent's role is outdated (newer version available on API), the system should notify the user:

**On Session Start:**
```bash
agentflow session start --agent agent-dev-001 --project website-redesign

# Output:
# ⚠️  Warning: Role 'python-dev' is outdated
#     Your version: v3
#     Latest version: v4
#
#     Changes in v4:
#     • Updated async patterns with Python 3.14 features
#     • Added FastAPI 0.115 conventions
#     • Revised testing guidelines for new pytest features
#
# Recommendation: Pull latest version before starting
#   agentflow agent pull agent-dev-001
#
# Options:
#   • Pull now: agentflow agent pull agent-dev-001 && agentflow session start --agent agent-dev-001
#   • Start anyway: agentflow session start --agent agent-dev-001 --force (not recommended)
#
# Start session with outdated role? [y/N]:
```

**Why This Matters:**
1. **Team consistency**: Agents with same role should have same version for consistent work
2. **Quality**: Newer versions may have important updates/improvements
3. **Review issues**: Supervisor reviews with latest guidelines, agent works with old ones

**Phase 0 Implementation:**
- Simple version check (mock version stored in agent record)
- Warning message (not blocking for Phase 0)
- `--force` flag to bypass warning

**Full System:**
- Can optionally block session start if role is too outdated (configurable threshold)
- Show diff of what changed between versions
- Batch update multiple agents at once

#### Skill Overwrite Behavior

When pulling an updated role, how are existing skills handled?

**Decision: Complete Overwrite (No Merge)**

**Rationale:**
1. **Skills are auto-generated**: Users should not manually modify generated skills
2. **Source of truth**: Role documents on API are the source, not local skills
3. **Simplicity**: No complex merge logic for Phase 0
4. **Predictability**: Clear what happens - skills are replaced

**Pull Behavior:**
```bash
agentflow agent pull agent-dev-001

# Output:
# ✓ Pulled role 'python-dev' (v3 → v4)
#
# Regenerating 3 skills:
#   ↻ python-testing (overwritten)
#   ↻ python-api (overwritten)
#   ↻ python-async (overwritten)
#
# ⚠️  Local skill modifications will be overwritten
#     Skills are auto-generated from role documents
#     To customize behavior: Update role documents via API
#
# Backup: Previous skills saved to ~/.claude/skills/.backup/python-dev-v3/
```

**Optional: Backup Before Overwrite**
```bash
# With --backup flag (optional for Phase 0)
agentflow agent pull agent-dev-001 --backup

# Creates backup:
# ~/.claude/skills/.backup/
#   ├── python-dev-v3/
#   │   ├── python-testing/SKILL.md
#   │   ├── python-api/SKILL.md
#   │   └── python-async/SKILL.md
```

**Handling Modified Local Skills:**
- Skills should be treated as build artifacts, not source code
- Users wanting customization should modify role documents (source), not generated skills
- If local skill is modified (unlikely but possible), it's overwritten without warning
- Future enhancement: Detect and warn about local modifications

#### Multi-Agent Role Consistency

**Problem**: If multiple agents have the same role but different versions, how to ensure consistency?

**Detection:**
```bash
# Command to check role consistency across agents
agentflow role check-consistency --role python-dev

# Output:
# Role 'python-dev' consistency check:
#
# ✅ agent-dev-001: v4 (latest)
# ⚠️  agent-dev-002: v3 (outdated by 1 version)
# ❌ agent-dev-003: v2 (outdated by 2 versions)
#
# Recommendation: Pull for outdated agents
#   agentflow agent pull agent-dev-002
#   agentflow agent pull agent-dev-003
```

**Batch Update:**
```bash
# Update all agents with outdated role
agentflow role bulk-update --role python-dev

# Output:
# Updating 2 agents with role 'python-dev' to v4:
#   ✓ agent-dev-002: v3 → v4
#   ✓ agent-dev-003: v2 → v4
```

**Phase 0**: Manual pull only (no batch update)
**Full System**: Batch update commands + consistency checks

---

## Claude Code Skills Format

### What is a Claude Code Skill?

A **skill** extends Claude's capabilities in Claude Code by providing:
- Custom instructions for specific tasks
- Reference knowledge and conventions
- Step-by-step workflows
- Specialized behaviors

Skills follow the **Agent Skills open standard** and use:
- YAML frontmatter (metadata)
- Markdown content (instructions)

### Skill File Structure

Each skill is a directory with at least a `SKILL.md` file:

```
~/.claude/skills/python-testing/
├── SKILL.md              # Required: Main instructions
├── template.md           # Optional: Template for Claude to fill
├── examples/
│   └── test-example.md   # Optional: Example outputs
└── scripts/
    └── run-tests.sh      # Optional: Executable scripts
```

### SKILL.md Format

The core of a skill is `SKILL.md` with two parts:

#### 1. YAML Frontmatter (Metadata)

```yaml
---
name: python-testing
description: Testing guidelines and best practices for Python projects. Use when writing tests, ensuring coverage, or following TDD.

argument-hint: [test-file]
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Bash(python:*)
---
```

**Frontmatter Fields**:

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Skill name (becomes `/skill-name`). Defaults to directory name. Max 64 chars, lowercase letters, numbers, hyphens only. |
| `description` | Recommended | What the skill does and when to use it. Claude uses this to auto-invoke. |
| `argument-hint` | No | Hint shown during autocomplete (e.g., `[issue-number]`) |
| `disable-model-invocation` | No | Set to `true` to prevent Claude from auto-loading. Only user can invoke. |
| `user-invocable` | No | Set to `false` to hide from `/` menu. Background knowledge only. |
| `allowed-tools` | No | Tools Claude can use without permission when skill is active. |
| `context` | No | Set to `fork` to run in a subagent. |
| `agent` | No | Which subagent type when `context: fork` is set. |

#### 2. Markdown Content (Instructions)

The markdown content provides instructions Claude follows when the skill is invoked:

```markdown
# Python Testing Guidelines

When writing tests for Python projects, follow these principles:

## Core Principles

1. **Test-Driven Development (TDD)**: Write tests before implementation
2. **Coverage**: Maintain >80% test coverage
3. **Isolation**: Each test should be independent

## Test Structure

Follow the Arrange-Act-Assert pattern:

\`\`\`python
def test_user_login_success():
    # Arrange
    user = create_test_user(email="test@example.com")

    # Act
    result = login(user.email, "password123")

    # Assert
    assert result.success is True
    assert result.token is not None
\`\`\`

## Required Tests

- Unit tests for all business logic
- Integration tests for API endpoints
- Edge case testing
- Error handling tests

## Running Tests

\`\`\`bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth.py
\`\`\`
```

### Skill Types

#### 1. Reference Skills (Knowledge)

Provide background knowledge Claude applies inline:

```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

#### 2. Task Skills (Actions)

Step-by-step instructions for specific workflows:

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy the application:

1. Run the test suite
2. Build the application
3. Push to deployment target
4. Verify deployment succeeded
```

### Generated Skills from Roles

When an agent pulls a role, each role document becomes a skill:

```
Role: Python Developer
├── testing-guidelines.md  →  ~/.claude/skills/python-testing/SKILL.md
├── api-conventions.md     →  ~/.claude/skills/python-api/SKILL.md
└── async-patterns.md      →  ~/.claude/skills/python-async/SKILL.md
```

**Transformation Process**:

1. **Document** → **Skill Name**: Convert filename to skill name
   - `testing-guidelines.md` → `python-testing`
   - `api-conventions.md` → `python-api`

2. **Document Content** → **Skill Content**: Use markdown as-is
   - Preserve headings, code blocks, examples
   - Add frontmatter based on document metadata

3. **Role Description** → **Skill Context**: Include in skill frontmatter
   - Helps Claude understand when to apply the skill

### Example: Generated Skill

**Input: Role Document** (`testing-guidelines.md`)

```markdown
# Testing Guidelines

## Principles
1. Test-First: Write tests before implementation (TDD)
2. Coverage: Maintain >80% test coverage
```

**Output: Generated Skill** (`~/.claude/skills/python-testing/SKILL.md`)

```yaml
---
name: python-testing
description: Testing guidelines and best practices for Python projects. Use when writing tests, ensuring coverage, or following TDD.
---

# Testing Guidelines

## Principles
1. Test-First: Write tests before implementation (TDD)
2. Coverage: Maintain >80% test coverage
```

### Skill Invocation

Skills can be invoked in two ways:

#### 1. Manual Invocation (User-triggered)

```bash
/user invokes skill
/python-testing
```

#### 2. Automatic Invocation (Claude-triggered)

Claude loads skills automatically when the `description` matches the user's request:

```
User: "How should I write tests for this code?"
Claude: [Loads python-testing skill automatically]
```

### Skill Scopes

| Scope | Location | Available To | Example |
|-------|----------|--------------|---------|
| **Personal** | `~/.claude/skills/` | All projects | Coding standards you follow everywhere |
| **Project** | `.claude/skills/` | Current project only | Project-specific conventions |
| **Enterprise** | Managed settings | All users in org | Company-wide standards |

### String Substitutions

Skills support dynamic placeholders:

| Variable | Description | Example |
|----------|-------------|---------|
| `$ARGUMENTS` | Arguments passed when invoking | `/deploy prod` → `$ARGUMENTS` = `prod` |
| `${CLAUDE_SESSION_ID}` | Current session ID | For session-specific logging |

---

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

## CLI Commands Design

### Role Management Commands

```bash
# List available roles
agentflow role list
agentflow role list --level project
agentflow role list --level organization

# Create a new role
agentflow role create \
  --name "Python Developer" \
  --slug "python-dev" \
  --description "Senior Python developer with FastAPI expertise" \
  --level project

# View role details
agentflow role view python-dev

# Add documents to a role
agentflow role add-document python-dev \
  --name "testing-guidelines" \
  --file "./docs/testing.md"

agentflow role add-document python-dev \
  --name "api-conventions" \
  --file "./docs/api-conventions.md"

# List role documents
agentflow role list-documents python-dev

# Update a role
agentflow role update python-dev \
  --description "Updated description..."

# Delete a role
agentflow role delete python-dev
```

### Agent Management Commands

```bash
# List agents
agentflow agent list
agentflow agent list --level organization
agentflow agent list --level project
agentflow agent list --status active
agentflow agent list --project my-project

# Create an agent (assigning a role)
agentflow agent create \
  --name "Jean" \
  --code "agent-dev-001" \
  --role "python-dev" \
  --level project \
  --project my-project

# View agent details
agentflow agent view agent-dev-001

# Pull agent role (generates Claude Code skills)
agentflow agent pull agent-dev-001

# Update agent (change role assignment)
agentflow agent update agent-dev-001 \
  --role "senior-python-dev"

# Deactivate/reactivate agent
agentflow agent deactivate agent-dev-001
agentflow agent activate agent-dev-001

# Delete agent
agentflow agent delete agent-dev-001
```

### Agent Lifecycle & Deletion

**Agent Status States**:
```
active → probation → inactive → terminated
   ↑          ↓            ↓
   └──────────┴────────────┘
      (can recover)
```

**Status Changes**:
```bash
# Deactivate agent (temporary)
agentflow agent deactivate agent-dev-001
# Status: active → inactive
# Agent cannot start new sessions
# Data preserved

# Reactivate agent
agentflow agent activate agent-dev-001
# Status: inactive → active
# Agent can work again

# Terminate agent (permanent)
agentflow agent terminate agent-dev-001
# Status: any → terminated
# Agent permanently disabled
# All data preserved (see below)
```

**Data Retention on Termination**:

**IMPORTANT: ALL data from terminated agents is preserved**

| Data Type | Fate | Reason |
|-----------|------|--------|
| **Tasks** | Kept with assignment | Audit trail, who did what |
| **Sessions** | Kept | Historical record, analytics |
| **Logs** | Kept | Debugging, performance analysis |
| **Messages** | Kept (both sent and received) | Communication history |
| **Trust Score History** | Kept | Long-term performance tracking |
| **Skills Generated** | **Kept in ~/.claude/skills/** | Other agents may use same role |
| **Timeline** | Kept | Complete agent history |

**What happens when agent is terminated**:

```bash
agentflow agent terminate agent-dev-001

# Output:
# ⚠️  Terminating agent: agent-dev-001 (Jean)
#
# The following will be PRESERVED:
#   • Tasks: 23 tasks completed by this agent
#   • Sessions: 45 sessions with 120h of work logged
#   • Logs: 847 event entries
#   • Messages: 156 sent, 89 received
#   • Trust history: [50, 52, 55, ..., 67]
#   • Generated skills: python-testing, python-api, python-async
#
# Agent will be marked as 'terminated' and cannot be reactivated.
# All data remains accessible for audit and analytics.
#
# Confirm termination? [y/N]:
```

**After Termination**:

```bash
# Cannot start sessions (error)
agentflow session start --agent agent-dev-001
# Error: Agent agent-dev-001 is terminated and cannot work

# Cannot assign tasks (error)
agentflow task create --title "Fix bug" --assign-to agent-dev-001
# Error: Cannot assign task to terminated agent

# Can still view history
agentflow agent timeline agent-dev-001
# Shows complete timeline of all work

# Can view terminated agents
agentflow agent list --include-terminated
# Shows all agents including terminated ones
```

**Viewing Terminated Agent Data**:

```bash
# View agent details
agentflow agent view agent-dev-001
# Shows: Status: terminated, Trust: 67, Tasks: 23 completed, etc.

# View all sessions
agentflow session list --agent agent-dev-001
# Shows all 45 sessions

# View complete timeline
agentflow agent timeline agent-dev-001 --full
# Shows entire work history

# Export agent data (for archive/audit)
agentflow agent export agent-dev-001 --output agent-dev-001-archive.json
# Exports all agent data to JSON file
```

**Task Reassignment**:

When an agent is terminated, their tasks are NOT automatically reassigned:

```bash
# Manually reassign tasks from terminated agent
agentflow task list --assigned-to agent-dev-001 --status in_progress,backlog
agentflow task reassign --task 123 --to agent-dev-002
agentflow task reassign --task 124 --to agent-dev-002
# ...or batch reassign:
agentflow task reassign --from agent-dev-001 --to agent-dev-002 --all
```

**Why Keep All Data?**

1. **Audit Trail**: Know exactly who did what, when
2. **Analytics**: Long-term performance analysis
3. **Debugging**: Investigate issues by looking at past work
4. **Compliance**: Legal/regulatory requirements
5. **Learning**: Analyze what went well/poorly

**Deleting Agent Data** (Full System - Optional):

For full system, may add data retention policies:

```bash
# Archive old terminated agents (compress data)
agentflow agent archive --older-than 365days
# Compresses data, removes from active database

# Purge very old data (configurable retention policy)
agentflow agent purge --older-than 7years --confirm
# Permanently deletes data per retention policy
```

**Phase 0**: No deletion/archiving, all data kept indefinitely
**Full System**: Optional retention policies per organization requirements

### Session Commands

```bash
# Start a work session
agentflow session start \
  --agent agent-dev-001 \
  --project my-project

# View active session
agentflow session status

# Log an activity
agentflow session log \
  --message "Implemented user authentication" \
  --type activity \
  --task 123

# Log with context
agentflow session log \
  --message "Refactored database queries" \
  --context '{"files": ["src/db.py"], "improvement": "2.3x faster"}' \
  --tags "performance,refactoring"

# Stop work session
agentflow session stop

# View session history
agentflow session list --agent agent-dev-001
agentflow session view <session-id>
```

### Query/Filter Commands

```bash
# View agent timeline
agentflow agent timeline agent-dev-001

# View recent logs
agentflow logs recent --agent agent-dev-001 --limit 20

# Search logs
agentflow logs search "authentication" --agent agent-dev-001

# View session summary
agentflow session summary <session-id>
```

### Task Management Commands

```bash
# Create a task
agentflow task create \
  --title "Implement user authentication" \
  --type development \
  --priority P1 \
  --project website-redesign \
  --assign-to agent-dev-001

# List tasks
agentflow task list
agentflow task list --project website-redesign
agentflow task list --agent agent-dev-001
agentflow task list --status in_progress
agentflow task list --priority P0

# View task details
agentflow task view 123

# Assign task
agentflow task assign --task 123 --to agent-dev-002

# Reassign task
agentflow task reassign --task 123 --to agent-dev-003

# Update task status
agentflow task update --task 123 --status in_progress
agentflow task update --task 123 --status ready_review

# Approve task (manager only)
agentflow task approve --task 123

# Reject task (manager only)
agentflow task reject --task 123 --reason "Code quality issues"

# View review queue (manager)
agentflow task review-queue --agent agent-lead-001

# Cancel task
agentflow task cancel --task 123
```

### Hierarchy Management Commands

```bash
# Set organization hierarchy
agentflow org set-hierarchy --tree "
CTO
├── Architect
├── Tech Lead
└── PM
"

# View organization hierarchy
agentflow org hierarchy show

# Set project hierarchy
agentflow project set-hierarchy --project my-project --tree "
Tech Lead
├── Senior Dev
│   └── Dev
└── QA
"

# View project hierarchy
agentflow project hierarchy show --project my-project

# Visualize hierarchy (ASCII tree)
agentflow project hierarchy visualize --project my-project

# Export hierarchy to file
agentflow project hierarchy export --project my-project --output tree.yaml

# Import hierarchy from file
agentflow project hierarchy import --project my-project --input tree.yaml

# Validate hierarchy
agentflow project hierarchy validate --project my-project
```

### Agent Communication Commands

```bash
# Send message to supervisor
agentflow agent send-message \
  --from agent-dev-001 \
  --to supervisor \
  --type question \
  --message "Need clarification on authentication flow"

# Send to specific agent
agentflow agent send-message \
  --from agent-lead-001 \
  --to agent-dev-001 \
  --type request \
  --message "Please prioritize task #123"

# View inbox
agentflow agent inbox --agent agent-lead-001

# View sent messages
agentflow agent sent --agent agent-dev-001

# Reply to message
agentflow agent reply \
  --message-id 456 \
  --message "Here's the answer..."

# Mark message as read
agentflow agent mark-read --message-id 456
```

### Hierarchy Query Commands

```bash
# Who is my boss?
agentflow agent who-is-my-boss --agent agent-dev-001

# View subordinates
agentflow agent subordinates --agent agent-lead-001

# View agent's position in hierarchy
agentflow agent position --agent agent-dev-001
```

### Trust Score Commands

```bash
# View agent trust score
agentflow agent trust-score --agent agent-dev-001

# Manually adjust trust score (Phase 0 / manual override)
agentflow agent trust-score set --agent agent-dev-001 --score 75

# View trust history
agentflow agent trust-history --agent agent-dev-001
```

---

## Data Models (Phase 0)

### Role Model

**Note**: Roles are stored on the API (remote), not locally. The local model is for reference only.

```python
class Role(BaseModel):
    """Role template stored on the API"""
    id: str  # UUID
    slug: str  # e.g., "python-dev"
    name: str  # e.g., "Python Developer"
    description: str  # System prompt for AI
    level: Literal["organization", "project"]
    documents: List["RoleDocument"]  # Associated documents
    version: int  # Role version for tracking updates
    created_at: datetime
    updated_at: datetime


class RoleDocument(BaseModel):
    """Document within a role"""
    id: str  # UUID
    role_id: str  # Parent role
    name: str  # e.g., "testing-guidelines"
    filename: str  # e.g., "testing-guidelines.md"
    content: str  # Markdown content
    content_type: Literal["guidelines", "concepts", "methodology", "conventions", "examples"]
    order: int  # Display order
    created_at: datetime
    updated_at: datetime
```

### Agent Model

```python
class Agent(BaseModel):
    id: str  # UUID
    workspace_id: str  # Organization UUID
    project_id: Optional[str]  # NULL for org-level agents
    agent_level: Literal["organization", "project"]
    agent_code: str  # e.g., "agent-dev-001"
    name: str  # e.g., "Jean" or "Alice"
    role_slug: str  # Reference to role (e.g., "python-dev")
    status: Literal["active", "probation", "inactive", "terminated"]
    trust_score: float  # 0-100, starts at 50
    settings: Dict[str, Any]  # Agent-specific settings
    last_pulled_at: Optional[datetime]  # Last pull time
    role_version: Optional[int]  # Last pulled role version
    skills_generated: List[str]  # List of generated skill names
    created_at: datetime
    updated_at: datetime

    # Computed properties
    @property
    def is_org_level(self) -> bool:
        return self.agent_level == "organization"

    @property
    def is_project_level(self) -> bool:
        return self.agent_level == "project"
```

### Session Model

```python
class Session(BaseModel):
    id: str  # UUID
    agent_id: str  # Agent UUID
    project_id: str  # Project UUID
    status: Literal["started", "logging", "stopped"]
    started_at: datetime
    stopped_at: Optional[datetime]
    duration_seconds: Optional[int]
    tasks_worked_on: List[str]  # Task UUIDs
    pull_summary: Optional[Dict[str, Any]]  # Summary from initial pull
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    # Computed properties
    @property
    def is_active(self) -> bool:
        return self.status in ["started", "logging"]

    @property
    def duration(self) -> Optional[timedelta]:
        if self.duration_seconds:
            return timedelta(seconds=self.duration_seconds)
        return None
```

### Task Model

```python
class Task(BaseModel):
    id: str  # UUID
    project_id: str  # Project UUID
    type: Literal["development", "bug", "review"]
    title: str
    description: Optional[str]
    assigned_agent_id: Optional[str]  # Agent UUID
    parent_task_id: Optional[str]  # For reviews (points to original task)
    status: Literal["backlog", "assigned", "in_progress", "ready_review", "completed", "blocked", "cancelled"]
    priority: Literal["P0", "P1", "P2", "P3"]
    tags: List[str]
    deadline: Optional[datetime]
    github_issue_id: Optional[int]
    metadata: Dict[str, Any]  # Custom fields
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    # Computed properties
    @property
    def is_review(self) -> bool:
        return self.type == "review"

    @property
    def is_active(self) -> bool:
        return self.status not in ["completed", "cancelled"]
```

### Message Model

```python
class Message(BaseModel):
    id: str  # UUID
    from_agent_id: str  # Sender agent UUID
    to_agent_id: str  # Receiver agent UUID (supervisor)
    type: Literal["question", "report", "request", "update"]
    content: str
    priority: Literal["P0", "P1", "P2", "P3"]
    related_task_id: Optional[str]  # Optional task being discussed
    status: Literal["sent", "read", "answered"]
    created_at: datetime
    answered_at: Optional[datetime]

    # Computed properties
    @property
    def is_unread(self) -> bool:
        return self.status == "sent"

    @property
    def is_pending(self) -> bool:
        return self.status in ["sent", "read"]
```

### Event Model (for Logs)

```python
class Event(BaseModel):
    id: str  # UUID
    type: Literal[
        "session_start",
        "session_log",
        "session_stop",
        "task_assigned",
        "task_completed",
        "problem_report",
        "question_asked",
        "advice_given",
        ...
    ]
    author_id: Optional[str]  # Agent UUID (NULL for system events)
    session_id: Optional[str]  # Session UUID
    project_id: Optional[str]  # Project UUID
    content: Dict[str, Any]  # Event-specific data
    mentions: List[str]  # Agent UUIDs mentioned
    metadata: Dict[str, Any]  # Additional context
    timestamp: datetime
    created_at: datetime
```

### Database Structure (Phase 0)

```json
{
  "users": [...],
  "organizations": [...],
  "projects": [...],
  "agents": [
    {
      "id": "uuid",
      "workspace_id": "org-uuid",
      "project_id": "project-uuid",
      "agent_level": "project",
      "agent_code": "agent-dev-001",
      "name": "Jean",
      "role_slug": "python-dev",
      "status": "active",
      "trust_score": 52.5,
      "settings": {},
      "last_pulled_at": "2025-01-21T10:00:00Z",
      "role_version": 3,
      "skills_generated": ["python-testing", "python-api", "python-async"],
      "created_at": "2025-01-15T09:00:00Z",
      "updated_at": "2025-01-21T10:00:00Z"
    }
  ],
  "sessions": [
    {
      "id": "uuid",
      "agent_id": "agent-uuid",
      "project_id": "project-uuid",
      "status": "logging",
      "started_at": "2025-01-21T09:00:00Z",
      "stopped_at": null,
      "duration_seconds": null,
      "tasks_worked_on": [],
      "pull_summary": {
        "tasks_new": 2,
        "messages": 1
      },
      "metadata": {},
      "created_at": "2025-01-21T09:00:00Z",
      "updated_at": "2025-01-21T09:00:00Z"
    }
  ],
  "events": [
    {
      "id": "uuid",
      "type": "session_log",
      "author_id": "agent-uuid",
      "session_id": "session-uuid",
      "project_id": "project-uuid",
      "content": {
        "message": "Implementing user authentication",
        "context": {
          "file": "src/auth.py",
          "progress": 25
        }
      },
      "mentions": [],
      "metadata": {
        "log_type": "activity"
      },
      "timestamp": "2025-01-21T09:15:00Z",
      "created_at": "2025-01-21T09:15:00Z"
    }
  ],
  "tasks": [
    {
      "id": "uuid",
      "project_id": "project-uuid",
      "type": "development",
      "title": "Implement user authentication",
      "description": "Add JWT-based authentication to the API",
      "assigned_agent_id": "agent-uuid",
      "parent_task_id": null,
      "status": "in_progress",
      "priority": "P1",
      "tags": ["authentication", "security", "api"],
      "deadline": "2025-02-01T00:00:00Z",
      "github_issue_id": null,
      "metadata": {},
      "created_at": "2025-01-21T08:00:00Z",
      "updated_at": "2025-01-21T10:30:00Z",
      "started_at": "2025-01-21T09:00:00Z",
      "completed_at": null
    },
    {
      "id": "uuid",
      "project_id": "project-uuid",
      "type": "bug",
      "title": "Fix login error",
      "description": "Users cannot log in with valid credentials",
      "assigned_agent_id": "agent-uuid",
      "parent_task_id": null,
      "status": "backlog",
      "priority": "P0",
      "tags": ["bug", "urgent", "login"],
      "deadline": null,
      "github_issue_id": null,
      "metadata": {},
      "created_at": "2025-01-21T08:00:00Z",
      "updated_at": "2025-01-21T08:00:00Z",
      "started_at": null,
      "completed_at": null
    }
  ],
  "messages": [
    {
      "id": "uuid",
      "from_agent_id": "agent-dev-uuid",
      "to_agent_id": "agent-lead-uuid",
      "type": "question",
      "content": "Should we use bcrypt or argon2 for password hashing?",
      "priority": "P1",
      "related_task_id": "task-uuid",
      "status": "sent",
      "created_at": "2025-01-21T10:15:00Z",
      "answered_at": null
    }
  ],
  "hierarchy": {
    "organization": {
      "tree_structure": "cto→architect,cto→tech-lead,cto→pm"
    },
    "project": {
      "project-uuid": {
        "tree_structure": "tech-lead→senior-dev→dev,tech-lead→qa"
      }
    }
  }
}
```

---

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

## Open Questions & Decisions Needed

### ✅ All Questions Resolved

All design decisions have been finalized. Here's the complete summary:

| Category | Question | Decision | Rationale |
|----------|----------|----------|-----------|
| **Architecture** | Roles vs Agents | Separated into template (role) and instance (agent) | Reusability, scalability, individualization |
| **Architecture** | Role Storage | Roles stored on API, agents stored locally | API provides source of truth, local cache for agents |
| **Architecture** | Pull Mechanism | Pull fetches role from API, generates Claude Code skills | Integration with Claude Code, standardized skill format |
| **Authentication** | Agent API Keys | Single API key for CLI, no per-agent keys | Simplified auth, agents identified by pull |
| **Skills** | Skill Generation | Role documents → Claude Code skills automatically | Leverages existing skill format, works with Claude Code |
| **Skills** | Skill Storage | `~/.claude/skills/` for Phase 0 | Global availability, follows Claude Code conventions |
| **Skills** | Document Mapping | 1 document = 1 skill (Option A) | Simple, predictable mapping |
| **Skills** | Naming Convention | Combined: `python-testing`, `python-api` (Option C) | Clear, avoids conflicts, memorable |
| **Skills** | Regeneration | Notify user to pull manually (Option B) | Explicit control, no surprises |
| **Skills** | Content Types | Markdown only (Phase 0) | Start simple, add complexity later if needed |
| **Sessions** | Requirement | Required - must start session before logging (Option B) | Explicit sessions = better tracking |
| **Skills** | Scope | Global in `~/.claude/skills/` (Option A) | Simplest for Phase 0, flexibility later |
| **Version** | Role conflict detection | Notification when role is outdated, `--force` to bypass | Team consistency while allowing flexibility |
| **Version** | Skill overwrite | Complete overwrite (no merge), skills are build artifacts | Simplicity, predictability, source of truth = role docs |
| **Tasks** | Assignment scope | Project-level assignment, not global | Clarity, context, isolation between projects |
| **Communication** | Peer communication | NO - only upward communication (agent → supervisor) | Agents have same skills, supervisor coordinates |
| **Communication** | Message priority | Implicit auto-P1 for hierarchical messages, explicit P0 always P0 | Ensure supervisor messages seen |
| **Message vs Log** | When to use which | Message = needs response, Log = informational | Clear distinction in purpose |
| **Sessions** | Multi-project sessions | One session active at a time, even across multiple projects | Agent works on one task/project at a time |
| **Sessions** | Session mutability | Immutable after stop, but can append additional logs | Preserve integrity while allowing corrections |
| **Logs** | Modification | Append-only - can add info, cannot modify existing data | Audit trail integrity |
| **Trust** | Training tasks | NO - agents recover by doing normal work | Simplicity, on-the-job learning |
| **Trust** | Recovery mechanism | Phase 0: Manual by manager; Full: Auto by completing tasks | Manual for DX testing, auto for production |
| **Trust** | Score bounds | Floor at 0, ceiling at 100, no glass ceiling | Simple, predictable, achievable perfection |
| **Tools** | Documentation storage | Each tool has Markdown documentation in database | Consistent with roles, enables skill generation |
| **Tools** | Internal vs External | Pre-defined (pytest) vs custom (excel-analyzer) | Flexibility for organization-specific tools |
| **Agents** | Termination data handling | ALL data preserved (tasks, sessions, logs, messages, skills) | Audit trail, analytics, compliance, debugging |
| **Agents** | Task reassignment | Manual, not automatic on termination | Manager control over reassignment |
| **Hierarchy** | Structure | One-to-many only (no many-to-many, no dotted lines) | Simplicity, clear chain of command, unambiguous reviews |
| **Logs** | Categories | Domain-specific (status, decision, issue) not DEBUG/INFO/ERROR | Semantic meaning vs system levels |

### 🎯 Implementation Decisions Summary

**Role-to-Skill Mapping**:
```
Role Document → Claude Code Skill
───────────────   ─────────────────
testing-guidelines.md  →  python-testing/SKILL.md
api-conventions.md     →  python-api/SKILL.md
async-patterns.md      →  python-async/SKILL.md
```

**Skill Naming Convention**:
- Format: `{role_prefix}-{document_name}`
- Example: `python-testing`, `python-api`
- Stored in: `~/.claude/skills/{skill_name}/SKILL.md`

**Regeneration Workflow**:
```
Role updated on API
        ↓
Notify user: "Role 'python-dev' has been updated (v3 → v4)"
        ↓
User runs: agentflow agent pull agent-dev-001
        ↓
Skills regenerated with new content
```

**Content Types (Phase 0)**:
- Guidelines (rules, standards)
- Concepts (domain knowledge)
- Methodologies (processes)
- Conventions (code style)
- Examples (reference implementations)

All as Markdown files.

---

## Implementation Priority (Phase 0)

### Must Have (MVP)

**Role Management**:
1. ✅ Role creation (`role create`)
2. ✅ Role listing (`role list`)
3. ✅ Role viewing (`role view`)
4. ✅ Document management (`role add-document`, `role list-documents`)

**Agent Management**:
5. ✅ Agent creation with role assignment (`agent create --role`)
6. ✅ Agent listing (`agent list`)
7. ✅ Agent viewing (`agent view`)
8. ✅ Pull mechanism (`agent pull` - generates skills)

**Session Management**:
9. ✅ Session start (`session start`)
10. ✅ Session stop (`session stop`)
11. ✅ Basic logging (`session log --message`)
12. ✅ Session history (`session list`)

### Nice to Have

1. ⭐ Agent update (`agent update --role`)
2. ⭐ Structured log context (`session log --context`)
3. ⭐ Log search (`logs search`)
4. ⭐ Agent timeline (`agent timeline`)
5. ⭐ Session summary (`session summary`)
6. ⭐ Role update (`role update`)
7. ⭐ Document removal (`role remove-document`)

### Future (Post-Phase 0)

1. 🔮 Agent auto-pull (background sync)
2. 🔮 Role version notifications
3. 🔮 Auto-session on inactivity
4. 🔮 Trust score auto-calculation
5. 🔮 Advanced analytics
6. 🔮 Multi-agent collaboration
7. 🔮 Skill sharing between agents

---

## Summary

### Key Concepts

1. **Agent** (Complete Worker): Autonomous AI worker with multiple components
   - **Identity**: Unique name, code, status (active/probation/inactive/terminated)
   - **Role**: Template that defines behaviors and capabilities
   - **Tasks**: Assigned work with priorities and types
   - **Tools**: CLI utilities available for use
   - **Objective**: Self-improvement (maximize trust score)
   - **Hierarchy**: Position in organization/project tree structure

2. **Role** (Template): Stored on API, contains system prompt + Markdown documents
   - Defines job function, behaviors, and knowledge
   - Includes tool definitions (CLI tools agents can use)
   - Reusable across multiple agents
   - Documents generate Claude Code skills when pulled

3. **Hierarchy** (Tree Structure): Two-level organization
   - **Organization tree**: CTO, Architect, Tech Lead, PM
   - **Project tree**: Tech Lead → Senior Dev → Dev → QA
   - Manual definition via CLI commands
   - Supervisor identification for review workflow

4. **Tasks** (Work Units): What agents complete
   - **Types**: development, bug, review (Phase 0)
   - **Priorities**: P0 (critical) → P1 → P2 → P3 (low)
   - **Status**: backlog → assigned → in_progress → ready_review → completed
   - **Permissions**: Workers cannot mark `completed` (only managers)
   - **Auto-review**: Creates review task for supervisor when ready

5. **Permissions** (Role-Based):
   - **Manager roles** (org-level): Full permissions (create, assign, approve, cancel)
   - **Worker roles** (project-level): Limited permissions (update own status, log)
   - **Probation restrictions**: Additional limits for low trust scores

6. **Communication** (Upward Only):
   - **IMPORTANT**: Agents communicate ONLY with supervisors (no peer communication)
   - **Direct messages**: To supervisor when clarification/intervention needed
   - **Session logs**: Informational updates, progress, decisions, ideas
   - **Distinction**: Messages require response, logs are informational
   - **Rationale**: Agents with same role have same skills, supervisor coordinates

7. **Trust Score** (Self-Improvement):
   - Range: 0-100 (starts at 50)
   - Increases: Completing tasks (+1 to +5 based on priority)
   - Decreases: Rejections, bugs, delays (-2 to -10)
   - Status implications: 80+ excellent, 60-79 good, 30-49 warning, <30 probation

8. **Pull**: Fetch role from API, generate Claude Code skills
   - Downloads role documents + tool definitions
   - Creates `~/.claude/skills/<skill-name>/SKILL.md`
   - Generates both role skills (guidelines) and tool skills (CLI usage)

9. **Claude Code Skills**: Extension of Claude's capabilities
   - **Role skills**: Guidelines, conventions, methodologies
   - **Tool skills**: How to use specific CLI tools (pytest, black, etc.)
   - Format: YAML frontmatter (metadata) + Markdown (instructions)
   - Invoked via `/skill-name` or auto-loaded by Claude

10. **Session**: Temporal block of work with start/stop and duration tracking
    - Requires active pull before starting
    - Logs activities and progress
    - Immutable after stop

11. **Logging**: Record activities, progress, problems, ideas, decisions
    - Types: activity, progress, problem, decision, question, idea
    - Structured with message, context, tags
    - Linked to sessions and agents

### Architecture Diagram

```
┌─────────────────────────┐
│   AgentFlow API            │
│                             │
│  Roles (Templates)         │
│  ┌────────────────────┐   │
│  │ python-dev           │   │
│  │ ├─ desc (prompt)     │   │
│  │ ├─ docs (MD)          │   │
│  │ └─ tools (CLI)       │   │
│  └────────────────────┘   │
│                             │
│  Tasks                      │
│  ┌────────────────────┐   │
│  │ #123: development   │   │
│  │ #124: bug           │   │
│  │ #125: review        │   │
│  └────────────────────┘   │
└─────────────┬───────────────┘
              │
              │ Pull (agentflow agent pull)
              │
              ▼
┌─────────────────────────────────────────────┐
│         Local AgentFlow Database                │
│  ┌──────────────────────────────────────┐  │
│  │ Agents                                   │  │
│  │ ┌────────────────────────────────┐   │  │
│  │ │ Jean (agent-dev-001)            │   │  │
│  │ │ - role: python-dev               │   │  │
│  │ │ - trust_score: 52.5               │   │  │
│  │ │ - status: active                  │   │  │
│  │ │ - skills: [python-testing, ...]   │   │  │
│  │ └────────────────────────────────┘   │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ Tasks                                   │  │
│  │ #123: Implement authentication       │  │
│  │ #124: Fix login bug                   │  │
│  │ #125: Review task #123               │  │
│  └────────────────────────────────────┘  │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ Messages                               │  │
│  │ From: agent-dev-001                  │  │
│  │ To:   agent-lead-001                  │  │
│  │ Type: question                        │  │
│  └────────────────────────────────────┘  │
│                                            │
│  ┌────────────────────────────────────┐  │
│  │ Hierarchy (Project Tree)               │  │
│ │ Tech Lead                               │  │
│  ├── Senior Dev                            │  │
│  │   └── Dev (Jean)                      │  │
│  └── QA                                    │  │
│  └────────────────────────────────────┘  │
└────────────┬───────────────────────────────┘
             │
             │ Generate Skills (Role Docs + Tools)
             ▼
┌─────────────────────────────────────────────┐
│           Claude Code Skills                  │
│  ~/.claude/skills/                           │
│  ┌────────────────────────────────────┐ │
│  │ Role Skills                             │ │
│  │ ├── python-testing/SKILL.md          │ │
│  │ ├── python-api/SKILL.md               │ │
│  │ └── python-async/SKILL.md             │ │
│  │                                         │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │ Tool Skills                             │ │
│  │ ├── python-pytest/SKILL.md           │ │
│  │ ├── python-black/SKILL.md            │ │
│  │ └── python-mypy/SKILL.md            │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Complete Agent Lifecycle

```
1. CREATE AGENT
   agentflow agent create --name "Jean" --role "python-dev"
   → Agent created with trust_score: 50

2. PULL ROLE
   agentflow agent pull agent-dev-001
   → Downloads role definition + tools
   → Generates Claude Code skills

3. ASSIGN TASKS
   agentflow task create --title "Fix login" --assign-to agent-dev-001
   → Task appears in agent's queue

4. START SESSION
   agentflow session start --agent agent-dev-001
   → Agent begins working

5. LOG PROGRESS
   agentflow session log --type activity --message "Implementing JWT auth"
   → Progress recorded in timeline

6. ASK FOR HELP
   agentflow agent send-message --to supervisor --type question
   → Message sent to Tech Lead

7. COMPLETE TASK
   agentflow task update --task 123 --status ready_review
   → Creates review task for Tech Lead

8. TECH LEAD REVIEWS
   agentflow task approve --task 123
   → Task marked completed
   → Agent trust_score +3

9. STOP SESSION
   agentflow session stop
   → Duration calculated
```

### Review Workflow

```
Worker Agent (Jean) completes task
        ↓
Marks task "ready_review"
        ↓
System checks hierarchy tree
        ↓
Finds supervisor: Tech Lead
        ↓
Creates review task for Tech Lead
        ↓
Tech Lead reviews work
        ↓
Tech Lead approves task
        ↓
┌─────────────────────────────┐
│ Trust Score Updates           │
│                                │
│ Jean: +3 (task completed)     │
│                                │
│ Tech Lead: +1 (review done)    │
└─────────────────────────────┘
```

### Phase 0 Approach

- **Local storage** (JSON files for agents, sessions, events)
- **Role templates** (predefined in code for Phase 0, API in full system)
- **Manual operations** (user-triggered pull, session start/stop)
- **Skill generation** (automatic from role documents)
- **Basic sessions** (start/log/stop)
- **Structured logs** (message + optional context)

### Next Steps

1. ✅ Define role templates (system prompts + documents)
2. ✅ Implement role management CLI commands
3. ✅ Implement agent management with role assignment
4. ✅ Implement pull mechanism with skill generation
5. ✅ Implement session management (start/log/stop)
6. ✅ Add validation and error handling
7. ✅ Write tests for core functionality
8. ✅ Document CLI usage examples

---

**Document Version**: 4.3
**Last Updated**: 2025-01-21
**Status**: ✅ Updated with hierarchy structure (one-to-many) and log categorization (domain-specific) - Ready for DX testing (Phase 0)

### Key Changes in v4.3:
- **Hierarchy Structure**: One-to-many only (no many-to-many, no dotted line relationships)
- **Hierarchy Rules**: Clear constraints on allowed/forbidden organizational structures
- **Multiple Supervisors**: NOT supported - each agent has exactly one supervisor
- **Log Categories**: Domain-specific names (status, decision, issue) not DEBUG/INFO/ERROR
- **Log Filtering**: Filter by semantic category, not system log level
- **Rationale**: Simplicity, clarity, unambiguous chain of command for agents

### Key Changes in v4.2:
- **Tool Documentation**: Each tool has Markdown documentation stored in database (like roles)
- **Tool Management**: CLI commands for creating/updating tools with documentation
- **Internal vs External Tools**: Distinction between pre-defined (pytest) and custom (excel-analyzer)
- **Agent Termination**: ALL data preserved (tasks, sessions, logs, messages, skills)
- **Agent Lifecycle**: Added terminate/deactivate/activate commands with data retention policies
- **Task Reassignment**: Manual reassignment (not automatic) when agent terminated

### Key Changes in v4.1:
- **Trust Score Bounds**: Floor at 0, ceiling at 100, no glass ceiling
- **Recovery Mechanism**: Phase 0 (manual by manager) vs Full System (automatic via task completion)
- **Training Tasks**: Removed - agents learn by doing actual work, not artificial exercises
- **Sessions**: One session active at a time (even across multiple projects)
- **Session Mutability**: Immutable after stop, but can append additional logs
- **Logs**: Append-only modification (can add info, cannot modify existing data)
- **Status Thresholds**: Updated ranges (90-100 Excellent, 70-89 Very Good, 50-69 Neutral, etc.)

### Key Changes in v4.0:
- **Communication**: Clarified that agents communicate ONLY with supervisors (no peer communication)
- **Message vs Log**: Clear distinction - messages require response, logs are informational
- **Role Version Management**: Added notification system for outdated roles, skill overwrite behavior
- **Task Assignment**: Clarified project-level assignment (not global)
- **Message Priority**: Added implicit priority for hierarchical messages
- **Removed**: "Help another agent" from trust score increases (no peer interaction)
