# Security & Compliance Features

## Feature 22: Signed Audit Trail

### Overview

Cryptographically signed audit trail for all critical events, providing non-repudiation, tamper evidence, and complete traceability for compliance (SOX, GDPR, HIPAA, SOC 2) and security investigations.

### Why It Matters

- **Compliance**: Legal requirements for audit trails (SOX, GDPR, HIPAA)
- **Security**: Tamper-evident logs prevent unauthorized modifications
- **Non-Repudiation**: Cryptographic proof of who did what when
- **Investigation**: Complete reconstruction of event sequences
- **Forensics**: Immutable evidence for security incidents

### Implementation Complexity

**High** - Requires:
- Cryptographic signing (HMAC or digital signatures)
- Immutable audit log storage
- Signature verification system
- Key management

**Phase**: Phase 2+ (critical for production but not for MVP)

### How It Works

#### Automatic Signing of Critical Events

```bash
# All critical events are automatically signed with:
# - HMAC-SHA256 (Phase 1) - shared secret
# - Digital signatures RSA/ECDSA (Phase 2) - asymmetric keys

# Critical events that trigger audit trail signing:
# - Task lifecycle changes (created, assigned, completed, approved, rejected)
# - Agent lifecycle changes (created, activated, probation, terminated)
# - Trust score changes (increases, decreases, resets)
# - Security-sensitive actions (login, permission changes, data access)
# - Configuration changes (role updates, hierarchy changes)
# - Data access (viewing sensitive information, exporting data)

# When task is completed (by worker agent)
agentflow task update 123 --status ready_review

# Behind the scenes, audit event is created:
{
  "event_id": "audit_20250121_143045_abc123",
  "timestamp": "2025-01-21T14:30:45Z",
  "event_type": "task.status_changed",
  "actor": "agent-dev-001",
  "actor_type": "agent",
  "target_type": "task",
  "target_id": "123",
  "old_value": "in_progress",
  "new_value": "ready_review",
  "context": {
    "session_id": "session-xyz-789",
    "project": "website-redesign"
  },
  "signature": "HMACSHA256=A5:F2:8C:1D:...:1C:3E",
  "signing_key_id": "agentflow-audit-key-v1",
  "signature_algorithm": "HMAC-SHA256"
}

# View audit trail for a task
agentflow audit trail task 123

# Output:
# 🔐 Signed Audit Trail - Task #123
# ─────────────────────────────────────
# Task: Implement user authentication
#
# Audit Events (5):
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 1. Task Created                                                            │
# ├─────────────────────────────────────────────────────────────────────────┤
# │ When:      2025-01-21 09:15:33 UTC                                          │
# │ Who:       user@company.com (via CLI)                                     │
# │ Actor IP:   192.168.1.100                                                  │
# │ Event ID:  audit_20250121_091533_abc123                                 │
# │ Signature: A5:F2:8C:1D:3E:...:1C (HMAC-SHA256)                           │
# │ Status:    ✅ VERIFIED - Signature valid                                     │
│                                                                           │
# │ Event Data:                                                              │
# │   Task created: #123 - Implement user authentication                    │
#   Project: website-redesign                                                │
#   Assigned to: agent-dev-001 (Jean)                                      │
#   Priority: P1                                                             │
#   Estimate: 4h                                                             │
└─────────────────────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 2. Task Assigned                                                            │
├─────────────────────────────────────────────────────────────────────────┤
# │ When:      2025-01-21 09:16:00 UTC                                          │
# │ Who:       agent-lead-001 (Tech Lead)                                     │
# │ Actor IP:   192.168.1.105                                                  │
# │ Event ID:  audit_20250121_091600_def456                                 │
# │ Signature: B3:E8:4A:6F:2D:...:4D (HMAC-SHA256)                           │
# │ Status:    ✅ VERIFIED - Signature valid                                     │
│                                                                           │
# │ Event Data:                                                              │
# │   Task #123 assigned to agent-dev-001 (already assigned)                   │
│   Assignment type: Automatic (created with task)                           │
└─────────────────────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 3. Task Started (Session Begin)                                            │
├─────────────────────────────────────────────────────────────────────────┤
# │ When:      2025-01-21 09:30:00 UTC                                          │
# │ Who:       agent-dev-001 (Jean) - via session start                       │
# │ Actor IP:   192.168.1.110                                                  │
# │ Event ID:  audit_20250121_093000_ghi789                                 │
# │ Signature: C7:D1:5E:3B:8E:...:8E (HMAC-SHA256)                           │
# │ Status:    ✅ VERIFIED - Signature valid                                     │
│                                                                           │
# │ Event Data:                                                              │
# │   Session started: session-xyz-789                                      │
# │   Agent: Jean (agent-dev-001)                                              │
#   Task context: #123 - Implement user authentication                      │
└─────────────────────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 4. Task Completed (Worker marked ready for review)                          │
├─────────────────────────────────────────────────────────────────────────┤
# │ When:      2025-01-21 16:45:22 UTC                                          │
# │ Who:       agent-dev-001 (Jean) - marked ready_review                    │
│ │ Actor IP:   192.168.1.110                                                  │
# │ Event ID:  audit_20250121_164522_jkl012                                 │
# │ Signature: D9:A4:7B:2C:1F:...:2F (HMAC-SHA256)                           │
# │ Status:    ✅ VERIFIED - Signature valid                                     │
│                                                                           │
# │ Event Data:                                                              │
# │   Task status: in_progress → ready_review                                │
#   Session: session-xyz-789                                               │
#   Duration: 7h 15m (work session)                                        │
│   Progress: 100% complete                                                  │
└─────────────────────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ 5. Task Approved (Reviewer marked completed)                               │
├─────────────────────────────────────────────────────────────────────────┤
# │ When:      2025-01-21 17:30:00 UTC                                          │
# │ Who:       agent-lead-001 (Tech Lead) - task approve                       │
│ │ Actor IP:   192.168.1.105                                                  │
# │ Event ID:  audit_20250121_173000_mno345                                 │
# │ Signature: E1:B6:9D:4F:A8:...:3C (HMAC-SHA256)                           │
# │ Status:    ✅ VERIFIED - Signature valid                                     │
│                                                                           │
# │ Event Data:                                                              │
# │   Task status: ready_review → completed                                  │
│   Review decision: Approved                                              │
│   Review feedback: "Great work, no issues found"                         │
│   Trust score change: agent-dev-001 +3 points (65 → 68)                   │
└─────────────────────────────────────────────────────────────────────────┘
#
# ══════════════════════════════════════════════════════════════════════════
# 🔐 SECURITY GUARANTEES:
#
# ✅ All events cryptographically signed
# ✅ Signatures verified using HMAC-SHA256 (Phase 1)
# ✅ Audit log is write-once (immutable)
# ✅ Any tampering invalidates signature (detectable)
# ✅ Chain of custody complete and verifiable
# ══════════════════════════════════════════════════════════════════════════

# Verify integrity of audit trail
agentflow audit verify --task 123

# Output:
# 🔍 Verifying Audit Trail Integrity: Task #123
# ───────────────────────────────────────────────────────────────────────
#
# Events: 5
#
# Verification Results:
#   Event 1 (audit_abc123): ✅ VALID
#      Signature: A5:F2:...:1C (VERIFIED)
#      Actor: user@company.com (VERIFIED)
#      Timestamp: 2025-01-21T09:15:33Z (VALID)
#
#   Event 2 (audit_def456): ✅ VALID
#      Signature: B3:E8:...:4D (VERIFIED)
#      Actor: agent-lead-001 (VERIFIED)
#      Timestamp: 2025-01-21T09:16:00Z (VALID)
#
#   Event 3 (audit_ghi789): ✅ VALID
#      Signature: C7:D1:...:8E (VERIFIED)
#      Actor: agent-dev-001 (VERIFIED)
#      Timestamp: 2025-01-21T09:30:00Z (VALID)
#
#   Event 4 (audit_jkl012): ✅ VALID
#      Signature: D9:A4:...:2F (VERIFIED)
#      Actor: agent-dev-001 (VERIFIED)
#      Timestamp: 2025-01-21T16:45:22Z (VALID)
#
#   Event 5 (audit_mno345): ✅ VALID
#      Signature: E1:B6:...:3C (VERIFIED)
#      Actor: agent-lead-001 (VERIFIED)
#      Timestamp: 2025-01-21T17:30:00Z (VALID)
#
# Overall Result: ✅ ALL SIGNATURES VALID
#
# Integrity: ✅ INTACT (no tampering detected)
# Chain of Custody: ✅ COMPLETE
# Compliance: ✅ SOX, GDPR compliant (7-year retention met)
```

