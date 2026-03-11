# WeChat Article Fetcher - CLI Usage Guide

## Command Reference

### Basic Usage

```bash
# Get yesterday's articles
python skill.py fetch --since yesterday

# Fetch specific accounts
python skill.py fetch --accounts "量子位" "PaperAgent"

# Specify date range
python skill.py fetch --start-date 2025-01-15 --end-date 2025-01-20

# Only get high-scoring articles
python skill.py fetch --min-score 70

# Preview without saving to Obsidian
python skill.py fetch --dry-run
```

## Complete Parameters

| Parameter | Short | Type | Default | Description |
|-----------|-------|------|---------|-------------|
| `--since` | | string | yesterday | Time filter: yesterday, today, specific date |
| `--start-date` | | string | | Start date (YYYY-MM-DD) |
| `--end-date` | | string | | End date (YYYY-MM-DD) |
| `--accounts` | | list | | Specific WeChat accounts to fetch |
| `--min-score` | | int | 50 | Minimum relevance score (0-100) |
| `--limit` | | int | 50 | Maximum articles to fetch |
| `--save-obsidian` | | flag | false | Save to Obsidian vault |
| `--output-path` | | string | | Custom Obsidian vault path |
| `--dry-run` | | flag | false | Preview without saving |

## Usage Examples

### Daily Research Workflow

```bash
# Get yesterday's articles and save to Obsidian
python skill.py fetch --since yesterday --save-obsidian
```

**Output**: Saves to `wechat-official-aacount/YYYY-MM-DD-汇总.md`

### Topic-Specific Fetching

```bash
# Get AI Agent articles from specific accounts
python skill.py fetch \
  --accounts "量子位" "PaperAgent" "机器之心" \
  --min-score 70 \
  --save-obsidian
```

**Output**: Only articles with score ≥70 from specified accounts

### Date Range Query

```bash
# Get articles from last week
python skill.py fetch \
  --start-date 2025-01-13 \
  --end-date 2025-01-19 \
  --save-obsidian
```

**Output**: All articles from the specified date range

### Preview Before Saving

```bash
# See what will be fetched
python skill.py fetch --since yesterday --dry-run

# Preview with score threshold
python skill.py fetch --min-score 80 --dry-run
```

**Output**: Console preview with article count and scores

## Output Format

### Obsidian Format

**File**: `wechat-official-aacount/YYYY-MM-DD-微信公众号文章汇总.md`

```markdown
---
title: "2025-01-19 微信公众号文章汇总"
date: 2025-01-19
tags: [wechat, daily-summary, ai-agent, system]
created: 2025-01-19T08:30:00Z
research_focus: [AI Agent, System Design]
statistics:
  total_articles: 45
  must_read: 8
  high_priority: 15
---

## 🔥 Must Read (Score: 90-100)

### [[Agentic AI 综述]]
**来源**: [[PaperAgent]]
**评分**: 95/100
**核心内容**: 全面分析 Agentic AI 范式演进与系统架构...
**研究关联**: 直接相关核心研究，必读
**行动项**:
- [ ] 阅读完整论文
- [ ] 分析架构图
**链接**: [原文](...)

## 📚 High Priority (Score: 70-89)

### [[LLM系统优化实战]]
**来源**: [[机器之心]]
**评分**: 85/100
...
```

### JSON Format

```json
{
  "date": "2025-01-19",
  "total_articles": 45,
  "articles": [
    {
      "title": "Agentic AI 综述",
      "source": "PaperAgent",
      "score": 95,
      "category": "must_read",
      "summary": "全面分析 Agentic AI 范式...",
      "tags": ["ai-agent", "llm", "system"],
      "actions": ["阅读完整论文", "分析架构图"],
      "link": "https://..."
    }
  ]
}
```

## Research Interest Ranking

See `references/ranking-system.md` for complete details on:
- 6-tier priority system
- Keyword matching algorithm
- Score calculation logic
- Category assignment rules

## Quick Reference

### Common Commands

```bash
# Daily routine (every morning)
python skill.py fetch --since yesterday --save-obsidian

# Quick check (preview only)
python skill.py fetch --dry-run

# High-value articles only
python skill.py fetch --min-score 80 --save-obsidian

# Specific date range
python skill.py fetch --start-date YYYY-MM-DD --end-date YYYY-MM-DD
```

### Custom Output Path

```bash
# Save to custom location
python skill.py fetch \
  --save-obsidian \
  --output-path /custom/path/to/obsidian/vault
```

### Account Management

```bash
# List all followed accounts
python skill.py list-accounts

# Add new account
python skill.py add-account --name "新账号" --fakeid "fake_id"

# Remove account
python skill.py remove-account --name "旧账号"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| MCP connection failed | Check MCP server is running: `mcp call wechat list_followed_accounts` |
| No articles found | Check date range, verify accounts are followed |
| Obsidian save failed | Check vault path permissions, verify Obsidian is open |
| Scores seem wrong | Adjust ranking config in `~/.wechat-fetcher-config.json` |

## Integration with Automation

### LaunchAgent Setup

**File**: `~/Library/LaunchAgents/com.user.wechat.articles.daily.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.wechat.articles.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/skill.py</string>
        <string>fetch</string>
        <string>--since</string>
        <string>yesterday</string>
        <string>--save-obsidian</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>45</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/wechat_fetch.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/wechat_fetch.error</string>
</dict>
</plist>
</plist>
```

**Load agent**:
```bash
launchctl load ~/Library/LaunchAgents/com.user.wechat.articles.daily.plist
```

**Unload agent**:
```bash
launchctl unload ~/Library/LaunchAgents/com.user.wechat.articles.daily.plist
```

### Cron Alternative

```bash
# Edit crontab
crontab -e

# Add line for daily 7:45 AM fetch
45 7 * * * cd /path/to/wechat-article-fetcher && /usr/bin/python3 skill.py fetch --since yesterday --save-obsidian >> /tmp/wechat_fetch.log 2>&1
```
