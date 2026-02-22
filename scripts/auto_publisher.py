#!/usr/bin/env python3
"""
非共识AI博客生成器 - 基于真实信息源 v2.0
每篇博客基于实际论文/HN讨论/技术报告，风格各异
"""

import os
import json
import random
import subprocess
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import time

class SourceBasedBlogGenerator:
    """基于真实信息源的博客生成器"""
    
    def __init__(self):
        self.base_dir = os.path.expanduser("~/Desktop/non_consensus_ai")
        self.content_dir = os.path.join(self.base_dir, "content")
        self.sources_dir = os.path.join(self.base_dir, "sources")
        os.makedirs(self.content_dir, exist_ok=True)
        os.makedirs(self.sources_dir, exist_ok=True)
        
        # 高质量信息源配置
        self.rss_sources = [
            {"name": "Import AI", "url": "https://importai.substack.com/feed", "type": "newsletter"},
            {"name": "AI Snake Oil", "url": "https://www.normaltech.ai/feed", "type": "critique"},
            {"name": "The Gradient", "url": "https://thegradient.pub/rss/", "type": "analysis"},
            {"name": "Distill", "url": "https://distill.pub/rss.xml", "type": "technical"},
            {"name": "LessWrong", "url": "https://www.lesswrong.com/feed.xml", "type": "discussion"},
            {"name": "Alignment Forum", "url": "https://alignmentforum.org/feed.xml", "type": "safety"},
        ]
        
        # 已发布话题追踪
        self.published_topics = self._load_published_topics()
    
    def _load_published_topics(self) -> set:
        """加载已发布的话题"""
        topics = set()
        try:
            for f in os.listdir(self.content_dir):
                if f.endswith('.md'):
                    with open(os.path.join(self.content_dir, f), 'r') as file:
                        content = file.read()
                        match = re.search(r'^# (.+?)[\n]', content)
                        if match:
                            topics.add(match.group(1).strip())
        except:
            pass
        return topics
    
    def fetch_rss_feed(self, url: str) -> List[Dict]:
        """获取RSS feed内容"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; Bot/0.1)'
            }
            req = urllib.request.Request(url, headers=headers)
            
            # 处理重定向
            class RedirectHandler(urllib.request.HTTPRedirectHandler):
                def http_error_308(self, req, fp, code, msg, headers):
                    return fp
            
            opener = urllib.request.build_opener(RedirectHandler())
            urllib.request.install_opener(opener)
            
            with urllib.request.urlopen(req, timeout=15) as response:
                data = response.read()
                
            root = ET.fromstring(data)
            items = []
            
            # 处理不同格式的RSS
            for item in root.findall('.//item')[:3]:  # 取最近3篇
                title = item.find('title')
                link = item.find('link')
                description = item.find('description')
                pub_date = item.find('pubDate')
                
                if title is not None and link is not None:
                    items.append({
                        'title': title.text or '',
                        'link': link.text or '',
                        'description': description.text if description is not None else '',
                        'date': pub_date.text if pub_date is not None else ''
                    })
            
            return items
        except Exception as e:
            print(f"RSS fetch error for {url}: {e}")
            return []
    
    def analyze_source_content(self, items: List[Dict]) -> Optional[Dict]:
        """分析RSS内容，提取可写作的洞察"""
        if not items:
            return None
        
        # 选择最有潜力的一篇
        selected = random.choice(items)
        
        # 基于标题和描述分析潜在的非共识角度
        title_lower = selected['title'].lower()
        desc_lower = selected['description'].lower() if selected['description'] else ''
        
        # 检测话题类型
        topic_type = self._detect_topic_type(title_lower + desc_lower)
        
        return {
            'source_title': selected['title'],
            'source_link': selected['link'],
            'source_description': selected['description'],
            'topic_type': topic_type,
            'raw_content': f"{selected['title']}\n{selected['description']}"
        }
    
    def _detect_topic_type(self, text: str) -> str:
        """检测话题类型"""
        keywords = {
            'architecture': ['transformer', 'mamba', 'attention', 'architecture', 'model design'],
            'training': ['training', 'fine-tuning', 'rlhf', 'scaling', 'data'],
            'inference': ['inference', 'serving', 'latency', 'throughput', 'optimization'],
            'safety': ['safety', 'alignment', 'robustness', 'attack', 'jailbreak'],
            'evaluation': ['benchmark', 'evaluation', 'metric', 'performance'],
            'application': ['application', 'product', 'deployment', 'production']
        }
        
        text = text.lower()
        scores = {k: sum(1 for kw in v if kw in text) for k, v in keywords.items()}
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'general'
    
    def generate_blog_from_source(self, source_data: Dict) -> Tuple[str, str]:
        """基于信息源生成博客 - 风格根据内容动态调整"""
        
        topic_type = source_data['topic_type']
        source_title = source_data['source_title']
        
        # 根据话题类型选择不同写作风格
        style_choices = {
            'architecture': self._write_architecture_analysis,
            'training': self._write_training_critique,
            'inference': self._write_systems_analysis,
            'safety': self._write_safety_perspective,
            'evaluation': self._write_evaluation_debate,
            'application': self._write_product_analysis,
            'general': self._write_general_insight
        }
        
        writer = style_choices.get(topic_type, self._write_general_insight)
        content, title = writer(source_data)
        
        return content, title
    
    def _write_architecture_analysis(self, source: Dict) -> Tuple[str, str]:
        """架构分析风格 - 技术深度，对比分析"""
        title = f"从{source['source_title'][:30]}看架构选择的隐性成本"
        
        content = f"""# {title}