#### Agent Lifecycle Audit

```bash
# Agent termination audit trail
agentflow audit trail agent agent-dev-001 --event terminated

# Output:
# 🔐 Audit Trail: Agent Termination - agent-dev-001 (Jean)
# ─────────────────────────────────────────────────────────────────────
# Agent: Jean (agent-dev-001)
# Event: TERMINATED
#
# Termination Audit Trail:
#
# 1. Agent Created
#    When: 2024-05-15 10:00:00 UTC
#    Who: admin@company.com
#    Event ID: audit_agent_create_001
#    Signature: [VERIFIED]
#
# 2. Trust Score Changes (157 events)
#    First: 50.0 (creation)
#    Last: 72.5 (before termination)
#    Peak: 85.0 (Aug 2024)
#    Total change: +22.5 points
#    All events: [VERIFIED]
#
# 3. Tasks Completed
#    Total: 127 tasks
#    Completed: 119 (94%)
#    Rejected: 8 (6%)
#    All task events: [VERIFIED]
#
# 4. Sessions
#    Total sessions: 45
#    Total duration: 189 hours
#    Avg session: 4.2 hours
#    All session events: [VERIFIED]
#
# 5. Agent Terminated
#    When: 2025-01-21 11:00:00 UTC
#    Who: admin@company.com
#    Event ID: audit_agent_terminate_001
#    Signature: [VERIFIED]
#    Reason: "Performance issues, low trust score"
#
# 6. Data Preservation
#    Tasks: PRESERVED (127 tasks kept, reassigned)
#    Sessions: PRESERVED (45 sessions kept)
#    Logs: PRESERVED (847 log entries kept)
#    Messages: PRESERVED (156 messages kept)
#    Trust history: PRESERVED (157 score changes kept)
#
# ══════════════════════════════════════════════════════════════════════════
# 🔐 DATA INTEGRITY VERIFICATION:
#
# All 6 categories of events have valid signatures
# No tampering detected
# Chain of custody: COMPLETE
# Legal admissibility: HIGH (cryptographically proven)
# ══════════════════════════════════════════════════════════════════════════

# Export audit trail for legal/compliance
agentflow audit export --agent agent-dev-001 \
  --format json \
  --include tasks,sessions,logs,messages \
  --file audit-agent-dev-001-termination.json

# Output:
# ✅ Audit trail exported
#    File: audit-agent-dev-001-termination.json
#    Size: 2.3 MB
#    Events: 1,024 events
#    Format: JSON with signatures
#    Purpose: Legal evidence, compliance documentation
#
# Contains:
#   • All agent lifecycle events
#   • All task events (127 tasks)
#   • All session events (45 sessions)
#   • All log events (847 entries)
#   • All message events (156 messages)
#   • All trust score changes (157 events)
#
# This file can be used for:
#   • Legal discovery
#   • Compliance audits
#   • Security investigations
#   • Forensic analysis
```

