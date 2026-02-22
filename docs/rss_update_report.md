# RSS源更新总结报告

## 📊 项目：非共识AI
## 📅 更新日期：2026-02-17

---

## ✅ 本次新增 (来自 awesome_ML_AI_RSS_feed)

### 🏆 高价值独立博客 (5个)

| 名称 | RSS URL | 类型 | 权重 | 独特价值 |
|------|---------|------|------|----------|
| **Jay Alammar** | jalammar.github.io/feed.xml | 可视化 | ⭐⭐⭐⭐⭐ | 图解Transformer等复杂概念 |
| **inFERENCe** | inference.vc/rss | 深度洞察 | ⭐⭐⭐⭐⭐ | 因果推断、生成模型 |
| **AI Weirdness** | aiweirdness.com/rss | AI批判 | ⭐⭐⭐⭐⭐ | AI失败案例、局限展示 |
| **Seita's Place** | danieltakeshi.github.io | RL/机器人 | ⭐⭐⭐⭐ | 研究+工程实践反思 |
| **David Stutz** | davidstutz.de/feed | 论文评论 | ⭐⭐⭐⭐ | 博士生独立视角 |

### 🔥 现有高质量源 (已有16个)

**HN社区精选 (9个)**:
- karpathy.ai, surfingcomplexity.blog, ratfactor.com
- danluu.com, jvns.ca, 0byte.io
- practical.engineering, notnotp.com, governance.fyi

**学术研究 (3个)**:
- distill.pub, thegradient.pub, alignmentforum.org

**Newsletter (5个)**:
- Import AI, AI Snake Oil, One Useful Thing
- The Batch, RL Weekly

---

## 📈 总统计

| 类别 | 数量 | 高权重(⭐⭐⭐⭐⭐) |
|------|------|-----------------|
| 独立博客 | 14个 | 8个 |
| 学术研究 | 3个 | 1个 |
| Newsletter | 5个 | 3个 |
| **总计** | **22个** | **12个** |

---

## 🎯 筛选标准回顾

### ✅ 纳入标准
- 独立作者/小型团队 ✓
- 独特视角或批判性思考 ✓
- 内容深度 > 数量 ✓
- 非大厂官方声音 ✓

### ❌ 排除标准
- 纯营销/PR内容 (如NVIDIA博客)
- 新闻聚合 (缺乏原创)
- Reddit等噪音源
- 质量不稳定

---

## 💡 推荐追踪优先级

### 第一梯队 (每日检查)
1. **AI Weirdness** - 发现AI局限和非预期行为
2. **inFERENCe** - 深度技术洞察
3. **Jay Alammar** - 新概念可视化

### 第二梯队 (每周检查)
4. **HN精选独立博客** - danluu, jvns等
5. **学术研究** - Distill, BAIR
6. **Newsletter** - Import AI, AI Snake Oil

### 第三梯队 (每月检查)
7. **大厂研究博客** - Anthropic, OpenAI等

---

## 📁 相关文件

```
non_consensus_ai/
├── config/
│   └── rss_feeds.md              ← 主RSS列表 (已更新)
├── docs/
│   ├── external_rss_curated.md   ← 本次筛选详情
│   └── hn_rss_curated.md         ← HN精选
└── scripts/
    └── rss_aggregator.py         ← 脚本已更新
```

---

## 🔗 快速访问链接

```bash
# HN AI话题
https://hnrss.org/newest?q=artificial+intelligence+OR+machine+learning+OR+llm

# 独立博客RSS合集 (通过rss_aggregator.py生成)
cd ~/Desktop/non_consensus_ai/scripts
python3 rss_aggregator.py
```

---

## ✨ 核心价值

从awesome_ML_AI_RSS_feed筛选出的5个新源，补充了：

1. **可视化能力** - Jay Alammar的图解风格
2. **数学深度** - inFERENCe的技术洞察
3. **批判视角** - AI Weirdness的幽默+反思
4. **RL/机器人** - Seita's Place的专业深度
5. **独立声音** - David Stutz的非大厂视角

---

**项目状态**: ✅ 运行中 (每15分钟自动生成内容)
**话题库**: 20个高质量非共识话题
**RSS源**: 22个精选源
