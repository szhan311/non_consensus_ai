# 评测的幻觉：Import AI 445: Timing superintellig

*基于：[Import AI 445: Timing superintelligence; AIs solve frontier math proofs; a new ML research benchmark](https://importai.substack.com/p/import-ai-445-timing-superintelligence)*

## 分数的暴政

Will 2026 be looked back on as the pivotal year for making decisions about the singularity?

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

- 启发本文的原始内容：Import AI 445: Timing superintelligence; AIs solve frontier math proofs; a new ML research benchmark
- 相关学术讨论：[Beyond the Imitation Game](https://arxiv.org/abs/2206.04615)

---

*最后更新：2026-02-24*
