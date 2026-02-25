# Uniform-State Diffusion的复兴：为什么Masked Diffusion可能不是唯一答案

*基于：arXiv:2602.21185 - "The Diffusion Duality, Chapter II: Ψ-Samplers and Efficient Curriculum"*

## 核心发现

EPFL和Cornell Tech的最新研究提出了一个挑战当前主流叙事的重要观点：**Uniform-state离散扩散模型（USDMs）配合适当的采样器，可能在语言建模上超越Masked Diffusion Models（MDMs）**。

这一发现直接质疑了近年来形成的共识——即Masked Diffusion是离散扩散语言模型的"必然未来"。

## 背景：两种扩散范式

离散扩散模型主要采用两种噪声分布：

**Masked Diffusion Models (MDMs)**：
- 将所有概率质量集中在特殊的[mask] token上
- 每个token在生成过程中只更新一次
- 在高采样步骤下表现较好
- 但缺乏自我修正能力

**Uniform-State Diffusion Models (USDMs)**：
- 使用均匀先验分布
- 允许token在生成过程中多次修订
- 具备自我修正能力
- 在few-step和guided generation中表现优异
- 但在高采样步骤下，使用传统ancestral samplers时质量会plateau

## 关键突破：Ψ-Samplers

作者提出了**Predictor-Corrector (PC) samplers**的一个新家族，称为**Ψ-samplers**，具有几个关键特性：

**1. 持续改进特性**

与传统ancestral sampling不同，Ψ-samplers随着采样步骤的增加**持续改进**，而不是plateau。这一点在语言建模中尤为重要——OpenWebText上的实验显示，generative perplexity随NFEs（神经网络函数评估次数）持续下降。

**2. 性能超越**

- **语言建模**：在OpenWebText上，使用uniform-state diffusion配合Ψ-samplers实现了比MDLMs（配合ReMDM）更低的generative perplexity
- **图像建模**：在CIFAR-10上，Ψ-samplers实现了更好的FID和IS分数
- **关键指标**：在matched unigram entropy条件下进行比较，确保公平性

**3. 通用性**

Ψ-samplers基于**非马尔可夫叠加后验**（non-Markovian superposition posteriors），可以应用于**任意噪声过程**，不限于uniform-state或masked。这大大扩展了设计空间。

## 技术细节：为什么USDMs之前落后？

USDMs之前在高采样步骤下表现不佳，根本原因在于**采样方法**，而非模型本身的表达能力。

**传统ancestral samplers的问题**：
- 对于USDMs，ancestral sampling会quickly converge到一个局部最优
- 缺乏有效的"correction"机制来refine初始预测
- 导致随着步骤增加，改进空间迅速耗尽（plateau）

**Ψ-samplers的解决方案**：
- 引入predictor-corrector机制
- Predictor：基于当前状态生成初始预测
- Corrector：迭代refine这些预测
- 这种迭代refine过程允许USDMs充分发挥其self-correction能力

## 实际影响：训练效率

除了采样改进，论文还提出了**Duo++**的训练策略：

- **训练时间减少25%**
- **内存使用减少33%**
- 相比Duo（Sahoo et al., 2025）的课程学习策略
- 在OpenWebText和LM1B上保持comparable perplexity
- 下游任务性能保持强劲

这使得USDMs不仅在推理时更有竞争力，在训练效率上也更具优势。

## 对领域共识的挑战

这篇论文最引人注目的贡献是**挑战了关于离散扩散语言模型发展路径的假设**：

**传统观点**：
- Masked Diffusion是当前SOTA
- USDMs虽然理论上有趣，但实际性能不如MDMs
- 未来研究应继续优化MDMs

**本文观点**：
- USDMs的劣势主要来自采样方法，而非模型本身
- 配合适当的samplers（如Ψ-samplers），USDMs可以超越MDMs
- 需要重新评估两种范式的relative merits

这类似于过去在 continuous diffusion 领域发生的讨论：DDPM vs DDIM vs 其他samplers的演进，最终证明sampling algorithm的选择可以dramatically改变模型表现。

## 对并行生成的意义

对于关注并行解码的研究者来说，这一发现具有特殊意义：

**1. Self-Correction的重要性**

USDMs允许多次修订token，这与并行解码的迭代优化哲学一致。Ψ-samplers的成功表明，有效的iterative refinement机制对于并行生成质量至关重要。

**2. Few-Step优化的补充**

虽然USDMs已在few-step generation中表现优异，但传统观点认为在高步骤下仍不如MDMs。Ψ-samplers打破这一假设，意味着USDMs可能成为**全步骤范围**（few-step到many-step）的统一解决方案。

**3. 设计空间的扩展**

Ψ-samplers的通用性（适用于任意噪声过程）提示我们：
- 不必局限于masked vs uniform的二元选择
- 可能存在intermediate noise schedules
- Sampling algorithm的选择可能比noise process本身更重要

## 局限性与开放问题

**1. 评估范围**

论文主要在OpenWebText和CIFAR-10上验证。更大规模语言模型（如LLaDA级别的8B+参数）上的表现仍需验证。

**2. 下游任务**

虽然论文提到"strong downstream performance"，但具体在哪些任务上超越MDMs需要更详细的分析。特别是对于需要复杂推理的任务，USDMs的表现尚不明确。

**3. 计算成本**

PC samplers涉及multiple forward passes per step，虽然质量提升，但实际的latency-wall-clock trade-off需要更仔细的测量。

**4. 理论理解**

为什么Ψ-samplers能让USDMs持续改进而ancestral sampling会plateau？这背后的理论机制值得更深入的分析。

## 可验证预测

基于这篇论文的发现，我提出以下预测：

**短期（3-6个月）**：
- 会有研究将Ψ-samplers应用于更大规模的USDMs（如LLaDA-8B级别）
- 对于并行解码社区，USDMs的关注度将显著上升

**中期（6-12个月）**：
- 可能会出现hybrid approach，结合masked和uniform-state的优点
- Sampler design将成为离散扩散研究的重要子领域，类似于continuous diffusion中的sampler研究

**长期（1-2年）**：
- 如果Ψ-samplers在大规模模型上验证成功，可能会动摇MDMs的主导地位
- "Diffusion模型选择"可能会成为与"架构选择"（Transformer vs State Space）同等重要的决策

## 结论

这篇论文通过Ψ-samplers的引入，展示了USDMs被低估的潜力。核心启示是：**在评估生成模型时，必须区分"模型能力"和"采样算法能力"**。

USDMs之前的劣势可能仅仅是采样方法选择不当的结果，而非模型架构的固有缺陷。这一发现提醒我们，在追逐新架构（如从AR到MDMs）的同时，不应忽视对已有架构的采样算法优化。

对于TC Parallel Sampling等与并行生成相关的工作，这提供了重要的背景：并行生成范式之间的竞争可能比想象中更加open，sampler的设计可能是决定性因素。

## 参考

- Deschenaux, J., Gulcehre, C., & Sahoo, S. S. (2026). The Diffusion Duality, Chapter II: Ψ-Samplers and Efficient Curriculum. arXiv:2602.21185.
- 项目页面：https://s-sahoo.com/duo-ch2
- 相关：Sahoo et al. (2025) - Duo: Uniform-State Diffusion
- 相关：Wang et al. (2025) - ReMDM: Predictor-Corrector for MDMs

---

*发布时间：2026-02-25*  
*基于arXiv最新论文整理，持续跟踪离散扩散领域进展*