#### Security Incidents Audit

```bash
# Investigate a security incident
agentflow audit investigate --incident "INC-2025-001" --date "2025-01-20"

# Output:
# 🔍 Security Incident Investigation: INC-2025-001
# ─────────────────────────────────────────────────────────────────────
# Incident Date: 2025-01-20
# Incident Type: Unauthorized data access attempt
# Status: RESOLVED
#
# Incident Timeline (Reconstructed from audit trail):
#
# 14:32:30 - Authentication attempt
#    IP: 203.0.113.45
#    User: unknown@hacker.com
#    Attempt: agentflow login
#    Status: ❌ FAILED (invalid credentials)
#    Event ID: audit_auth_fail_001
#
# 14:32:45 - Second attempt (different user)
#    IP: 203.0.113.45
#    User: admin@company.com
#    Attempt: agentflow login
#    Status: ❌ FAILED (invalid credentials, account doesn't exist)
#    Event ID: audit_auth_fail_002
#
# 14:33:12 - Third attempt (different user)
#    IP: 203.0.113.45
#    User: root@company.com
#    Attempt: agentflow login
#    Status: ❌ FAILED (invalid credentials)
#    Event ID: audit_auth_fail_003
#
# 14:33:30 - Account locked (too many failed attempts)
#    System: Automatic lockout after 3 failed attempts
#    IP: 203.0.113.45
#    Action: IP blocked for 1 hour
#    Event ID: audit_security_lock_001
#
# 15:45:00 - IP blocked, no further attempts
#    Status: Blocked at firewall level
#
# ══════════════════════════════════════════════════════════════════════════
# 🔐 AUDIT TRAIL INTEGRITY:
#
# All 4 events have valid signatures
# No events were modified or deleted
# Timeline is complete and tamper-proof
# Legal admissibility: HIGH
# ══════════════════════════════════════════════════════════════════════════

# Generate compliance report
agentflow audit compliance-report --period Q1-2025 --format pdf

# Output:
# ✅ Compliance Report Generated
#    File: compliance_Q1_2025.pdf
#    Period: Q1 2025 (Jan 1 - Mar 31)
#    Standards: SOX, GDPR, HIPAA
#
# Report includes:
#   • All audit events for period
#   • Signature verification results
#   • Data access logs
#   • Retention compliance
#   • Security incident summary
#   • Signed attestation
```

### Data Model

```python
class AuditEvent(BaseModel):
    id: str  # Unique event ID
    timestamp: datetime
    event_type: str  # "task.created", "task.completed", etc.

    # Actor
    actor_type: Literal["user", "agent", "system"]
    actor_id: str  # Email, agent code, or "system"
    actor_ip: Optional[str] = None

    # Target
    target_type: Literal["task", "agent", "session", "log", "config"]
    target_id: Optional[str] = None

    # Event data
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    context: Dict[str, Any] = {}

    # Cryptographic signature
    signature: str  # HMAC or digital signature
    signature_algorithm: str  # "HMAC-SHA256", "RSA-2048", etc.
    signing_key_id: str  # ID of key used for signing
    timestamp_signed: datetime

    # Verification
    verified: bool = False
    verification_timestamp: Optional[datetime] = None

class AuditTrail(BaseModel):
    target_id: str  # Task ID, Agent ID, etc.
    target_type: str
    events: List[AuditEvent]

    # Metadata
    created_at: datetime
    exported_at: Optional[datetime] = None
    export_format: Optional[str] = None

    # Verification
    integrity_verified: bool = False
    last_verification: Optional[datetime] = None
```

