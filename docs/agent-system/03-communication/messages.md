# Agent Communication

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
