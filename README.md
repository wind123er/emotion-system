# Emotion Engine

> A production-ready emotion system for AI characters.
> 8 base emotions, time-aware decay, mixed-emotion synthesis.
> YAML-configured, Python-powered.

---

## Features

- **8 Base Emotions**: Joy, Security, Affection, Longing, Worry, Loneliness, Frustration, Sadness
- **Time-Aware Decay**: Emotions decay at different rates when user is absent
- **Event-Driven Triggers**: Map user actions to emotional responses
- **Mixed Emotion Synthesis**: Multiple high emotions combine into nuanced expressions
- **Time Context**: Day/night/work/special-day emotional rules
- **Python Engine**: Ready-to-use EmotionEngine class
- **OpenClaw Compat**: Optional SKILL.md for OpenClaw deployments

## Quick Start

```bash
pip install pyyaml
```

```python
from emotion_engine import EmotionEngine
ai = EmotionEngine('./config/')
ai.process_event('user_says_hello')
print(ai.get_expression_style())
```

## Structure

```
EmotionEngine/
├── emotion_engine.py    # Python engine
├── SKILL.md             # OpenClaw compat mode
├── config/              # YAML configuration (edit these)
├── examples/
│   └── default_config/  # Ready-to-use default
└── LICENSE
```

## License: MIT
