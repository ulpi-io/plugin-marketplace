# WeChat Article Fetcher - Ranking System

## Overview

Articles are automatically scored and ranked based on your research interests (AI Agent, System Design, GitHub Open Source). Scores range from 0-100, determining the article category.

## Priority Tiers

### Tier 1: Core Research (Priority: 10)

**Keywords**: AI Agent, Agent for System, Multi-Agent System, Autonomous Agents, LLM Agent

**Score Range**: 90-100

**Description**: Directly related to core research area. These are **Must Read** articles.

**Example Articles**:
- "Agentic AI: 综述与展望"
- "Multi-Agent Systems for Distributed Optimization"
- "LLM Agents in Production: 实战经验"

**Matching**:
- Exact phrase match: +30 points
- Title contains 2+ keywords: +25 points
- Content analysis: +35 points
- Source reputation: +10 points

### Tier 2: System Design (Priority: 8-9)

**Keywords**: System Design, Distributed Systems, Operating Systems, Computer Architecture

**Score Range**: 80-89

**Description**: High relevance to systems research. **High Priority** articles.

**Example Articles**:
- "Distributed Systems Design Patterns"
- "Operating Systems for the Cloud Era"
- "Scalability Best Practices"

**Matching**:
- Exact phrase match: +25 points
- Title contains keywords: +20 points
- Content depth: +30 points
- Technical quality: +15 points

### Tier 3: GitHub Open Source (Priority: 8)

**Keywords**: GitHub Open Source, Open Source Tools, Framework Libraries, Practical Implementations

**Score Range**: 75-89

**Description**: Interesting tools and implementations. **High Priority** or **Interesting** based on utility.

**Example Articles**:
- "10个Must-Have的AI开源工具"
- "GitHub精选：最新ML框架"
- "实战项目：构建生产级Agent"

**Matching**:
- Contains GitHub link: +20 points
- Tool/framework mentioned: +15 points
- Practical utility: +25 points
- Active development: +15 points

### Tier 4: AI/ML Core (Priority: 7-8)

**Keywords**: Machine Learning, Deep Learning, Reinforcement Learning, Transformers, LLMs

**Score Range**: 70-84

**Description**: Relevant AI/ML research. **Interesting** or **High Priority**.

**Example Articles**:
- "Transformer架构详解"
- "深度学习优化新方法"
- "LLM训练技巧分享"

**Matching**:
- Technical terms match: +20 points
- Research paper discussion: +25 points
- Implementation details: +20 points
- Educational value: +15 points

### Tier 5: Academic Research (Priority: 6-7)

**Keywords**: SOTA methods, Benchmarks, Paper Reviews, Top conferences (NeurIPS, ICML, OSDI, SOSP, ICSE)

**Score Range**: 65-79

**Description**: Academic progress and paper reviews. **Interesting**.

**Example Articles**:
- "NeurIPS 2024最佳论文解读"
- "SOTA方法对比分析"
- "顶会论文综述"

**Matching**:
- Conference mention: +20 points
- Paper analysis depth: +25 points
- Novel contribution: +20 points
- Citation/impact: +10 points

### Tier 6: Practice Guides (Priority: 4-5)

**Keywords**: Tutorials, Best Practices

**Score Range**: 50-69

**Description**: Practical tutorials and guides. **Interesting** if relevant.

**Example Articles**:
- "Python性能优化教程"
- "代码审查最佳实践"
- "Docker入门指南"

**Matching**:
- Tutorial quality: +20 points
- Practical relevance: +20 points
- Beginner/intermediate level: +15 points

## Score Calculation Algorithm

```python
def calculate_article_score(article, research_interests):
    """Calculate relevance score (0-100)"""

    base_score = 0

    # 1. Tier priority bonus
    tier = identify_tier(article, research_interests)
    base_score += tier['priority'] * 10

    # 2. Keyword matching
    keyword_score = calculate_keyword_match(
        article['title'],
        article['content'],
        research_interests[tier]['keywords']
    )
    base_score += keyword_score

    # 3. Content quality assessment
    quality_score = assess_quality(article)
    base_score += quality_score

    # 4. Source reputation
    source_bonus = get_source_reputation(article['source'])
    base_score += source_bonus

    # 5. Recency bonus (for recent articles)
    if article['days_old'] < 7:
        base_score += 5

    return min(base_score, 100)  # Cap at 100
```

### Keyword Matching Details