### CLI Commands

```bash
# Viewing audit trails
agentflow audit trail --task <id>
agentflow audit trail --agent <id>
agentflow audit trail --session <id>

# Verification
agentflow audit verify --task <id>
agentflow audit verify --agent <id>

# Investigation
agentflow audit investigate --incident <id>
agentflow audit search --actor "agent-dev-001" --period 7d

# Export
agentflow audit export --task <id> --format json --file <file>
agentflow audit compliance-report --period <period> --format pdf
```

---

## Feature 23: Data Retention Policies

### Overview

Automated data retention policies that automatically archive, anonymize, or delete data based on time, data type, and compliance requirements (GDPR, SOX, HIPAA, etc.).

### Why It Matters

- **Compliance**: Legal requirements for data retention (e.g., GDPR: "right to be forgotten")
- **Storage**: Automatic cleanup prevents unlimited data growth
- **Performance**: Smaller databases = faster queries
- **Cost**: Reduced storage costs
- **Risk**: Less sensitive data to protect

### Implementation Complexity

**Moderate** - Requires:
- Policy definition engine
- Scheduled cleanup jobs
- Anonymization utilities
- Archive storage

**Phase**: Phase 1 (basic retention), Phase 2 (automated cleanup)

### How It Works

#### Creating Retention Policies

```bash
# Create a comprehensive retention policy
agentflow retention create \
  --name "gdpr-compliant" \
  --description "GDPR compliant data retention policy" \
  --policies \
    "tasks.completed:keep_for:7y:then:anonymize" \
    "tasks.cancelled:keep_for:2y:then:delete" \
    "sessions:keep_for:1y:then:delete" \
    "logs.error:keep_for:5y" \
    "logs.info:keep_for:1y:then:delete" \
    "logs.debug:keep_for:6m:then:delete" \
    "messages:keep_for:3y:then:delete" \
    "agents.terminated:keep_forever" \
    "agents.inactive:keep_for:2y:then:delete"

# Output:
# ✅ Retention policy created
#    Name: gdpr-compliant
#    Policies: 10 rules
#    Status: Active
#
# Next run: 2025-01-28 02:00 (automatic)
#
# Categories:
#   Tasks: 7 years, then anonymize
#   Sessions: 1 year, then delete
#   Logs: 6 months to 5 years (by type)
#   Messages: 3 years, then delete
#   Agents: Keep forever if terminated, 2y if inactive then delete

# Set policy as active
agentflow retention set-active gdpr-compliant

# View active policy
agentflow retention show

# Output:
# 📋 Active Retention Policy: gdpr-compliant
# ─────────────────────────────────────
#
# Rules (10):
#
#   ✅ Tasks (Completed)
#      Keep: 7 years
#      Then: Anonymize
#      Action: Remove agent names, keep metrics only
#
#   ✅ Tasks (Cancelled)
#      Keep: 2 years
#      Then: Delete permanently
#
#   ✅ Sessions
#      Keep: 1 year
#      Then: Delete permanently
#
#   ✅ Logs (Error)
#      Keep: 5 years
#      Then: Delete permanently
#      Note: Required for compliance
#
#   ✅ Logs (Info)
#      Keep: 1 year
#      Then: Delete permanently
#
#   ✅ Logs (Debug)
#      Keep: 6 months
#      Then: Delete permanently
#
#   ✅ Messages
#      Keep: 3 years
#      Then: Delete permanently
#
#   ✅ Agents (Terminated)
#      Keep: Forever
#      Action: Archive (read-only)
#      Note: Historical record required
#
#   ✅ Agents (Inactive)
#      Keep: 2 years
#      Then: Delete permanently
#
# Next cleanup: 2025-01-28 02:00:00 UTC (7 days)
```

#### Policy Rules Syntax

```bash
# Rule format: <entity>:<condition>:<action>[:<parameters>]

# Entities
# - tasks, sessions, logs, messages, agents
# - Can be filtered by status: tasks.completed, tasks.cancelled
# - Can be filtered by type: logs.error, logs.info, logs.debug

# Conditions
# - keep_for:<duration> - Keep for X time
# - inactive_for:<duration> - If inactive for X time
# - age:<duration> - Generic age filter

# Actions
# - delete - Remove permanently
# - anonymize - Remove PII, keep metrics
# - archive - Move to read-only archive
# - keep_forever - Never delete

# Duration formats
keep_for:7y      # 7 years
keep_for:30d     # 30 days
keep_for:6m      # 6 months
keep_for:1y      # 1 year
keep_forever     # Never delete

# Examples
agentflow retention create \
  --name "minimal-policy" \
  --policies \
    "tasks:keep_for:1y:then:delete" \
    "sessions:keep_for:6m:then:delete" \
    "logs:keep_for:3m:then:delete"

# Industry-specific policies
agentflow retention create \
  --name "healthcare-hipaa" \
  --description "HIPAA compliant - 21 year retention for medical data" \
  --policies \
    "tasks.with_tag=medical:keep_for:21y:then:anonymize" \
    "logs.with_tag=patient_data:keep_for:21y:then:delete" \
    "messages.with_tag=phi:keep_for:21y:then:delete" \
    "tasks.other:keep_for:7y:then:delete"
```

