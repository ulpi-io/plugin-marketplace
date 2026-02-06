# hello-world

An example reference plugin from the Ulpi Marketplace. It demonstrates the
simplest possible plugin structure: a single skill with no tools, hooks, or
configuration.

## What it does

Provides a `greet` skill that responds to user greetings and questions about
Ulpi marketplace plugins with a brief, friendly message.

## Plugin structure

```
hello-world/
  .claude-plugin/
    plugin.json        # Plugin metadata (name, version, author, license)
  skills/
    greet/
      SKILL.md         # Skill definition with frontmatter and instructions
  README.md
```

- **plugin.json** -- Required. Declares the plugin identity and metadata.
- **skills/** -- Each subdirectory is a skill. The `SKILL.md` frontmatter
  (`name`, `description`) is used for discovery; the body contains the
  instructions injected into the agent context.

## Using this as a starting point

1. Copy this directory and rename it to your plugin name.
2. Update `plugin.json` with your own metadata.
3. Replace or add skills under `skills/`.
4. Add tools, hooks, or configuration as needed for more advanced plugins.
