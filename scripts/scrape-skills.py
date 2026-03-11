#!/usr/bin/env python3
"""
Scrape skills.sh leaderboard using playwright-cli.

Scrolls through the skills leaderboard, collecting all skills with >= 1000
installs, and writes them to skills-tracked.md.

Usage:
    python3 scrape-skills.py                      # scrape all skills >= 1000 installs
    python3 scrape-skills.py --min-installs 5000  # only skills >= 5000 installs
    python3 scrape-skills.py --dry-run            # print results, don't write file

Requires: playwright-cli (npm install -g @playwright/cli)
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUTPUT_FILE = ROOT / "skills-tracked.md"

# JS runs in Node context — must use page.evaluate() for DOM access
JS_EXTRACT = r"""async page => {
  const r = await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('main a'));
    return links
      .filter(a => a.href.match(/skills\.sh\/[^\/]+\/[^\/]+\/[^\/]+/))
      .map(a => {
        const h3 = a.querySelector('h3');
        const p = a.querySelector('p');
        const divs = a.querySelectorAll(':scope > div');
        const rankDiv = divs[0];
        const installDiv = divs[divs.length - 1];
        if (h3 && p && rankDiv && installDiv) {
          return {
            rank: parseInt(rankDiv.textContent.trim()),
            name: h3.textContent.trim(),
            repo: p.textContent.trim(),
            installs: installDiv.textContent.trim()
          };
        }
        return null;
      })
      .filter(Boolean);
  });
  return JSON.stringify(r);
}"""

JS_SCROLL = r"""async page => {
  await page.evaluate(() => window.scrollBy(0, window.innerHeight * 3));
  await new Promise(r => setTimeout(r, 800));
  return 'scrolled';
}"""


def cli(*args, timeout=30):
    """Run playwright-cli command, return stdout."""
    result = subprocess.run(
        ["playwright-cli", *args],
        capture_output=True, text=True, timeout=timeout,
    )
    return result.stdout, result.returncode


def run_code(js):
    """Run JS via playwright-cli run-code and parse the JSON result."""
    stdout, rc = cli("run-code", js)
    if rc != 0:
        return None

    # Output format:
    #   ### Result
    #   "<escaped JSON string>"
    #   ### Ran Playwright code
    #   ...
    for line in stdout.splitlines():
        line = line.strip()
        # Match the quoted JSON string line
        if line.startswith('"') and line.endswith('"'):
            inner = line[1:-1].replace('\\"', '"')
            try:
                return json.loads(inner)
            except json.JSONDecodeError:
                pass
    return None


def parse_installs(s):
    """Convert '496.3K' or '997' to a number."""
    s = s.strip()
    if s.endswith("K"):
        return float(s[:-1]) * 1000
    elif s.endswith("M"):
        return float(s[:-1]) * 1_000_000
    return float(s.replace(",", ""))


def scrape(min_installs=1000, max_iterations=300):
    """Open browser, scroll skills.sh, collect skills above threshold."""
    print("Opening skills.sh...")
    cli("open", "https://skills.sh", timeout=30)

    all_skills = []
    seen = set()
    done = False
    iteration = 0

    print(f"Collecting skills with >= {min_installs:,} installs...")

    while not done and iteration < max_iterations:
        iteration += 1

        data = run_code(JS_EXTRACT)
        if not isinstance(data, list):
            data = []

        new_count = 0
        for s in data:
            key = f"{s['rank']}:{s['name']}"
            if key in seen:
                continue
            seen.add(key)

            if parse_installs(s["installs"]) < min_installs:
                done = True
                break

            all_skills.append(s)
            new_count += 1

        if new_count > 0:
            last = all_skills[-1]
            print(f"  [{iteration}] {len(all_skills)} skills "
                  f"(#{last['rank']} {last['name']} {last['installs']})")

        if not done:
            run_code(JS_SCROLL)

    print("Closing browser...")
    cli("close")

    all_skills.sort(key=lambda x: x["rank"])
    return all_skills


def write_tracked(skills):
    """Write skills-tracked.md."""
    with open(OUTPUT_FILE, "w") as f:
        f.write("# Skills with 1000+ Installs (from skills.sh)\n\n")
        f.write("Rank | Skill | Repo | Installs\n")
        f.write("--- | --- | --- | ---\n")
        for s in skills:
            f.write(f"{s['rank']} | {s['name']} | {s['repo']} | {s['installs']}\n")
    print(f"Written {len(skills)} skills to {OUTPUT_FILE}")


def main():
    parser = argparse.ArgumentParser(description="Scrape skills.sh leaderboard")
    parser.add_argument("--min-installs", type=int, default=1000,
                        help="Minimum install count (default: 1000)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print results without writing file")
    args = parser.parse_args()

    skills = scrape(min_installs=args.min_installs)

    print(f"\nCollected {len(skills)} skills with >= {args.min_installs:,} installs")
    if skills:
        print(f"  Top:    #{skills[0]['rank']} {skills[0]['name']} ({skills[0]['installs']})")
        print(f"  Bottom: #{skills[-1]['rank']} {skills[-1]['name']} ({skills[-1]['installs']})")

    if args.dry_run:
        for s in skills:
            print(f"  {s['rank']} | {s['name']} | {s['repo']} | {s['installs']}")
    else:
        write_tracked(skills)


if __name__ == "__main__":
    main()
