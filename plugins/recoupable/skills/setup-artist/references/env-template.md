# Environment File Templates

Two files to create at the artist workspace root.

---

## `.env.example`

This is the reference file that gets committed. All variables are commented out — agents uncomment and fill them in `.env` as services are connected.

```
# {Artist Name} — Environment Variables
# Copy this file to .env and fill in real values.
# NEVER commit .env — only .env.example gets checked in.

# Social accounts (add as accounts are set up)
# TIKTOK_USERNAME=
# TIKTOK_PASSWORD=
# INSTAGRAM_USERNAME=
# INSTAGRAM_PASSWORD=
# YOUTUBE_USERNAME=
# YOUTUBE_PASSWORD=
# TWITTER_USERNAME=
# TWITTER_PASSWORD=
# FACEBOOK_USERNAME=
# FACEBOOK_PASSWORD=

# Content posting
# POSTBRIDGE_API_KEY=

# AI services
# FAL_KEY=
# RECOUP_API_KEY=

# Distribution (add when connected)
# DISTROKID_API_KEY=

# Merch (add when connected)
# SHOPIFY_ACCESS_TOKEN=

# Website (add when connected)
# VERCEL_TOKEN=
```

---

## `.env`

This is the actual secrets file — never committed. Start with just a header:

```
# {Artist Name} — Secrets
# Add credentials here as services are connected.
# See .env.example for all available variables.
# NEVER commit this file.
```

---

## Important

Make sure `.env` is covered by `.gitignore` at the repo root or artist level. The monorepo root `.gitignore` typically already includes `.env` and `.env.local`.
