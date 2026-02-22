# 非共识AI (Non-Consensus AI)

基于第一性原理的深度非共识洞察生成系统。

## 项目结构

```
non_consensus_ai/
├── content/          # 生成的非共识内容
├── config/           # 配置文件
│   └── rss_feeds.md  # RSS源列表
├── scripts/          # 自动化脚本
│   ├── insight_miner.py      # 主生成脚本
│   ├── hn_monitor.py         # HN监控
│   ├── rss_aggregator.py     # RSS聚合
│   └── rss_monitor.py        # RSS监控
└── docs/             # 文档
    ├── x_content_collector.md  # X内容收集模板
    ├── hn_rss_curated.md       # HN精选RSS
    ├── hn_rss_feeds_list.md    # RSS订阅列表
    └── hn_daily_digest.md      # 每日监控模板
```

## 核心功能

### 1. 自动非共识挖掘 (每15分钟)
```bash
cd ~/Desktop/non_consensus_ai/scripts
python3 insight_miner.py
```

自动生成基于第一性原理的深度反直觉洞察，保存到 `content/` 目录。

### 2. HN话题监控
```bash
python3 scripts/hn_monitor.py
```

跟踪Hacker News热门AI讨论，发现高质量信源。

### 3. RSS内容聚合
```bash
python3 scripts/rss_aggregator.py
```

管理20+高质量RSS源，生成订阅列表。

## 内容特点

- ✅ **正确的非共识**：有理有据，不是为反对而反对
- ✅ **可验证预测**：6个月内可观察的验证信号
- ✅ **小红书风格**：爆火格式，易于传播
- ✅ **方法论隐形**：不出现"第一性原理"等术语

## 话题库 (20个高质量话题)

涵盖领域：
- 技术架构 (RAG、多模态、模型效率)
- 编程文化 (AI编码工具、技能退化、身份危机)
- 商业模式 (开源模型、AI创业、ChatGPT)
- 社会影响 (AI写作、法律服务、教育)
- AI安全 (对齐、RLHF、研究可信度)

## 优质信源

### HN社区精选
- karpathy.ai (Andrej Karpathy)
- surfingcomplexity.blog (Lorin Hochstein)
- danluu.com (Dan Luu)
- jvns.ca (Julia Evans)
- normaltech.ai (AI Snake Oil)

### RSS订阅
- distill.pub
- thegradient.pub
- alignmentforum.org
- lesswrong.com

### Newsletter
- Import AI (Jack Clark)
- AI Snake Oil
- One Useful Thing (Ethan Mollick)

## 使用流程

### 日常自动化
1. cron每15分钟运行 `insight_miner.py`
2. 内容自动保存到 `content/`
3. 无需人工干预

### 内容发现
1. 浏览 HN RSS: https://hnrss.org/frontpage
2. 发现好内容 → 粘贴到 `docs/x_content_collector.md`
3. 定期整理 → 更新 `scripts/insight_miner.py` 话题库

### 质量监控
1. 每周回顾 `content/` 生成的内容
2. 检查验证预测是否应验
3. 迭代改进话题库

## 输出示例

```
🔥 说点得罪人的：AGI时间表都是骗局，是为了融资和炒作

❌ 表面观点：
AI领袖们的预测是真诚的

✅ 真正的洞察：
AGI时间表确实被夸大，但真正的问题是'AGI'这个词本身无意义...

💡 为什么这是对的：
...

🔮 可验证预测：
6个月内你会看到...

👇 你觉得这个分析站得住脚吗？
评论区理性讨论👀

#AGI预测 #AI趋势 #深度思考 #行业洞察
```

## 技术栈

- Python 3
- cron (定时任务)
- RSSHub (RSS聚合)
- HNRSS (HN监控)

## 维护

- 话题库：定期从HN/X/RSS发现新话题
- 信源质量：根据HN社区反馈调整权重
- 内容质量：人工审核，迭代改进

---

**项目定位**：结果导向的非共识AI内容生成系统
**更新频率**：每15分钟自动生成
**人工介入**：仅需内容发现和质量审核


## 内容索引
- [20260222_003636] [ChatGPT](content/post_20260222_003636.md)

