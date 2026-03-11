#!/usr/bin/env python3
"""
WeChat Article Fetcher Skill
Main entry point for Claude Skills system
Fetch, analyze, and rank WeChat official account articles
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def parse_skill_arguments():
    """Parse arguments passed from Claude Skills system."""
    parser = argparse.ArgumentParser(
        description="WeChat Article Fetcher - Fetch and analyze WeChat articles",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Fetch command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch articles from WeChat')
    fetch_parser.add_argument(
        '--accounts',
        nargs='+',
        help='Specific account names to fetch (default: all followed accounts)'
    )
    fetch_parser.add_argument(
        '--since',
        choices=['yesterday', 'today', 'week', 'month'],
        default='yesterday',
        help='Fetch articles since when (default: yesterday)'
    )
    fetch_parser.add_argument(
        '--start-date',
        help='Start date (YYYY-MM-DD format)'
    )
    fetch_parser.add_argument(
        '--end-date',
        help='End date (YYYY-MM-DD format)'
    )
    fetch_parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='Maximum articles to fetch (default: 50)'
    )
    fetch_parser.add_argument(
        '--min-score',
        type=int,
        default=50,
        help='Minimum relevance score (0-100) to include (default: 50)'
    )
    fetch_parser.add_argument(
        '--save-obsidian',
        action='store_true',
        help='Save to Obsidian vault'
    )
    fetch_parser.add_argument(
        '--output-path',
        help='Obsidian vault path (default: auto-detect)'
    )
    fetch_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview without saving'
    )
    fetch_parser.add_argument(
        '--format',
        choices=['markdown', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
    )

    # List command
    list_parser = subparsers.add_parser('list', help='List followed accounts')
    list_parser.add_argument(
        '--format',
        choices=['table', 'json'],
        default='table',
        help='Output format (default: table)'
    )

    return parser.parse_args()

def call_mcp_tool(server, tool, params=None):
    """Call an MCP tool via subprocess."""
    cmd = ['mcp', 'call', server, tool]

    if params:
        import json
        cmd.append(json.dumps(params))

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except Exception as e:
        print(f"❌ Error calling MCP tool: {e}", file=sys.stderr)
        return None

def list_accounts(args):
    """List all followed WeChat accounts."""
    result = call_mcp_tool('wechat', 'list_followed_accounts')

    if not result:
        print("❌ Failed to list accounts", file=sys.stderr)
        return False

    if args.format == 'json':
        print(result)
    else:
        import json
        accounts = json.loads(result)
        print(f"\n📱 Followed Accounts ({len(accounts)}):\n")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account['name']}")
            print(f"   fakeid: {account['fakeid']}")
        print()

    return True

def fetch_articles(args):
    """Fetch and analyze WeChat articles."""
    from wechat_fetcher import WeChatArticleFetcher

    # Calculate date range
    if args.start_date and args.end_date:
        start_date = args.start_date
        end_date = args.end_date
    else:
        today = datetime.now(timezone.utc).date()

        if args.since == 'yesterday':
            start_date = (today - timedelta(days=1)).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif args.since == 'today':
            start_date = today.strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif args.since == 'week':
            start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')
        elif args.since == 'month':
            start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
            end_date = today.strftime('%Y-%m-%d')

    # Initialize fetcher
    fetcher = WeChatArticleFetcher(
        start_date=start_date,
        end_date=end_date,
        min_score=args.min_score,
        limit=args.limit
    )

    # Fetch articles
    if args.accounts:
        print(f"📱 Fetching articles from: {', '.join(args.accounts)}")
        articles = fetcher.fetch_from_accounts(args.accounts)
    else:
        print("📱 Fetching articles from all followed accounts...")
        articles = fetcher.fetch_all()

    if not articles:
        print("❌ No articles found", file=sys.stderr)
        return False

    # Analyze and rank
    print(f"📊 Analyzing {len(articles)} articles...")
    ranked_articles = fetcher.analyze_and_rank(articles)

    # Generate output
    if args.format == 'json':
        print(json.dumps(ranked_articles, indent=2, ensure_ascii=False))
    else:
        report = fetcher.generate_markdown_report(ranked_articles)
        print(report)

    # Save to Obsidian
    if args.save_obsidian and not args.dry_run:
        print("💾 Saving to Obsidian...")
        success = fetcher.save_to_obsidian(report)
        if success:
            print("✅ Saved successfully!")
        else:
            print("❌ Failed to save", file=sys.stderr)
            return False

    return True

def main():
    """Main entry point."""
    args = parse_skill_arguments()

    if not args.command:
        print("❌ No command specified", file=sys.stderr)
        print("Available commands: fetch, list")
        return 1

    try:
        if args.command == 'fetch':
            success = fetch_articles(args)
            return 0 if success else 1
        elif args.command == 'list':
            success = list_accounts(args)
            return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
