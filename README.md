# ClawController

**Mission Control for AI Agent Teams**

A task management dashboard designed for orchestrating multiple AI agents. Track tasks, monitor agent status, manage workflows, and coordinate your AI workforce from a single interface.

![ClawController Dashboard](https://clawcontroller.com/screenshots/saas-dashboard.png)

## Features

- **Kanban Board** — Drag-and-drop task management with INBOX → ASSIGNED → IN_PROGRESS → REVIEW → DONE workflow
- **Agent Management** — Create, edit, and monitor AI agents with live status indicators
- **Squad Chat** — Route messages to agents with @mentions
- **Activity Feed** — Real-time task activity and agent updates
- **Recurring Tasks** — Schedule repeating tasks with pause/resume
- **Auto-Assignment** — Configure rules to auto-assign tasks by tag
- **Announcements** — Broadcast updates to your team
- **Dark Theme** — "Cyber Claw" theme with orange accents

## Tech Stack

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** FastAPI + SQLite + SQLAlchemy
- **Real-time:** WebSockets for live updates

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+

### Installation

```bash
# Clone the repository
git clone https://github.com/mdonan90/ClawController.git
cd ClawController

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### Running

**Option 1: Use the start script**

```bash
./start.sh
```

**Option 2: Manual start**

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
npm run dev -- --port 5001 --host 0.0.0.0
```

Access the dashboard at `http://localhost:5001`

### Stopping

```bash
./stop.sh
```

## Configuration

### Auto-Assignment Rules

Edit `backend/main.py` to configure automatic task assignment by tag:

```python
ASSIGNMENT_RULES = {
    "coding": "dev",
    "trading": "trader",
    "marketing": "brand",
    # Add your rules here
}
```

### OpenClaw Integration

ClawController integrates with [OpenClaw](https://openclaw.ai) for live agent status. Set your OpenClaw workspace path:

```python
# In backend/main.py
OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/config.yaml")
```

If OpenClaw is not installed, ClawController uses the internal agent database.

## API Reference

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create a task |
| GET | `/api/tasks/{id}` | Get task by ID |
| PATCH | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| POST | `/api/tasks/{id}/activity` | Log activity |
| GET | `/api/tasks/{id}/activity` | Get activity history |

### Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agents` | List all agents |
| POST | `/api/agents` | Create agent |
| DELETE | `/api/agents/{id}` | Delete agent |

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chat` | Get chat history |
| POST | `/api/chat` | Send message |
| POST | `/api/chat/send-to-agent` | Route to specific agent |

## Task Lifecycle

```
INBOX → ASSIGNED → IN_PROGRESS → REVIEW → DONE
```

- **INBOX**: Unassigned tasks waiting for triage
- **ASSIGNED**: Task assigned to an agent, not started
- **IN_PROGRESS**: Agent actively working (auto-triggers on first activity)
- **REVIEW**: Work complete, awaiting human approval (auto-triggers on "completed/done/finished")
- **DONE**: Approved and closed (manual transition only)

## Screenshots

| Trading Dashboard | SaaS Operations | Agency Workflow |
|-------------------|-----------------|-----------------|
| ![Trading](https://clawcontroller.com/screenshots/trading-dashboard.png) | ![SaaS](https://clawcontroller.com/screenshots/saas-dashboard.png) | ![Agency](https://clawcontroller.com/screenshots/agency-dashboard.png) |

## Contributing

Contributions welcome! Please open an issue or PR.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [Website](https://clawcontroller.com)
- [Documentation](https://clawcontroller.com/docs)
- [OpenClaw](https://openclaw.ai)