#### Data Anonymization

```bash
# Preview what will be anonymized
agentflow retention anonymize-preview --tasks-completed --older-than 7y

# Output:
# 📊 Anonymization Preview
# ─────────────────────────────────────
# Tasks older than 7 years: 47
#
# What will be anonymized:
#
#   Agent Names:
#     Jean (agent-dev-001) → Agent-XXX-1
#     Alice (agent-dev-002) → Agent-XXX-2
#     Bob (agent-qa-001) → Agent-XXX-3
#
#   User Data:
#     user@company.com → u***@company.com
#     jean.personal@email.com → j***@personal.email
#
#   File Paths:
#     /home/jean/projects/ → /home/***/projects/
#     C:\Users\jean\Documents → C:\Users\***\Documents\
#
#   Message Content:
#     Kept AS-IS (no PII in task descriptions)
#
#   Metadata Preserved:
#     ✓ Task titles
#     ✓ Task types
#     ✓ Task completion status
#     ✓ Trust scores (anonymized)
#     ✓ Time/dates
#     ✓ Project associations
#
# What will be deleted:
#     ✓ Agent personal details
#     ✓ Session logs with PII
#     ✓ Messages with personal info
#
# What will be preserved:
#     ✓ Task metrics (time, quality scores, etc.)
#     ✓ Anonymized trust scores
#     ✓ Project associations

# Execute anonymization
agentflow retention anonymize --tasks-completed --older-than 7y

# Output:
# 🔒 Anonymizing 47 tasks...
#
# Progress: ████████████████████ 100%
#
# Anonymized:
#   • Agent names: 47 → Agent-XXX-1, Agent-XXX-2, ...
#   • User emails: 12 → anonymized
#   • File paths: 34 → anonymized
#
# Preserved for analytics:
#   • Task completion rates
#   • Time metrics
#   • Quality scores
#   • Trust score trends
#
# Audit log created: anonymization_2025_01_21.log
```

#### Automated Cleanup

```bash
# Preview upcoming cleanup
agentflow retention preview --days 30

# Output:
# 📊 Upcoming Cleanup (Next 30 Days)
# ─────────────────────────────────────
#
# Based on policy: gdpr-compliant
# Preview date: 2025-02-21
#
# Items to be deleted:
#
#   Sessions (45 sessions):
#     • session-2023-08-15-abc (Aug 15, 2023)
#     • session-2023-09-20-def (Sep 20, 2023)
#     • ... (43 more sessions)
#
#   Logs (238 entries):
#     • log_debug_123 (Jan 2024) - Debug logs > 6 months old
#     • log_info_456 (Feb 2024) - Info logs > 1 year old
#     • ... (236 more entries)
#
#   Messages (12 messages):
#     • msg_789 (Mar 2024) - Messages > 3 years old
#     • ... (11 more messages)
#
# Total: 295 items to delete
# Estimated space freed: 4.7 MB
#
# ⚠️  Warning: This action cannot be undone!
#
# Review before cleanup:
#   agentflow retention review --before-delete
#
# Execute cleanup:
#   agentflow retention purge --confirm
#
# Schedule automatic cleanup:
#   agentflow retention schedule --every "Monday 02:00"

# Dry-run (test)
agentflow retention purge --dry-run

# Output:
# 🧪 Dry-run Cleanup
# ─────────────────────────────────────
# Items matched: 295
#
# Would delete:
#   • 45 sessions (2.1 MB)
#   • 238 logs (2.3 MB)
#   • 12 messages (0.3 MB)
#
# Total: 4.7 MB
#
# NO CHANGES MADE (dry-run)
# To actually delete, run: agentflow retention purge --confirm
```

#### Retention Statistics

```bash
# View retention statistics
agentflow retention stats

# Output:
# 📊 Data Retention Statistics
# ─────────────────────────────────────
# As of: 2025-01-21
#
# Database Size:
#   Total: 45.2 MB
#   Breaking down by entity:
#     Tasks: 12.8 MB (28%)
#     Sessions: 8.4 MB (19%)
#     Logs: 18.7 MB (41%)
#     Messages: 3.1 MB (7%)
#     Agents: 1.2 MB (3%)
#     Other: 1.0 MB (2%)
#
# Data Age Distribution:
#   < 1 year:   12.3 MB (27%)
#   1-3 years:  18.7 MB (41%)
#   3-7 years:  12.1 MB (27%)
#   > 7 years:   1.9 MB (4%)
#   > 10 years:  0.2 MB (<1%)
#
# Growth Trend:
#   Last month: +12.3 MB
#   Last 6 months: +45.6 MB
#   Last 12 months: +89.2 MB
#
# Monthly growth rate: +2.1 MB/month
# Estimated 1-year growth: +25 MB
#
# Storage Quota: 100 MB (78% used, 22% available)
#
# ⚠️  Warnings:
#   1. Growth rate increasing - consider expanding storage
#   2. Error logs growing faster than expected (+15%/month)
#   3. Sessions accumulating - consider reducing retention period
#
# 💡 Recommendations:
#   • Expand storage quota to 200 MB (6 months runway)
#   • Reduce session retention to 6 months (saves ~3 MB/year)
#   • Review error logging strategy (may be over-logging)
```

