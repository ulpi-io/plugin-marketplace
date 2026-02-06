# Ulpi Plugin Marketplace

Central catalog for Claude Code plugins by Ulpi.

## Installation

Add this marketplace to Claude Code:

```bash
claude plugin marketplace add ulpi-io/marketplace
```

Then install any plugin from the catalog:

```bash
claude plugin install hello-world@ulpi-marketplace
```

## Available Plugins

| Plugin | Type | Description |
|--------|------|-------------|
| [hello-world](./plugins/hello-world) | Bundled | Example plugin with a greeting skill |
| [review](https://github.com/ulpi-io/plan-review.ulpi.io) | External | Plan & code review with annotations |

## Creating a Plugin

Plugins can be **bundled** (inside this repo under `plugins/`) or **external** (in a separate GitHub repo).

At minimum, a plugin needs:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json      # name, version, description
├── skills/              # optional
├── hooks/               # optional
├── agents/              # optional
└── .mcp.json            # optional
```

To publish a plugin to this marketplace, add an entry to `.claude-plugin/marketplace.json`.

See [CLAUDE.md](./CLAUDE.md) for full details on plugin structure and contribution steps.

## Repository Structure

```
marketplace/
├── .claude-plugin/
│   └── marketplace.json   # plugin catalog (source of truth)
├── plugins/
│   └── hello-world/       # bundled example plugin
├── CLAUDE.md              # detailed developer documentation
└── README.md              # this file
```

## License

[Apache-2.0](./LICENSE)
