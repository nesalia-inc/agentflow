# Projects Feature Proposal

## Overview

This document proposes adding a **Projects** feature to AgentFlow, allowing workspaces to organize work into projects, similar to how GitHub organizations have repositories and projects.

## Motivation

Currently, AgentFlow has a two-level hierarchy:
```
Workspace -> Session -> Commit
```

While this works for simple use cases, it lacks granularity for organizing work within a workspace. Users working on multiple features or components within the same workspace have no way to group related sessions together.

### The Problem

A developer working on a web application might have sessions related to:
- Authentication system
- Payment processing
- User profile management
- API endpoints

With the current structure, all these sessions live at the same level in the workspace, making it difficult to:
- See all work related to a specific feature
- Understand the context of a session without reading its description
- Generate reports per feature/component
- Track progress on specific initiatives

### The Solution

Introduce a **Project** entity as an intermediate level:
```
Workspace -> Project -> Session -> Commit
```

## Concept Design

### What is a Project?

A **Project** in AgentFlow represents a logical grouping of related work sessions within a workspace. Similar to GitHub Projects or Jira Epics, it helps organize work around specific features, components, or initiatives.

**Examples of projects**:
- "Authentication" - All sessions related to login, registration, OAuth
- "Payment System" - All sessions related to payments, refunds, billing
- "API v2" - All sessions working on the next API version
- "Bug Fixes" - All bug fix sessions
- "Documentation" - All documentation improvements

### Relationship to GitHub Projects

**GitHub's structure:**
```
Organization -> Repository -> Project -> Issues/Pull Requests
```

**AgentFlow's proposed structure:**
```
Workspace -> Project -> Sessions -> Commits
```

Just as GitHub Projects organize issues and PRs within a repository, AgentFlow Projects organize sessions within a workspace.

## Data Model

### Project Entity

```python
class Project(Base):
    __tablename__ = "projects"

    id: str                    # Unique project identifier
    workspace_id: str          # Foreign key to workspace
    name: str                  # Project name (e.g., "Authentication")
    description: str | None    # Optional detailed description
    status: str                # "active", "archived", "completed"
    created_at: datetime
    updated_at: datetime | None

    # Relationships
    workspace: Workspace
    sessions: List[Session]    # All sessions in this project
```

### Updated Session Entity

```python
class Session(Base):
    # ... existing fields ...
    project_id: str | None     # Foreign key to project (optional)

    # Relationships
    project: Project | None    # Session belongs to a project
```

**Note**: `project_id` is **optional** to allow backward compatibility and flexibility. Sessions can exist without being assigned to a project.

## CLI Commands

### Project Management

```bash
# Create a new project
agentflow project create "Authentication" \
    --description "Login, registration, and OAuth functionality"

# List all projects in current workspace
agentflow project list

# Show project details
agentflow project show <project-id>

# Rename a project
agentflow project rename <project-id> "Auth & Security"

# Archive a project (mark as inactive)
agentflow project archive <project-id>

# Delete a project (does not delete sessions)
agentflow project delete <project-id>
```

### Session Integration

```bash
# Start a session in a project
agentflow session start "Add OAuth support" --project "Authentication"

# Move existing session to a project
agentflow session move <session-id> --project "Payment System"

# Remove session from project
agentflow session move <session-id> --no-project

# List all sessions in a project
agentflow project sessions <project-id>
```

### Filtering & Queries

```bash
# Show commits for a specific project
agentflow log --project "Authentication"

# Show stats for a project
agentflow project stats <project-id>

# Show active projects
agentflow project list --status active
```

## User Stories & Use Cases

### Use Case 1: Feature Development

**Scenario**: Developer is building an authentication system.

```bash
# Create project
agentflow project create "Authentication" \
    -d "User authentication and authorization system"

# Work on different aspects
agentflow session start "Add login form" --project "Authentication"
# ... work ...
agentflow session commit "feat: add login form"

agentflow session start "Implement OAuth" --project "Authentication"
# ... work ...
agentflow session commit "feat: implement OAuth with Google"

# See all authentication work
agentflow log --project "Authentication"
```

### Use Case 2: Sprint Organization

**Scenario**: Team using AgentFlow for sprint planning.

```bash
# Create projects for sprint goals
agentflow project create "Sprint 23 - User Profile"
agentflow project create "Sprint 23 - Performance"
agentflow project create "Sprint 23 - Bug Fixes"

# Assign sessions to sprint goals
agentflow session start "Optimize database queries" --project "Sprint 23 - Performance"
agentflow session start "Fix login timeout" --project "Sprint 23 - Bug Fixes"

# Generate sprint report
agentflow project stats "Sprint 23 - Performance"
# Output:
# Total sessions: 5
# Total time: 12h 30m
# Commits: 5
# First session: 2025-01-10
# Last session: 2025-01-15
```

