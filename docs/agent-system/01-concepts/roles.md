# Roles

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
