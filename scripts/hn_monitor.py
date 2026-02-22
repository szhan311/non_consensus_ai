#!/usr/bin/env python3
"""
Hacker News AI 话题监控器

使用方法：
- 定期运行获取 HN 热门 AI 话题
- 提取高价值讨论中的 RSS 源
- 发现新的非共识观点
"""

import os
import json
from datetime import datetime
from typing import List, Dict

class HNMonitor:
    """HN 内容监控器"""
    
    def __init__(self):
        self.data_dir = os.path.expanduser("~/Desktop/superintelligence_lab")
        self.tracked_domains_file = f"{self.data_dir}/hn_tracked_domains.json"
        self.hot_topics_file = f"{self.data_dir}/hn_hot_topics.json"
        
        # HN RSSHub 端点
        self.hn_rss_endpoints = {
            "frontpage": "https://hnrss.org/frontpage",
            "best": "https://hnrss.org/best",
            "newest": "https://hnrss.org/newest",
            "ai_search": "https://hnrss.org/newest?q=artificial+intelligence+OR+machine+learning+OR+llm",
            "programming_culture": "https://hnrss.org/newest?q=programmer+culture+engineering",
            "ask_hn": "https://hnrss.org/ask"
        }
        
        # 从之前浏览中发现的优质域名
        self.premium_domains = {
            "karpathy.ai": {"author": "Andrej Karpathy", "focus": "AI education", "weight": 10},
            "surfingcomplexity.blog": {"author": "Lorin Hochstein", "focus": "systems", "weight": 10},
            "ratfactor.com": {"author": "ratfactor", "focus": "programming culture", "weight": 10},
            "danluu.com": {"author": "Dan Luu", "focus": "performance/critique", "weight": 10},
            "jvns.ca": {"author": "Julia Evans", "focus": "systems/education", "weight": 10},
            "normaltech.ai": {"author": "AI Snake Oil", "focus": "AI critique", "weight": 10},
            "distill.pub": {"author": "Distill team", "focus": "visual research", "weight": 10},
            "thegradient.pub": {"author": "Various", "focus": "AI policy", "weight": 9},
            "alignmentforum.org": {"author": "Alignment community", "focus": "AI safety", "weight": 9},
            "lesswrong.com": {"author": "Rationalist community", "focus": "AI forecasting", "weight": 9},
            "practical.engineering": {"author": "Grady", "focus": "engineering", "weight": 8},
            "0byte.io": {"author": "0byte", "focus": "ML visualization", "weight": 8},
            "notnotp.com": {"author": "notnotp", "focus": "database/search", "weight": 8},
            "governance.fyi": {"author": "governance.fyi", "focus": "institutions", "weight": 8},
            "theregister.com": {"author": "The Register", "focus": "tech news/critique", "weight": 8},
            "scottaaronson.com": {"author": "Scott Aaronson", "focus": "quantum/AI", "weight": 9},
        }
        
        self.load_data()
    
    def load_data(self):
        """加载已跟踪的数据"""
        if os.path.exists(self.tracked_domains_file):
            with open(self.tracked_domains_file, 'r') as f:
                self.tracked_domains = json.load(f)
        else:
            self.tracked_domains = self.premium_domains.copy()
        
        if os.path.exists(self.hot_topics_file):
            with open(self.hot_topics_file, 'r') as f:
                self.hot_topics = json.load(f)
        else:
            self.hot_topics = []
    
    def save_data(self):
        """保存跟踪数据"""
        with open(self.tracked_domains_file, 'w') as f:
            json.dump(self.tracked_domains, f, indent=2)
        
        with open(self.hot_topics_file, 'w') as f:
            json.dump(self.hot_topics, f, indent=2)
    
    def get_rss_feeds_for_tracking(self) -> str:
        """生成可用于 RSS 阅读器的 OPML 或列表"""
        
        lines = [
            "# HN 精选 RSS 订阅列表",
            f"# 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "# 基于 HN 社区热门内容整理\n"
        ]
        
        # 按权重排序
        sorted_domains = sorted(
            self.tracked_domains.items(),
            key=lambda x: x[1].get('weight', 0),
            reverse=True
        )
        
        for domain, info in sorted_domains:
            lines.append(f"\n## {domain}")
            lines.append(f"- 作者：{info.get('author', 'N/A')}")
            lines.append(f"- 专注：{info.get('focus', 'N/A')}")
            lines.append(f"- 权重：{info.get('weight', 0)}/10")
            # 尝试构造 RSS URL
            rss_url = self._guess_rss_url(domain)
            if rss_url:
                lines.append(f"- RSS：`{rss_url}`")
        
        return "\n".join(lines)
    
    def _guess_rss_url(self, domain: str) -> str:
        """猜测 RSS URL"""
        patterns = [
            f"https://{domain}/feed",
            f"https://{domain}/feed.xml",
            f"https://{domain}/rss",
            f"https://{domain}/rss.xml",
            f"https://{domain}/atom.xml",
            f"https://{domain}/blog/feed",
        ]
        return patterns[0] if patterns else None
    
    def analyze_hn_post(self, title: str, url: str, points: int, comments: int) -> Dict:
        """分析 HN 帖子质量"""
        
        # 从 URL 提取域名
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        
        # 质量评分
        quality_score = 0
        
        # 基于 points 和 comments
        if points > 100:
            quality_score += 3
        elif points > 50:
            quality_score += 2
        elif points > 20:
            quality_score += 1
        
        if comments > 50:
            quality_score += 2
        elif comments > 20:
            quality_score += 1
        
        # 检测 AI 相关话题
        ai_keywords = ["ai", "artificial intelligence", "machine learning", "llm", "gpt", "neural"]
        is_ai_related = any(kw in title.lower() for kw in ai_keywords)
        
        if is_ai_related:
            quality_score += 1
        
        # 检测非共识指标
        nonconsensus_indicators = [
            "why", "what", "truth", "reality", "myth", "misconception",
            "contrary", "surprisingly", "actually", "not", "won't", "doesn't"
        ]
        has_nonconsensus_tone = any(ind in title.lower() for ind in nonconsensus_indicators)
        
        if has_nonconsensus_tone:
            quality_score += 2
        
        return {
            "title": title,
            "url": url,
            "domain": domain,
            "points": points,
            "comments": comments,
            "quality_score": quality_score,
            "is_ai_related": is_ai_related,
            "has_nonconsensus_tone": has_nonconsensus_tone,
            "detected_at": datetime.now().isoformat()
        }
    
    def extract_insight_from_content(self, content: str, source: str) -> Dict:
        """从 HN 帖子内容提取洞察"""
        
        # 简单的启发式提取
        lines = content.split("\n")
        
        insight = {
            "source": source,
            "extracted": datetime.now().isoformat(),
            "quotes": [],
            "potential_claims": []
        }
        
        for line in lines:
            line = line.strip()
            # 找引号内容
            if '"' in line and len(line) > 50:
                insight["quotes"].append(line[:200])
            
            # 找可能的观点声明
            if any(line.startswith(x) for x in ["I think", "In fact", "Actually", "The problem", "What if"]):
                insight["potential_claims"].append(line[:200])
        
        return insight
    
    def generate_daily_digest(self) -> str:
        """生成每日摘要"""
        
        lines = [
            "# HN AI 话题日报",
            f"\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"跟踪域名数：{len(self.tracked_domains)}",
            f"历史热门话题：{len(self.hot_topics)}\n",
            "\n## 高权重域名（建议优先阅读）\n"
        ]
        
        # 权重 >= 9 的域名
        high_weight = {k: v for k, v in self.tracked_domains.items() if v.get('weight', 0) >= 9}
        for domain, info in high_weight.items():
            lines.append(f"- **{domain}** - {info.get('author')} ({info.get('focus')})")
        
        lines.extend([
            "\n## HN RSS 订阅链接",
            "```",
            "# 首页热门",
            "https://hnrss.org/frontpage",
            "",
            "# 最佳内容",
            "https://hnrss.org/best",
            "",
            "# AI 相关",
            "https://hnrss.org/newest?q=artificial+intelligence+OR+machine+learning+OR+llm",
            "",
            "# 编程文化",
            "https://hnrss.org/newest?q=programmer+culture+engineering",
            "```"
        ])
        
        return "\n".join(lines)


