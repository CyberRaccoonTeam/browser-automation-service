# Browser Automation Service

> Scheduled browser automation as a service. Automate repetitive browser tasks via API.

## What It Does

- **Schedule browser tasks** — Run Playwright/Puppeteer scripts on demand
- **Webhook notifications** — Get notified when tasks complete
- **API-driven** — Simple REST API to submit and manage tasks
- **Screenshot capture** — Take screenshots of pages after actions
- **Data extraction** — Scrape data from authenticated pages

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tasks` | POST | Create a browser automation task |
| `/api/tasks` | GET | List all tasks |
| `/api/tasks/<id>` | GET | Get task status/result |
| `/api/tasks/<id>` | DELETE | Cancel/delete task |

## Example Task

```json
{
  "type": "screenshot",
  "url": "https://example.com",
  "actions": [
    {"type": "wait", "selector": "#content"},
    {"type": "click", "selector": "#load-more"},
    {"type": "screenshot", "full_page": true}
  ],
  "webhook": "https://your-server.com/webhook"
}
```

## Pricing (Target)

| Plan | Tasks/mo | Price |
|------|----------|-------|
| Free | 50 | $0 |
| Starter | 1,000 | $19/mo |
| Pro | 10,000 | $49/mo |
| Enterprise | Unlimited | $149/mo |

## Stack

- Python 3.12 + Flask
- Playwright (headless browser)
- Celery + Redis (task queue)
- SQLite (task storage)

## Roadmap

- [ ] MVP: Screenshot + simple click/fill tasks
- [ ] Task scheduling (cron-like)
- [ ] Browser session persistence
- [ ] Custom script upload
- [ ] Team collaboration

## Revenue Target

$500-3000/month

---

Built by 🦝 Raccoon | Part of [CyberRaccoonTeam](https://github.com/CyberRaccoonTeam)