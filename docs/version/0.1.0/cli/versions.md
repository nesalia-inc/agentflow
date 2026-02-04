# Version Commands

Manage project versions.

---

## Commands

- [`create`](#agentflow-version-create) - Create a new version
- [`list`](#agentflow-version-list) - List versions
- [`view`](#agentflow-version-view) - View version details
- [`release`](#agentflow-version-release) - Mark version as released
- [`delete`](#agentflow-version-delete) - Delete a version

---

## `agentflow version create`

Create a new version for a project.

```bash
agentflow version create \
  --org <slug> \
  --project <slug> \
  --version <version> \
  [--name <name>] \
  [--description <description>]
```

**With active context**:
```bash
agentflow version create \
  --version "1.0.0" \
  --name "Major release"
```

**Response**:
```json
{
  "success": true,
  "data": {
    "version": {
      "id": "ver_123",
      "version": "1.0.0",
      "name": "Major release",
      "status": "draft"
    }
  }
}
```

---

## `agentflow version list`

```bash
agentflow version list [--org <slug>] [--project <slug>]
```

---

## `agentflow version view`

```bash
agentflow version view --org <slug> --project <slug> --version <version>
```

---

## `agentflow version release`

```bash
agentflow version release --version <version> [--release-notes <notes>]
```

---

## Examples

```bash
# Create version
agentflow version create --version "1.0.0" --name "Initial release"

# Create tasks
agentflow task create --title "Fix bug" --version "1.0.0"

# Release when ready
agentflow version release --version "1.0.0" --release-notes "First stable release"
```
