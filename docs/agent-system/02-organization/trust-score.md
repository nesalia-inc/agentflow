# Reward & Punition System

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
