# 产品化的现实检验：Innate Immunity

*基于：[Innate Immunity](https://www.lesswrong.com/posts/FtyCrmrEAhrhuwjaB/innate-immunity)*

## 从Demo到Product的距离

Published on February 23, 2026 5:00 AM GMT<br/><br/><p><i>Summary: I've been reading Parham's Immunology, and have learned a lot of things that I think people here would enjoy hearing about. So, I'm t

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

- 本文受Innate Immunity启发
- 相关商业分析：[One Useful Thing](https://www.oneusefulthing.org/)

---

*最后更新：2026-02-23*
