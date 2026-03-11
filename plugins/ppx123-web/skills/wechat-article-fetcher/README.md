# WeChat Article Fetcher Skill

一个强大的微信公众号文章获取和分析工具，支持基于研究兴趣的智能排序。

## 功能特性

- 🎯 **智能排序**: 基于研究兴趣自动评分排序
- 📱 **多账号支持**: 获取指定公众号或所有关注账号的文章
- 📅 **日期过滤**: 支持灵活的日期范围查询
- 💾 **Obsidian 集成**: 自动保存到 Obsidian vault
- 🏷️ **自动标签**: 智能添加相关标签
- 📊 **质量过滤**: 自动过滤低质量内容

## 研究兴趣优先级

### Tier 1 (优先级 10): 核心研究
- AI Agent for System
- Multi-Agent Systems
- Autonomous Agents
- LLM Agent

### Tier 2 (优先级 8-9): 系统设计
- System Design
- Distributed Systems
- Operating Systems
- Computer Architecture

### Tier 3 (优先级 8): GitHub 开源项目
- GitHub Open Source Projects
- Open Source Tools
- Framework Libraries
- Practical Implementations

### Tier 4 (优先级 7-8): AI/ML 核心
- Machine Learning
- Deep Learning
- LLMs, Transformers

### Tier 5 (优先级 6-7): 学术研究
- SOTA, Benchmarks
- Paper Reviews
- Top Conferences

## 使用方法

### 作为 Claude Skill 使用

在 Claude Code 中直接调用：

```
请使用 wechat-article-fetcher 获取昨天的文章
```

```
使用 wechat-article-fetcher 获取"量子位"和"PaperAgent"的文章
```

```
使用 wechat-article-fetcher 生成一份关于 GitHub 开源项目的报告
```

### 命令行使用

```bash
# 查看关注的所有公众号
python3 skill.py list

# 获取昨天的文章
python3 skill.py fetch

# 获取指定公众号的文章
python3 skill.py fetch --accounts "量子位" "PaperAgent"

# 指定日期范围
python3 skill.py fetch --start-date 2025-01-15 --end-date 2025-01-20

# 只获取高评分文章
python3 skill.py fetch --min-score 70

# 保存到 Obsidian
python3 skill.py fetch --save-obsidian

# 预览模式（不保存）
python3 skill.py fetch --dry-run
```

## 输出示例

### Frontmatter
```yaml
---
title: "2025-01-19 微信公众号文章汇总"
date: 2025-01-19
tags: [wechat, daily-summary, ai-agent, system, github]
created: 2025-01-19T09:00:00Z
statistics:
  total_articles: 12
  must_read: 4
  high_priority: 3
  interesting: 3
---
```

### 文章格式
```markdown
## 🔥 Must Read (Score: 9-10)

### 1. Agentic AI 综述

**来源**:: PaperAgent
**评分**:: 10/100

**核心内容**:: 全面分析 Agentic AI 范式演进与系统架构...

**研究关联**:: Directly related to AI Agent for System

**行动项**::
- [ ] 阅读完整论文
- [ ] 分析架构图
- [ ] 评估是否可用于当前项目

**相关链接**:: [原文](https://...)
```

## 文件结构

```
wechat-article-fetcher/
├── Skill.md              # Skill 说明文档
├── skill.py              # 主入口文件
├── wechat_fetcher.py     # 核心实现
├── pyproject.toml        # 项目配置
├── setup.sh              # 安装脚本
└── README.md             # 本文档
```

## 依赖要求

- Python >= 3.8
- MCP (Model Context Protocol) tools:
  - `wechat`: 获取微信公众号文章
  - `obsidian`: 保存到 Obsidian vault

## 安装

```bash
cd ~/.claude/skills/wechat-article-fetcher
./setup.sh
```

## 与自动化脚本的配合

### 自动化脚本 (LaunchAgent)
- 文件: `~/Library/LaunchAgents/com.user.wechat.articles.daily.plist`
- 运行时间: 每天早上 7:45
- 功能: 自动获取昨天的文章并保存到 Obsidian
- 适合: 日常使用

### Skill (wechat-article-fetcher)
- 触发方式: 按需调用
- 功能: 灵活获取任意时间、任意账号的文章
- 适合: 临时需求、专题研究

## 示例场景

### 场景 1: 晨间阅读
每天早上 7:45 自动运行，起床后打开 Obsidian 查看新汇总。

### 场景 2: 专题研究
```
使用 wechat-article-fetcher 获取最近一周关于 multi-agent 的文章
```

### 场景 3: 发现开源项目
```
使用 wechat-article-fetcher 找出本月介绍的 GitHub 开源项目，设置 min-score 为 70
```

### 场景 4: 公众号调研
```
使用 wechat-article-fetcher 获取"机器之心"最近一个月的所有文章
```

## 故障排查

### MCP 工具不可用
```bash
# 检查 MCP 是否安装
which mcp

# 测试 WeChat MCP
mcp call wechat list_followed_accounts

# 测试 Obsidian MCP
mcp call obsidian obsidian_list_files_in_vault
```

### 没有获取到文章
- 检查日期范围是否正确
- 确认公众号已关注
- 查看日志: `/tmp/wechat_fetch.log`

### Obsidian 保存失败
- 检查 Obsidian vault 路径
- 确保 `wechat-official-aacount/` 文件夹存在

## 配置文件

可选配置文件: `~/.wechat-fetcher-config.json`

```json
{
  "research_interests": {
    "tier_1": ["AI Agent for System", "Multi-Agent Systems"],
    "tier_3": ["GitHub Open Source", "Open Source Tools"]
  },
  "obsidian_path": "wechat-official-aacount",
  "default_limit": 50,
  "min_score_threshold": 50
}
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
