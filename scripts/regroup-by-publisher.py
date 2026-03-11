#!/usr/bin/env python3
"""
Sync skills from skills-tracked.md into publisher-grouped plugins.

Each GitHub repo becomes ONE plugin containing all its skills.
E.g. anthropics/skills → plugins/anthropics-skills/skills/{skill1,skill2,...}

Usage:
    python3 sync-skills-grouped.py                # sync only NEW repos
    python3 sync-skills-grouped.py --all          # re-sync everything
    python3 sync-skills-grouped.py --limit 500    # top 500 skills only
    python3 sync-skills-grouped.py --dry-run      # preview without changes
"""

import argparse
import json
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


def repo_to_publisher(repo):
    """Convert 'anthropics/skills' to 'anthropics' (org name)."""
    return repo.split("/")[0]


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


def group_by_publisher(skills):
    """Group skills by their GitHub org/publisher."""
    groups = {}
    for s in skills:
        publisher = repo_to_publisher(s["repo"])
        groups.setdefault(publisher, []).append(s)
    return groups


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
    """Find the directory containing SKILL.md for a given skill name."""
    if repo_path is None:
        return None

    search_prefixes = ["skills", "plugin/skills"]
    github_plugins = repo_path / ".github" / "plugins"
    if github_plugins.exists():
        try:
            for d in github_plugins.iterdir():
                if d.is_dir() and (d / "skills").is_dir():
                    search_prefixes.append(f".github/plugins/{d.name}/skills")
        except OSError:
            pass
    if (repo_path / ".claude" / "skills").is_dir():
        search_prefixes.append(".claude/skills")

    # Exact match
    for prefix in search_prefixes:
        candidate = repo_path / prefix / skill_name
        if (candidate / "SKILL.md").exists():
            return candidate

    # Suffix match
    name_parts = skill_name.split("-")
    for prefix in search_prefixes:
        skills_root = repo_path / prefix
        if not skills_root.exists():
            continue
        try:
            dirs = [d.name for d in skills_root.iterdir() if d.is_dir()]
        except OSError:
            continue
        for i in range(len(name_parts)):
            suffix = "-".join(name_parts[i:])
            for d in dirs:
                if d == suffix:
                    return skills_root / d
        for d in dirs:
            if d in skill_name or skill_name in d:
                candidate = skills_root / d
                if (candidate / "SKILL.md").exists():
                    return candidate

    # Fuzzy: find all SKILL.md files
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


def copy_skill(skill_source_dir, target_skills_dir, skill_name):
    """Copy a single skill into the plugin's skills/ directory."""
    dst = target_skills_dir / skill_name
    dst.mkdir(parents=True, exist_ok=True)

    for item in skill_source_dir.iterdir():
        src = skill_source_dir / item.name
        dest = dst / item.name
        if src.is_symlink() and not src.exists():
            continue
        try:
            if src.is_dir():
                shutil.copytree(src, dest, dirs_exist_ok=True,
                                ignore_dangling_symlinks=True)
            else:
                shutil.copy2(src, dest)
        except (shutil.Error, OSError) as e:
            print(f"    WARN: skipped {item.name}: {e}")


def create_publisher_plugin(plugin_name, repos, skill_names):
    """Create a publisher plugin with all its skills already copied.

    repos is a list of repo strings (e.g. ['vercel-labs/skills', 'vercel-labs/agent-skills']).
    Returns the plugin directory path.
    """
    plugin_dir = PLUGINS_DIR / plugin_name
    claude_dir = plugin_dir / ".claude-plugin"
    claude_dir.mkdir(parents=True, exist_ok=True)

    # Remove embedded .git directories
    for git_dir in plugin_dir.rglob(".git"):
        if git_dir.is_dir():
            shutil.rmtree(git_dir)

    # Create plugin.json
    skills_list = ", ".join(skill_names)
    repos_str = ", ".join(repos)
    description = f"{len(skill_names)} skills from {repos_str}: {skills_list}"
    plugin_json = {
        "name": plugin_name,
        "version": "1.0.0",
        "description": description,
        "author": {"name": plugin_name},
        "repositories": [f"https://github.com/{r}" for r in repos],
        "skills": skill_names,
    }
    with open(claude_dir / "plugin.json", "w") as f:
        json.dump(plugin_json, f, indent=2)
        f.write("\n")

    return plugin_dir


