# AgentFlow Roadmap

This document outlines the planned development phases for AgentFlow CLI.

## Current Status

**Version**: 0.1.0 (MVP Complete)

**Completed Features**:
- Configuration system (init, show, test)
- Workspace management (create, list, switch, current)
- Session tracking (start, status, abort)
- Action logging during active sessions
- Session commit with parent-child relationships
- Commit history (log, show commands)
- Support for PostgreSQL and SQLite
- 34 passing tests
- Ready for PyPI publication

---

## Phase A: Polish & UX Improvements

**Goal**: Enhance day-to-day user experience and usability

**Estimated Time**: 2-3 days

**Planned Features**:

### Session & Workspace Management
- `agentflow session edit` - Modify task description of active session
- `agentflow workspace rename` - Rename existing workspace
- `agentflow workspace delete` - Delete workspace with confirmation
- `agentflow workspace description` - Add/edit workspace description

### Advanced Filtering
- `agentflow log --workspace <name>` - Filter commits by workspace
- `agentflow log --author <name>` - Filter commits by author
- `agentflow log --since <date>` - Filter commits from date
- `agentflow log --until <date>` - Filter commits until date
- `agentflow log --grep <pattern>` - Search commit messages
- `agentflow log --reverse` - Show in chronological order

### Output Formats
- `--json` flag for JSON output (CI/CD integration)
- `--no-color` flag for script/automation friendly output
- Formatted table output for commit lists

### Shell Integration
- Bash completion script
- Zsh completion script
- Commit ID completion with prefix matching
- Workspace name completion

**Value**: High user satisfaction, minimal complexity

---

## Phase B: Advanced Features

**Goal**: Add powerful Git-inspired features

**Estimated Time**: 5-7 days

**Planned Features**:

### Tagging System
- `agentflow tag create <name> <commit-id>` - Create tag on commit
- `agentflow tag list` - List all tags
- `agentflow tag delete <name>` - Delete tag
- `agentflow show <tag-name>` - Show tagged commit
- Mark important milestones and versions

### Commit Comparison
- `agentflow diff <commit1> <commit2>` - Compare two commits
- `agentflow diff <commit>` - Compare with current state
- Show differences in sessions, actions, duration
- Visual diff output

### Import/Export
- `agentflow workspace export <file>` - Export workspace to JSON
- `agentflow workspace import <file>` - Import workspace from JSON
- Backup and migration between databases
- Cross-instance data transfer

### Statistics & Reports
- `agentflow stats` - Global statistics (total time, session count)
- `agentflow stats --workspace <name>` - Per-workspace statistics
- `agentflow stats --period <days>` - Statistics over time period
- Charts and visualizations (optional)
- Productivity metrics

### Advanced Search
- `agentflow search <pattern>` - Search all commits
- `agentflow search --action <pattern>` - Search in action descriptions
- `agentflow search --description <pattern>` - Search in commit descriptions
- Full-text search across workspaces

**Value**: Powerful features for power users

---

## Phase C: CI/CD & Automation

**Goal**: Professional development workflow

**Estimated Time**: 2-3 days

**Planned Features**:

### GitHub Actions CI
- Automated tests on every pull request
- Linting with ruff
- Type checking with mypy
- Multi-version testing (Python 3.14, 3.15+)
- Multi-platform testing (Windows, Linux, macOS)

### GitHub Actions Release
- Trigger on git tags (v*)
- Automated build process
- Automatic PyPI publishing via Trusted Publisher
- Automatic GitHub Release creation with release notes
- No manual intervention required

### Quality Assurance
- Code coverage reporting (pytest-cov)
- Status badges in README
- Pre-commit hooks setup
  - black (optional formatting)
  - ruff (linting)
  - mypy (type checking)
- Contributing guidelines

**Value**: High project value, ensures code quality

---

## Phase D: Integrations & Ecosystem

**Goal**: Connect AgentFlow with other tools

**Estimated Time**: 10-15 days (excluding web dashboard)

**Planned Features**:

### Git Integration
- Link AgentFlow commits to Git commits
- `agentflow commit --git` - Create Git commit alongside AgentFlow commit
- Store Git commit hash in AgentFlow commits
- Sync workflows between AgentFlow and Git
- Branch awareness

