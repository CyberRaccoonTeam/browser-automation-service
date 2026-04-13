# Browser Automation Service

![RaccoonLabs](https://img.shields.io/badge/Built%20by-RaccoonLabs-blueviolet)

REST API for headless browser automation — screenshots, PDFs, scraping, and more.

## What It Does
Part of the **RaccoonLabs API Suite**. This service exposes browser automation as a REST API: take screenshots, generate PDFs, fill forms, and scrape dynamic content. Built on Flask with Playwright. Stripe-powered pricing with 3 tiers: **Starter $9/mo**, **Pro $29/mo**, **Enterprise $99/mo**.

## Tech Stack
- Python 3.10+, Flask
- Playwright
- Stripe API

## Quick Start
```bash
git clone https://github.com/CyberRaccoonTeam/browser-automation-service.git
cd browser-automation-service
pip install -r requirements.txt
flask run
# POST /screenshot {"url": "https://example.com"}
```

## Pricing
| Tier | Price | Requests/mo |
|------|-------|-------------|
| Starter | $9 | 5,000 |
| Pro | $29 | 25,000 |
| Enterprise | $99 | Unlimited |

## License
MIT License

## Links
- **RaccoonLabs:** https://github.com/CyberRaccoonTeam
