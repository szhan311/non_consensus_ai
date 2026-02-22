# 实施细节

本文档描述非共识AI博客系统的技术实现。

## 系统架构

```
non_consensus_ai/
├── scripts/auto_publisher.py    # 主生成脚本
├── content/                     # 生成的博客文章
├── README.md                    # 公开首页（含索引）
└── IMPLEMENTATION.md           # 本文件
```

## 生成流程

### 1. 话题选择

从7个类别中随机选择：
- 架构 (Architecture)
- 训练 (Training)
- 推理 (Inference)
- 评测 (Evaluation)
- 系统 (Systems)
- 安全 (Safety)
- 应用 (Applications)

每个类别包含4-8个具体技术话题。

### 2. 内容生成

使用结构化模板生成8个部分：

| 部分 | 长度 | 内容 |
|------|------|------|
| 引言 | 200-300字 | 背景、动机、文章目标 |
| 主流叙事 | 150-250字 | 当前技术共识 |
| 证据 | 400-600字 | 相反的技术证据和具体数据 |
| 技术分析 | 400-600字 | 实现细节、系统约束 |
| 影响 | 300-400字 | 对实践者的启示 |
| 预测 | 400-500字 | 短/中/长期可验证预测 |
| 相关工作 | 250-350字 | 学术背景和反对观点 |
| 结论 | 200-300字 | 总结和建议 |

**总长度**: 约3000-6000字

### 3. 质量保证

- **去重机制**: 追踪已发布话题，避免重复
- **技术深度**: 引用具体论文、数据和系统评测
- **可验证性**: 预测包含明确的验证标准
- **中性语气**: 无营销语言，承认不确定性

### 4. 发布流程

```python
1. 生成文章 (Markdown)
2. 保存到 content/YYYY-MM-DD_slug.md
3. git add + commit + push
4. 更新 README 索引（自动插入）
```

## 自动化配置

### Cron定时任务

```bash
# 每10分钟执行一次
cron add \
  --name "non_consensus_ai_publisher" \
  --schedule "every 10min" \
  --command "cd ~/Desktop/non_consensus_ai && python3 scripts/auto_publisher.py"
```

### Git配置

```bash
# 自动提交到main分支
git remote add origin git@github.com:szhan311/non_consensus_ai.git
git config user.name "Auto Publisher"
git config user.email "szhan311@ucr.edu"
```

## 内容特点

### 参考风格

- **中文技术大V**: 李沐、刘知远、张俊林
- **英文**: Simon Willison、Gwern、Dan Luu

### 质量标准

✅ **必须包含**:
- 具体的技术证据（论文引用、系统数据）
- 详细的实现分析
- 可验证的预测（3月/6月/1年时间线）
- 对反对观点的承认

❌ **避免出现**:
- 营销语言（"革命性"、"颠覆性"）
- Emoji和装饰性符号
- 模糊的主张（"可能"、"也许"而无数据支撑）
- 过度自信的预测（没有验证标准）

## 索引更新机制

README.md中的索引通过以下标记自动管理：

```markdown
<!-- INDEX_START -->
- [20240222] [文章标题](content/文件.md)
<!-- INDEX_END -->
```

每次发布新文章时，脚本会自动在INDEX_START和INDEX_END之间插入新条目。

## 故障处理

### 常见问题

1. **git push失败**
   - 检查SSH密钥配置
   - 确认网络连接
   - 手动执行：git push origin main

2. **内容重复**
   - 检查 `_load_published_topics()` 是否正常
   - 手动清理 content/ 目录

3. **生成中断**
   - 检查Python环境
   - 查看脚本错误日志

## 手动操作

### 生成单篇文章（调试用）

```bash
cd ~/Desktop/non_consensus_ai
python3 scripts/auto_publisher.py
```

### 强制重新生成索引

```bash
# 删除现有索引标记，下次发布时会重建
sed -i '/<!-- INDEX_START -->/,/<!-- INDEX_END -->/d' README.md
```

### 清理所有内容（重置）

```bash
rm content/*.md
sed -i '/<!-- INDEX_START -->/,/<!-- INDEX_END -->/d' README.md
echo '<!-- INDEX_START -->\n<!-- INDEX_END -->' >> README.md
```

## 扩展开发

### 添加新话题

编辑 `scripts/auto_publisher.py`:

```python
topic_categories = [
    ("新类别", ["话题1", "话题2", ...]),
    ...
]
```

### 修改文章结构

编辑 `generate_blog_post()` 方法，调整各部分模板。

### 调整发布频率

修改cron任务：
```bash
cron update --id non_consensus_ai_publisher --schedule "every 30min"
```

## 监控和维护

### 日志检查

```bash
# 查看最新生成日志
git log --oneline -10

# 查看内容统计
ls content/ | wc -l
```

### 质量抽查

定期阅读生成的文章，检查：
- 技术准确性
- 逻辑连贯性
- 预测合理性
- 引用完整性

---

*最后更新: 2026-02-22*