def update_marketplace(pub_groups, version="1.0.6"):
    """Update marketplace.json with publisher-grouped plugins."""
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

    # Sort publishers by total installs descending
    sorted_pubs = sorted(
        pub_groups.items(),
        key=lambda x: sum(parse_installs(s["installs"]) for s in x[1]),
        reverse=True,
    )

    for publisher, skills in sorted_pubs:
        plugin_dir = PLUGINS_DIR / publisher
        if not (plugin_dir / ".claude-plugin" / "plugin.json").exists():
            continue
        skill_names = [s["name"] for s in skills]
        skills_list = ", ".join(skill_names)
        plugins.append({
            "name": publisher,
            "description": f"{len(skills)} skills: {skills_list}",
            "source": f"./plugins/{publisher}",
            "category": "skills",
        })

    marketplace = {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": "ulpi-marketplace",
        "version": version,
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


def clean_old_plugins():
    """Remove all plugin directories except hello-world."""
    if not PLUGINS_DIR.exists():
        return 0
    removed = 0
    for d in PLUGINS_DIR.iterdir():
        if d.is_dir() and d.name != "hello-world":
            shutil.rmtree(d, ignore_errors=True)
            removed += 1
    return removed


def main():
    parser = argparse.ArgumentParser(description="Sync skills grouped by publisher")
    parser.add_argument("--all", action="store_true",
                        help="Re-sync all (clean and rebuild)")
    parser.add_argument("--limit", type=int,
                        help="Only process top N skills from the list")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be done without making changes")
    args = parser.parse_args()

    if not TRACKED_FILE.exists():
        print(f"ERROR: {TRACKED_FILE} not found")
        sys.exit(1)

    skills = parse_tracked_skills(limit=args.limit)
    pub_groups = group_by_publisher(skills)
    existing = get_existing_plugins()

    print(f"Found {len(skills)} skills from {len(pub_groups)} publishers")
    print(f"Existing plugins: {len(existing)}")

    if args.dry_run:
        sorted_pubs = sorted(
            pub_groups.items(),
            key=lambda x: sum(parse_installs(s["installs"]) for s in x[1]),
            reverse=True,
        )
        for publisher, group in sorted_pubs:
            total = sum(parse_installs(s["installs"]) for s in group)
            exists = publisher in existing
            status = "EXISTS" if exists else "NEW"
            repos = sorted(set(s["repo"] for s in group))
            print(f"  [{status}] {publisher} ({len(group)} skills, {len(repos)} repos, {total:.0f} installs)")
        print(f"\nWould create {len(pub_groups)} publisher plugins")
        return

    # Determine which publishers need syncing
    if args.all:
        repos_to_sync = pub_groups
    else:
        repos_to_sync = {
            pub: skills for pub, skills in pub_groups.items()
            if pub not in existing
        }
    print(f"Publishers to sync: {len(repos_to_sync)}")

    if not repos_to_sync:
        print("Nothing new to sync.")
        total_plugins = update_marketplace(pub_groups)
        print(f"Marketplace updated: {total_plugins} plugins")
        return

    # Build index of existing local skill dirs: skill_name -> path to skills/skill_name/
    local_skills = {}
    for d in PLUGINS_DIR.iterdir():
        if not d.is_dir() or d.name == "hello-world":
            continue
        skills_dir = d / "skills"
        if not skills_dir.exists():
            continue
        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                local_skills[skill_dir.name] = skill_dir

    print(f"Found {len(local_skills)} skills locally in plugins/")

    # Reorganize: move skills into publisher-grouped plugin dirs
    # First, collect what goes where (don't move yet)
    plan = {}  # publisher -> [(skill_name, source_path, repo)]
    for publisher, pub_skills in repos_to_sync.items():
        for s in pub_skills:
            source = local_skills.get(s["name"])
            if source is None:
                continue
            plan.setdefault(publisher, []).append((s["name"], source, s["repo"]))

    # Now create new publisher dirs in a temp location, then swap
    temp_plugins = PLUGINS_DIR.parent / "plugins-new"
    if temp_plugins.exists():
        shutil.rmtree(temp_plugins)
    temp_plugins.mkdir()

    # Copy hello-world
    hw = PLUGINS_DIR / "hello-world"
    if hw.exists():
        shutil.copytree(hw, temp_plugins / "hello-world")

    synced_repos = 0
    synced_skills = 0
    failed_skills = []

    for publisher, entries in plan.items():
        plugin_dir = temp_plugins / publisher
        target_skills_dir = plugin_dir / "skills"
        target_skills_dir.mkdir(parents=True, exist_ok=True)

        skill_names_ok = []
        repos_used = []

        for skill_name, source_path, repo in entries:
            dst = target_skills_dir / skill_name
            try:
                shutil.copytree(source_path, dst, dirs_exist_ok=True,
                                ignore_dangling_symlinks=True)
                skill_names_ok.append(skill_name)
                synced_skills += 1
                if repo not in repos_used:
                    repos_used.append(repo)
            except (shutil.Error, OSError) as e:
                print(f"    SKIP {skill_name}: {e}")
                failed_skills.append(skill_name)

        if skill_names_ok:
            # Create plugin.json
            claude_dir = plugin_dir / ".claude-plugin"
            claude_dir.mkdir(parents=True, exist_ok=True)
            skills_list = ", ".join(skill_names_ok)
            repos_str = ", ".join(repos_used)
            description = f"{len(skill_names_ok)} skills from {repos_str}: {skills_list}"
            plugin_json = {
                "name": publisher,
                "version": "1.0.0",
                "description": description,
                "author": {"name": publisher},
                "repositories": [f"https://github.com/{r}" for r in repos_used],
                "skills": skill_names_ok,
            }
            with open(claude_dir / "plugin.json", "w") as f:
                json.dump(plugin_json, f, indent=2)
                f.write("\n")

            # Remove embedded .git dirs
            for git_dir in plugin_dir.rglob(".git"):
                if git_dir.is_dir():
                    shutil.rmtree(git_dir)

            synced_repos += 1
            print(f"  OK {publisher} ({len(skill_names_ok)} skills from {len(repos_used)} repos)")
        else:
            if plugin_dir.exists():
                shutil.rmtree(plugin_dir, ignore_errors=True)

    # Swap old plugins for new (keeps plugins-old as backup)
    old_plugins = PLUGINS_DIR.parent / "plugins-old"
    if old_plugins.exists():
        shutil.rmtree(old_plugins)
    PLUGINS_DIR.rename(old_plugins)
    temp_plugins.rename(PLUGINS_DIR)
    print(f"\nOld plugins saved to plugins-old/ — delete manually when satisfied")

    # Update marketplace
    total_plugins = update_marketplace(pub_groups)

    print(f"\nDone: {synced_repos} repos synced, {synced_skills} skills, "
          f"{len(failed_skills)} failed, {total_plugins} total plugins in marketplace")
    if failed_skills:
        print(f"Failed: {', '.join(failed_skills[:20])}{'...' if len(failed_skills) > 20 else ''}")


if __name__ == "__main__":
    main()
