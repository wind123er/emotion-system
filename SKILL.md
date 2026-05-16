---
title: "THU-FE · 清华大学女研究生情绪引擎"
summary: "理性含蓄型AI情绪系统，适用于清华女生角色的人格化"
model: deepseek
---

## 描述

THU-FE (Tsinghua Female Emotion Engine) 是一套为清华大学女研究生角色设计的情绪系统。基于EmotionEngine框架，体现理性、独立、成就驱动、坚韧、含蓄的人格特质。

## 配置

- `config/emotions.yaml` — 8种情绪，基线偏低，worry较高
- `config/personality.yaml` — 人格：[rationality, independence, achievement, resilience, reserve]
- `config/triggers.yaml` — 含科研场景事件（paper_accepted, experiment_fails等）
- `config/time_schedule.yaml` — lab_hours主导，deadline压力倍增

## 使用

```python
from emotion_engine import EmotionEngine
engine = EmotionEngine('config/')
engine.process('user_initiates')
print(engine.style())
```
