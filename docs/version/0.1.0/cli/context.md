# Context Management

Manage active context for efficient CLI usage.

---

## Context File

**Location**: `~/.agentflow/context.json`

**Structure**:
```json
{
  "api_key": "ak_live_...",
  "user": {
    "id": "user_123",
    "email": "david@example.com",
    "name": "David"
  },
  "active_org": "acme",
  "active_project": "website",
  "active_version": null
}
```

---

## `agentflow use`

Set organization and project in one command.

```bash
agentflow use --org <slug> --project <slug>
```

**Response**:
```json
{
  "success": true,
  "data": {
    "context": {
      "active_org": "acme",
      "active_project": "website"
    }
  },
  "message": "Context set to acme/website"
}
```

---

## Context Resolution Order

1. **Flags override everything**
2. **Active context from file**
3. **Error if required context missing**

**Example**:
```bash
# Uses acme from context, overrides project
agentflow task list --project "api"

# Uses both from context
agentflow task list

# Error: no org in context
agentflow task list
# → Error: No active organization. Use --org flag or run 'agentflow org use'
```

---

## Prompt Display

```bash
# No context
$ agentflow task list

# Org context
[acme] $ agentflow task list

# Org + project context
[acme/website] $ agentflow task list

# With version
[acme/website@1.0.0] $
```
