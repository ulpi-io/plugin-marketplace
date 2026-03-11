#!/usr/bin/env python3
"""
Copy top N publishers from plugins_bk/ into plugins/.

All publisher dirs live in plugins_bk/. This script copies the top N
(by total installs) into plugins/ for testing incrementally.

Usage:
    python3 scripts/trim-plugins.py 10          # copy top 10 publishers
    python3 scripts/trim-plugins.py 20          # copy top 20
    python3 scripts/trim-plugins.py 10 --dry-run # preview only

First time setup:
    mv plugins plugins_bk
    mkdir plugins
    cp -r plugins_bk/hello-world plugins/
    python3 scripts/trim-plugins.py 10
"""

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
PLUGINS_DIR = ROOT / "plugins"
BACKUP_DIR = ROOT / "plugins_bk"
TRACKED_FILE = ROOT / "skills-tracked.md"

KEEP_ALWAYS = {"hello-world"}


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


def get_top_publishers(limit):
    publishers = {}
    with open(TRACKED_FILE) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("---") or line.startswith("Rank"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) != 4:
                continue
            try:
                int(parts[0])
            except ValueError:
                continue
            pub = parts[2].split("/")[0]
            publishers.setdefault(pub, 0)
            publishers[pub] += parse_installs(parts[3])

    sorted_pubs = sorted(publishers.items(), key=lambda x: x[1], reverse=True)
    return [pub for pub, _ in sorted_pubs[:limit]]


def main():
    parser = argparse.ArgumentParser(description="Copy top N publishers from plugins_bk/ to plugins/")
    parser.add_argument("count", type=int, help="Number of top publishers to copy")
    parser.add_argument("--dry-run", action="store_true", help="Preview without copying")
    args = parser.parse_args()

    if not BACKUP_DIR.exists():
        print(f"ERROR: {BACKUP_DIR} not found. Move plugins/ to plugins_bk/ first.")
        return

    top = get_top_publishers(args.count)

    # Clear plugins/ except hello-world
    if not args.dry_run:
        for d in PLUGINS_DIR.iterdir():
            if d.is_dir() and d.name not in KEEP_ALWAYS:
                shutil.rmtree(d)

    copied = 0
    skipped = []
    for pub in top:
        src = BACKUP_DIR / pub
        if not src.exists():
            skipped.append(pub)
            continue
        if args.dry_run:
            print(f"  Would copy {pub}")
        else:
            dst = PLUGINS_DIR / pub
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore_dangling_symlinks=True)
        copied += 1

    if args.dry_run:
        print(f"\nWould copy {copied} publishers ({len(skipped)} not in plugins_bk/)")
    else:
        print(f"Copied {copied} publishers to plugins/ ({len(skipped)} not found)")

    if skipped:
        print(f"Skipped: {', '.join(skipped)}")


if __name__ == "__main__":
    main()
