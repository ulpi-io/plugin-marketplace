# WeChat Article Fetcher Examples

## Example 1: Daily Morning Routine

### User Request

```
获取昨天所有关注公众号的文章
```

### AI Action

```bash
python skill.py fetch --since yesterday --save-obsidian
```

### Output Summary

```
✅ Fetched 45 articles from 12 accounts
📊 Statistics:
   🔥 Must Read (90-100): 8 articles
   📚 High Priority (70-89): 15 articles
   💡 Interesting (50-69): 18 articles
   ⚠️ Skipped (<50): 4 articles

💾 Saved to: wechat-official-aacount/2025-01-19-微信公众号文章汇总.md
```

### Sample Output (Obsidian Format)

```markdown
---
title: "2025-01-19 微信公众号文章汇总"
date: 2025-01-19
tags: [wechat, daily-summary, ai-agent, system]
statistics:
  total_articles: 45
  must_read: 8
  high_priority: 15
---

## 🔥 Must Read (Score: 90-100)

### [[Agentic AI 综述：从理论到实践]]
**来源**: [[PaperAgent]]
**评分**: 98/100
**核心内容**: 全面分析Agentic AI范式演进与系统架构，涵盖从理论模型到生产部署的完整技术栈。重点讨论了Multi-Agent协作机制和工具调用优化策略。
**研究关联**: 直接相关核心研究，必读
**行动项**:
- [ ] 阅读完整论文
- [ ] 分析架构图
- [ ] 学习工具调用模式
**链接**: [原文](https://mp.weixin.qq.com/s/...)

---

## 📚 High Priority (Score: 70-89)

### [[分布式系统中的共识算法优化]]
**来源**: [[InfoQ]]
**评分**: 82/100
**核心内容**: 探讨Raft和PBFT在大规模分布式系统中的性能优化，提出了一种混合共识机制...
**研究关联**: 系统设计相关，值得阅读
**行动项**:
- [ ] 了解混合共识机制
- [ ] 对比Raft/PBFT性能
**链接**: [原文](...)
```

---

## Example 2: Topic-Specific Fetching

### User Request

```
获取量子位和PaperAgent最近关于AI Agent的文章
```

### AI Action

```bash
python skill.py fetch \
  --accounts "量子位" "PaperAgent" \
  --start-date 2025-01-13 \
  --end-date 2025-01-19 \
  --min-score 70 \
  --save-obsidian
```

### Output

```
✅ Fetched 22 articles from 2 accounts
🔍 Filter: min-score 70+
📊 Results:
   Must Read: 6
   High Priority: 16
   (Skipped: 35 articles below threshold)
```

---

## Example 3: Discover GitHub Projects

### User Request

```
找出最近介绍的GitHub开源项目
```

### AI Action

```bash
# Search for GitHub-related content
python skill.py fetch \
  --since yesterday \
  --min-score 60 \
  | grep -i "github\|开源" | head -20
```

### Sample Results

```
💡 Interesting Projects Found:

1. AutoGPT (Score: 85) - 📚 High Priority
   Source: 量子位
   Summary: 自主AI代理框架，可自动完成复杂任务...
   GitHub: https://github.com/Significant-Gravitas/AutoGPT

2. LangChain (Score: 88) - 📚 High Priority
   Source: PaperAgent
   Summary: LLM应用开发框架，支持链式调用和工具集成...
   GitHub: https://github.com/langchain-ai/langchain

3. AgentProtocol (Score: 75) - 💡 Interesting
   Source: 机器之心
   Summary: 标准化Agent通信协议...
   GitHub: https://github.com/e2b-dev/agent-protocol
```

---

## Example 4: Preview Before Saving

### User Request

```
预览一下今天会有多少文章
```

### AI Action

```bash
python skill.py fetch --since yesterday --dry-run
```

### Console Output

```
📊 Preview: WeChat Articles for 2025-01-18

🔥 Must Read (9): High-priority research articles
📚 High Priority (18): Relevant technical content
💡 Interesting (25): General interest articles
⚠️ Skipped (12): Below threshold (<50)

Total: 64 articles from 15 accounts

Account breakdown:
  量子位: 12 articles (3 must-read, 5 high-priority)
  PaperAgent: 8 articles (4 must-read, 3 high-priority)
  机器之心: 10 articles (2 must-read, 4 high-priority)
  InfoQ: 9 articles (0 must-read, 3 high-priority)
  ... (11 more accounts)

Run with --save-obsidian to save all articles.
```

