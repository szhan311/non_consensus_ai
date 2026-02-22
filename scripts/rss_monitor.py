#!/usr/bin/env python3
"""
RSS 内容监控器 - 定期检查关键RSS源，提取非共识洞察

使用方法：
1. 运行此脚本获取最新RSS内容
2. 提取有价值的非共识话题
3. 自动更新到 insight_miner.py
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict

class RSSMonitor:
    """RSS内容监控器"""
    
    def __init__(self):
        self.feeds_file = os.path.expanduser("~/Desktop/superintelligence_lab/rss_feeds.md")
        self.collected_file = os.path.expanduser("~/Desktop/superintelligence_lab/rss_collected_insights.json")
        self.load_collected()
        
    def load_collected(self):
        """加载已收集的洞察"""
        if os.path.exists(self.collected_file):
            with open(self.collected_file, 'r', encoding='utf-8') as f:
                self.collected = json.load(f)
        else:
            self.collected = {"insights": [], "last_check": None}
    
    def save_collected(self):
        """保存收集的洞察"""
        with open(self.collected_file, 'w', encoding='utf-8') as f:
            json.dump(self.collected, f, ensure_ascii=False, indent=2)
    
    def extract_from_rss_content(self, title: str, content: str, source: str) -> Dict:
        """从RSS内容提取非共识洞察"""
        
        # 检测争议性话题的关键词
        controversy_indicators = [
            "won't", "not automatically", "by default", "contrary to",
            "myth", "misconception", "surprisingly", "actually",
            "what we got wrong", "the problem with", "why X fails",
            "hidden", "secret", "truth", "reality"
        ]
        
        # 检测反直觉模式
        counterintuitive_patterns = [
            r"(?i)despite .*, (?:we|they|it)",
            r"(?i)contrary to (?:popular belief|expectations)",
            r"(?i)the real (?:reason|problem|issue)",
            r"(?i)what .*(?:don't|doesn't) tell you",
            r"(?i)why .* (?:won't|isn't|doesn't)"
        ]
        
        text_lower = (title + " " + content).lower()
        
        # 计算争议分数
        controversy_score = sum(1 for indicator in controversy_indicators if indicator in text_lower)
        
        # 检测反直觉模式
        pattern_matches = sum(1 for pattern in counterintuitive_patterns if re.search(pattern, title + " " + content))
        
        # 话题分类
        topic_categories = {
            "编程/开发": ["coding", "programming", "developer", "software", "code"],
            "商业模式": ["business", "startup", "market", "revenue", "pricing"],
            "AI能力": ["capability", "ability", "performance", "benchmark"],
            "社会影响": ["society", "impact", "job", "work", "labor"],
            "安全/对齐": ["safety", "alignment", "risk", "harm"],
            "研究/学术": ["research", "study", "paper", "academic"]
        }
        
        detected_category = "AI趋势"
        for category, keywords in topic_categories.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_category = category
                break
        
        insight = {
            "title": title,
            "source": source,
            "extracted_at": datetime.now().isoformat(),
            "controversy_score": controversy_score,
            "pattern_matches": pattern_matches,
            "category": detected_category,
            "quality_score": controversy_score + pattern_matches,
            "is_nonconsensus": controversy_score >= 2 or pattern_matches >= 1
        }
        
        return insight
    
    def format_for_insight_miner(self, insight: Dict, original_content: str) -> Dict:
        """格式化为 insight_miner 话题格式"""
        
        # 构建提示词，用于生成完整的话题格式
        prompt = f"""基于以下内容，生成一个非共识洞察话题：

标题：{insight['title']}
来源：{insight['source']}
类别：{insight['category']}
内容摘要：{original_content[:800]}

请生成JSON格式：
{{
    "surface_claim": "大众普遍接受的观点（一句话）",
    "mainstream_assumption": "主流假设是什么",
    "core_facts": ["事实1", "事实2", "事实3", "事实4"],
    "deep_insight": "真正的深度洞察（用**强调关键词）",
    "why_correct": "为什么这个分析可能是对的",
    "insight_level": 8-10,
    "field": "{insight['category']}"
}}

要求：
- surface_claim 应该是大众普遍相信的观点
- deep_insight 应该是反直觉但有理的观点
- core_facts 应该是客观可验证的事实
- 不要出现"第一性原理"等方法论词汇
"""
        
        return {
            "prompt": prompt,
            "metadata": insight
        }
    
    def generate_report(self) -> str:
        """生成收集报告"""
        lines = [
            "# RSS 非共识洞察收集报告",
            f"\n最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"已收集洞察数：{len(self.collected['insights'])}",
            "\n## 高价值洞察（quality_score >= 3）\n"
        ]
        
        high_value = [i for i in self.collected['insights'] if i.get('quality_score', 0) >= 3]
        high_value.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        
        for idx, insight in enumerate(high_value[:10], 1):
            lines.append(f"{idx}. **{insight['title']}**")
            lines.append(f"   - 来源：{insight['source']}")
            lines.append(f"   - 类别：{insight['category']}")
            lines.append(f"   - 质量分：{insight.get('quality_score', 0)}")
            lines.append("")
        
        return "\n".join(lines)


def main():
    """主函数"""
    monitor = RSSMonitor()
    
    # 显示当前状态
    print("="*70)
    print("RSS 非共识洞察监控器")
    print("="*70)
    print(f"\n已收集洞察：{len(monitor.collected['insights'])} 条")
    print(f"最后检查：{monitor.collected.get('last_check', '从未')}")
    
    # 生成报告
    report = monitor.generate_report()
    report_file = os.path.expanduser("~/Desktop/superintelligence_lab/rss_report.md")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n报告已保存：{report_file}")
    
    # 显示高价值洞察
    high_value = [i for i in monitor.collected['insights'] if i.get('quality_score', 0) >= 3]
    if high_value:
        print(f"\n高价值洞察（{len(high_value)} 条）：")
        for insight in high_value[:5]:
            print(f"  - {insight['title'][:60]}... (质量分: {insight.get('quality_score', 0)})")
    else:
        print("\n暂无高价值洞察。请手动添加从RSS获取的内容。")
    
    print("\n" + "="*70)
    print("使用提示：")
    print("1. 手动浏览RSS源列表中的链接")
    print("2. 发现有趣的内容后，粘贴到 x_content_collector.md")
    print("3. 我会定期整理并更新到 insight_miner.py")
    print("="*70)


if __name__ == "__main__":
    main()
