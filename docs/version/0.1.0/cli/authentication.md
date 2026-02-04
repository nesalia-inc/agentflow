# Authentication Commands

User authentication for the `agentflow` CLI.

---

## Commands

- [`register`](#agentflow-auth-register) - Create a new user account
- [`login`](#agentflow-auth-login) - Authenticate and store API key
- [`logout`](#agentflow-auth-logout) - Clear local credentials
- [`status`](#agentflow-auth-status) - Check authentication status

---

## `agentflow auth register`

Create a new user account.

```bash
agentflow auth register \
  --email <email> \
  --password <password> \
  --name <name>
```

**Flags**:
- `--email` (required): User email address
- `--password` (required): Password
- `--name` (required): Full name

**Response**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_123",
      "email": "david@example.com",
      "name": "David",
      "created_at": "2025-02-03T10:00:00Z"
    },
    "api_key": "ak_live_..."
  },
  "message": "Account created successfully"
}
```

**Error Codes**:
- `EMAIL_EXISTS`: Email already registered
- `INVALID_EMAIL`: Email format invalid
- `WEAK_PASSWORD`: Password too weak

---

## `agentflow auth login`

Authenticate and store API key locally.

```bash
agentflow auth login \
  --email <email> \
  --password <password>
```

**Alternative** (with API key):
```bash
agentflow auth login --api-key <api_key>
```

**Flags**:
- `--email`: User email
- `--password`: User password
- `--api-key`: API key (alternative to email+password)

**Response**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_123",
      "email": "david@example.com",
      "name": "David"
    },
    "api_key": "ak_live_..."
  },
  "message": "Logged in successfully"
}
```

**Side Effect**: Writes to `~/.agentflow/context.json`

**Error Codes**:
- `INVALID_CREDENTIALS`: Email or password incorrect
- `USER_NOT_FOUND`: User does not exist
- `INVALID_API_KEY`: API key invalid

---

## `agentflow auth logout`

Clear local credentials.

```bash
agentflow auth logout
```

**Response**:
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**Side Effect**: Removes API key from `~/.agentflow/context.json`

---

## `agentflow auth status`

Check authentication status.

```bash
agentflow auth status
```

**Response (authenticated)**:
```json
{
  "success": true,
  "data": {
    "authenticated": true,
    "user": {
      "id": "user_123",
      "email": "david@example.com",
      "name": "David"
    },
    "context": {
      "active_org": "acme",
      "active_project": "website",
      "active_version": null
    }
  },
  "message": "Current mode: User (CEO view)"
}
```

**Response (not authenticated)**:
```json
{
  "success": true,
  "data": {
    "authenticated": false,
    "context": null
  },
  "message": "Not authenticated"
}
```

---

## Context File

**Location**: `~/.agentflow/context.json`

**Structure** (when logged in):
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

**After logout**:
```json
{
  "api_key": null,
  "user": null,
  "active_org": null,
  "active_project": null,
  "active_version": null
}
```

---

## Security Notes

### API Key Storage

The API key is stored locally in `~/.agentflow/context.json`. Ensure:

```bash
# File permissions should be restricted
chmod 600 ~/.agentflow/context.json
```

### Password Requirements

- Minimum 12 characters
- Must contain uppercase, lowercase, and numbers
- Special characters recommended

### API Key Format

```
ak_live_<random>    # Production keys
ak_test_<random>    # Test keys
ak_agent_<random>   # Agent keys (generated, not manual)
```

---

## Examples

### Complete Auth Flow

```bash
# 1. Register
agentflow auth register \
  --email "david@example.com" \
  --password "SecurePass123!" \
  --name "David"

# 2. Check status
agentflow auth status
→ authenticated: true

# 3. Logout
agentflow auth logout

# 4. Check status again
agentflow auth status
→ authenticated: false

# 5. Login again
agentflow auth login \
  --email "david@example.com" \
  --password "SecurePass123!"
```

### With API Key

```bash
# Use API key directly (no password needed)
agentflow auth login --api-key "ak_live_abc123..."
```

This is useful for:
- CI/CD pipelines
- Automated scripts
- Testing