---

## Example 5: High-Value Research Digest

### User Request

```
生成一份关于AI Agent的最新文章报告
```

### AI Action

```bash
# Fetch with high score threshold
python skill.py fetch \
  --start-date 2025-01-13 \
  --end-date 2025-01-19 \
  --min-score 80 \
  --save-obsidian
```

### Generated Report Summary

```markdown
# AI Agent Research Digest (Jan 13-19, 2025)

## 📊 Week Overview
- Total High-Value Articles: 24
- Core Research Papers: 8
- Production Experiences: 6
- Tool & Framework Updates: 10

## 🔥 Essential Reading

### Agentic AI Architecture Evolution
**Score**: 98/100 | **Source**: PaperAgent
**Key Insights**:
- 从单Agent到Multi-Agent的架构演进
- 工具调用的性能优化策略
- 生产环境部署最佳实践
**Actions**: [阅读全文] [分析架构]

### LLM Agent in Production at Scale
**Score**: 95/100 | **Source**: 量子位
**Key Insights**:
- 处理10K+并发的Agent系统设计
- 错误处理和重试机制
- 监控和可观测性方案
**Actions**: [学习生产经验]

## 📚 Important Updates

### New Agent Frameworks (8 articles)
- AgentProtocol v2.0 release
- LangSmith debug tool
- CrewAI multi-agent orchestration
- ... (5 more)

### Research Papers (6 articles)
- "Multi-Agent Collaboration Theory" (NeurIPS 2024)
- "Tool Learning in LLMs" (ICLR 2025)
- ... (4 more)

## 💡 Tools & Resources

### GitHub Projects (10 projects)
1. AutoGPT - Autonomous agents
2. BabyAGI - Task automation
3. AgentGPT - Web-based agent builder
... (7 more)

---

**Full report saved to**: wechat-official-aacount/2025-01-19-AI-Agent-Digest.md
```

---

## Example 6: Custom Date Range Research

### User Request

```
获取去年12月所有关于System Design的文章
```

### AI Action

```bash
python skill.py fetch \
  --start-date 2024-12-01 \
  --end-date 2024-12-31 \
  --min-score 60 \
  --save-obsidian
```

### Output

```
✅ Fetched 156 articles from December 2024
🔍 Filter: System Design related, score ≥60

📊 Breakdown:
  Distributed Systems: 42 articles
  Database Design: 28 articles
  Microservices: 21 articles
  Performance Optimization: 19 articles
  Architecture Patterns: 18 articles
  Cloud Native: 15 articles
  Other: 13 articles

💾 Saved to: wechat-official-aacount/2024-12-System-Design-汇总.md

🔥 Top 3 Articles:
  1. "分布式事务的终极解决方案" (Score: 92)
  2. "亿级流量系统架构设计" (Score: 89)
  3. "云原生架构演进之路" (Score: 87)
```

---

## Ranking Examples

### Article A: Perfect Match

**Title**: "Agentic AI综述：Multi-Agent系统设计"

**Scoring**:
- Tier 1 keyword "Agentic AI" in title: +30
- Tier 1 keyword "Multi-Agent" in content: +20
- High-quality content (3000+ words): +15
- Has code examples: +10
- Source "量子位": +15
- Recent (<7 days): +5

**Total**: **95/100** → 🔥 Must Read

### Article B: Good Match

**Title**: "分布式系统设计模式与实践"

**Scoring**:
- Tier 2 keyword "分布式系统" in title: +25
- Tier 2 keyword "设计模式" in content: +15
- Medium length (1500 words): +10
- Has diagrams: +5
- Source "InfoQ": +10

**Total**: **65/100** → 📚 High Priority

### Article C: Weak Match

**Title**: "Python入门教程（下）"

**Scoring**:
- Tutorial content: +20
- Short length (<500 words): +0
- Generic source: +5
- No technical terms: +0

**Total**: **25/100** → ⚠️ Skipped (below 50 threshold)
