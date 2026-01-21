# Pulling an Agent & Skill Generation

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
