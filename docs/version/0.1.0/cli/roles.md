# Role Commands

Roles are **global templates** defined at the user level, independent of organizations. A role defines skills, competencies, rules, and **authority level** (1-10) for security.

## Concepts

- **Global**: Roles exist at the user level, not tied to organizations
- **Reusable**: Can be instantiated as multiple agents
- **Hierarchical**: Each role has an authority level (1-10)
- **Documented**: Roles have documents that define skills and rules

---

## Commands

- [`create`](#agentflow-role-create) - Create a new role
- [`list`](#agentflow-role-list) - List all roles
- [`view`](#agentflow-role-view) - View role details and documents
- [`update`](#agentflow-role-update) - Update role properties
- [`add-document`](#agentflow-role-add-document) - Add a document to a role
- [`list-documents`](#agentflow-role-list-documents) - List role documents
- [`remove-document`](#agentflow-role-remove-document) - Remove a document
- [`delete`](#agentflow-role-delete) - Delete a role

---

## `agentflow role create`

Create a new role (global, no organization required).

```bash
agentflow role create \
  --name <name> \
  --slug <slug> \
  --level <level> \
  [--description <description>]
```

**Flags**:
- `--name` (required): Role name
- `--slug` (required): URL-friendly identifier
- `--level` (required): Authority level (1-10)
- `--description`: Role description

**Authority Levels**:
- **1-2**: Junior roles (basic tasks)
- **3-4**: Senior roles (complex tasks)
- **5-6**: Lead roles (can manage juniors)
- **7-8**: Architect roles (strategic decisions)
- **9-10**: C-level roles (executive decisions)

**Examples**:
```bash
# Junior role
agentflow role create \
  --name "Junior Developer" \
  --slug "junior-dev" \
  --level 1

# Senior role
agentflow role create \
  --name "Senior Developer" \
  --slug "senior-dev" \
  --level 3 \
  --description "Expert in multiple technologies"

# CTO role
agentflow role create \
  --name "CTO" \
  --slug "cto" \
  --level 10 \
  --description "Chief Technology Officer"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "role": {
      "id": "role_abc123",
      "user_id": "user_123",
      "name": "Frontend Developer",
      "slug": "frontend-dev",
      "level": 3,
      "description": "Expert React, TypeScript et UX",
      "document_count": 0,
      "created_at": "2025-02-03T10:00:00Z"
    }
  },
  "message": "Role created successfully"
}
```

**Error Codes**:
- `SLUG_EXISTS`: Role slug already exists for this user
- `INVALID_SLUG`: Slug format invalid
- `INVALID_LEVEL`: Level must be between 1 and 10
- `UNAUTHENTICATED`: User not logged in

---

## `agentflow role list`

List all roles for the current user.

```bash
agentflow role list [--format <format>]
```

**Flags**:
- `--format`: Output format (json|table|csv|raw, default: json)

**Response**:
```json
{
  "success": true,
  "data": {
    "roles": [
      {
        "id": "role_abc123",
        "name": "Frontend Developer",
        "slug": "frontend-dev",
        "level": 3,
        "description": "Expert React, TypeScript et UX",
        "document_count": 3,
        "agent_count": 5,
        "created_at": "2025-02-03T10:00:00Z"
      },
      {
        "id": "role_def456",
        "name": "Backend Developer",
        "slug": "backend-dev",
        "level": 3,
        "description": "Expert Python, PostgreSQL, APIs",
        "document_count": 5,
        "agent_count": 3,
        "created_at": "2025-02-03T11:00:00Z"
      }
    ],
    "total": 2
  }
}
```

---

## `agentflow role view`

View role details and documents.

```bash
agentflow role view --slug <slug>
```

**Flags**:
- `--slug` (required): Role slug

**Response**:
```json
{
  "success": true,
  "data": {
    "role": {
      "id": "role_abc123",
      "name": "Frontend Developer",
      "slug": "frontend-dev",
      "level": 3,
      "description": "Expert React, TypeScript et UX",
      "created_at": "2025-02-03T10:00:00Z"
    },
    "documents": [
      {
        "id": "doc_123",
        "title": "React Best Practices",
        "content": "# React Best Practices\n\n- Use functional components...",
        "created_at": "2025-02-03T10:30:00Z"
      },
      {
        "id": "doc_456",
        "title": "TypeScript Guidelines",
        "content": "# TypeScript Guidelines\n\n...",
        "created_at": "2025-02-03T11:00:00Z"
      }
    ],
    "stats": {
      "document_count": 2,
      "agent_count": 5
    }
  }
}
```

**Error Codes**:
- `NOT_FOUND`: Role not found
- `ACCESS_DENIED`: Role belongs to different user

---

## `agentflow role update`

Update role properties.

```bash
agentflow role update \
  --slug <slug> \
  [--name <name>] \
  [--description <description>]
```

**Flags**:
- `--slug` (required): Role slug
- `--name`: New name
- `--description`: New description

**Note**: Cannot change level after creation (create new role instead).

**Response**:
```json
{
  "success": true,
  "data": {
    "role": {
      "id": "role_abc123",
      "name": "Senior Frontend Developer",
      "slug": "frontend-dev",
      "level": 3,
      "description": "Updated description",
      "updated_at": "2025-02-03T12:00:00Z"
    }
  },
  "message": "Role updated successfully"
}
```

---

## `agentflow role add-document`

Add a document to a role. Documents contain the skills, rules, and best practices that agents will use.

```bash
agentflow role add-document \
  --role <slug> \
  --title <title> \
  [--content <content>] \
  [--file <path>]
```

**Flags**:
- `--role` (required): Role slug
- `--title` (required): Document title
- `--content`: Document content (markdown)
- `--file`: Path to markdown file (alternative to --content)

**With content**:
```bash
agentflow role add-document \
  --role "frontend-dev" \
  --title "React Best Practices" \
  --content "# React Best Practices

- Use functional components with hooks
- Implement proper error boundaries
- Follow React performance optimization patterns
- Always handle loading and error states
- Use TypeScript for type safety"
```

**With file**:
```bash
agentflow role add-document \
  --role "frontend-dev" \
  --title "Coding Standards" \
  --file ./standards/react.md
```

**Response**:
```json
{
  "success": true,
  "data": {
    "document": {
      "id": "doc_789",
      "role_id": "role_abc123",
      "title": "React Best Practices",
      "content": "# React Best Practices...",
      "created_at": "2025-02-03T13:00:00Z"
    }
  },
  "message": "Document added to role frontend-dev"
}
```

**Error Codes**:
- `NOT_FOUND`: Role not found
- `FILE_NOT_FOUND`: Specified file does not exist
- `NO_CONTENT`: Must provide either --content or --file

---

## `agentflow role list-documents`

List all documents in a role.

```bash
agentflow role list-documents --slug <slug> [--format <format>]
```

**Flags**:
- `--slug` (required): Role slug
- `--format`: Output format

**Response**:
```json
{
  "success": true,
  "data": {
    "role": {
      "id": "role_abc123",
      "name": "Frontend Developer",
      "slug": "frontend-dev"
    },
    "documents": [
      {
        "id": "doc_123",
        "title": "React Best Practices",
        "created_at": "2025-02-03T10:30:00Z"
      },
      {
        "id": "doc_456",
        "title": "TypeScript Guidelines",
        "created_at": "2025-02-03T11:00:00Z"
      }
    ],
    "total": 2
  }
}
```

---

## `agentflow role remove-document`

Remove a document from a role.

```bash
agentflow role remove-document \
  --role <slug> \
  --document <document-id> \
  --confirm
```

**Flags**:
- `--role` (required): Role slug
- `--document` (required): Document ID
- `--confirm`: Required to prevent accidental deletion

**Response**:
```json
{
  "success": true,
  "data": {
    "deleted_document": {
      "id": "doc_123",
      "title": "React Best Practices"
    }
  },
  "message": "Document removed from role"
}
```

**Error Codes**:
- `NOT_FOUND`: Role or document not found
- `ACCESS_DENIED`: Document belongs to different role

---

## `agentflow role delete`

Delete a role.

```bash
agentflow role delete --slug <slug> --confirm
```

**Flags**:
- `--slug` (required): Role slug
- `--confirm`: Required to prevent accidental deletion

**Response**:
```json
{
  "success": true,
  "data": {
    "deleted_role": {
      "id": "role_abc123",
      "name": "Frontend Developer",
      "slug": "frontend-dev"
    }
  },
  "message": "Role deleted successfully"
}
```

**Error Codes**:
- `NOT_FOUND`: Role not found
- `ACCESS_DENIED`: Role belongs to different user
- `IN_USE`: Role is used by existing agents (must delete agents first)

---

## Role Level System

### Level Capabilities

| Level | Can Create Agents | Can Work On Tasks |
|-------|------------------|-------------------|
| 1 | None | Level 1 tasks only |
| 2 | Level 1 agents | Levels 1-2 tasks |
| 3 | Level 1-2 agents | Levels 1-3 tasks |
| 4 | Level 1-3 agents | Levels 1-4 tasks |
| 5 | Level 1-4 agents | Levels 1-5 tasks |
| 6 | Level 1-5 agents | Levels 1-6 tasks |
| 7 | Level 1-6 agents | Levels 1-7 tasks |
| 8 | Level 1-7 agents | Levels 1-8 tasks |
| 9 | Level 1-8 agents | Levels 1-9 tasks |
| 10 | Level 1-9 agents | All levels (CEO level) |

### Example Role Hierarchy

```bash
# Level 1: Junior Developer
agentflow role create \
  --name "Junior Developer" \
  --slug "junior-dev" \
  --level 1 \
  --description "Entry-level developer"

# Level 3: Senior Developer
agentflow role create \
  --name "Senior Developer" \
  --slug "senior-dev" \
  --level 3 \
  --description "Experienced developer, can mentor juniors"

# Level 5: Tech Lead
agentflow role create \
  --name "Tech Lead" \
  --slug "tech-lead" \
  --level 5 \
  --description "Team leader, can review code and architecture"

# Level 10: CTO
agentflow role create \
  --name "CTO" \
  --slug "cto" \
  --level 10 \
  --description "Chief Technology Officer, full organizational control"
```

---

## Examples

### Complete Role Setup

```bash
# 1. Create role
agentflow role create \
  --name "Frontend Developer" \
  --slug "frontend-dev" \
  --level 3 \
  --description "Expert React, TypeScript and UX"

# 2. Add best practices document
agentflow role add-document \
  --role "frontend-dev" \
  --title "React Best Practices" \
  --content "# React Best Practices
- Use functional components
- Implement proper error boundaries
- Optimize performance
- Use TypeScript for type safety"

# 3. Add coding standards
agentflow role add-document \
  --role "frontend-dev" \
  --title "Code Style Guide" \
  --file ./standards/frontend.md

# 4. View role
agentflow role view --slug "frontend-dev"

# 5. List documents
agentflow role list-documents --slug "frontend-dev"
```

### Using Roles for Agents

```bash
# Create agent from role
agentflow agent create \
  --role "frontend-dev" \
  --name "Alice"

# Agent inherits the role's level and documents
```