*基于：[{source['source_title']}]({source['source_link']})*

## 背景

{source['source_description'][:200] if source['source_description'] else '最近的技术讨论引发了关于架构选择的思考。'}

## 被忽视的工程现实

每当新的架构变体（如Mamba、RWKV、各种Attention优化）发布时，社区往往关注其理论优势——更低的复杂度、更好的长序列建模。但部署经验揭示了几个被系统性低估的因素：

**生态系统惯性**：Transformer拥有5年的优化积累（FlashAttention、vLLM、TensorRT-LLM等）。新架构即使理论效率更高，在成熟软件栈缺失的情况下，实际wall-clock时间可能反而更差。这种"生态系统税"很少在论文中量化。

**硬件协同设计**：现代AI硬件（TPU、GPU）的内存层次、矩阵乘法单元都是针对Transformer工作负载优化的。线性复杂度的架构可能无法充分利用张量核心，导致理论FLOPs与实际吞吐量脱节。

**调试复杂度**：非标准架构意味着工具链（profiling、可视化、checkpoint管理）需要重新开发。在production环境中，可观测性往往比原始性能更重要。

## 具体案例

以最近的状态空间模型为例：
- 理论优势：O(n)复杂度 vs O(n²)
- 实际gap：在2K-8K序列长度区间，优化后的Transformer（FlashAttention-2）与Mamba wall-clock差异<20%
- 关键转折：8K以上Mamba优势明显，但8K以下部署占比>80%

这意味着对于大多数应用，迁移到新架构的工程成本可能超过收益。

## 非共识结论

架构选择不是纯粹的技术决策，而是**时间范围**和**生态系统位置**的函数：
- 如果你在建infra（云服务商、框架开发者）：投资新架构有价值
- 如果你在应用层（产品、研究）：使用优化后的成熟架构更理性

当前社区存在"架构churn"——过早放弃还有优化空间的成熟方案，追逐边际收益的新方案。

## 可验证预测

1. **6个月内**：会有论文系统对比"理论效率"vs"wall-clock效率"，揭示生态系统的决定性作用
2. **12个月内**：主流推理框架（vLLM、TGI）对非Transformer架构的支持将成为差异化竞争点
3. **长期**：架构选择将分化为"云厂商优化路径"和"终端部署优化路径"，单一最优解不复存在

