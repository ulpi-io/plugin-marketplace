#!/usr/bin/env python3
"""
Generate docs/data.json for the GitHub Pages site.

Reads skills-tracked.md and plugin metadata to produce a JSON file
that the static site loads at runtime.

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


def load_tracked():
    """Parse skills-tracked.md."""
    skills = []
    with open(TRACKED_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("---") or line.startswith("Rank"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                continue
            try:
                rank = int(parts[0])
            except ValueError:
                continue
            skills.append({
                "rank": rank,
                "name": parts[1],
                "repo": parts[2],
                "installs": parts[3],
                "installs_num": parse_installs(parts[3]),
            })
    return skills


def enrich_with_descriptions(skills):
    """Add descriptions from plugin.json where available."""
    for s in skills:
        pj = PLUGINS_DIR / s["name"] / ".claude-plugin" / "plugin.json"
        if pj.exists():
            try:
                with open(pj) as f:
                    meta = json.load(f)
                desc = meta.get("description", "")
                # Clean up auto-generated descriptions
                desc = re.sub(r"\s*skill from \S+$", "", desc)
                s["description"] = desc
                s["synced"] = True
            except (json.JSONDecodeError, OSError):
                s["description"] = ""
                s["synced"] = False
        else:
            s["description"] = ""
            s["synced"] = False
    return skills


def build_stats(skills):
    publishers = set(s["repo"] for s in skills)
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
    skills = load_tracked()
    skills = enrich_with_descriptions(skills)
    stats = build_stats(skills)

    # Remove installs_num from output (only used for sorting)
    output_skills = []
    for s in skills:
        output_skills.append({
            "rank": s["rank"],
            "name": s["name"],
            "repo": s["repo"],
            "installs": s["installs"],
            "description": s["description"],
            "synced": s["synced"],
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
