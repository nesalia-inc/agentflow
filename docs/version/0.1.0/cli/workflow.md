# Complete Workflow Example

Demonstrates the complete AgentFlow workflow from setup to task completion.

---

## Part 1: CEO Setup (Human CLI)

```bash
# 1. Register
agentflow auth register \
  --email "david@example.com" \
  --password "SecurePass123!" \
  --name "David"

# 2. Create roles with authority levels
agentflow role create --name "Junior Dev" --slug "junior" --level 1
agentflow role create --name "Frontend Dev" --slug "frontend" --level 3
agentflow role add-document \
  --role "frontend" \
  --title "React Best Practices" \
  --content "# React Best Practices\n- Use functional components"

# 3. Create organization
agentflow org create --name "My Startup" --slug "mystartup"
agentflow org use --slug "mystartup"

# 4. Create agents
agentflow agent create --role "frontend" --name "Alice"  # Level 3
agentflow agent create --role "junior" --name "Bob"    # Level 1

# 5. Create project
agentflow project create --name "My App" --slug "myapp"
agentflow project use --slug "myapp"

# 6. Create version
agentflow version create --version "0.1.0" --name "Initial release"

# 7. Create tasks with required levels
agentflow task create --title "Fix typo" --priority "P3" --required-level 1
agentflow task create --title "Build homepage" --priority "P0" --required-level 3
agentflow task create --title "Database migration" --priority "P0" --required-level 5

# 8. Assign tasks
agentflow task assign --task-id "task_typo" --agent "agent_bob"
agentflow task assign --task-id "task_homepage" --agent "agent_alice"

# 9. Launch Alice's agent token
agentflow agent launch --agent "agent_alice"
```

---

## Part 2: Agent Works (Agent CLI)

```bash
# 10. Alice starts with token
$ agentflow-agent --config ~/.agentflow/agents/agent_alice/token.json

# 11. Check status
$ agentflow-agent status
→ Current mode: Agent Alice (Frontend Developer, Level 3)

# 12. List tasks (only assigned to Alice)
$ agentflow-agent task list
→ 1 task: "Build homepage" (Level 3)

# 13. View role documents
$ agentflow-agent role view --slug "frontend"
→ Shows React Best Practices

# 14. Start task
$ agentflow-agent task start --task-id "task_homepage"
→ Task started and assigned to you (Alice)

# 15. Try to work on higher-level task (fails)
$ agentflow-agent task start --task-id "task_migration"
→ Error: Task requires authority level 5. Your level: 3.

# 16. Complete task
$ agentflow-agent task complete --task-id "task_homepage" \
  --success "Homepage built with React and TypeScript"

# 17. Exit
$ exit
```

---

## Part 3: CEO Monitors

```bash
# 18. Check progress
[mystartup/myapp] $ agentflow version view --version "0.1.0"

# 19. Release version
[mystartup/myapp] $ agentflow version release \
  --version "0.1.0" \
  --release-notes "Initial MVP release"
```

---

## Security Highlights

- Alice (Level 3) **cannot** work on Level 5 tasks
- Alice **cannot** create other agents
- Alice **cannot** view all tasks
- Alice **cannot** "exit" to CEO mode
- CEO (Level 10) has **full control**
