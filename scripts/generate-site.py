#!/usr/bin/env python3
"""
Generate docs/data.json for the GitHub Pages site.

Reads plugin metadata from plugins/ directory and cross-references
skills-tracked.md for install counts.

Usage:
    python3 generate-site.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
PLUGINS_DIR = ROOT / "plugins"
TRACKED_FILE = ROOT / "skills-tracked.md"
DOCS_DIR = ROOT / "docs"
DATA_FILE = DOCS_DIR / "data.json"


def parse_installs(s):
    s = s.strip()
    if s.endswith("K"):
        return float(s[:-1]) * 1000
    elif s.endswith("M"):
        return float(s[:-1]) * 1_000_000
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return 0


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


def load_plugins():
    """Load all plugin metadata from plugins/ directory, expanding individual skills."""
    install_counts = load_install_counts()
    skills = []

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
            # Use first repo as the canonical repo
            repos = [r.strip() for r in repos_str.split(",")]
            first_repo = repos[0] if repos else plugin_name
            skill_names = [s.strip() for s in skills_str.split(",") if s.strip()]

            # Deduplicate skill names while preserving order
            seen = set()
            unique_skills = []
            for s in skill_names:
                if s not in seen:
                    seen.add(s)
                    unique_skills.append(s)

            for skill_name in unique_skills:
                installs = install_counts.get(skill_name, "")
                skills.append({
                    "name": skill_name,
                    "repo": first_repo,
                    "installs": installs,
                    "installs_num": parse_installs(installs) if installs else 0,
                    "description": "",
                    "plugin": plugin_name,
                })
        else:
            # Non-standard description (e.g. hello-world)
            installs = install_counts.get(plugin_name, "")
            skills.append({
                "name": plugin_name,
                "repo": plugin_name,
                "installs": installs,
                "installs_num": parse_installs(installs) if installs else 0,
                "description": desc,
                "plugin": plugin_name,
            })

    # Sort by installs descending
    skills.sort(key=lambda s: -s["installs_num"])

    return skills


def build_stats(skills):
    publishers = set(s["plugin"] for s in skills)
    total_installs = sum(s["installs_num"] for s in skills)
    if total_installs >= 1_000_000:
        total_str = f"{total_installs / 1_000_000:.1f}M"
    elif total_installs >= 1000:
        total_str = f"{total_installs / 1000:.1f}K"
    else:
        total_str = str(int(total_installs))
    return {
        "total_skills": len(skills),
        "total_publishers": len(publishers),
        "total_installs": total_str,
    }


def main():
    skills = load_plugins()
    stats = build_stats(skills)

    # Remove installs_num from output (only used for sorting)
    output_skills = []
    for i, s in enumerate(skills):
        output_skills.append({
            "rank": i + 1,
            "name": s["name"],
            "repo": s["repo"],
            "installs": s["installs"],
            "description": s["description"],
            "synced": True,
            "plugin": s["plugin"],
        })

    data = {
        "stats": stats,
        "skills": output_skills,
    }

    DOCS_DIR.mkdir(exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")

    print(f"Written {DATA_FILE} ({len(output_skills)} skills, {stats['total_publishers']} publishers)")


if __name__ == "__main__":
    main()