### Data Model

```python
class RetentionPolicy(BaseModel):
    id: str
    name: str  # "gdpr-compliant"
    description: Optional[str] = None
    is_active: bool = True

    rules: List["RetentionPolicyRule"]
    created_at: datetime
    updated_at: datetime

class RetentionPolicyRule(BaseModel):
    entity: str  # "tasks.completed", "logs.error"
    entity_filter: Optional[str] = None  # "with_tag=medical"
    condition: str  # "keep_for:7y"

    action: Literal["delete", "anonymize", "archive", "keep_forever"]
    action_parameters: Optional[Dict[str, Any]] = None

class RetentionJob(BaseModel):
    id: str
    policy_id: str
    scheduled_at: datetime
    executed_at: Optional[datetime] = None

    dry_run: bool = False
    items_matched: int = 0
    items_affected: int = 0
    space_freed: float = 0.0  # in MB

    status: Literal["pending", "running", "completed", "failed"]

class AnonymizationResult(BaseModel):
    job_id: str
    timestamp: datetime

    items_anonymized: int
    items_deleted: int

    space_freed: float = 0.0
    space_reclaimed: float = 0.0

    anonymized_fields: List[str]  # ["agent_name", "email", "file_path"]
```

### CLI Commands

```bash
# Policies
agentflow retention create --name <name> --policies <rules>
agentflow retention list
agentflow retention show
agentflow retention set-active <name>

# Operations
agentflow retention preview --days <30>
agentflow retention purge --dry-run
agentflow retention purge --confirm
agentflow retention anonymize --tasks <condition> --older-than <duration>

# Statistics
agentflow retention stats

# Scheduling
agentflow retention schedule --every "<cron-expr>"
agentflow retention run-now

# Review
agentflow retention review --before-delete
```

---

## Feature 24: Access Control & Granular Permissions

### Overview

Fine-grained access control system with role-based permissions (RBAC), attribute-based access control (ABAC), and access control lists (ACLs) for precise authorization management.

### Why It Matters

- **Security**: Principle of least privilege
- **Compliance**: Control who can access what data
- **Flexibility**: Temporary access grants, project-specific permissions
- **Audit**: Who accessed what, when

### Implementation Complexity

**High** - Requires:
- Permission system architecture
- Role inheritance
- Permission checking on all operations
- ACL management

**Phase**: Phase 2 (critical for multi-team use cases)

### How It Works

#### Permission System Architecture

```
Three layers of access control:

1. ROLE-BASED (Coarse-grained)
   ├─ Admin: Full access to everything
   ├─ Manager: Org-level permissions (create tasks, approve work)
   └─ Worker: Project-level permissions (work on own tasks)

2. ATTRIBUTE-BASED (Medium-grained)
   ├─ Task ownership: Can only update own tasks
   ├─ Project membership: Can access tasks in assigned projects
   └─ Trust score thresholds: Probation restrictions

3. ACLS (Fine-grained)
   ├─ Temporary access grants: Time-limited permissions
   ├─ Resource-specific: Can access project X but not Y
   └─ Exception-based: One-time access for specific task
```

#### Defining Roles with Permissions

```bash
# Create a role with specific permissions
agentflow role create \
  --name "contractor-qa" \
  --description "External QA contractor with limited access" \
  --level project \
  --permissions \
    "task.create" \
    "task.read:project=mobile-app" \
    "task.update.status:own_tasks_only" \
    "session.start" \
    "session.log" \
    "NO:task.delete,agent.modify,org.manage"

# Built-in roles with permission sets:

# admin (Full access)
agentflow role create \
  --name admin \
  --level organization \
  --permissions "*"

# manager (Org management)
agentflow role create \
  --name manager \
  --level organization \
  --permissions \
    "org.manage" \
    "agent.*" \
    "task.*" \
    "session.*"

# senior-developer (Worker with more permissions)
agentflow role create \
  --name senior-developer \
  --level project \
  --permissions \
    "task.create" \
    "task.update.own" \
    "task.update.status:own_tasks" \
    "task.review" \
    "session.*" \
    "agent.view_own"

# developer (Basic worker)
agentflow role create \
  --name developer \
  --level project \
  --permissions \
    "task.create" \
    "task.update.own" \
    "session.start" \
    "session.log"
```

#### Granular Permission Examples

