"""
WeChat Article Fetcher - Core implementation
Fetch, analyze, and rank WeChat articles based on research interests
"""

import json
import subprocess
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional


class WeChatArticleFetcher:
    """Main class for fetching and analyzing WeChat articles."""

    # Research interest tiers for ranking
    RESEARCH_INTERESTS = {
        # Tier 1: Core research areas (highest priority)
        "tier_1": {
            "keywords": [
                "agent for system", "ai agent", "multi-agent system",
                "autonomous agent", "llm agent", "agent framework"
            ],
            "weight": 10
        },

        # Tier 2: System & Architecture
        "tier_2": {
            "keywords": [
                "system design", "distributed system", "operating system",
                "computer architecture", "concurrent", "scalability"
            ],
            "weight": 8.5
        },

        # Tier 3: GitHub Open Source Projects
        "tier_3": {
            "keywords": [
                "github", "open source", "开源项目", "开源工具",
                "framework", "library", "implementation", "代码实现"
            ],
            "weight": 8
        },

        # Tier 4: AI/ML Core
        "tier_4": {
            "keywords": [
                "machine learning", "deep learning", "reinforcement learning",
                "transformer", "large language model", "llm", "neural network"
            ],
            "weight": 7.5
        },

        # Tier 5: Academic Research
        "tier_5": {
            "keywords": [
                "sota", "benchmark", "paper review", "arxiv",
                "neurips", "icml", "icse", "osdi", "sosp", "论文"
            ],
            "weight": 6.5
        },

        # Tier 6: General Tech
        "tier_6": {
            "keywords": [
                "tutorial", "best practice", "practice", "guide", "技巧"
            ],
            "weight": 4.5
        }
    }

    def __init__(
        self,
        start_date: str,
        end_date: str,
        min_score: int = 50,
        limit: int = 50
    ):
        """
        Initialize the fetcher.

        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            min_score: Minimum relevance score (0-100)
            limit: Maximum articles to fetch
        """
        self.start_date = start_date
        self.end_date = end_date
        self.min_score = min_score
        self.limit = limit

    def call_mcp_tool(self, server: str, tool: str, params: Dict = None) -> Optional[str]:
        """
        Call an MCP tool via subprocess.

        Args:
            server: MCP server name
            tool: Tool name
            params: Tool parameters

        Returns:
            Tool output or None if failed
        """
        cmd = ['mcp', 'call', server, tool]

        if params:
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
                print(f"⚠️  MCP tool failed: {result.stderr}", file=__import__('sys').stderr)
                return None
        except Exception as e:
            print(f"❌ Error calling MCP tool: {e}", file=__import__('sys').stderr)
            return None

    def list_accounts(self) -> List[Dict[str, str]]:
        """Get all followed WeChat accounts."""
        result = self.call_mcp_tool('wechat', 'list_followed_accounts')

        if not result:
            return []

        return json.loads(result)

    def fetch_from_accounts(self, account_names: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch articles from specific accounts.

        Args:
            account_names: List of account names

        Returns:
            List of articles
        """
        accounts = self.list_accounts()
        all_articles = []

        # Find account fakeids by name
        account_map = {acc['name']: acc['fakeid'] for acc in accounts}

        for name in account_names:
            if name not in account_map:
                print(f"⚠️  Account not found: {name}", file=__import__('sys').stderr)
                continue

            fakeid = account_map[name]
            articles = self._fetch_articles_from_account(fakeid, name)
            all_articles.extend(articles)

        return all_articles

    def fetch_all(self) -> List[Dict[str, Any]]:
        """Fetch articles from all followed accounts."""
        accounts = self.list_accounts()
        all_articles = []

        for account in accounts:
            articles = self._fetch_articles_from_account(
                account['fakeid'],
                account['name']
            )
            all_articles.extend(articles)

        return all_articles

    def _fetch_articles_from_account(
        self,
        fakeid: str,
        account_name: str
    ) -> List[Dict[str, Any]]:
        """Fetch articles from a single account."""
        params = {
            "fakeid": fakeid,
            "start_date": self.start_date,
            "limit": 20
        }

        result = self.call_mcp_tool('wechat', 'get_account_articles', params)

        if not result:
            return []

        try:
            data = json.loads(result)
            articles = data.get('articles', [])

            # Add account name to each article
            for article in articles:
                article['account'] = account_name

            return articles
        except json.JSONDecodeError:
            print(f"⚠️  Failed to parse articles from {account_name}", file=__import__('sys').stderr)
            return []

    def calculate_relevance_score(self, article: Dict[str, Any]) -> int:
        """
        Calculate relevance score based on research interests.

        Args:
            article: Article data

        Returns:
            Relevance score (0-100)
        """
        score = 0
        text = (
            article.get('title', '') + ' ' +
            article.get('content', '') + ' ' +
            article.get('digest', '')
        ).lower()

        # Score based on research interest tiers
        for tier in self.RESEARCH_INTERESTS.values():
            for keyword in tier['keywords']:
                if keyword.lower() in text:
                    score += tier['weight']

        # Normalize to 0-100
        return min(int(score * 2), 100)

    def analyze_and_rank(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze and rank articles by relevance.

        Args:
            articles: List of articles

        Returns:
            Ranked list of articles with analysis
        """
        analyzed_articles = []

        for article in articles:
            score = self.calculate_relevance_score(article)

            # Filter by minimum score
            if score < self.min_score:
                continue

            # Add analysis
            analyzed_article = {
                **article,
                'relevance_score': score,
                'tier': self._get_tier_label(score),
                'summary': self._generate_summary(article),
                'research_alignment': self._get_research_alignment(article),
                'action_items': self._generate_action_items(article, score)
            }

            analyzed_articles.append(analyzed_article)

        # Sort by relevance score (descending)
        analyzed_articles.sort(key=lambda x: x['relevance_score'], reverse=True)

        # Limit results
        return analyzed_articles[:self.limit]

    def _get_tier_label(self, score: int) -> str:
        """Get tier label based on score."""
        if score >= 90:
            return "Must Read"
        elif score >= 70:
            return "High Priority"
        elif score >= 50:
            return "Interesting"
        else:
            return "Skipped"

    def _generate_summary(self, article: Dict[str, Any]) -> str:
        """Generate a brief summary of the article."""
        # Use digest if available, otherwise truncate content
        digest = article.get('digest', '').strip()
        content = article.get('content', '')

        if digest:
            return digest[:200] + '...' if len(digest) > 200 else digest
        elif content:
            return content[:200] + '...' if len(content) > 200 else content
        else:
            return "No summary available"

    def _get_research_alignment(self, article: Dict[str, Any]) -> str:
        """Get research alignment explanation."""
        text = article.get('title', '') + ' ' + article.get('digest', '')

        alignments = []

        # Check for tier 1 keywords
        for keyword in self.RESEARCH_INTERESTS['tier_1']['keywords']:
            if keyword.lower() in text.lower():
                alignments.append(f"Directly related to {keyword}")
                break

        # Check for tier 3 keywords (GitHub)
        for keyword in self.RESEARCH_INTERESTS['tier_3']['keywords']:
            if keyword.lower() in text.lower():
                alignments.append("Interesting open source project/tool")
                break

        return '; '.join(alignments) if alignments else "General tech article"

    def _generate_action_items(self, article: Dict[str, Any], score: int) -> List[str]:
        """Generate action items based on article type and score."""
        items = []

        if score >= 90:
            items.append("Read full paper/article")
            items.append("Analyze key insights")

        # Check for GitHub/Code links
        content = article.get('content', '') + article.get('title', '')
        if 'github' in content.lower() or '代码' in content or '开源' in content:
            items.append("Check out GitHub repository")
            items.append("Evaluate code quality")

        if score >= 70:
            items.append("Bookmark for reference")

        return items

    def generate_markdown_report(self, articles: List[Dict[str, Any]]) -> str:
        """Generate a Markdown report."""
        if not articles:
            return "# No articles found\n\nNo articles matched your criteria."

        # Calculate statistics
        total = len(articles)
        must_read = sum(1 for a in articles if a['relevance_score'] >= 90)
        high_priority = sum(1 for a in articles if 70 <= a['relevance_score'] < 90)
        interesting = sum(1 for a in articles if 50 <= a['relevance_score'] < 70)

        # Generate frontmatter
        created_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        frontmatter = f"""---
title: "{self.end_date} 微信公众号文章汇总"
date: {self.end_date}
tags: [wechat, daily-summary, ai-agent, system, github]
created: {created_time}
research_focus: [AI Agent, Agent for System, Multi-Agent System]
statistics:
  total_articles: {total}
  must_read: {must_read}
  high_priority: {high_priority}
  interesting: {interesting}
---

"""

        # Generate header
        header = f"""# 微信公众号文章汇总 - {self.end_date}

> 📅 时间范围：{self.start_date} 至 {self.end_date}
> 🎯 研究聚焦：AI Agent, Agent for System, Multi-Agent System
> 📊 分析文章：{total} 篇

---

"""

        # Group articles by tier
        must_read_articles = [a for a in articles if a['relevance_score'] >= 90]
        high_priority_articles = [a for a in articles if 70 <= a['relevance_score'] < 90]
        interesting_articles = [a for a in articles if 50 <= a['relevance_score'] < 70]

        # Generate sections
        sections = []

        if must_read_articles:
            sections.append(self._generate_section("🔥 Must Read (Score: 9-10)", must_read_articles))

        if high_priority_articles:
            sections.append(self._generate_section("📚 High Priority (Score: 7-8)", high_priority_articles))

        if interesting_articles:
            sections.append(self._generate_section("💡 Interesting (Score: 5-6)", interesting_articles))

        # Generate statistics
        stats = f"""
## 📊 今日统计

| 分类 | 数量 | 占比 |
|------|------|------|
| 🔥 Must Read | {must_read} | {must_read/total*100:.0f}% |
| 📚 High Priority | {high_priority} | {high_priority/total*100:.0f}% |
| 💡 Interesting | {interesting} | {interesting/total*100:.0f}% |

---

*本文档由自动化脚本生成 - {datetime.now().strftime('%Y年%m月%d日 %H:%M')}*
"""

        return frontmatter + header + '\n\n'.join(sections) + stats

    def _generate_section(self, title: str, articles: List[Dict[str, Any]]) -> str:
        """Generate a section for articles."""
        lines = [f"## {title}\n"]

        for i, article in enumerate(articles, 1):
            title_text = article.get('title', 'Untitled')
            account = article.get('account', 'Unknown')
            score = article['relevance_score']
            summary = article.get('summary', '')
            alignment = article.get('research_alignment', '')
            action_items = article.get('action_items', [])
            url = article.get('url', '#')

            lines.append(f"### {i}. {title_text}\n")
            lines.append(f"**来源**:: {account}")
            lines.append(f"**评分**:: {score}/100\n")
            lines.append(f"**核心内容**:: {summary}\n")
            lines.append(f"**研究关联**:: {alignment}\n")

            if action_items:
                lines.append("**行动项**::")
                for item in action_items:
                    lines.append(f"- [ ] {item}")
                lines.append("")

            lines.append(f"**相关链接**:: [原文]({url})")
            lines.append("\n---\n")

        return '\n'.join(lines)

    def save_to_obsidian(self, content: str) -> bool:
        """
        Save content to Obsidian vault.

        Args:
            content: Markdown content to save

        Returns:
            True if successful, False otherwise
        """
        filename = f"{self.end_date}-汇总.md"
        filepath = f"wechat-official-aacount/{filename}"

        params = {
            "filepath": filepath,
            "content": content
        }

        result = self.call_mcp_tool('obsidian', 'obsidian_append_content', params)

        return result is not None
