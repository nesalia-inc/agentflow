# v0.1.0 Analysis - Next.js + PayloadCMS Architecture

**Date**: 2025-02-03
**Version**: 0.1.0-pre
**Status**: Exploratory Analysis

---

## Executive Summary

The v0.1.0 proposal consists of **reversing the implementation order** by starting with a web interface using Next.js and PayloadCMS, then adding a CLI on top, rather than the original CLI-first approach.

---

## Current Planned Architecture

### Original Roadmap

```
Phase 0 → Phase 1 → Phase 2
   ↓         ↓          ↓
CLI     API (Hono)   Web (Next.js)
Local     tRPC        Dashboard
JSON    PostgreSQL   Interface
```

**Phase 0** (current):
- Python CLI with Typer
- Local JSON storage (~/.agentflow/data.json)
- No backend, no database
- Goal: Validate command UX

**Phase 1** (future):
- Hono + tRPC API
- PostgreSQL + Drizzle ORM
- Migrate CLI to HTTP client

**Phase 2** (future):
- Next.js Dashboard
- tRPC client for type safety
- TanStack Query + Zustand

---

## New v0.1.0 Proposal

### Proposed Architecture

```
v0.1.0
   ↓
Next.js + PayloadCMS
   ├── Public website
   ├── Integrated REST/GraphQL API
   ├── Payload admin panel
   └── CLI (Python) consumer
```

### Proposed Tech Stack

- **Frontend**: Next.js 15 (App Router)
- **CMS**: PayloadCMS 3.x
- **Database**: PostgreSQL
- **ORM**: Drizzle ORM (via Payload)
- **CLI**: Python 3.14 + Typer + httpx
- **Auth**: NextAuth.js or Payload Auth

---

## Approach Comparison

### 1. Development Order

| Aspect | Original Approach | v0.1.0 Approach |
|--------|-------------------|-----------------|
**First deliverable** | Functional CLI | Complete web interface |
**Validation** | Terminal command UX | Web user experience |
**Target audience** | Technical users | Non-technical users |
**Initial backend** | Local JSON storage | Full REST API + CMS |

### 2. Technical Implications

#### PayloadCMS vs Hono + tRPC

| Criteria | Hono + tRPC | PayloadCMS |
|---------|-------------|------------|
**Base type** | Pure API framework | Headless CMS |
**Advantages** | Full type safety, RPC | Auto-generated admin panel, automatic CRUD |
**Disadvantages** | Admin panel to build | Less flexible API-side |
**Learning curve** | tRPC to master | CMS concepts to learn |
**Best for** | Custom API, complex business logic | CRUD apps, content management |

#### Authentication

| Aspect | Original Approach | v0.1.0 with Payload |
|--------|-------------------|---------------------|
**CLI Auth** | Custom API keys | API keys via Payload |
**Web Auth** | NextAuth.js + tRPC | Payload Auth or NextAuth |
**Users** | Custom users table | Payload Users Collection |
**Permissions** | Custom RBAC | Payload Access Control |

### 3. Developer Experience (DX)

#### v0.1.0 Positives

1. **Immediate Admin Panel**
   - Payload automatically generates admin interface
   - CRUD on all entities without frontend code
   - Quickly validate data model

2. **Public Website**
   - Next.js App Router + Payload = easy website
   - Integrated documentation, landing page, blog
   - SEO friendly from the start

3. **Documented API**
   - Payload automatically generates OpenAPI/GraphQL
   - CLI can consume API directly
   - No separate API schema maintenance

4. **Natural Monorepo**
   ```
   apps/
   ├── web/          # Next.js + Payload
   ├── admin/        # Payload Admin (optional)
   └── cli/          # Python CLI consumer
   ```

#### Potential Negatives

1. **CMS Coupling**
   - Payload imposes its data structure
   - Less flexible than custom Hono API
   - "CMS" vs "API" mindset patterns

2. **Performance**
   - Heavier than Hono
   - Overhead for simple operations
   - Edge hosting more complex

3. **Initial Complexity**
   - More concepts to learn (Payload blocks, globals, collections)
   - Heavier initial configuration

---

## Essential Design Questions

### 1. Role Management

**Question**: How are agent roles managed?

