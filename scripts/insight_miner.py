#!/usr/bin/env python3
"""
非共识AI内容生成器 - 基于RSS/HN高质量内容

不再使用固定话题库，而是：
1. 从RSS源获取最新内容
2. 分析内容中的非共识观点
3. 生成深度洞察
"""

import os
import json
import random
from datetime import datetime
from typing import List, Dict, Optional

class NonConsensusGenerator:
    """基于实时内容的非共识生成器"""
    
    def __init__(self):
        self.content_dir = os.path.expanduser("~/Desktop/non_consensus_ai/content")
        self.rss_sources = self._load_rss_sources()
        self.recent_topics = self._load_recent_topics()
        
    def _load_rss_sources(self) -> List[Dict]:
        """加载RSS源配置"""
        return [
            # 高价值独立博客
            {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/", "type": "llm_apps"},
            {"name": "Dynomight", "url": "https://dynomight.net/feed.xml", "type": "analysis"},
            {"name": "Gwern", "url": "https://gwern.substack.com/feed", "type": "research"},
            {"name": "Gary Marcus", "url": "https://garymarcus.substack.com/feed", "type": "critique"},
            {"name": "AI Snake Oil", "url": "https://www.normaltech.ai/feed", "type": "social_impact"},
            {"name": "inFERENCe", "url": "https://www.inference.vc/rss", "type": "technical"},
            {"name": "AI Weirdness", "url": "https://aiweirdness.com/rss", "type": "humor_critique"},
            
            # HN社区精选
            {"name": "surfingcomplexity", "url": "https://surfingcomplexity.blog/feed/", "type": "systems"},
            {"name": "ratfactor", "url": "https://ratfactor.com/feed/", "type": "culture"},
            {"name": "danluu", "url": "https://danluu.com/atom.xml", "type": "performance"},
            {"name": "jvns", "url": "https://jvns.ca/atom.xml", "type": "education"},
            
            # Newsletter
            {"name": "Import AI", "url": "https://importai.substack.com/feed", "type": "news"},
            {"name": "One Useful Thing", "url": "https://www.oneusefulthing.org/rss", "type": "education"},
        ]
    
    def _load_recent_topics(self) -> List[str]:
        """加载最近生成的话题，避免重复"""
        recent = []
        try:
            files = sorted(os.listdir(self.content_dir))
            for f in files[-5:]:  # 最近5个文件
                if f.endswith('.md'):
                    with open(f"{self.content_dir}/{f}", 'r') as file:
                        content = file.read()
                        # 提取第一行作为话题
                        first_line = content.split('\n')[0]
                        recent.append(first_line)
        except:
            pass
        return recent
    
    def get_suggested_source(self) -> Dict:
        """推荐一个RSS源供用户查看"""
        # 随机推荐一个源
        source = random.choice(self.rss_sources)
        return {
            "source": source,
            "suggestion": f"请浏览 {source['name']} ({source['url']})，寻找有价值的非共识观点。",
            "looking_for": [
                "反直觉的发现",
                "对主流观点的质疑",
                "被忽视的事实",
                "有争议的预测"
            ]
        }
    
    def generate_from_content(self, source_title: str, source_content: str, source_url: str) -> str:
        """基于外部内容生成非共识洞察"""
        
        # 分析框架
        analysis_prompt = self._create_analysis_framework(source_title, source_content)
        
        return analysis_prompt
    
    def _create_analysis_framework(self, title: str, content: str) -> str:
        """创建分析框架 - 指导LLM如何分析"""
        
        return f"""基于以下内容，生成深度非共识分析：

原文标题：{title}

原文摘要：
{content[:800]}

请按以下结构分析：

1. **表面共识**
   这个领域大多数人默认接受的观点是什么？

2. **被忽视的事实**
   有哪些关键事实被主流讨论忽略了？

3. **反直觉的洞察**
   如果上述事实很重要，那么更准确的结论应该是什么？

4. **支撑逻辑**
   为什么这个反直觉的结论可能是对的？

5. **可验证的预测**
   如果这个分析成立，未来6个月我们会观察到什么？

6. **自我质疑**
   我可能在哪个环节错了？什么样的证据会推翻这个分析？

要求：
- 专注于洞察本身，不迎合任何平台风格
- 逻辑链条清晰，有理有据
- 承认不确定性，保持开放态度
- 用markdown格式输出
"""
    
    def save_generated_content(self, content: str, source: str) -> str:
        """保存生成的内容"""
        os.makedirs(self.content_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{self.content_dir}/insight_{timestamp}.md"
        
        # 添加元数据
        full_content = f"""---
source: {source}
generated_at: {timestamp}
---

{content}
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        return filename
    
    def generate_prompt_for_manual_input(self) -> str:
        """生成提示，引导用户输入内容"""
        suggestion = self.get_suggested_source()
        
        return f"""
【非共识AI内容生成】

{suggestion['suggestion']}

寻找：
- {suggestion['looking_for'][0]}
- {suggestion['looking_for'][1]}
- {suggestion['looking_for'][2]}
- {suggestion['looking_for'][3]}

当你找到有价值的内容，请提供：
1. 标题
2. 链接  
3. 核心观点（复制关键段落）

我将基于这些内容生成深度分析。
"""


def main():
    """主函数 - 显示推荐源"""
    generator = NonConsensusGenerator()
    
    print("="*70)
    print("非共识AI内容生成器")
    print("="*70)
    print("\n【模式变更】不再使用固定话题库")
    print("【新流程】基于RSS/HN高质量内容实时生成\n")
    
    # 推荐一个源
    suggestion = generator.get_suggested_source()
    source = suggestion['source']
    
    print(f"📖 推荐查看：{source['name']}")
    print(f"   类型：{source['type']}")
    print(f"   URL：{source['url']}\n")
    
    print("寻找：")
    for item in suggestion['looking_for']:
        print(f"   • {item}")
    
    print("\n" + "="*70)
    print("当你发现好内容，请提供：")
    print("1. 标题")
    print("2. 链接")
    print("3. 核心观点（关键段落）")
    print("="*70)


if __name__ == "__main__":
    main()
