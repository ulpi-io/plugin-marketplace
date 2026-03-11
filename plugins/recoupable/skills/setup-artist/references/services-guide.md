# Services Guide Template

Create this as `config/SERVICES.md` in the artist workspace.

---

```markdown
---
name: Services
description: "How to connect and track services for {Artist Name}. Read this before adding any service. Don't pre-fill — add services as you learn about them."
---

# Services

This file teaches agents how to register tools, accounts, and capabilities for this artist. **Start empty. Add as you go.**

## When to Add a Service

Add a service entry when you have **real information** — a handle, an API key, a confirmed account. Don't create placeholder entries for services that don't exist yet.

Common triggers:
- User mentions a social media handle → add it to `social/`
- User sets up a new tool → add it to the relevant category
- An API key or credential is provided → add the service and store the key in `.env`

## Where Services Live

Each service is stored as a JSON file in `config/services/`:

```
config/services/
  tiktok.json
  instagram.json
  fal.json
  postbridge.json
```

One file per service. Created when the service is first connected.

## Service File Format

```json
{
  "name": "tiktok",
  "category": "social",
  "handle": "@handle",
  "status": "active",
  "use": "What this service is used for in one sentence.",
  "auth": {
    "type": "login | api-key | oauth",
    "env": "ENV_VAR_NAME or { username: 'ENV_USER', password: 'ENV_PASS' }"
  }
}
```

**Fields:**
- `name` — service identifier (lowercase, matches filename)
- `category` — one of: `social`, `posting`, `ai`, `distribution`, `merch`, `website`, `email`, `other`
- `handle` — username, page name, or URL (if applicable)
- `status` — `active`, `not-setup`, or `in-progress`
- `use` — one sentence explaining what the agent uses this service for
- `auth` — how to authenticate. Always reference env var names, never store actual secrets here

## Categories

| Category | What belongs here | Examples |
|----------|------------------|----------|
| `social` | Social media accounts the agent logs into for engagement | TikTok, Instagram, YouTube, Twitter, Facebook |
| `posting` | Tools that automate content posting across platforms | PostBridge |
| `ai` | AI services used by the content pipeline | fal (video/image gen), recoup-chat (text gen) |
| `distribution` | Music distribution to streaming platforms | DistroKid, TuneCore |
| `merch` | Merchandise and e-commerce | Shopify |
| `website` | Website hosting and management | Vercel |
| `email` | Artist email for business and fan communication | Email address |

## Credentials

All secrets go in the `.env` file at the artist root — **never** in service JSON files. The `auth.env` field in each service file tells agents which env var(s) to use.

## Universal Services

These are services every artist will eventually need. Don't create them ahead of time — add them when they're actually set up:

- **Social accounts** — TikTok, Instagram, YouTube, Twitter, Facebook
- **PostBridge** — automated content posting across all platforms
- **fal** — AI video/image generation (often pre-configured)
- **recoup-chat** — AI text generation (often pre-configured)
- **Email** — `{artist-slug}@recoupable.com`
```
