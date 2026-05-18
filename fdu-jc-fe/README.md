# Emotion Engine — FDU-JC-FE

> 复旦大学新闻学院女研究生情绪系统
> Fudan University · School of Journalism · Female Graduate
> Standard 8-core emotion engine × FDU personality profile

---

## 架构

```
EmotionEngine-FDU/
├── emotion_engine.py     # Python引擎
├── config/
│   ├── emotions.yaml     # 标准8情绪 + FDU基线/衰减
│   ├── triggers.yaml     # 事件触发规则（含人格倍数）
│   ├── personality.yaml  # 人格画像配置
│   └── mood_state.yaml   # 当前情绪状态（自动更新）
├── LICENSE
└── README.md
```

## 8种基础情绪

与BMU-FE相同的8种标准情绪，基线根据复旦新闻学院女研究生人格调整：

| 情绪 | 基线 | 衰减 | FDU特色 |
|:----|:---:|:----|:--------|
| Joy | 2 | 慢 | 不容易嗨，发现好故事时飙升 |
| Security | 4 | 中 | 独立但不孤僻 |
| Affection | 3 | 慢 | 嘴硬，心事藏得深 |
| Longing | 5 | 慢 | 总在追寻，记者天性 |
| Worry | 4 | 中 | 对社会敏感，职业警觉 |
| Loneliness | 3 | 慢 | 习惯独处，但深夜最明显 |
| Frustration | 3 | 快 | 容易烦但忘得快 |
| Sadness | 2 | 中 | 不容易被击垮 |

## 人格影响

- **触发倍数**：同一事件对不同人格的情绪影响幅度不同（如"套话"触发FDU沮丧×1.5）
- **基线偏移**：人格决定了情绪的自然状态（如新闻学院女生worry基线4，比标准高）
- **表达风格**：高共情力×高独立性 → 表达风格含蓄但锐利

## 快速开始

```bash
pip install pyyaml
python emotion_engine.py
```

MIT License