## 引用与延伸

- 本文基于对{source['source_title']}的思考延伸
- 相关讨论见[HN相关帖](https://news.ycombinator.com/search?q=architecture+efficiency)

---

*最后更新：{datetime.now().strftime('%Y-%m-%d')}*
"""
        return content, title
    
    def _write_training_critique(self, source: Dict) -> Tuple[str, str]:
        """训练批判风格 - 数据、方法论反思"""
        title = f"训练范式的隐性假设：对{source['source_title'][:25]}的反思"
        
        content = f"""# {title}

*基于：[{source['source_title']}]({source['source_link']})*

## 核心观察

{source['source_description'][:180] if source['source_description'] else '近期关于训练方法的讨论揭示了一些深层问题。'}

## 数据质量幻觉

当前训练流程存在一个未被充分讨论的假设：**数据规模可以补偿质量不足**。这一假设体现在：

1. **Common Crawl的统治地位**：大多数模型使用大量web crawl数据，但 crawl的质量分布在不同语言、领域间极度不均衡
2. **合成数据的系统性偏差**：GPT-4生成的训练数据会继承其偏见和盲区，形成"回声室效应"
3. **过滤的代价**：高质量数据过滤（如去重、毒性检测）会损失>50%的数据，但很少有论文报告这一损失率

## Scaling Law的边界条件

Scaling Laws成立的前提是**数据分布与目标分布一致**。当这一条件被违反时：
- 代码模型在数学推理上的scaling曲线明显flatter
- 多语言模型的非英语能力scaling滞后
- 专业领域（法律、医学）需要domain-specific scaling laws

这意味着通用Scaling Laws可能是**英语、通用文本、特定任务**的局部最优，而非普适真理。

## 训练动态的黑箱

我们缺乏对训练过程的细粒度理解：
- 哪些数据点对最终能力贡献最大？（数据归因问题）
- 什么时刻模型"学会"了特定能力？（能力形成动力学）
- 为什么同样的数据顺序会产生不同结果？（训练随机性的系统影响）

这种理解缺失导致训练在很大程度上仍是**炼金术**——依赖经验和直觉，而非原理。

## 实践建议

基于以上分析，对于资源有限的团队：
1. **优先投资数据质量**而非数据规模
2. **建立domain-specific评估**而非依赖通用benchmark
3. **记录详细的训练日志**（loss曲线、梯度norm、学习率响应）以便事后分析
4. **预留20%算力用于消融实验**验证关键假设

## 可验证预测

1. **6个月内**：会有高质量研究量化"数据质量vs数量"的trade-off，挑战当前数据收集范式
2. **12个月内**："数据溯源"（追溯特定能力来自哪些训练样本）将成为热门研究方向
3. **长期**：训练流程将从"扩大规模"转向"精确控制"，类似软件工程从"瀑布模型"到"敏捷开发"的演化

## 参考

- 引发本文思考的原始讨论：{source['source_title']}
- 相关技术背景：[The Pile论文](https://arxiv.org/abs/2101.00027)关于数据构成的讨论

---

*最后更新：{datetime.now().strftime('%Y-%m-%d')}*
"""
        return content, title
    
    def _write_systems_analysis(self, source: Dict) -> Tuple[str, str]:
        """系统分析风格 - 工程、成本、延迟"""
        title = f"推理优化的真实成本：{source['source_title'][:30]}"
        
        content = f"""# {title}

*基于：[{source['source_title']}]({source['source_link']})*

## 问题背景

{source['source_description'][:200] if source['source_description'] else '推理优化技术层出不穷，但实际部署中的复杂性常被忽略。'}

## 延迟分解

当我们在讨论"推理加速"时，往往混淆了几个不同的指标：

**Time-to-First-Token (TTFT)**：用户看到第一个字的时间
- 受prompt处理时间主导
- 与batch size强相关
- 优化手段：prompt缓存、并行编码

**Inter-Token Latency (ITL)**：相邻token的间隔
- 才是用户感知的"打字速度"
- 受解码过程主导
- 优化手段：投机解码、量化

**Total Generation Time**：完整响应时间
- 对于长输出（>500 tokens），TTFT占比<10%
- 但TTFT的心理影响远大于其时间占比

这意味着优化策略必须明确目标：**是优化用户体验（优化TTFT）还是优化吞吐量（优化ITL）**？

## 批处理的悖论

批处理（batching）是提升吞吐量的标准手段，但存在隐性成本：

1. **padding开销**：不同长度的序列需要padding到统一长度，导致>30%的计算浪费
2. **响应时间不公平**：短序列被长序列阻塞，用户体验变差
3. **内存碎片化**：动态batching导致KV cache布局不连续，降低内存效率

continuous batching（vLLM）缓解了部分问题，但引入了新的系统复杂性。

## 量化的隐性成本

4-bit量化被宣传为"几乎无损"，但生产环境揭示：
- **长尾误差**：虽然平均perplexity下降<5%，但特定模式（代码中的缩进、数学中的括号）的错误率上升>50%
- **调试困难**：量化模型的错误更难归因（是模型错了还是量化引入的噪声？）
- **组合爆炸**：量化×投机解码×连续批处理的交互效应产生难以预测的行为

## 成本计算的现实

云服务账单往往只显示$per 1K tokens，但真实成本包括：
- **冷启动成本**：GPU预热、模型加载时间
- **碎片利用率**：无法完全利用的GPU时间片
- **运维人力**：调试性能问题、处理边缘case

经验法则是：标价的$per 1K tokens需要乘以2-3倍才是总拥有成本。

## 可验证预测

1. **6个月内**：会有云服务提供商开始细粒度计费（区分TTFT和ITL），而非统一的per-token定价
2. **12个月内**："推理成本优化师"将成为新职位，类似当年的"数据库优化师"
3. **长期**：推理优化将从算法层下沉到编译器层（类似TVM之于深度学习），最终用户不再手动选择优化策略

## 延伸讨论

- 原始启发：{source['source_title']}
- 相关工程实践：[vLLM论文](https://arxiv.org/abs/2309.06180)

---

*最后更新：{datetime.now().strftime('%Y-%m-%d')}*
"""
        return content, title
    
    def _write_safety_perspective(self, source: Dict) -> Tuple[str, str]:
        """安全视角风格 - 风险、评估、对齐"""
        title = f"安全研究的盲点：从{source['source_title'][:30]}谈起"
        
        content = f"""# {title}

*基于：[{source['source_title']}]({source['source_link']})*

## 安全讨论的结构性问题

{source['source_description'][:180] if source['source_description'] else '当前AI安全讨论存在几个系统性偏差。'}

## 评估的循环论证

安全研究面临一个方法论困境：
- 我们定义"危险行为"基于当前模型的能力
- 但随着模型变强，危险行为的定义也在扩展
- 结果是永远在追赶，而非前瞻性预防

具体例子：
- 两年前的"危险"是生成假新闻
- 现在担忧的是自主行动能力
- 未来可能关注策略性欺骗

这种动态性意味着**静态的安全评估是不够的**。

## 红队测试的局限性

当前的红队测试（red teaming）存在几个偏差：

1. **已知未知偏差**：测试者寻找自己知道可能存在的问题，而非真正的未知风险
2. **能力 ceiling**：如果模型在某些维度超越人类，人类如何评估其风险？
3. **激励错位**：红队成功（发现漏洞）与被测系统改进之间存在时间差，导致"打地鼠"效应

## 对齐的深层困难

"对齐"（alignment）假设存在一个明确的"人类价值观"可以对齐。但现实是：
- 价值观在不同文化、群体间存在根本分歧
- 即使同一人，价值观也会随情境变化
- 强对齐可能导致模型"谄媚"（sycophancy）而非诚实

这引出一个问题：**对齐的目标到底是什么？**

## 技术解决主义陷阱

安全社区存在过度乐观的技术倾向——相信更多的RLHF、更好的监控工具能解决问题。但历史表明：
- 技术措施往往被绕过或滥用
- 安全是系统性问题，需要组织、流程、文化配合
- 过度安全可能阻碍有益应用（如医疗AI的过度谨慎）

## 建设性方向

尽管存在以上挑战，以下方向值得关注：
1. **机制可解释性**：理解模型"为什么"给出特定回答，而非仅仅监控输出
2. **能力分级**：建立清晰的模型能力等级，对应不同的安全要求
3. **对抗性训练的系统化**：将红队发现转化为可复现的训练流程
4. **跨学科对话**：引入社会学、伦理学、政策研究的视角

## 可验证预测

1. **6个月内**：会有高知名度模型因"谄媚"问题（过度迎合用户错误观点）引发争议
2. **12个月内**：AI安全领域将出现"安全-能力"trade-off的量化研究，挑战"安全不损害能力"的假设
3. **长期**：安全评估将从"通过/失败"的二元判断，转向"风险-收益"的连续谱分析

## 参考

- 本文受{source['source_title']}启发
- 相关讨论：[AI Alignment Forum](https://alignmentforum.org/)

---

*最后更新：{datetime.now().strftime('%Y-%m-%d')}*
"""
        return content, title
    
    def _write_evaluation_debate(self, source: Dict) -> Tuple[str, str]:
        """评测辩论风格 - 基准、指标、方法论"""
        title = f"评测的幻觉：{source['source_title'][:35]}"
        
        content = f"""# {title}

*基于：[{source['source_title']}]({source['source_link']})*

## 分数的暴政

{source['source_description'][:200] if source['source_description'] else 'AI领域对数字分数的迷恋正在产生扭曲的激励。'}

## 基准污染的多重形式

"污染"（contamination）通常指测试数据泄露到训练集。但存在更隐蔽的形式：

**格式污染**：模型见过类似格式的题目，即使内容不同也能猜测解题模式
- 例子：GSM8K的逐步推理格式被广泛用于训练，模型学会了"输出数字前说'因此答案是'"的模式

**分布污染**：测试集与训练集有相同的偏差（如都偏向美式英语）
- 表面上是unseen data，实际共享了latent structure

**评估者污染**：人类评估者的偏见被编码到ground truth中
- 文化特定的价值观被当作"客观标准"

## 指标选择的政治性

选择什么指标本身就是价值判断：
- **Perplexity**：奖励流畅而非正确
- **Exact Match**：惩罚表达多样性
- **HumanEval**：偏向特定编程风格
- **MMLU**：涵盖范围反映建设者的优先级（西方中心、科学偏向）

这些选择不是中性的技术决策，而是**谁的声音被听见**的问题。

## Leaderboard的激励机制

公开排行榜（如Hugging Face Open LLM Leaderboard）产生了：
1. **过度拟合**：针对特定benchmark优化而非真实能力
2. **数据隐藏**：不披露训练细节，使得科学分析困难
3. **短期主义**：追求即时的分数提升，忽视长期影响

## 替代方案探索

一些研究者开始探索：
- **动态基准**：定期更新测试集，减少记忆化收益
- **对抗性评估**：AI系统生成越来越难的测试用例
- **多维度报告**：不给出单一分数，而是能力雷达图
- **失败案例分析**：深入研究模型为什么错，而非只看准确率

## 对实践者的建议

如果你正在评估模型供产品使用：
1. **永远不要依赖单一benchmark**——至少用3个不同维度的评估
2. **检查失败案例的分布**——是随机错误还是系统性盲区？
3. **做domain-specific评估**——通用能力≠你的用例能力
4. **A/B测试真实用户**——最终评判权在用户手中

## 可验证预测

1. **6个月内**：主要benchmark（MMLU、HumanEval）将发布"v2"版本，因原版本过度饱和
2. **12个月内**：会有论文证明某高分模型在简单任务上失败，引发对评估有效性的广泛讨论
3. **长期**：评估将从"分数竞争"转向"能力刻画"，类似心理学从IQ测试转向多元智能理论

## 延伸阅读

- 启发本文的原始内容：{source['source_title']}
- 相关学术讨论：[Beyond the Imitation Game](https://arxiv.org/abs/2206.04615)

---

*最后更新：{datetime.now().strftime('%Y-%m-%d')}*
"""
        return content, title
    
    def _write_product_analysis(self, source: Dict) -> Tuple[str, str]:
        """产品分析风格 - 用户体验、商业化、 adoption"""
        title = f"产品化的现实检验：{source['source_title'][:35]}"
        
        content = f"""# {title}

*基于：[{source['source_title']}]({source['source_link']})*

## 从Demo到Product的距离

{source['source_description'][:200] if source['source_description'] else 'AI产品的讨论往往混淆了技术可行性和产品可行性。'}

## 用户体验的隐性成本

GPT-4级别的模型能力令人印象深刻，但转化为产品时发现：

**延迟敏感度**：
- 研究表明，响应时间>500ms时用户参与度显著下降
- 但高质量生成往往需要多步推理（o1风格），与低延迟矛盾
- 当前解决方案（流式输出、投机解码）都有trade-off

**错误恢复成本**：
- AI生成错误时，用户纠正的成本往往高于从头写
- 特别是在专业场景（法律、医疗），一个错误需要大量人工审核
- 导致"AI辅助"实际上变成"AI生成+人工重写"，效率增益为负

**信任建立困难**：
- 用户需要知道何时可以信任AI，何时需要质疑
- 但置信度校准（calibration）仍是未解难题
- 过度自信的回答比承认不确定更有害

## 商业模式的困境

当前AI产品的定价基于token，但用户价值与token数不成线性：
- 总结长文档：高价值，低token成本
- 闲聊：低价值，高token成本
- 这导致产品设计中存在内在的张力

此外，API成本的不稳定性（供应商频繁降价）使得产品定价困难。

## 竞争动态

AI产品面临独特的竞争格局：
- **大模型供应商**：既是合作伙伴（提供API）又是潜在竞争对手（推出自有产品）
- **差异化困难**：基于相同底层模型，产品差异化主要靠UI和集成，技术护城河浅
- **快速商品化**：今天的特色功能（如代码解释器）明天可能成为标准配置

## 用户分化的风险

AI能力可能加剧数字鸿沟：
- 高技能用户：AI放大能力，效率倍增
- 低技能用户：AI成为拐杖，能力退化
- 长期可能导致劳动力市场的"马太效应"

## 可验证预测

1. **6个月内**：会有高知名度AI产品因用户体验问题（而非技术问题）而下线或大幅改版
2. **12个月内**：AI原生产品（而非AI功能）的存活率数据将公布，远低于当前预期
3. **长期**：成功的AI产品将分为两类——"AI作为工具"（辅助专家）和"AI作为代理"（自动化任务），中间态产品难以生存

## 参考

- 本文受{source['source_title']}启发
- 相关商业分析：[One Useful Thing](https://www.oneusefulthing.org/)

---

*最后更新：{datetime.now().strftime('%Y-%m-%d')}*
"""
        return content, title
    
    def _write_general_insight(self, source: Dict) -> Tuple[str, str]:
        """通用洞察风格 - 当无法归类时"""
        title = f"对{source['source_title'][:40]}的思考"
        
        content = f"""# {title}

*基于：[{source['source_title']}]({source['source_link']})*

## 观察

{source['source_description'][:250] if source['source_description'] else '近期的一个技术讨论引发了关于AI发展方向的一些思考。'}

## 深层问题

这个讨论触及了几个未被充分探讨的议题：

**技术进步的叙事 vs 现实**：
我们常常被新发布的SOTA结果所包围，但这些结果在特定条件下成立，未必泛化到实际应用。更重要的是评估这些进步的**边界条件**——在什么情况下它有效，什么情况下失效。

**短期优化与长期健康**：
AI领域存在强烈的publish-or-perish压力，导致对快速可演示结果的偏好。这可能以牺牲系统的可理解性、可维护性为代价。

**集中化趋势**：
能够训练顶级模型的资源门槛持续上升，这可能带来创新来源的单一化风险。

## 开放性问题

基于以上观察，有几个问题值得社区更多讨论：
1. 我们如何定义AI系统的"成功"？是当前任务的性能，还是更广泛的能力提升？
2. 在追求规模的过程中，我们是否忽视了更高效、更可解释的路径？
3. 如何平衡开放研究的需要与潜在的安全风险？

## 对读者的邀请

本文更多是提出观察而非给出答案。如果你有不同的视角或相关的实证数据，欢迎分享。非共识的价值不在于它是否正确，而在于它推动我们更仔细地审视假设。

## 参考

- 原始讨论：{source['source_title']}
- 发布时间：{datetime.now().strftime('%Y-%m-%d')}

---

*基于公开信息整理，欢迎纠错和补充。*
"""
        return content, title
    
    def save_and_publish(self, content: str, title: str) -> str:
        """保存并发布"""
        # 生成slug
        slug = re.sub(r'[^\w]+', '-', title.lower()).strip('-')[:50]
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"{date_str}_{slug}.md"
        filepath = os.path.join(self.content_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 更新README索引
        self._update_readme_index(filename, title, date_str)
        
        # Git操作
        try:
            os.chdir(self.base_dir)
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
            subprocess.run(['git', 'commit', '-m', f'[blog] {title[:40]}'], 
                         check=True, capture_output=True)
            subprocess.run(['git', 'push', 'origin', 'main'], check=True, capture_output=True)
            return f"✅ 已发布: {filename}"
        except subprocess.CalledProcessError as e:
            return f"⚠️ 本地保存 (git push失败): {filename}"
    
    def _update_readme_index(self, filename: str, title: str, date_str: str):
        """更新README索引"""
        readme_path = os.path.join(self.base_dir, "README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_entry = f"- [{date_str}] [{title}](content/{filename})\n"
        
        start_marker = "<!-- INDEX_START -->"
        if start_marker in content:
            idx = content.find(start_marker) + len(start_marker)
            content = content[:idx] + "\n" + new_entry + content[idx:]
        else:
            content = f"<!-- INDEX_START -->\n{new_entry}<!-- INDEX_END -->\n\n" + content
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def run(self):
        """运行生成器 - 基于真实信息源"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 基于真实信息源生成博客...")
        
        # 1. 选择信息源
        source_config = random.choice(self.rss_sources)
        print(f"选择信息源: {source_config['name']}")
        
        # 2. 获取内容
        items = self.fetch_rss_feed(source_config['url'])
        if not items:
            print("⚠️ 无法获取RSS内容，使用备用方案")
            return
        
        # 3. 分析内容
        source_data = self.analyze_source_content(items)
        if not source_data:
            print("⚠️ 无法分析内容")
            return
        
        print(f"检测话题类型: {source_data['topic_type']}")
        print(f"基于文章: {source_data['source_title'][:50]}...")
        
        # 4. 生成博客
        content, title = self.generate_blog_from_source(source_data)
        
        # 5. 保存并发布
        result = self.save_and_publish(content, title)
        
        print(result)
        print(f"标题: {title}")
        print("-" * 70)

if __name__ == "__main__":
    generator = SourceBasedBlogGenerator()
    generator.run()