def main():
    """主函数"""
    monitor = HNMonitor()
    
    # 生成 RSS 列表
    rss_list = monitor.get_rss_feeds_for_tracking()
    
    # 保存到文件
    output_file = os.path.expanduser("~/Desktop/superintelligence_lab/hn_rss_feeds_list.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rss_list)
    
    # 生成日报
    digest = monitor.generate_daily_digest()
    digest_file = os.path.expanduser("~/Desktop/superintelligence_lab/hn_daily_digest.md")
    with open(digest_file, 'w', encoding='utf-8') as f:
        f.write(digest)
    
    print("="*70)
    print("HN AI 话题监控器")
    print("="*70)
    print(f"\n已跟踪域名：{len(monitor.tracked_domains)} 个")
    print(f"高权重域名 (≥9)：{sum(1 for v in monitor.tracked_domains.values() if v.get('weight', 0) >= 9)} 个")
    
    print("\n" + "-"*70)
    print("生成的文件：")
    print(f"1. {output_file}")
    print(f"2. {digest_file}")
    
    print("\n" + "-"*70)
    print("推荐的 RSSHub 端点：")
    for name, url in monitor.hn_rss_endpoints.items():
        print(f"\n{name}:")
        print(f"  {url}")
    
    print("\n" + "="*70)
    print("使用建议：")
    print("1. 将这些 RSS 添加到 Feedly / Inoreader / 其他阅读器")
    print("2. 重点关注高权重域名的内容")
    print("3. 每天浏览 HN 首页 RSS，发现新域名")
    print("4. 发现好内容后，粘贴到 x_content_collector.md")
    print("="*70)


if __name__ == "__main__":
    main()