### Use Case 3: Component Organization

**Scenario**: Full-stack app with frontend, backend, and DevOps work.

```bash
# Create component projects
agentflow project create "Frontend" -d "React components and UI"
agentflow project create "Backend" -d "API and business logic"
agentflow project create "DevOps" -d "CI/CD and infrastructure"

# Organize work by component
agentflow session start "Add user settings page" --project "Frontend"
agentflow session start "Implement settings API" --project "Backend"
agentflow session start "Setup deployment pipeline" --project "DevOps"

# View all frontend work
agentflow log --project "Frontend"
```

### Use Case 4: Backlog Management

**Scenario**: Planning future work without starting sessions yet.

```bash
# Create projects for planned features
agentflow project create "Payment Integration" --status archived
agentflow project create "Multi-tenancy" --status archived
agentflow project create "API v2" --status archived

# When ready to start work
agentflow project activate "Payment Integration"
agentflow session start "Research Stripe API" --project "Payment Integration"
```

## Design Considerations

### 1. Optional vs. Mandatory Projects

**Decision**: Projects are **optional**.

**Rationale**:
- Backward compatibility - existing workspaces continue working
- Flexibility - users can adopt projects gradually
- Simplicity - not over-engineering for simple use cases
- Some workspaces don't need projects (single-project workspace)

### 2. Project Status

**Status values**:
- `active` - Currently being worked on
- `archived` - Not active, but referenceable
- `completed` - Feature/project is done

**Benefits**:
- Focus on active work
- Historical context without clutter
- Clear completion indicators

### 3. Project Deletion

**Decision**: Deleting a project **does not delete** its sessions.

**Rationale**:
- Sessions contain valuable work history
- Sessions can be re-assigned to other projects
- Safety - prevent accidental data loss

**Alternative**: `--cascade` flag to delete sessions too (if explicitly requested)

### 4. Session Migration

**Scenario**: User has existing sessions, wants to add projects later.

```bash
# Create project
agentflow project create "Authentication"

# Assign existing sessions
agentflow session move <session-id-1> --project "Authentication"
agentflow session move <session-id-2> --project "Authentication"

# Or bulk assign by pattern
agentflow session assign --project "Authentication" --grep "auth"
```

### 5. Display & Visualization

**Log command output**:
```
$ agentflow log

Authentication (3 commits):
  abc123 feat: add login form (2 hours ago)
  def456 feat: implement OAuth (1 day ago)

Payment System (2 commits):
  ghi789 feat: add Stripe integration (3 hours ago)

Other (1 commit):
  jkl012 chore: update dependencies (5 hours ago)
```

**Or flat view with project indicator**:
```
$ agentflow log

abc123 feat: add login form (2 hours ago) [Authentication]
def456 feat: implement OAuth (1 day ago) [Authentication]
ghi789 feat: add Stripe integration (3 hours ago) [Payment System]
jkl012 chore: update dependencies (5 hours ago)
```

## Implementation Phases

### Phase 1: Core Functionality
- Project entity and database migration
- Basic CRUD operations (create, list, show, delete)
- Session-project association
- Filtering by project

### Phase 2: Enhanced Features
- Project status (active/archived/completed)
- Session move/reassign
- Project statistics
- Better visualization in log output

### Phase 3: Advanced Features
- Bulk operations
- Project templates
- Project labels/tags
- Project dependencies
- Project milestones

## Migration Path

### For Existing Users

When upgrading to version with projects:
1. Existing workspaces have **no projects** by default
2. Existing sessions have `project_id = NULL`
3. Everything continues working as before
4. Users can optionally create projects and organize sessions

### For New Users

- Projects are introduced in documentation
- Quick start shows optional project usage
- Default workspace creation prompts: "Create a project? (y/n)"

## Alternatives Considered

### Alternative 1: Tags instead of Projects
**Rejected**: Tags don't provide hierarchy or clear ownership
### Alternative 2: Folders/Nested Workspaces
**Rejected**: Too complex, breaks workspace concept
### Alternative 3: Categories/Labels
**Rejected**: Less structured, harder to query and visualize

## Open Questions

1. Should projects have deadlines/due dates?
2. Should projects support color coding?
3. Should sessions be required to belong to a project?
4. Should we support project templates?
5. How to handle projects across multiple workspaces?

## Conclusion

Adding Projects to AgentFlow will provide:
- ✅ Better organization of work within workspaces
- ✅ Clearer context for sessions and commits
- ✅ Improved reporting and statistics
- ✅ Familiar mental model for GitHub users
- ✅ Backward compatibility (optional feature)

**Recommended Priority**: **Phase B** (Advanced Features)
**Estimated Complexity**: Medium
**User Value**: High for teams and complex projects

---

**Proposed Version**: v0.3.0
**Status**: Proposal - Open for Feedback
