# 安全研究的盲点：从Realistic Evaluations Will Not谈起

*基于：[Realistic Evaluations Will Not Prevent Evaluation Awareness](https://www.lesswrong.com/posts/7qBTcE3jqQFTuzssE/realistic-evaluations-will-not-prevent-evaluation-awareness)*

## 安全讨论的结构性问题

Published on February 24, 2026 5:51 PM GMT<br/><br/><h2>One Minute Summary</h2><p>I think there's a fundamental limit to behavioral alignment evaluations that gets worse as models 

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

- 本文受Realistic Evaluations Will Not Prevent Evaluation Awareness启发
- 相关讨论：[AI Alignment Forum](https://alignmentforum.org/)

---

*最后更新：2026-02-24*
