#!/usr/bin/env python3
"""
AI RSS 聚合器 - 从知名AI博客获取非共识内容

使用 RSSHub 或其他RSS服务获取内容
"""

import os
import json
import random
from datetime import datetime
from typing import List, Dict

class RSSFeedAggregator:
    """RSS内容聚合器"""
    
    def __init__(self):
        # 知名AI RSS源配置
        self.rss_sources = {
            "curated_independent": [
                {
                    "name": "Jay Alammar",
                    "url": "https://jalammar.github.io/feed.xml",
                    "type": "visualization",
                    "weight": 10,
                    "description": "技术可视化、概念解释 - The Illustrated Transformer"
                },
                {
                    "name": "inFERENCe (Ferenc Huszár)",
                    "url": "https://www.inference.vc/rss",
                    "type": "technical_insights",
                    "weight": 10,
                    "description": "因果推断、生成模型、元学习"
                },
                {
                    "name": "AI Weirdness (Janelle Shane)",
                    "url": "https://aiweirdness.com/rss",
                    "type": "ai_critique",
                    "weight": 10,
                    "description": "AI失败案例、批判性视角"
                },
                {
                    "name": "Seita's Place (Daniel Seita)",
                    "url": "https://danieltakeshi.github.io/feed.xml",
                    "type": "rl_robotics",
                    "weight": 9,
                    "description": "机器人、深度强化学习"
                },
                {
                    "name": "David Stutz",
                    "url": "http://davidstutz.de/feed",
                    "type": "paper_reviews",
                    "weight": 9,
                    "description": "AI论文独立评论"
                }
            ],
            "hn_curated": [
                {
                    "name": "surfingcomplexity.blog",
                    "url": "https://surfingcomplexity.blog/feed/",
                    "type": "independent_blog",
                    "weight": 10,
                    "description": "系统安全、复杂系统失效分析"
                },
                {
                    "name": "ratfactor.com",
                    "url": "https://ratfactor.com/feed/",
                    "type": "independent_blog",
                    "weight": 10,
                    "description": "编程文化、身份认同"
                },
                {
                    "name": "danluu.com",
                    "url": "https://danluu.com/atom.xml",
                    "type": "independent_blog",
                    "weight": 10,
                    "description": "性能分析、批判思考"
                },
                {
                    "name": "jvns.ca",
                    "url": "https://jvns.ca/atom.xml",
                    "type": "independent_blog",
                    "weight": 10,
                    "description": "系统编程、Julia Evans"
                },
                {
                    "name": "0byte.io",
                    "url": "https://0byte.io/rss/",
                    "type": "independent_blog",
                    "weight": 9,
                    "description": "技术可视化"
                },
                {
                    "name": "governance.fyi",
                    "url": "https://www.governance.fyi/feed",
                    "type": "independent_blog",
                    "weight": 8,
                    "description": "制度分析"
                }
            ],
            "research_labs": [
                {
                    "name": "Anthropic Research",
                    "url": "https://www.anthropic.com/rss.xml",
                    "type": "company_blog",
                    "weight": 10
                },
                {
                    "name": "OpenAI Blog",
                    "url": "https://openai.com/blog/rss.xml",
                    "type": "company_blog",
                    "weight": 9
                },
                {
                    "name": "DeepMind Blog",
                    "url": "https://deepmind.google/discover/blog/rss/",
                    "type": "company_blog",
                    "weight": 9
                },
                {
                    "name": "Google AI Blog",
                    "url": "https://ai.googleblog.com/feeds/posts/default",
                    "type": "company_blog",
                    "weight": 8
                },
                {
                    "name": "Microsoft Research",
                    "url": "https://www.microsoft.com/en-us/research/feed/",
                    "type": "company_blog",
                    "weight": 8
                },
                {
                    "name": "Meta AI Research",
                    "url": "https://ai.meta.com/blog/rss/",
                    "type": "company_blog",
                    "weight": 8
                }
            ],
            "publications": [
                {
                    "name": "Distill.pub",
                    "url": "https://distill.pub/rss.xml",
                    "type": "academic",
                    "weight": 10
                },
                {
                    "name": "The Gradient",
                    "url": "https://thegradient.pub/rss/",
                    "type": "academic",
                    "weight": 9
                },
                {
                    "name": "ML/AI Papers with Code",
                    "url": "https://paperswithcode.com/rss",
                    "type": "academic",
                    "weight": 8
                }
            ],
            "newsletters": [
                {
                    "name": "Import AI (Jack Clark)",
                    "url": "https://importai.substack.com/feed",
                    "type": "newsletter",
                    "weight": 10
                },
                {
                    "name": "The Batch (Andrew Ng)",
                    "url": "https://www.deeplearning.ai/the-batch/rss/",
                    "type": "newsletter",
                    "weight": 9
                },
                {
                    "name": "AI Snake Oil",
                    "url": "https://aisnakeoil.substack.com/feed",
                    "type": "newsletter",
                    "weight": 10
                },
                {
                    "name": "One Useful Thing (Ethan Mollick)",
                    "url": "https://www.oneusefulthing.org/rss",
                    "type": "newsletter",
                    "weight": 9
                },
                {
                    "name": "AI Alignment Newsletter",
                    "url": "https://rohinshah.com/alignment-newsletter/rss.xml",
                    "type": "newsletter",
                    "weight": 8
                }
            ],
            "thinkers": [
                {
                    "name": "LessWrong - AI",
                    "url": "https://www.lesswrong.com/feed.xml?view=curated-rss",
                    "type": "community",
                    "weight": 9
                },
                {
                    "name": "AI Alignment Forum",
                    "url": "https://www.alignmentforum.org/feed.xml?view=curated-rss",
                    "type": "community",
                    "weight": 9
                },
                {
                    "name": "Slate Star Codex",
                    "url": "https://slatestarcodex.com/feed/",
                    "type": "blog",
                    "weight": 8
                }
            ],
            "tech_critique": [
                {
                    "name": "Wired - AI",
                    "url": "https://www.wired.com/feed/tag/ai/latest/rss",
                    "type": "tech_news",
                    "weight": 7
                },
                {
                    "name": "MIT Tech Review - AI",
                    "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
                    "type": "tech_news",
                    "weight": 8
                },
                {
                    "name": "The Verge - AI",
                    "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
                    "type": "tech_news",
                    "weight": 7
                }
            ]
        }
        
        # RSSHub镜像列表（用于需要RSSHub的源）
        self.rsshub_instances = [
            "https://rsshub.app",
            "https://rsshub.rssforever.com",
            "https://rsshub.pseudoyu.com",
            "https://rsshub.fivecolorme.com",
            "https://rsshub.thzu.top"
        ]
    
    def get_all_feeds(self) -> List[Dict]:
        """获取所有RSS源"""
        all_feeds = []
        for category, feeds in self.rss_sources.items():
            for feed in feeds:
                feed['category'] = category
                all_feeds.append(feed)
        return all_feeds
    
    def get_high_priority_feeds(self) -> List[Dict]:
        """获取高优先级源（weight >= 9）"""
        all_feeds = self.get_all_feeds()
        return [f for f in all_feeds if f['weight'] >= 9]
    
    def generate_feed_list_markdown(self) -> str:
        """生成RSS源列表文档"""
        lines = ["# AI RSS 源列表\n", "最后更新：{}\n".format(datetime.now().strftime("%Y-%m-%d"))]
        
        for category, feeds in self.rss_sources.items():
            lines.append(f"\n## {category.replace('_', ' ').title()}\n")
            for feed in feeds:
                weight_stars = "⭐" * (feed['weight'] // 2)
                lines.append(f"- **{feed['name']}** {weight_stars}")
                lines.append(f"  - URL: `{feed['url']}`")
                lines.append(f"  - Type: {feed['type']}")
                lines.append("")
        
        return "\n".join(lines)
    
    def fetch_feed_with_fallback(self, url: str) -> Dict:
        """尝试获取RSS feed，使用RSSHub作为fallback"""
        # 这里会集成实际的RSS获取逻辑
        # 可以使用 feedparser 库
        pass
    
    def extract_insights_from_content(self, title: str, content: str, source: str) -> Dict:
        """从内容中提取非共识洞察"""
        # 分析框架：
        # 1. 寻找争议性声明
        # 2. 识别反直觉观点
        # 3. 提取可验证的预测
        # 4. 记录来源和可信度
        
        insight = {
            "source": source,
            "title": title,
            "extracted_at": datetime.now().isoformat(),
            "potential_insights": [],
            "controversy_score": 0,
            "novelty_score": 0
        }
        
        # 关键词检测：争议性话题
        controversy_keywords = [
            "surprisingly", "contrary", "unlike", "despite", "however",
            "wrong", "myth", "misconception", "actually", "in fact",
            "what if", "what we got wrong", "the real reason",
            "nobody talks about", "hidden", "secret", "truth"
        ]
        
        # 关键词检测：反直觉
        counterintuitive_keywords = [
            "opposite", "reverse", "paradox", "counterintuitive",
            "less is more", "slower is faster", "weaker is stronger",
            "the problem with", "why X fails", "the dark side"
        ]
        
        content_lower = content.lower()
        
        for keyword in controversy_keywords:
            if keyword in content_lower:
                insight["controversy_score"] += 1
        
        for keyword in counterintuitive_keywords:
            if keyword in content_lower:
                insight["novelty_score"] += 1
        
        return insight


class RSSInsightMiner:
    """从RSS内容挖掘非共识洞察"""
    
    def __init__(self):
        self.aggregator = RSSFeedAggregator()
        self.collected_insights = []
    
    def process_rss_item(self, item: Dict) -> Dict:
        """处理单个RSS条目"""
        insight = {
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "source": item.get("source", ""),
            "published": item.get("published", ""),
            "content": item.get("summary", item.get("description", "")),
            "extracted_insight": None,
            "insight_quality_score": 0
        }
        
        # 提取潜在的非共识洞察
        extracted = self.aggregator.extract_insights_from_content(
            insight["title"],
            insight["content"],
            insight["source"]
        )
        
        insight["extracted_insight"] = extracted
        insight["insight_quality_score"] = (
            extracted["controversy_score"] + 
            extracted["novelty_score"]
        )
        
        return insight
    
    def generate_insight_miner_topic(self, insight: Dict) -> Dict:
        """将RSS洞察转换为insight_miner话题格式"""
        # 使用LLM来分析和转换
        # 这里定义prompt模板
        
        prompt_template = """
基于以下RSS文章，提取一个非共识洞察：

标题：{title}
来源：{source}
内容摘要：{content}

请分析：
1. 表面观点是什么？（大众怎么看）
2. 真正的洞察是什么？（反直觉但有理的观点）
3. 支撑这个事实的关键事实是什么？
4. 为什么这个分析可能是对的？（深层逻辑）
5. 6个月内可能出现什么验证信号？

输出格式（JSON）：
{{
    "surface_claim": "...",
    "mainstream_assumption": "...",
    "core_facts": ["...", "...", "...", "..."],
    "deep_insight": "...",
    "why_correct": "...",
    "insight_level": 8-10,
    "field": "..."
}}
"""
        
        return {
            "prompt": prompt_template.format(
                title=insight["title"],
                source=insight["source"],
                content=insight["content"][:500]
            ),
            "source_url": insight["link"],
            "quality_score": insight["insight_quality_score"]
        }


def main():
    """主函数 - 生成RSS源列表"""
    aggregator = RSSFeedAggregator()
    
    # 生成文档
    markdown = aggregator.generate_feed_list_markdown()
    
    # 保存
    output_dir = os.path.expanduser("~/Desktop/superintelligence_lab")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/rss_feeds.md", 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print("="*70)
    print("AI RSS 源列表已生成")
    print("="*70)
    print(f"\n共 {len(aggregator.get_all_feeds())} 个RSS源")
    print(f"高优先级源：{len(aggregator.get_high_priority_feeds())} 个")
    print(f"\n保存位置：{output_dir}/rss_feeds.md")
    print("\n高优先级源：")
    for feed in aggregator.get_high_priority_feeds()[:5]:
        stars = "⭐" * (feed['weight'] // 2)
        print(f"  - {feed['name']} {stars}")


if __name__ == "__main__":
    main()