### Editor Integrations
- VS Code extension
  - Sidebar panel showing sessions/commits
  - Quick actions from editor
  - Status bar integration
- Neovim/Emacs plugin
  - View commits from editor
  - Create sessions without leaving editor

### Project Management Integration
- Export to Jira, Linear, GitHub Issues
- Create tickets from sessions
- Link sessions to existing tickets
- Status synchronization

### Optional Web Dashboard
- Web interface for workspace visualization
- Charts and statistics
- Visual commit navigation
- Multi-user authentication
- Real-time session tracking

**Value**: Enhanced workflow, broader adoption potential

---

## Phase E: Architecture & Performance

**Goal**: Improve technical foundation

**Estimated Time**: 4-5 days

**Planned Improvements**:

### Database Optimizations
- Additional indexes for frequent queries
- Pagination for `agentflow log` (large commit histories)
- Connection pooling for better performance
- Query optimization
- Database migration system (Alembic)

### Error Handling & Validation
- Clearer error messages
- Input validation for all commands
- Dry-run mode for destructive operations
- Interactive confirmation for dangerous operations
- Graceful degradation

### Testing
- End-to-end integration tests
- Performance tests
- Load testing
- Increase coverage to 80-90%
- Fuzz testing for CLI inputs

### Documentation
- Complete API documentation
- Contribution guide
- Architecture documentation
- Advanced usage examples
- Troubleshooting guide

### Advanced Configuration
- Per-workspace configuration files
- Environment variable overrides
- Configuration templates
- Configuration validation

**Value**: Solid foundation for future growth

---

## Phase F: Multi-User & Collaboration

**Goal**: Enable team collaboration

**Estimated Time**: 15-20 days

**Planned Features**:

### Authentication
- `agentflow login` - User authentication
- `agentflow logout` - User logout
- Store user ID in commits and actions
- Filter by user in all commands

### Shared Workspaces
- Multi-user workspace access
- Permission system (read, write, admin)
- `agentflow workspace share --user <email>` - Share workspace
- `agentflow workspace unshare` - Revoke access
- Workspace ownership transfer

### Collaboration Features
- View active sessions of other users
- `agentflow users` - List workspace users
- Session attribution
- Collaborative filtering

### Notifications
- Notifications when users complete sessions
- Daily/weekly summary emails
- Activity feeds
- Subscription to workspace events

**Value**: Transform from single-user to team tool

---

## Prioritization

### Short Term (1-2 weeks) - Post v0.1.0
1. **Phase C: CI/CD & Automation** - Essential for professional project
2. **Phase A: Polish & UX** - Quick user satisfaction improvements
3. **Documentation** - Improve accessibility

### Medium Term (1-2 months) - Toward v0.2.0
1. **Phase B: Advanced Features** - Tags, diff, statistics
2. **Phase E: Architecture** - Performance and optimization
3. **Phase D: Git Integration** - Highly requested feature

### Long Term (3-6 months) - Toward v1.0.0
1. **Phase F: Multi-User** - If strong user demand
2. **Phase D: Web Dashboard** - If needed
3. **Phase D: Editor Integrations** - Premium UX

---

## Version Planning

### v0.1.0 (Current)
- MVP feature set
- Basic workspace and session management
- Commit history and tracking

### v0.2.0 (Planned)
- CI/CD automation
- UX improvements (filtering, completion)
- Advanced features (tags, diff, stats)
- Git integration

### v0.3.0 (Future)
- Import/export functionality
- Advanced search
- Performance optimizations
- Comprehensive testing

### v1.0.0 (Future Milestone)
- Multi-user support
- Full-featured collaboration
- Stable API
- Extensive documentation
- Editor integrations

---

## Contributing

If you're interested in contributing to any of these phases, please:

1. Check the [GitHub Issues](https://github.com/Developers-Secrets-Inc/agentflow/issues) for planned work
2. Open an issue to discuss your proposed contribution
3. Follow the contribution guidelines (once written)

We welcome contributions of all sizes!

---

**Last Updated**: 2025-01-16
