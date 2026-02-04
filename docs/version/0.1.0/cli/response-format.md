# Response Format - v0.1.0

All CLI commands return structured JSON responses for consistent parsing and automation.

---

## Success Response

### Structure

```json
{
  "success": true,
  "data": {
    // Entity-specific data
  },
  "message": "Optional human-readable message",
  "metadata": {
    "timestamp": "2025-02-03T10:00:00Z",
    "request_id": "req_abc123",
    "version": "0.1.0"
  }
}
```

### Examples

**Simple response**:
```json
{
  "success": true,
  "data": {
    "organization": {
      "id": "org_123",
      "name": "Acme Corp",
      "slug": "acme"
    }
  },
  "message": "Organization created successfully"
}
```

**Collection response**:
```json
{
  "success": true,
  "data": {
    "organizations": [
      { "id": "org_123", "name": "Acme Corp", "slug": "acme" },
      { "id": "org_456", "name": "Another Org", "slug": "another" }
    ],
    "total": 2,
    "page": 1,
    "per_page": 20
  }
}
```

---

## Error Response

### Structure

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      // Additional error context
    }
  },
  "metadata": {
    "timestamp": "2025-02-03T10:00:00Z",
    "request_id": "req_abc123"
  }
}
```

### Examples

**Not found**:
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Organization not found",
    "details": {
      "resource": "organization",
      "slug": "nonexistent"
    }
  }
}
```

**Validation error**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {
      "field": "slug",
      "issue": "Slug must contain only lowercase letters, numbers, and hyphens"
    }
  }
}
```

**Authorization error**:
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_LEVEL",
    "message": "Your authority level is too low for this action",
    "details": {
      "required_level": 5,
      "your_level": 3
    }
  }
}
```

---

## Output Formats

### JSON Format (Default)

Structured, machine-readable output:

```bash
$ agentflow org list --format json
```

```json
{
  "success": true,
  "data": {
    "organizations": [
      { "id": "org_123", "name": "Acme Corp", "slug": "acme" }
    ],
    "total": 1
  }
}
```

### Table Format

Human-readable ASCII table:

```bash
$ agentflow org list --format table
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    Organizations                         ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Slug      Name              Status      Created           ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ acme      Acme Corp         Active      2025-02-03        ┃
┃ startup   My Startup        Active      2025-02-01        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
Total: 2 organizations
```

### CSV Format

Comma-separated values for data export:

```bash
$ agentflow org list --format csv
```

```csv
id,name,slug,status,created_at
org_123,Acme Corp,acme,active,2025-02-03T10:00:00Z
org_456,My Startup,startup,active,2025-02-01T10:00:00Z
```

### Raw Format

IDs only, useful for scripting and piping:

```bash
$ agentflow org list --format raw
```

```
org_123
org_456
```

**Example with piping**:
```bash
# Get all org IDs and process each one
agentflow org list --format raw | while read org_id; do
  agentflow org view --slug "$org_id"
done
```

---

## Pagination

List commands that return multiple items support pagination:

```bash
agentflow task list --page 2 --per-page 50
```

**Response**:
```json
{
  "success": true,
  "data": {
    "tasks": [ /* ... */ ],
    "total": 150,
    "page": 2,
    "per_page": 50,
    "total_pages": 3
  }
}
```

---

## Filtering

List commands support filtering via flags:

```bash
# Filter by status
agentflow task list --status "in_progress"

# Filter by priority
agentflow task list --priority "P0"

# Filter by agent
agentflow task list --agent "agent_123"

# Combine filters
agentflow task list --status "in_progress" --priority "P0"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "filter": {
      "status": "in_progress",
      "priority": "P0",
      "agent": "agent_123"
    },
    "tasks": [ /* ... */ ],
    "total": 3
  }
}
```

---

## Exit Codes

| Code | Meaning | Usage |
|------|---------|-------|
| `0` | Success | Script continues |
| `1` | Generic error | Check response for details |
| `2` | Authentication error | Re-authenticate needed |
| `3` | Not found | Resource doesn't exist |
| `4` | Validation error | Fix input and retry |
| `5` | API error | Server-side problem, retry later |

**Example**:
```bash
agentflow task start --task-id "task_123"
exit_code=$?

if [ $exit_code -eq 0 ]; then
  echo "Task started successfully"
else
  echo "Error starting task (exit code: $exit_code)"
fi
```

---

## Metadata

All responses include metadata:

```json
{
  "success": true,
  "data": { /* ... */ },
  "metadata": {
    "timestamp": "2025-02-03T10:00:00Z",
    "request_id": "req_abc123",
    "version": "0.1.0",
    "server_time": "2025-02-03T10:00:15Z",
    "execution_time_ms": 45
  }
}
```

**Fields**:
- `timestamp`: When the request was received
- `request_id`: Unique identifier for support/debugging
- `version`: API version
- `server_time`: Server's current time
- `execution_time_ms**: Request processing time in milliseconds

---

## Request ID for Support

Always include the `request_id` when reporting issues:

```bash
$ agentflow task start --task-id "task_123"
{
  "success": false,
  "error": { "code": "SERVER_ERROR", "message": "..." },
  "metadata": {
    "request_id": "req_abc123"
  }
}
```

When reporting: "Request ID: req_abc123 failed with SERVER_ERROR"