**Options**:

| Option A - Payload Collection | Option B - Files + Sync | Option C - Code Roles |
|------------------------------|---------------------------|----------------------|
Roles in DB | Roles in Git + sync | Roles in code |
Pro: Edit UI | Pro: Git versioning | Pro: Type safety |
Con: No Git | Con: Complex sync | Con: No UI |

**Recommendation**: Option A for v0.1.0 (speed), migrate to B later.

### 2. CLI Integration

**Question**: How does Python CLI interact with Payload?

**Options**:

| Option REST | Option GraphQL | Option SDK |
|-------------|---------------|------------|
Standard REST API | GraphQL endpoint | Generated Python SDK |
Simple, universal | Type safety | Better DX |

**Recommendation**: Option REST to start (httpx), consider GraphQL later if needed.

### 3. Skills Generation

**Question**: Where and how are Claude Code skills generated?

**Current Flow**:
```
Role (DB) → CLI Pull → Generate skills → ~/.claude/skills/
```

**v0.1.0 Flow**:
```
Role (Payload Collection) → REST API → Python CLI → Generate skills → ~/.claude/skills/
```

**Consideration**: Payload can serve role documents via REST API.

### 4. Agent Authentication

**Question**: Do agents authenticate with API keys?

**Payload Support**:
- Payload has built-in API key system
- Can be extended for agents
- JWT tokens also supported

**Recommendation**: API keys with hash in Payload (similar to current design).

---

## Recommended v0.1.0 Architecture

### Project Structure

```
agentflow/
├── apps/
│   ├── web/                      # Next.js 15 + PayloadCMS
│   │   ├── src/
│   │   │   ├── app/              # Next.js App Router
│   │   │   │   ├── (marketing)/  # Public site
│   │   │   │   ├── (app)/        # App dashboard
│   │   │   │   └── api/          # API routes
│   │   │   ├── collections/      # Payload collections
│   │   │   │   ├── Users.ts
│   │   │   │   ├── Workspaces.ts
│   │   │   │   ├── Projects.ts
│   │   │   │   ├── Agents.ts
│   │   │   │   ├── Roles.ts
│   │   │   │   └── ...
│   │   │   ├── globals/          # Payload globals
│   │   │   └── components/       # React components
│   │   ├── payload.config.ts     # Payload config
│   │   ├── next.config.ts
│   │   └── package.json
│   │
│   └── cli/                      # Python CLI (API consumer)
│       ├── agentflow/
│       │   ├── cli.py            # Typer CLI
│       │   ├── client.py         # HTTP client (httpx)
│       │   ├── models.py         # Pydantic models
│       │   ├── commands/         # CLI commands
│       │   └── utils/
│       └── pyproject.toml
│
├── packages/
│   └── shared/                   # Shared types (if needed)
│       └── types.ts
│
├── docs/
│   └── version/
│       └── 0.1.0/                # v0.1.0 documentation
│           ├── ANALYSIS.md       # This document
│           ├── DESIGN.md         # Detailed design
│           └── API.md            # API specification
│
└── package.json
```

### Payload Collections (v0.1.0 MVP)

```typescript
// collections/Users.ts
{
  slug: 'users',
  fields: [
    { name: 'email', type: 'email', required: true },
    { name: 'name', type: 'text', required: true },
    { name: 'apiKey', type: 'text', hidden: true },
  ]
}

// collections/Workspaces.ts
{
  slug: 'workspaces',
  fields: [
    { name: 'name', type: 'text', required: true },
    { name: 'slug', type: 'text', required: true },
    { name: 'owner', type: 'relationship', relationTo: 'users' },
  ]
}

// collections/Projects.ts
{
  slug: 'projects',
  fields: [
    { name: 'name', type: 'text', required: true },
    { name: 'slug', type: 'text', required: true },
    { name: 'workspace', type: 'relationship', relationTo: 'workspaces' },
    { name: 'githubUrl', type: 'text' },
  ]
}

// collections/Agents.ts
{
  slug: 'agents',
  fields: [
    { name: 'agentCode', type: 'text', required: true },
    { name: 'name', type: 'text', required: true },
    { name: 'role', type: 'relationship', relationTo: 'roles' },
    { name: 'workspace', type: 'relationship', relationTo: 'workspaces' },
    { name: 'project', type: 'relationship', relationTo: 'projects' },
    { name: 'trustScore', type: 'number', default: 50 },
    { name: 'status', type: 'select', options: ['active', 'probation', 'inactive'] },
  ]
}

// collections/Roles.ts
{
  slug: 'roles',
  fields: [
    { name: 'title', type: 'text', required: true },
    { name: 'slug', type: 'text', required: true },
    { name: 'documents', type: 'array', fields: [
      { name: 'title', type: 'text' },
      { name: 'content', type: 'richText' },
    ]},
  ]
}

// collections/Sessions.ts (Phase 2)
// collections/Events.ts (Phase 2)
// collections/Tasks.ts (Phase 2)
```

