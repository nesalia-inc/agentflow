# Project Commands

Manage projects within organizations.

---

## Commands

- [`create`](#agentflow-project-create) - Create a new project
- [`list`](#agentflow-project-list) - List projects
- [`view`](#agentflow-project-view) - View project details
- [`use`](#agentflow-project-use) - Set active project
- [`delete`](#agentflow-project-delete) - Delete a project

---

## `agentflow project create`

Create a new project.

```bash
agentflow project create \
  --org <slug> \
  --name <name> \
  --slug <slug> \
  [--description <description>] \
  [--github-url <url>]
```

**Flags**:
- `--org`: Organization slug (optional if org active)
- `--name` (required): Project name
- `--slug` (required): Project slug
- `--description`: Project description
- `--github-url`: GitHub repository URL

**With active org**:
```bash
agentflow project create \
  --name "Website Redesign" \
  --slug "website"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "project": {
      "id": "proj_123",
      "organization_id": "org_123",
      "name": "Website Redesign",
      "slug": "website",
      "description": "Complete overhaul",
      "github_url": "https://github.com/acme/website",
      "is_active": true,
      "created_at": "2025-02-03T10:00:00Z"
    }
  }
}
```

**Error Codes**:
- `ORG_NOT_SET`: No active org and --org not provided
- `SLUG_EXISTS`: Project slug already exists in org
- `NOT_FOUND`: Organization not found

---

## `agentflow project list`

List projects in an organization.

```bash
agentflow project list [--org <slug>] [--format <format>]
```

**Response**:
```json
{
  "success": true,
  "data": {
    "organization": {
      "id": "org_123",
      "name": "Acme Corp",
      "slug": "acme"
    },
    "projects": [
      {
        "id": "proj_123",
        "name": "Website Redesign",
        "slug": "website",
        "is_active": true,
        "version_count": 3,
        "task_count": 35,
        "created_at": "2025-02-03T10:00:00Z"
      }
    ],
    "total": 1
  }
}
```

---

## `agentflow project view`

View project details.

```bash
agentflow project view \
  --org <slug> \
  --slug <slug>
```

**Response**:
```json
{
  "success": true,
  "data": {
    "project": {
      "id": "proj_123",
      "name": "Website Redesign",
      "slug": "website",
      "description": "Complete overhaul",
      "github_url": "https://github.com/acme/website",
      "is_active": true,
      "created_at": "2025-02-03T10:00:00Z"
    },
    "versions": [
      {
        "id": "ver_123",
        "version": "1.0.0",
        "name": "Major release",
        "status": "in_progress",
        "task_count": 15,
        "completed_tasks": 3
      }
    ],
    "stats": {
      "version_count": 3,
      "total_tasks": 35,
      "completed_tasks": 23
    }
  }
}
```

---

## `agentflow project use`

Set active project context.

```bash
agentflow project use --slug <slug>
```

**Response**:
```json
{
  "success": true,
  "data": {
    "context": {
      "active_org": "acme",
      "active_project": "website",
      "active_version": null
    },
    "project": {
      "id": "proj_123",
      "name": "Website Redesign",
      "slug": "website"
    }
  },
  "message": "Active project set to Website Redesign (website)"
}
```

---

## `agentflow project delete`

Delete a project.

```bash
agentflow project delete \
  --org <slug> \
  --slug <slug> \
  --confirm
```

**Response**:
```json
{
  "success": true,
  "data": {
    "deleted_project": {
      "id": "proj_123",
      "name": "Website Redesign",
      "slug": "website"
    }
  }
}
```