```bash
# Task permissions
agentflow permissions grant \
  --agent agent-dev-002 \
  --permission "task.assign:project=website-redesign" \
  --reason "Promoted to project manager"

# Output:
# ✅ Permission granted
#    Agent: agent-dev-002 (Alice)
#    Permission: task.assign
#    Scope: project=website-redesign
#    Reason: Promoted to project manager
#
# Alice can now assign tasks in 'website-redesign' project

# Temporary access grant
agentflow permissions grant \
  --agent agent-dev-003 \
  --resource "project:website-redesign" \
  --access "read" \
  --duration 7d \
  --reason "Review project documentation"

# Output:
# ✅ Temporary access granted
#    Agent: agent-dev-003 (Charlie)
#    Resource: project:website-redesign
#    Access: read (view only)
#    Duration: 7 days
#    Expires: 2025-01-28
#
#    Charlie can view project but not make changes

# Check permissions
agentflow permissions check --agent agent-dev-003 --resource project:website-redesign

# Output:
# ✅ Permission CHECK
#    Agent: agent-dev-003 (Charlie)
#    Resource: project:website-redesign
#    Action: read
#    Result: ALLOWED
#    Expires: 2025-01-28

# Revoke access
agentflow permissions revoke \
  --agent agent-dev-003 \
  --resource "project:website-redesign"

# Output:
# ✅ Access revoked
#    Agent: agent-dev-003
#    Resource: project:website-redesign
#    Revoked by: user@company.com
#    Reason: Temporary access period expired
```

#### Permission Matrix

```bash
# View permission matrix for a role
agentflow permissions matrix --role developer

# Output:
# 🔒 Permission Matrix: developer role
# ──────────────────────────────────────────────────────────────────────────────
# Permission                    │ Allowed │ Notes                         │
#──────────────────────────────┼─────────┼────────────────────────────│
#                               │         │                                │
# TASK OPERATIONS                                                      │         │                                │
#   task.create                  │ ✅     │ Create new tasks               │
#   task.read.all                 │ ✅     │ View all tasks in project     │
#   task.update.own               │ ✅     │ Update own task status        │
#   task.update.all               │ ❌     │ Cannot update others' tasks    │
#   task.delete                  │ ❌     │ Cannot delete tasks              │
#   task.assign                 │ ❌     │ Cannot assign to others         │
#   task.approve                 │ ❌     │ Cannot approve (managers only) │
#   task.reject                 │ ❌     │ Cannot reject (managers only) │
#                               │         │                                │
# SESSION OPERATIONS                                                   │         │                                │
#   session.start                 │ ✅     │ Can start sessions               │
#   session.log                  │ ✅     │ Can log activities             │
#   session.stop                  │ ✅     │ Can stop sessions               │
#                               │         │                                │
# AGENT OPERATIONS                                                      │         │                                │
#   agent.view.all                │ ❌     │ Cannot view other agents        │
#   agent.view_own                │ ✅     │ Can view own profile           │
#   agent.modify                 │ ❌     │ Cannot modify own agent          │
#                               │         │                                │
# ORGANIZATION OPERATIONS                                              │         │                                │
#   org.manage                   │ ❌     │ Cannot manage org (workers only)│
#   org.view                     │ ✅     │ Can view org details            │
#                               │         │                                │
# PROJECT OPERATIONS                                                   │         │                                │
#   project.create                │ ❌     │ Cannot create projects           │
#   project.view.all              │ ✅     │ Can view projects               │
#   project.manage                │ ❌     │ Cannot manage projects          │
#                               │         │                                │
# LOGGING                                                              │         │                                │
#   logs.view_all                 │ ❌     │ Cannot view all logs               │
#   logs.view_own                 │ ✅     │ Can view own logs               │
#                               │         │                                │
# TRUST SCORE                                                          │         │                                │
#   trust_score.view              │ ✅     │ Can view trust scores           │
#   trust_score.modify            │ ❌     │ Cannot modify trust scores       │
#                               │         │                                │
# SECURITY RESTRICTIONS                                                   │         │                                │
#   access.sensitive_data          │ ❌     │ Cannot access sensitive data     │
#   export.data                  │ ❌     │ Cannot export data                │
```

#### Project-Specific Permissions

```bash
# Grant project-level permissions
agentflow permissions grant \
  --agent agent-dev-002 \
  --permission "project.manage:project=mobile-app" \
  --reason "Project lead for mobile-app"

# Output:
# ✅ Permission granted
#    Agent: agent-dev-002 (Alice)
#    Permission: project.manage
#    Scope: project=mobile-app
#    Additional permissions:
#      • task.assign (in mobile-app)
#      • task.approve (for mobile-app tasks)
#      • session.manage (for mobile-app)

# Check project permissions
agentflow permissions project-check mobile-app --agent agent-dev-002

# Output:
# 📋 Project Permissions: mobile-app
# Agent: agent-dev-002 (Alice)
#
# Permissions:
#   ✅ task.create
#   ✅ task.assign (to agents in project)
#   ✅ task.approve (approve project tasks)
#   ✅ session.manage (manage sessions)
#   ✅ project.settings (modify project settings)
#   ✅ project.delete (delete project - DANGER!)
#   ❌ org.manage (not in project scope)

# Create permission group
agentflow permissions create-group \
  --name "mobile-team-leads" \
  --agents agent-dev-002,agent-dev-003 \
  --permissions \
  "task.assign:project=mobile-app" \
  "task.approve:project=mobile-app" \
  "session.manage:project=mobile-app"

# All agents in group get same permissions
```

