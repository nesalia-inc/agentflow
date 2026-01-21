# Tools & Skills Integration

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
