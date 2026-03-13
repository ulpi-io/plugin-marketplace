#!/usr/bin/env python3
"""
Generate README.md with a full table of contents grouped by publisher.

Reads each plugin's .claude-plugin/plugin.json, extracts individual skills,
and cross-references skills-tracked.md for install counts.

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
    """Load all plugin metadata from plugins/ directory.

    Each plugin directory is a publisher. Returns a list of publisher dicts,
    each containing the plugin name, source repos, and expanded skills with
    install counts.
    """
    install_counts = load_install_counts()
    publishers = []

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

        plugin_name = meta.get("name", d.name)
        desc = meta.get("description", "")

        # Parse "N skills from user/repo1, user/repo2: skill1, skill2, ..."
        m = re.match(r"(\d+) skills? from ([^:]+):\s*(.*)", desc)
        if m:
            repos_str = m.group(2).strip()
            skills_str = m.group(3).strip()
            repos = [r.strip() for r in repos_str.split(",")]
            skill_names = [s.strip() for s in skills_str.split(",") if s.strip()]

            # Deduplicate skill names while preserving order
            seen = set()
            unique_skills = []
            for s in skill_names:
                if s not in seen:
                    seen.add(s)
                    unique_skills.append(s)

            skills = []
            for skill_name in unique_skills:
                installs = install_counts.get(skill_name, "")
                skills.append({
                    "name": skill_name,
                    "installs": installs,
                    "installs_num": parse_installs(installs) if installs else 0,
                })

            total_installs = sum(s["installs_num"] for s in skills)
            publishers.append({
                "plugin": plugin_name,
                "repos": repos,
                "skills": skills,
                "total_installs": total_installs,
            })
        else:
            # Non-standard description (e.g. hello-world)
            installs = install_counts.get(plugin_name, "")
            publishers.append({
                "plugin": plugin_name,
                "repos": [],
                "skills": [{
                    "name": plugin_name,
                    "installs": installs,
                    "installs_num": parse_installs(installs) if installs else 0,
                }],
                "total_installs": parse_installs(installs) if installs else 0,
                "description": desc,
            })

    # Sort by total installs descending, then alphabetically
    publishers.sort(key=lambda p: (-p["total_installs"], p["plugin"]))
    return publishers


def generate_readme(publishers):
    """Generate the full README.md content."""
    total_skills = sum(len(p["skills"]) for p in publishers)

    lines = []
    lines.append('<p align="center">')
    lines.append('  <a href="https://ulpi.io"><img src="https://www.ulpi.io/media/ulpi-icon-512x512.png" alt="Ulpi" height="56"></a>')
    lines.append('  &nbsp;&nbsp;&times;&nbsp;&nbsp;')
    lines.append('  <a href="https://www.thecasualleader.com/"><img src="https://images.squarespace-cdn.com/content/v1/678a556b961d7f407a170440/e9bbb79f-6115-41b5-abac-a4a124d4c071/fulllogo.png?format=1500w" alt="The Casual Leader" height="56"></a>')
    lines.append('</p>')
    lines.append("")
    lines.append("# Plugin Marketplace")
    lines.append("")
    lines.append(f"A curated collection of {total_skills}+ agent skills, packaged as plugins for easy installation in the Claude Desktop app.")
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
    lines.append(f"## Plugins by Publisher ({total_skills} skills from {len(publishers)} publishers)")
    lines.append("")

    for pub in publishers:
        plugin = pub["plugin"]
        repos = pub["repos"]
        skills = pub["skills"]

        if repos:
            # Link to first repo
            first_repo = repos[0]
            if len(repos) > 1:
                lines.append(f"### [{first_repo}](https://github.com/{first_repo}) + {len(repos) - 1} more ({len(skills)} skills)")
            else:
                lines.append(f"### [{first_repo}](https://github.com/{first_repo}) ({len(skills)} skills)")
        else:
            lines.append(f"### {plugin} ({len(skills)} skills)")

        lines.append("")
        lines.append(f"Install: `claude plugin install {plugin}@ulpi-marketplace`")
        lines.append("")
        lines.append("| Skill | Installs |")
        lines.append("|-------|----------|")
        for s in sorted(skills, key=lambda x: -x["installs_num"]):
            installs = s["installs"] or "-"
            lines.append(f"| {s['name']} | {installs} |")
        lines.append("")

    # Credits
    lines.append("## Credits")
    lines.append("")
    lines.append("- **[skills.sh](https://skills.sh)** — The open agent skills directory where all skills are discovered and ranked")
    lines.append("- **All original skill authors** — Each plugin was created by its respective author and sourced from their GitHub repository. See individual plugin directories for original author and repository info")
    lines.append("- **[Ulpi](https://ulpi.io)** & **[The Casual Leader](https://www.thecasualleader.com/)** — Packaging and marketplace curation")
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

    publishers = load_plugins()
    readme = generate_readme(publishers)

    total_skills = sum(len(p["skills"]) for p in publishers)

    if args.dry_run:
        print(readme)
    else:
        README_FILE.write_text(readme)
        print(f"Written README.md ({total_skills} skills, {len(publishers)} publishers)")


if __name__ == "__main__":
    main()
