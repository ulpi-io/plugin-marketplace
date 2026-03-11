#!/usr/bin/env python3
"""
Generate README.md with a full table of contents grouped by publisher.

Reads each plugin's .claude-plugin/plugin.json, groups by publisher,
and writes a complete README.md.

Usage:
    python3 generate-toc.py          # regenerate README.md
    python3 generate-toc.py --dry-run  # print to stdout instead
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PLUGINS_DIR = ROOT / "plugins"
TRACKED_FILE = ROOT / "skills-tracked.md"
README_FILE = ROOT / "README.md"


def load_install_counts():
    """Parse skills-tracked.md and return {name: installs_str} mapping."""
    counts = {}
    if not TRACKED_FILE.exists():
        return counts
    with open(TRACKED_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("---") or line.startswith("Rank"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 4:
                counts[parts[1]] = parts[3]
    return counts


def parse_installs(s):
    """Convert '496.3K' or '997' to a number for sorting."""
    s = s.strip()
    if s.endswith("K"):
        return float(s[:-1]) * 1000
    elif s.endswith("M"):
        return float(s[:-1]) * 1_000_000
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return 0


def load_plugins():
    """Load all plugin metadata from plugins/ directory."""
    install_counts = load_install_counts()
    plugins = []
    for d in sorted(PLUGINS_DIR.iterdir()):
        if not d.is_dir():
            continue
        pj = d / ".claude-plugin" / "plugin.json"
        if not pj.exists():
            continue
        try:
            with open(pj) as f:
                meta = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        repo_url = meta.get("repository", "")
        repo = ""
        if "github.com/" in repo_url:
            repo = repo_url.split("github.com/")[-1].rstrip("/")

        name = meta.get("name", d.name)
        installs = install_counts.get(name, "")

        plugins.append({
            "name": name,
            "author": meta.get("author", {}).get("name", "unknown"),
            "repo": repo,
            "description": meta.get("description", ""),
            "installs": installs,
            "installs_num": parse_installs(installs) if installs else 0,
        })
    return plugins


def group_by_publisher(plugins):
    """Group plugins by repo, sorted by total downloads descending."""
    groups = {}
    for p in plugins:
        key = p["repo"] or p["author"]
        groups.setdefault(key, []).append(p)
    # Sort groups by total downloads descending, then alphabetically
    return sorted(groups.items(),
                  key=lambda x: (-sum(p["installs_num"] for p in x[1]), x[0]))


def generate_readme(plugins):
    """Generate the full README.md content."""
    groups = group_by_publisher(plugins)

    lines = []
    lines.append("# Ulpi Plugin Marketplace")
    lines.append("")
    lines.append(f"A curated collection of {len(plugins)}+ agent skills, packaged as plugins for easy installation in the Claude Desktop app.")
    lines.append("")
    lines.append("All skills are sourced from [skills.sh](https://skills.sh) — the open agent skills ecosystem. This marketplace re-packages them so Claude Desktop users can install them with a single command.")
    lines.append("")

    # Installation - Claude Desktop
    lines.append("## Installation (Claude Desktop)")
    lines.append("")
    lines.append("1. Open Claude Desktop")
    lines.append("2. Go to **Cowork** → **Customize** → **Skills**")
    lines.append("3. Above \"Personal plugins\", click the **+** button")
    lines.append("4. Select **Browse** → **Personal**")
    lines.append("5. Click **+** again")
    lines.append("6. Choose **Add marketplace from GitHub**")
    lines.append("7. Enter: `ulpi-io/plugin-marketplace`")
    lines.append("")
    lines.append("Once added, you can browse and install any of the plugins below.")
    lines.append("")

    # Installation - CLI
    lines.append("## Installation (CLI)")
    lines.append("")
    lines.append("```bash")
    lines.append("claude plugin marketplace add ulpi-io/plugin-marketplace")
    lines.append("```")
    lines.append("")
    lines.append("Then install any plugin:")
    lines.append("")
    lines.append("```bash")
    lines.append("claude plugin install frontend-design@ulpi-marketplace")
    lines.append("```")
    lines.append("")

    # TOC by publisher
    lines.append(f"## Plugins by Publisher ({len(plugins)} plugins from {len(groups)} publishers)")
    lines.append("")

    for repo, group in groups:
        if "/" in repo:
            lines.append(f"### [{repo}](https://github.com/{repo}) ({len(group)} plugins)")
        else:
            lines.append(f"### {repo} ({len(group)} plugins)")
        lines.append("")
        lines.append("| Plugin | Installs | Description |")
        lines.append("|--------|----------|-------------|")
        for p in sorted(group, key=lambda x: -x["installs_num"]):
            desc = p["description"]
            desc = re.sub(r"\s*skill from \S+$", "", desc)
            if not desc:
                desc = p["name"]
            installs = p["installs"] or "-"
            lines.append(f"| {p['name']} | {installs} | {desc} |")
        lines.append("")

    # Credits
    lines.append("## Credits")
    lines.append("")
    lines.append("- **[skills.sh](https://skills.sh)** — The open agent skills directory where all skills are discovered and ranked")
    lines.append("- **All original skill authors** — Each plugin was created by its respective author and sourced from their GitHub repository. See individual plugin directories for original author and repository info")
    lines.append("- **[Ulpi](https://ulpi.io)** — Packaging and marketplace curation")
    lines.append("")
    lines.append("This marketplace does not claim ownership of any skills. All credit goes to the original authors.")
    lines.append("")

    # Updating
    lines.append("## Updating the Marketplace")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scrape-skills.py        # re-scrape skills.sh leaderboard")
    lines.append("python3 sync-skills.py          # sync new skills into plugins/")
    lines.append("python3 sync-skills.py --all    # re-sync everything from scratch")
    lines.append("python3 generate-toc.py         # regenerate this README")
    lines.append("```")
    lines.append("")

    # License
    lines.append("## License")
    lines.append("")
    lines.append("Individual skills retain their original licenses. See each plugin directory for details.")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate README.md with plugin TOC")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print to stdout instead of writing README.md")
    args = parser.parse_args()

    plugins = load_plugins()

    readme = generate_readme(plugins)

    if args.dry_run:
        print(readme)
    else:
        README_FILE.write_text(readme)
        print(f"Written README.md ({len(plugins)} plugins, {len(group_by_publisher(plugins))} publishers)")


if __name__ == "__main__":
    main()
