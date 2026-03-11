# Ulpi Plugin Marketplace

A curated collection of 880+ agent skills, packaged as plugins for easy installation in the Claude Desktop app.

All skills are sourced from [skills.sh](https://skills.sh) — the open agent skills ecosystem. This marketplace re-packages them so Claude Desktop users can install them with a single command, without needing the CLI.

## Installation

Add this marketplace to Claude Code:

```bash
claude plugin marketplace add ulpi-io/plugin-marketplace
```

Then install any plugin:

```bash
claude plugin install frontend-design@ulpi-marketplace
```

## What's Included

880+ skills with 1,000+ installs each, from top skill authors including:

| Author | Examples |
|--------|----------|
| [Vercel Labs](https://github.com/vercel-labs) | react-best-practices, web-design-guidelines, agent-browser |
| [Anthropic](https://github.com/anthropics) | frontend-design, skill-creator, pdf, docx, pptx |
| [Microsoft](https://github.com/microsoft) | azure-ai, azure-compute, azure-cloud-migrate |
| [Remotion](https://github.com/remotion-dev) | remotion-best-practices |
| [Supabase](https://github.com/supabase) | supabase-postgres-best-practices |
| [Cloudflare](https://github.com/cloudflare) | cloudflare, wrangler |
| [Google Workspace](https://github.com/googleworkspace) | gws-gmail, gws-calendar, gws-docs |
| And hundreds more... | See [skills-tracked.md](./skills-tracked.md) for the full list |

## Credits

- **[skills.sh](https://skills.sh)** — The open agent skills directory where all skills are discovered and ranked
- **All original skill authors** — Each plugin in this marketplace was created by its respective author and is sourced from their GitHub repository. See individual plugin directories for original author and repository info
- **[Ulpi](https://ulpi.io)** — Packaging and marketplace curation

This marketplace does not claim ownership of any skills. All credit goes to the original authors. We simply re-package them to make installation easier for Claude Desktop users.

## Repository Structure

```
plugin-marketplace/
├── marketplace.json          # plugin catalog
├── plugins/                  # 880+ bundled skill plugins
│   ├── frontend-design/
│   ├── agent-browser/
│   ├── react-best-practices/
│   └── ...
├── skills-tracked.md         # full list of tracked skills with install counts
├── scrape-skills.py          # scrapes skills.sh leaderboard
├── sync-skills.py            # syncs skills into plugin directories
└── README.md
```

## Updating the Marketplace

```bash
# Re-scrape the skills.sh leaderboard
python3 scrape-skills.py

# Sync new skills into plugins/
python3 sync-skills.py

# Re-sync everything from scratch
python3 sync-skills.py --all
```

## License

Individual skills retain their original licenses. See each plugin directory for details.
