# Error Codes Reference

All errors follow this structure:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": {}
  }
}
```

---

## General Errors

| Code | Description |
|------|-------------|
| `UNAUTHENTICATED` | No valid API key |
| `INVALID_CREDENTIALS` | Email or password incorrect |
| `EMAIL_EXISTS` | Email already registered |
| `WEAK_PASSWORD` | Password does not meet requirements |
| `NOT_FOUND` | Resource not found |
| `SLUG_EXISTS` | Slug already exists |
| `INVALID_SLUG` | Slug format invalid |
| `INVALID_LEVEL` | Level must be between 1 and 10 |
| `ACCESS_DENIED` | User lacks permission |
| `NOT_EMPTY` | Cannot delete resource with dependencies |
| `ORG_NOT_SET` | No active organization |
| `PROJECT_NOT_SET` | No active project |
| `VERSION_NOT_FOUND` | Version does not exist |
| `INVALID_VERSION` | Version format invalid (not semver) |
| `INVALID_STATUS` | Invalid status transition |
| `ALREADY_STARTED` | Task already in progress |
| `INCOMPLETE_TASKS` | Cannot release version with incomplete tasks |
| `INVALID_PRIORITY` | Priority must be P0-P3 |

---

## Security & Authorization Errors

| Code | Description |
|------|-------------|
| `INSUFFICIENT_LEVEL` | Agent level too low for this action |
| `TASK_LEVEL_TOO_HIGH` | Task requires higher authority level |
| `CANNOT_CREATE_HIGHER_LEVEL` | Cannot create agent with higher level |
| `CANNOT_IMPERSONATE_CREATOR` | Cannot impersonate agent's creator |
| `CANNOT_MODIFY_OWN_AGENT` | Cannot modify own agent attributes |
| `CANNOT_MODIFY_CREATOR` | Cannot modify the agent that created you |
| `ASSIGNED_TO_OTHER` | Task is assigned to another agent |
| `CANNOT_VIEW_ALL_TASKS` | `--all` requires CEO/user mode |
| `COMMAND_NOT_AVAILABLE` | Command not available in agent CLI |
| `ROLE_LEVEL_MISMATCH` | Role level exceeds agent's maximum |
| `INACTIVE_AGENT` | Agent is inactive or on probation |
| `HAS_ASSIGNED_TASKS` | Agent has assigned tasks (must reassign first) |

---

## Validation Errors

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Invalid input data |
| `REQUIRED_FIELD_MISSING` | Required field not provided |
| `INVALID_FORMAT` | Field format is invalid |
| `NO_CONTENT` | Must provide either --content or --file |
| `FILE_NOT_FOUND` | Specified file does not exist |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Generic error |
| `2` | Authentication error |
| `3` | Not found |
| `4` | Validation error |
| `5` | API error |
