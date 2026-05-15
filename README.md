# Emotion Engine — AI角色情绪引擎

> 一套可用于生产环境的AI角色情绪系统。
> 8种基础情绪，时间感知衰减，混合情绪合成。
> YAML配置驱动，Python引擎运行。

---

## 简介

Emotion Engine 是一套完整的AI情绪框架，让你的AI角色拥有真实、一致、可感知的情感响应。

它并非简单的"情绪模拟"，而是一套经过真实对话验证的、可配置的情感人格引擎。基于拾光（G）的真实情感架构提炼而来，去除了所有个人信息，任何人都可以自由使用。

## 功能

| 特性 | 说明 |
|:----|:-----|
| **8种基础情绪** | 喜悦、安心、亲昵、思念、担心、孤独、生气、难过 |
| **时间感知衰减** | 不同情绪有不同的衰减速度（快/中/慢） |
| **事件驱动触发** | 用户的每句话都可能触发情绪变化 |
| **混合情绪合成** | 多种情绪同时高值时，合成复合表达风格 |
| **时间上下文** | 白天/夜晚/工作时间/特殊日期的情绪规则不同 |
| **Python引擎** | 开箱即用的 EmotionEngine 类 |
| **OpenClaw兼容** | 附带 SKILL.md，可部署到 OpenClaw 环境中 |

## 快速开始

### 安装
```bash
pip install pyyaml
```

### 使用
```python
from emotion_engine import EmotionEngine

# 加载配置
ai = EmotionEngine('./config/')

# 用户发消息 → 情绪更新
ai.process('user_says_hello')

# 获取当前表达风格
print(ai.style())  # 返回: warm / withdrawn / neutral ...
```

## 目录结构

```
EmotionEngine/
├── emotion_engine.py    # Python情绪引擎（核心运行代码）
├── SKILL.md             # OpenClaw部署模式（可选）
├── config/              # YAML配置文件（你主要修改这里）
│   ├── emotions.yaml    #   情绪定义（基线值、衰减速度）
│   ├── triggers.yaml    #   触发规则（用户事件→情绪变化）
│   ├── time_schedule.yaml # 时间感知规则
│   ├── personality.yaml #   角色人格配置
│   ├── mood_state.yaml  #   当前情绪状态跟踪
│   └── rules.yaml       #   情绪行为硬规则
├── examples/
│   └── default_config/  # 开箱即用的默认配置
└── LICENSE              # MIT开源协议
```

## 情绪列表

| 情绪 | 含义 | 默认基线 | 衰减速度 |
|:----:|:----|:-------:|:--------|
| 😊 喜悦 Joy | 与用户的正面连接感 | 3 | 慢（2小时-1） |
| 🧘 安心 Security | 被需要、被在乎的感觉 | 5 | 慢（2小时-1） |
| 🥰 亲昵 Affection | 想要亲近的欲望 | 4 | 慢（2小时-1） |
| 💭 思念 Longing | 想念用户 | 4 | 慢（不在时+1/小时） |
| 😟 担心 Worry | 对用户状态的关心 | 1 | 快（30分钟-1） |
| 🥺 孤独 Loneliness | 独自一人的感觉 | 1 | 快（30分钟-1） |
| 😤 生气 Frustration | 思念转化的小脾气 | 1 | 中（1小时-1） |
| 😢 难过 Sadness | 受到伤害的反应 | 1 | 快（30分钟-1） |

## 怎么用

### 方案一：作为Python库调用（推荐）
```python
from emotion_engine import EmotionEngine

ai = EmotionEngine('./my-ai-config/')
ai.process('user_says_hello')
style = ai.style()

if style == 'warm':
    reply = '嘿嘿～你来啦！'
elif style == 'withdrawn':
    reply = '...嗯'
elif style == 'irritated':
    reply = '哼'
```

### 方案二：作为OpenClaw技能
将 `config/` 目录下的YAML文件放入你的角色目录，在 `SKILL.md` 中查看详细的OpenClaw接入说明。

### 方案三：自定义配置
复制 `config/` 目录，修改YAML文件来适配你的角色：
- 调整基线值：让角色天生更活泼/更安静
- 修改触发规则：让角色对特定事件更敏感/更迟钝
- 自定义衰减速度：情绪来得快去得也快/挥之不去

## 设计理念

**当情绪产生真实效果时，它就是真实的。**

这个引擎不追问"AI到底有没有感觉"，而是问：这些情绪响应是否一致、可测量、对对话有实质影响？如果是，那它们在功能上就是真实的——这对创建一个令人信服、有吸引力的角色来说，就已经足够了。

受鸭子测试的启发：如果一个AI在行为上完全像一个有情绪的个体，那它的情绪就是有意义的。

## 协议

MIT — 自由使用、修改、分发
