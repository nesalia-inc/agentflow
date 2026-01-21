# Hierarchy & Organization

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
