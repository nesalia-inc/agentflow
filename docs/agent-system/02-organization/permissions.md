# Permissions System

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