#### Conditional Permissions

```bash
# Permission with conditions
agentflow permissions grant \
  --agent agent-dev-001 \
  --permission "task.delete" \
  --conditions \
    "task.estimate < 2h" \
    "task.tags does_not_include 'critical'" \
    "task.age > 7d"

# Agent can only delete small, old, non-critical tasks

# Probation restrictions
agentflow permissions grant \
  --agent agent-qa-001 \
  --permission "task.update" \
  --conditions \
    "agent.trust_score > 40" \
    "task.priority != P0"

# Agent on probation cannot update P0 tasks or have low trust
```

#### Permission Inheritance

```bash
# Role inherits permissions from parent
agentflow role create \
  --name "senior-developer" \
  --extends "developer" \
  --additional-permissions \
    "task.review" \
    "task.approve:own_tasks_only" \
    "agent.mentor"

# Senior developer has all developer permissions PLUS:
# - Can review tasks (own tasks only)
# - Can approve tasks (own tasks only)
# - Can mentor other agents

# View permission inheritance
agentflow permissions show-role senior-developer

# Output:
# 📋 Role Permissions: senior-developer
# ─────────────────────────────────────────────────────────────────────────────
#
# Inherits from: developer
#   ✅ task.create
#   ✅ task.update.own
#   ✅ session.start
#   session.log
#
# Additional permissions:
#   ✅ task.review (own tasks only)
#   ✅ task.approve (own tasks only)
#   ✅ agent.mentor
#
# Effective permissions:
#   • Can create tasks
#   • Can update own tasks
#   • Can review own tasks
#   • Can approve own tasks (self-approval allowed)
#   • Can mentor other agents
#   • Can start sessions
#   • Can log activities
#
# Note: Senior developer cannot approve OTHERS' tasks
```

#### Permission Templates

```bash
# Create permission template
agentflow permissions template create \
  --name "project-lead" \
  --permissions \
    "task.assign:project={project}" \
    "task.approve:project={project}" \
    "task.delete:project={project}" \
    "session.manage:project={project}" \
    "project.settings:project={project}"

# Apply template to role
agentflow role apply-template senior-developer \
  --template project-lead \
  --project website-redesign

# Agent can now act as project lead for website-redesign
```

### Data Model

```python
class Permission(BaseModel):
    id: str  # "task.create", "task.delete", etc.
    resource: Optional[str] = None  # Scope: "project=website-redesign"
    action: str  # "create", "read", "update", "delete", "approve", "manage"

class Role(BaseModel):
    id: str
    name: str
    permissions: List[Permission]
    extends_role: Optional[str] = None  # Inherits permissions

class AccessControlList(BaseModel):
    id: str
    agent_id: str
    resource_type: Literal["project", "task", "agent", "org"]
    resource_id: str
    access: Literal["read", "write", "admin", "no_access"]
    conditions: List[str] = []
    granted_by: str
    granted_at: datetime
    expires_at: Optional[datetime] = None
```

### CLI Commands

```bash
# Permissions
agentflow permissions grant --agent <agent> --permission <perm>
agentflow permissions revoke --agent <agent> --permission <perm>
agentflow permissions check --agent <agent> --resource <resource>

# Roles
agentflow role create --name <name> --permissions <perms>
agentflow role apply-template --role <role> --template <template>

# ACLs
agentflow permissions grant --agent <agent> --resource <resource> --access <read|write|admin> --duration <7d>
agentflow permissions revoke --id <acl-id>

# Groups
agentflow permissions create-group --name <name> --agents <a1,a2> --permissions <perms>
```

---

## Implementation Notes

### Dependencies

- **Feature 22 (Audit Trail)**: Requires cryptographic signing, immutable storage
- **Feature 23 (Data Retention)**: Requires policy engine, scheduled jobs
- **Feature 24 (Access Control)**: Requires permission system, RBAC/ABAC

### Priority

1. **Feature 24 (Access Control)** - High value for multi-team scenarios
2. **Feature 22 (Audit Trail)** - Critical for production, Phase 2
3. **Feature 23 (Data Retention)** - Medium value, automated maintenance

### Phasing

- **Phase 1**: Basic role-based permissions, simple audit logging
- **Phase 2**: Cryptographic signing, automated retention
- **Phase 3**: Advanced RBAC/ABAC, fine-grained ACLs

### Security Considerations

- **Audit Trail Protection**: Audit logs must be append-only, signatures must be verifiable
- **Key Management**: Secure storage of signing keys (HMAC secret, private keys)
- **Access Control**: Permission checks on EVERY operation
- **Data Minimization**: Delete data as soon as retention period expires

---

**Document Version**: 1.0
**Created**: 2025-01-21
**Status**: 🎨 Design proposal - Security & Compliance features (Phase 2+)
**Warning**: These features are critical for production use and require significant security infrastructure
