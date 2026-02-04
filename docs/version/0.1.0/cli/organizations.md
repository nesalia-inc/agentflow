# Organization Commands

Manage organizations in AgentFlow.

---

## Commands

- [`create`](#agentflow-org-create) - Create a new organization
- [`list`](#agentflow-org-list) - List organizations
- [`view`](#agentflow-org-view) - View organization details
- [`use`](#agentflow-org-use) - Set active organization
- [`delete`](#agentflow-org-delete) - Delete an organization

---

## `agentflow org create`

Create a new organization.

```bash
agentflow org create \
  --name <name> \
  --slug <slug> \
  [--description <description>]
```

**Flags**:
- `--name` (required): Organization name
- `--slug` (required): URL-friendly identifier
- `--description`: Organization description

**Response**:
```json
{
  "success": true,
  "data": {
    "organization": {
      "id": "org_123",
      "name": "Acme Corp",
      "slug": "acme",
      "description": "Tech startup",
      "owner_id": "user_123",
      "created_at": "2025-02-03T10:00:00Z"
    }
  },
  "message": "Organization created successfully"
}
```

**Error Codes**:
- `SLUG_EXISTS`: Organization slug already exists
- `INVALID_SLUG`: Slug format invalid
- `UNAUTHENTICATED`: User not logged in

---

## `agentflow org list`

List all organizations the user is a member of.

```bash
agentflow org list [--format <format>]
```

**Flags**:
- `--format`: Output format (json|table|csv|raw, default: json)

**Response**:
```json
{
  "success": true,
  "data": {
    "organizations": [
      {
        "id": "org_123",
        "name": "Acme Corp",
        "slug": "acme",
        "role": "owner",
        "project_count": 2,
        "member_count": 5,
        "created_at": "2025-02-03T10:00:00Z"
      }
    ],
    "total": 1
  }
}
```

---

## `agentflow org view`

View organization details.

```bash
agentflow org view --slug <slug>
```

**Flags**:
- `--slug` (required): Organization slug

**Response**:
```json
{
  "success": true,
  "data": {
    "organization": {
      "id": "org_123",
      "name": "Acme Corp",
      "slug": "acme",
      "description": "Tech startup",
      "owner": {
        "id": "user_123",
        "email": "david@example.com",
        "name": "David"
      },
      "created_at": "2025-02-03T10:00:00Z"
    },
    "projects": [
      {
        "id": "proj_123",
        "name": "Website Redesign",
        "slug": "website"
      }
    ],
    "members": [
      {
        "id": "user_123",
        "email": "david@example.com",
        "name": "David",
        "role": "owner"
      }
    ],
    "stats": {
      "project_count": 1,
      "member_count": 1
    }
  }
}
```

**Error Codes**:
- `NOT_FOUND`: Organization not found
- `ACCESS_DENIED`: User not a member

---

## `agentflow org use`

Set active organization context.

```bash
agentflow org use --slug <slug>
```

**Flags**:
- `--slug` (required): Organization slug

**Response**:
```json
{
  "success": true,
  "data": {
    "context": {
      "active_org": "acme",
      "active_project": null,
      "active_version": null
    },
    "organization": {
      "id": "org_123",
      "name": "Acme Corp",
      "slug": "acme"
    }
  },
  "message": "Active organization set to Acme Corp (acme)"
}
```

**Side Effect**: Updates `~/.agentflow/context.json`

---

## `agentflow org delete`

Delete an organization.

```bash
agentflow org delete --slug <slug> --confirm
```

**Flags**:
- `--slug` (required): Organization slug
- `--confirm`: Required to prevent accidental deletion

**Response**:
```json
{
  "success": true,
  "data": {
    "deleted_organization": {
      "id": "org_123",
      "name": "Acme Corp",
      "slug": "acme"
    }
  },
  "message": "Organization deleted successfully"
}
```

**Error Codes**:
- `NOT_FOUND`: Organization not found
- `ACCESS_DENIED`: User not owner
- `NOT_EMPTY`: Organization has projects (must delete first)

---

## Examples

```bash
# Create organization
agentflow org create \
  --name "My Startup" \
  --slug "mystartup" \
  --description "Tech company"

# Set as active
agentflow org use --slug "mystartup"

# View details
agentflow org view --slug "mystartup"

# List all
agentflow org list --format table
```
