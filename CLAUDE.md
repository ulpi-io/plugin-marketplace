# Plugin Marketplace

Central catalog for Claude Code plugins by Ulpi.

## What This Is

This repo IS a Claude Code marketplace. It contains:
- `.claude-plugin/marketplace.json` — the plugin catalog (source of truth)
- `plugins/` — bundled plugins (some plugins live here, others in separate repos)

## Plugin Locations

Plugins can live in two places:
1. **Bundled** — inside this repo's `plugins/` directory (source: `"./plugins/{name}"`)
2. **External** — in a separate GitHub repo or monorepo subfolder (source: `{"source": "github", "repo": "..."}`)

## Ecosystem

| Plugin | Location | Description |
|--------|----------|-------------|
| hello-world | `./plugins/hello-world` (bundled) | Example plugin with a greeting skill |
| review | `ulpi-io/plan-review.ulpi.io` (external) | Plan & code review with annotations |

## How Users Install

1. Add marketplace: `claude plugin marketplace add ulpi-io/marketplace`
2. Install plugin: `claude plugin install hello-world@ulpi-marketplace`

## How to Add a New Plugin

### Bundled plugin (lives in this repo):
1. Create `plugins/{name}/` with `.claude-plugin/plugin.json`
2. Add skills/, hooks/, agents/, .mcp.json as needed
3. Add entry to `.claude-plugin/marketplace.json`

### External plugin (separate repo or monorepo subfolder):
1. Create the plugin in its own repo (follow hello-world structure)
2. Add entry to `.claude-plugin/marketplace.json` with GitHub source:
   ```json
   {
     "name": "my-plugin",
     "source": { "source": "github", "repo": "ulpi-io/my-repo" },
     "version": "1.0.0"
   }
   ```

## Plugin Structure (minimum required)

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED — name, version, description
├── skills/                  # Optional — agent skills
├── hooks/                   # Optional — event hooks (hooks.json)
├── agents/                  # Optional — subagent definitions
├── .mcp.json                # Optional — MCP server config
└── README.md                # Recommended
```

## Tech Stack
- No build system needed for the marketplace itself
- Plugins that need binaries use Bun --compile (see Review plugin)
