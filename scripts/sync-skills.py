#!/usr/bin/env python3
"""
Sync skills from skills-tracked.md into the local marketplace.

Reads skills-tracked.md, clones source repos, finds each skill's
SKILL.md directory, and creates proper plugin directories under plugins/.
Updates marketplace.json (root + .claude-plugin/) when done.

Usage:
    python3 sync-skills.py              # sync only NEW skills (default)
    python3 sync-skills.py --all        # re-sync everything (fresh pull)
    python3 sync-skills.py --limit 20   # sync first 20 skills from the list
    python3 sync-skills.py --dry-run    # show what would be done
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
PLUGINS_DIR = ROOT / "plugins"
TRACKED_FILE = ROOT / "skills-tracked.md"
MARKETPLACE_FILES = [
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / "marketplace.json",
]


def parse_tracked_skills(limit=None):
    """Parse skills-tracked.md and return list of {rank, name, repo, installs}."""
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
            })
    if limit:
        skills = skills[:limit]
    return skills


def get_existing_plugins():
    """Return set of plugin names that already exist locally."""
    existing = set()
    if PLUGINS_DIR.exists():
        for d in PLUGINS_DIR.iterdir():
            if d.is_dir() and (d / ".claude-plugin" / "plugin.json").exists():
                existing.add(d.name)
    return existing


def clone_repo(repo, clone_dir):
    """Shallow-clone a GitHub repo. Returns the clone path."""
    dir_name = repo.replace("/", "--")
    dest = clone_dir / dir_name
    if dest.exists():
        return dest
    print(f"  Cloning {repo}...")
    result = subprocess.run(
        ["gh", "repo", "clone", repo, str(dest), "--", "--depth", "1"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  WARNING: Failed to clone {repo}: {result.stderr.strip()}")
        return None
    return dest


def find_skill_dir(repo_path, skill_name):
    """
    Find the directory containing SKILL.md for a given skill name.

    Tries multiple strategies:
    1. Exact match: skills/<skill_name>/SKILL.md
    2. Exact match in plugin/: plugin/skills/<skill_name>/SKILL.md
    3. Suffix match: look for dirs ending with key parts of the skill name
    4. Fuzzy: search all SKILL.md files and match by directory name similarity
    """
    if repo_path is None:
        return None

    # Build list of candidate skill root directories
    search_prefixes = ["skills", "plugin/skills"]
    # Also search .github/plugins/*/skills (e.g. microsoft/azure-skills)
    github_plugins = repo_path / ".github" / "plugins"
    if github_plugins.exists():
        try:
            for d in github_plugins.iterdir():
                if d.is_dir() and (d / "skills").is_dir():
                    search_prefixes.append(f".github/plugins/{d.name}/skills")
        except OSError:
            pass
    # Also search .claude/skills (e.g. some skill repos)
    if (repo_path / ".claude" / "skills").is_dir():
        search_prefixes.append(".claude/skills")

    # Strategy 1 & 2: exact match in common locations
    for prefix in search_prefixes:
        candidate = repo_path / prefix / skill_name
        if (candidate / "SKILL.md").exists():
            return candidate

    # Strategy 3: try stripping common prefixes from skill name
    name_parts = skill_name.split("-")
    for prefix in search_prefixes:
        skills_root = repo_path / prefix
        if not skills_root.exists():
            continue
        try:
            dirs = [d.name for d in skills_root.iterdir() if d.is_dir()]
        except OSError:
            continue

        # Try progressively shorter suffixes of the skill name
        for i in range(len(name_parts)):
            suffix = "-".join(name_parts[i:])
            for d in dirs:
                if d == suffix:
                    return skills_root / d

        # Try if any dir name is contained in skill name or vice versa
        for d in dirs:
            if d in skill_name or skill_name in d:
                candidate = skills_root / d
                if (candidate / "SKILL.md").exists():
                    return candidate

    # Strategy 4: find all SKILL.md files and pick best match
    try:
        result = subprocess.run(
            ["find", str(repo_path), "-name", "SKILL.md", "-maxdepth", "5"],
            capture_output=True, text=True, timeout=10,
        )
        skill_files = [Path(p.strip()) for p in result.stdout.strip().split("\n") if p.strip()]
        if len(skill_files) == 1:
            return skill_files[0].parent

        best_score = 0
        best_match = None
        for sf in skill_files:
            dir_name = sf.parent.name
            score = sum(1 for part in name_parts if part in dir_name)
            if score > best_score:
                best_score = score
                best_match = sf.parent
        if best_match and best_score > 0:
            return best_match
    except (subprocess.TimeoutExpired, OSError):
        pass

    return None


def create_plugin(skill_name, skill_source_dir, repo_name):
    """Create a plugin directory from a skill source directory."""
    plugin_dir = PLUGINS_DIR / skill_name
    claude_dir = plugin_dir / ".claude-plugin"
    target_skills_dir = plugin_dir / "skills" / skill_name

    # Clean existing
    if plugin_dir.exists():
        shutil.rmtree(plugin_dir)

    claude_dir.mkdir(parents=True, exist_ok=True)
    target_skills_dir.mkdir(parents=True, exist_ok=True)

    # Copy skill contents (skip broken symlinks)
    for item in skill_source_dir.iterdir():
        src = skill_source_dir / item.name
        dst = target_skills_dir / item.name
        # Skip broken symlinks
        if src.is_symlink() and not src.exists():
            continue
        try:
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True,
                                ignore_dangling_symlinks=True)
            else:
                shutil.copy2(src, dst)
        except (shutil.Error, OSError) as e:
            # Skip files/dirs that fail to copy (broken symlinks, permissions)
            print(f"    WARN: skipped {item.name}: {e}")

    # Remove any embedded .git directories
    for git_dir in plugin_dir.rglob(".git"):
        if git_dir.is_dir():
            shutil.rmtree(git_dir)

    # Create plugin.json
    plugin_json = {
        "name": skill_name,
        "version": "1.0.0",
        "description": f"{skill_name} skill from {repo_name}",
        "author": {"name": repo_name.split("/")[0]},
        "repository": f"https://github.com/{repo_name}",
    }
    with open(claude_dir / "plugin.json", "w") as f:
        json.dump(plugin_json, f, indent=2)
        f.write("\n")

    return True


def update_marketplace(skills):
    """Update marketplace.json with all synced plugins."""
    # Start with hello-world (bundled)
    plugins = [
        {
            "name": "hello-world",
            "description": "Example plugin demonstrating marketplace patterns",
            "source": "./plugins/hello-world",
            "version": "1.0.0",
            "author": {"name": "Ulpi"},
            "category": "productivity",
        }
    ]

    for s in skills:
        plugin_dir = PLUGINS_DIR / s["name"]
        if not (plugin_dir / ".claude-plugin" / "plugin.json").exists():
            continue
        plugins.append({
            "name": s["name"],
            "description": f"{s['name']} skill from {s['repo']}",
            "source": f"./plugins/{s['name']}",
            "category": "skills",
        })

    marketplace = {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": "ulpi-marketplace",
        "version": "1.0.1",
        "description": "Claude Code Plugin Marketplace collected  by Ulpi",
        "owner": {
            "name": "Ulpi",
            "email": "hello@ulpi.io",
        },
        "plugins": plugins,
    }

    for mp_file in MARKETPLACE_FILES:
        mp_file.parent.mkdir(parents=True, exist_ok=True)
        with open(mp_file, "w") as f:
            json.dump(marketplace, f, indent=2)
            f.write("\n")

    return len(plugins)


def main():
    parser = argparse.ArgumentParser(description="Sync skills into marketplace")
    parser.add_argument("--all", action="store_true",
                        help="Re-sync all skills (default: only new ones)")
    parser.add_argument("--limit", type=int,
                        help="Only process first N skills from the list")
    parser.add_argument("--from", type=int, dest="from_rank",
                        help="Start from this rank number (skip earlier skills)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without making changes")
    args = parser.parse_args()

    if not TRACKED_FILE.exists():
        print(f"ERROR: {TRACKED_FILE} not found")
        sys.exit(1)

    skills = parse_tracked_skills(limit=args.limit)
    if args.from_rank:
        skills = [s for s in skills if s["rank"] >= args.from_rank]
    existing = get_existing_plugins()
    print(f"Found {len(skills)} skills in tracked list, {len(existing)} already synced")

    # Build index lookup: skill name -> position in tracked list
    skill_index = {s["name"]: i + 1 for i, s in enumerate(skills)}
    total_tracked = len(skills)

    # Decide which skills to sync
    if args.all:
        to_sync = skills
        print(f"Mode: --all (re-syncing everything)")
    else:
        to_sync = [s for s in skills if s["name"] not in existing]
        skipped = len(skills) - len(to_sync)
        print(f"Mode: incremental ({len(to_sync)} new, {skipped} already exist)")

    if not to_sync:
        print("Nothing new to sync.")
        # Still update marketplace in case tracked list changed
        total_plugins = update_marketplace(skills)
        print(f"Marketplace updated: {total_plugins} plugins")
        return

    if args.dry_run:
        for s in to_sync:
            idx = skill_index[s["name"]]
            exists = s["name"] in existing
            status = "RESYNC" if exists else "NEW"
            print(f"  [{idx}/{total_tracked}] [{status}] {s['name']} <- {s['repo']} ({s['installs']})")
        return

    # Group by repo to minimize clones
    repos = {}
    for s in to_sync:
        repos.setdefault(s["repo"], []).append(s)

    print(f"Skills to sync come from {len(repos)} unique repos")

    # Clone repos into temp directory
    clone_dir = Path(tempfile.mkdtemp(prefix="skill-repos-"))
    print(f"Cloning repos to {clone_dir}")

    synced = 0
    failed = []

    for repo, repo_skills in repos.items():
        repo_path = clone_repo(repo, clone_dir)

        for s in repo_skills:
            idx = skill_index[s["name"]]
            skill_dir = find_skill_dir(repo_path, s["name"])
            if skill_dir is None:
                print(f"  [{idx}/{total_tracked}] SKIP {s['name']}: could not find SKILL.md in {repo}")
                failed.append(s["name"])
                continue

            if not (skill_dir / "SKILL.md").exists():
                print(f"  [{idx}/{total_tracked}] SKIP {s['name']}: no SKILL.md in {skill_dir}")
                failed.append(s["name"])
                continue

            create_plugin(s["name"], skill_dir, repo)
            synced += 1
            print(f"  [{idx}/{total_tracked}] OK {s['name']} <- {skill_dir.relative_to(repo_path)}")

        # Clean up cloned repo immediately to save disk space
        if repo_path and repo_path.exists():
            shutil.rmtree(repo_path, ignore_errors=True)

    # Update marketplace.json (always uses full skills list, not just to_sync)
    total_plugins = update_marketplace(skills)

    # Cleanup temp directory
    shutil.rmtree(clone_dir, ignore_errors=True)

    print(f"\nDone: {synced} synced, {len(failed)} failed, {total_plugins} total plugins in marketplace")
    if failed:
        print(f"Failed skills: {', '.join(failed)}")


if __name__ == "__main__":
    main()