---

## v0.1.0 Roadmap

### Week 1-2: Setup + Core Collections

- [ ] Initialize Next.js 15 + PayloadCMS
- [ ] Configure PostgreSQL (local + Docker)
- [ ] Create collections: Users, Workspaces, Projects
- [ ] Configure Payload auth
- [ ] Functional admin panel

### Week 3-4: Agents + Roles

- [ ] Agents collection
- [ ] Roles collection with documents
- [ ] API endpoint for role pulling
- [ ] API testing with curl/Postman

### Week 5-6: Python CLI

- [ ] Initialize Python CLI project (apps/cli)
- [ ] Implement HTTP client (httpx)
- [ ] Auth commands (login, api-keys)
- [ ] Workspace/project commands
- [ ] `agent pull` command (skills generation)

### Week 7-8: Frontend + Polish

- [ ] User dashboard Next.js
- [ ] Agent management interface
- [ ] Role management interface
- [ ] Public documentation site
- [ ] E2E testing

---

## v0.1.0 Benefits

1. **Immediate Visual Interface**
   - Visual validation of data model
   - Easier onboarding for new users
   - Admin panel for daily management

2. **Auto-Documented API**
   - Payload generates OpenAPI/GraphQL
   - Python CLI consumes API directly
   - No manual schema maintenance

3. **Included Website**
   - Landing page for the project
   - Integrated documentation
   - Blog for updates

4. **More "Market-Ready"**
   - More complete visual product
   - Easier to demonstrate
   - Attractive to early adopters

---

## Risks and Drawbacks

1. **Initial Overhead**
   - PayloadCMS imposes specific patterns
   - More concepts to learn
   - More complex setup than Hono alone

2. **Less API Flexibility**
   - Payload optimized for CRUD
   - Complex operations more difficult
   - May require custom routes

3. **Performance**
   - Heavier than pure Hono
   - Added latency from CMS layer
   - Edge hosting more complex

4. **Payload Dependency**
   - Roadmap depends on PayloadCMS
   - Breaking changes to manage
   - Potential vendor lock-in

---

## Recommendations

### If choosing v0.1.0:

1. **Start Simple**
   - MVP with core collections only
   - No sessions/events/timeline initially
   - Payload admin panel as main UI

2. **Careful API Design**
   - Structure Payload collections to reflect existing design
   - Maintain compatibility with design decisions already made
   - Document REST endpoints for CLI

3. **Python CLI in Parallel**
   - Don't wait for web to finish before starting CLI
   - Develop both in tandem
   - Validate API with CLI as soon as possible

4. **Clear Migration Path**
   - Keep data schemas compatible with existing design
   - Plan exit strategy if Payload doesn't fit
   - Document differences from Hono + tRPC architecture

### Hybrid Alternative

**Option**: Start with Payload for admin, but plan migration to Hono + tRPC for v0.2.0

```
v0.1.0: Next.js + Payload (Admin + CRUD)
v0.2.0: Add Hono + tRPC for complex business logic
v0.3.0: Full transition to Hono, Payload becomes admin-only
```

---

## Next Steps

1. **Decide**: Yes/No on PayloadCMS for v0.1.0
2. **If Yes**: Create DESIGN.md with detailed Payload schemas
3. **If No**: Continue with original CLI-first approach

---

**Status**: Awaiting decision
**Author**: Analysis prepared for discussion
**Next step**: Team validation of approach
