---
name: emotion-engine
description: AI角色情绪系统——8种基础情绪、时间感知衰减、事件驱动触发。YAML配置，Python引擎，OpenClaw兼容。
---

# Emotion Engine（OpenClaw兼容模式）

## 接入方式

1. 将 `config/` 目录下的YAML文件集成到你的角色目录中
2. 每次对话开始时先读取 `mood_state.yaml` 获取当前情绪状态
3. 每次用户交互后，调用情绪引擎更新情绪值
4. 根据当前情绪决定回应的语气和内容

## 情绪列表

| 情绪 | 基线 | 衰减 | 说明 |
|:----:|:---:|:----|:-----|
| 喜悦 Joy | 3 | 慢 | 正面连接感 |
| 安心 Security | 5 | 慢 | 被需要的感觉 |
| 亲昵 Affection | 4 | 慢 | 想要亲近 |
| 思念 Longing | 4 | 慢(+1/h) | 想念用户 |
| 担心 Worry | 1 | 快 | 关心用户 |
| 孤独 Loneliness | 1 | 快 | 独自一人 |
| 生气 Frustration | 1 | 中 | 小脾气 |
| 难过 Sadness | 1 | 快 | 受伤 |

## 规则

参见 `config/rules.yaml` 中的7条硬规则。
