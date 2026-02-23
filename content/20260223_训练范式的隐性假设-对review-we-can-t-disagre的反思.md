# 训练范式的隐性假设：对Review: "We can't disagre的反思

*基于：[Review: "We can't disagree forever"](https://www.lesswrong.com/posts/kAgnBc3JQQKAAdicP/review-we-can-t-disagree-forever)*

## 核心观察

Published on February 23, 2026 1:17 PM GMT<br/><br/><p>Some interesting results from <a href="https://www.polemarchakis.org/a16-cdf.pdf">We Can't Disagree Forever</a> by Geanakoplo

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

- 引发本文思考的原始讨论：Review: "We can't disagree forever"
- 相关技术背景：[The Pile论文](https://arxiv.org/abs/2101.00027)关于数据构成的讨论

---

*最后更新：2026-02-23*
