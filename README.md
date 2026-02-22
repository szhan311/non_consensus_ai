# Non-Consensus AI

High-quality technical analysis of AI/ML research and systems. Long-form blog posts examining the gap between claims and evidence.

## Project Structure

```
non_consensus_ai/
├── content/          # Generated blog posts (markdown)
├── drafts/           # Draft posts before publication
├── scripts/          # Automation scripts
│   └── auto_publisher.py   # Main blog generator
└── docs/             # Documentation and references
```

## Content Style

Inspired by: **Simon Willison**, **Gwern**, **Dan Luu**, **Andrej Karpathy**

### Key Characteristics

- **Long-form analysis** (1500-3000 words)
- **Technical depth** with specific evidence
- **Structured sections**:
  - Introduction (context and motivation)
  - Surface Narrative (common claims)
  - What Evidence Shows (contradictory findings)
  - Technical Deep-Dive (implementation details)
  - Implications (practical consequences)
  - Verifiable Predictions (falsifiable claims with timelines)
  - Related Work (context and counter-arguments)
  - Conclusion
- **Citation-heavy**: References to actual papers, systems, and benchmarks
- **Neutral tone**: No marketing language, no emoji
- **Falsifiable predictions**: Specific claims with verification criteria

## Topic Categories

1. **Architecture**: Transformers, State Space Models, MoE, Attention mechanisms
2. **Training**: Scaling Laws, Synthetic Data, RLHF, Distillation
3. **Inference**: Speculative Decoding, KV Cache, Batching, Cost optimization
4. **Evaluation**: Benchmark Contamination, Capability Overhang, Emergence
5. **Systems**: Distributed training, Serving infrastructure, Hardware
6. **Safety**: Alignment limitations, Jailbreak robustness, Monitoring
7. **Applications**: Code generation, Reasoning, Long context, Scientific discovery

## Generation Process

```bash
cd ~/Desktop/non_consensus_ai
python3 scripts/auto_publisher.py
```

The generator:
1. Selects a topic category and subtopic
2. Generates a full blog post with all sections
3. Saves to `content/` with date-prefixed filename
4. Updates README index
5. Commits and pushes to GitHub

## Publishing Schedule

- **Frequency**: Every 10 minutes (configurable)
- **Quality over quantity**: Each post is substantial technical analysis
- **No duplicates**: Tracks published topics to avoid repetition

## Example Output

```markdown
---
title: "Speculative Decoding: A Deeper Look at the Claims"
date: 2026-02-22
category: Inference
subtopic: Speculative Decoding
slug: speculative-decoding-a-deeper-look-at-the-claims
---

# Speculative Decoding: A Deeper Look at the Claims

*Published: 2026-02-22 | Category: Inference*

## Introduction

I've been following developments in Speculative Decoding closely over the past few months...

## The Surface Narrative

The standard claim is that speculative decoding provides nearly 'free' speedups of 2-3x...

## What the Evidence Actually Shows

**The speedup claims require important caveats:**

**Draft Model Quality Dependency**: Speedups are highly sensitive to draft model acceptance rates...

[Additional sections: Technical Deep-Dive, Implications, Verifiable Predictions, Related Work, Conclusion]

---

*This analysis is based on publicly available research and system evaluations. Corrections and counter-arguments are welcome.*

**Tags:** #Inference #SpeculativeDecoding #DeepDive
```

## GitHub Repository

**URL**: https://github.com/szhan311/non_consensus_ai

All posts are automatically committed and pushed to this repository.

## Content Quality

### Standards

- ✅ **Evidence-based**: Specific papers, systems, benchmarks cited
- ✅ **Technical depth**: Implementation details and system constraints
- ✅ **Nuanced**: Acknowledges complexity and counter-arguments
- ✅ **Falsifiable**: Predictions include verification criteria
- ✅ **Reference-rich**: Links to original sources

### Avoid

- ❌ Surface-level summaries
- ❌ Unsubstantiated claims
- ❌ Marketing language
- ❌ Emoji or clickbait formatting
- ❌ Generic advice without context

## Inspiration and References

### Writers
- **Simon Willison**: [simonwillison.net](https://simonwillison.net) - Deep dives into LLM capabilities
- **Gwern**: [gwern.net](https://www.gwern.net) - Long-form analysis with extensive citations
- **Dan Luu**: [danluu.com](https://danluu.com) - Systems performance and engineering
- **Andrej Karpathy**: [karpathy.ai](https://karpathy.ai) - Technical explanations

### Topics
- ** distill.pub**: Clear explanations of ML concepts
- **The Gradient**: Accessible technical perspectives
- **Alignment Forum**: Technical AI safety research

## Automation

The project uses cron for automatic publishing:

```bash
# Check current cron jobs
cron list

# Publishing runs every 10 minutes
# Job: non_consensus_ai_publisher
```

## Manual Workflow

If you want to review before publishing:

```bash
# Generate draft (saves to drafts/)
python3 scripts/generate_draft.py

# Review and edit
vim drafts/YYYY-MM-DD_title.md

# Publish manually
python3 scripts/publish_draft.py drafts/YYYY-MM-DD_title.md
```

## Future Improvements

- [ ] Add RSS feed generation
- [ ] Implement comment system via GitHub Issues
- [ ] Add search functionality
- [ ] Create tag-based navigation
- [ ] Add reading time estimates

---

**Project Goal**: Create a repository of high-quality technical analysis that stands up to scrutiny and remains useful over time.

## Content Index
- [20260222] [The Hidden Complexity of Attention Mechanisms](content/20260222_the-hidden-complexity-of-attention-mechanisms.md)