```python
def calculate_keyword_match(title, content, keywords):
    """Calculate keyword matching score"""

    score = 0
    title_lower = title.lower()
    content_lower = content.lower()

    for keyword in keywords:
        # Exact phrase match in title (highest weight)
        if keyword in title_lower:
            if keyword.lower() == title_lower:
                score += 30  # Title is exactly the keyword
            else:
                score += 15  # Keyword appears in title

        # Content mention (medium weight)
        keyword_count = content_lower.count(keyword.lower())
        if keyword_count > 0:
            # More mentions = higher relevance (with diminishing returns)
            score += min(keyword_count * 3, 20)

    return score
```

### Quality Assessment

```python
def assess_quality(article):
    """Assess article content quality"""

    score = 0

    # Length (longer = more depth usually)
    if len(article['content']) > 2000:
        score += 15
    elif len(article['content']) > 1000:
        score += 10
    elif len(article['content']) > 500:
        score += 5

    # Has code examples
    if has_code_blocks(article['content']):
        score += 10

    # Has diagrams/images
    if has_images(article['content']):
        score += 5

    # Cites papers or sources
    if has_citations(article['content']):
        score += 10

    # Technical depth (presence of technical terms)
    technical_term_count = count_technical_terms(article['content'])
    score += min(technical_term_count, 15)

    return score
```

### Source Reputation

```python
SOURCE_REPUTATION = {
    "量子位": 15,
    "PaperAgent": 15,
    "机器之心": 12,
    "新智元": 10,
    "InfoQ": 10,
    "大数据拣渣": 8,
    # ... more sources
}

def get_source_reputation(source_name):
    """Get source reputation bonus"""

    return SOURCE_REPUTATION.get(source_name, 5)  # Default 5
```

## Category Assignment

Based on final score:

```python
def assign_category(score):
    """Assign category based on score"""

    if score >= 90:
        return "🔥 Must Read"
    elif score >= 70:
        return "📚 High Priority"
    elif score >= 50:
        return "💡 Interesting"
    else:
        return "⚠️ Skipped"
```

## Configuration

### Custom Research Interests

Edit `~/.wechat-fetcher-config.json`:

```json
{
  "research_interests": {
    "tier_1": {
      "priority": 10,
      "keywords": ["AI Agent", "Multi-Agent Systems", "Autonomous Agents"]
    },
    "tier_2": {
      "priority": 9,
      "keywords": ["System Design", "Distributed Systems"]
    },
    "tier_3": {
      "priority": 8,
      "keywords": ["GitHub Open Source", "Open Source Tools"]
    }
  },
  "min_score_threshold": 50,
  "default_limit": 50
}
```

### Tuning Scoring

Adjust weights in ranking algorithm:

```python
# Increase weight for keyword matching
KEYWORD_MATCH_WEIGHT = 1.5  # Default: 1.0

# Decrease weight for source reputation
SOURCE_REPUTATION_WEIGHT = 0.5  # Default: 1.0

# Adjust quality assessment thresholds
QUALITY_LENGTH_THRESHOLD = 1500  # Default: 2000
```

## Examples

### Example 1: Perfect Match

**Article**: "Agentic AI综述：从理论到实践"

**Analysis**:
- Title contains "Agentic AI" (Tier 1 keyword): +30
- Content mentions "Multi-Agent" and "LLM Agent": +25
- Length 2500+ words: +15
- Has code examples: +10
- Source "量子位": +15
- Recency (<7 days): +5

**Total**: 30 + 25 + 15 + 10 + 15 + 5 = **100** (Must Read)

### Example 2: Good Match

**Article**: "分布式系统设计模式"

**Analysis**:
- Title contains "分布式系统" (Tier 2 keyword): +25
- Content depth: +20
- Length 1500 words: +10
- Has diagrams: +5
- Source "InfoQ": +10

**Total**: 25 + 20 + 10 + 5 + 10 = **70** (High Priority)

### Example 3: Weak Match

**Article**: "Python入门教程"

**Analysis**:
- Tutorial content: +20
- Practical relevance: +10
- Short length (<500 words): +0
- Generic source: +5

**Total**: 20 + 10 + 0 + 5 = **35** (Skipped - below threshold)

## Best Practices

### Improving Ranking Accuracy

1. **Regular keyword updates**: Keep research interests current
2. **Source feedback**: Mark low-quality sources for lower reputation
3. **Score tuning**: Adjust weights based on actual article quality
4. **Threshold calibration**: Set appropriate `min_score_threshold`

### Handling False Positives

- **Too many high scores**: Increase thresholds, adjust keyword weights
- **Missing relevant articles**: Add more keywords, lower tier priorities
- **Wrong categorization**: Fine-tune category boundaries

### Advanced Customization

```python
# Custom scoring function
def custom_score(article):
    # Your custom logic
    score = base_algorithm(article)

    # Add custom rules
    if "tutorial" in article['tags']:
        score -= 10  # Penalize tutorials

    if "production" in article['content']:
        score += 15  # Boost production experience

    return score
```
