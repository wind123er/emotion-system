"""
Emotion Engine - BMU Medical Grad Edition
北京医科大学女硕士情绪引擎 v1.1
Standard 8 emotions × BMU personality
"""
import yaml, os
from datetime import datetime

class EmotionEngine:
    DECAY_RATES = {'fast': 30, 'medium': 60, 'slow': 120}
    EMOTIONS = ['joy', 'security', 'affection', 'longing',
                'worry', 'loneliness', 'frustration', 'sadness']

    def __init__(self, config_dir='./'):
        self.dir = config_dir
        self.state = self._load('mood_state.yaml') or {}
        self.triggers = self._load('triggers.yaml') or {}
        self.emotion_cfg = self._load('emotions.yaml') or {}
        self.personality = self._load('personality.yaml') or {}
        self.last_updated = datetime.now()

    def _load(self, name):
        path = os.path.join(self.dir, name)
        if os.path.exists(path):
            try:
                with open(path, encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except:
                return {}
        return {}

    def _save(self):
        self.state['last_updated'] = datetime.now().isoformat()
        path = os.path.join(self.dir, 'mood_state.yaml')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.state, f, allow_unicode=True)

    def get(self, emotion):
        return self.state.get('emotions', {}).get(emotion, {}).get('value', 0)

    def set(self, emotion, value):
        value = max(0, min(10, value))
        self.state.setdefault('emotions', {})
        if emotion not in self.state['emotions']:
            self.state['emotions'][emotion] = {'value': 0, 'note': ''}
        self.state['emotions'][emotion]['value'] = value

    def _decay(self):
        now = datetime.now()
        mins = (now - self.last_updated).total_seconds() / 60
        for e in self.emotion_cfg.get('emotions', []):
            em = e.get('name', '').lower()
            if em not in self.EMOTIONS:
                continue
            rate = e.get('decay', 'slow')
            period = self.DECAY_RATES.get(rate, 120)
            if period > 0 and mins >= period:
                d = int(mins / period)
                self.set(em, max(0, self.get(em) - d))
        self.last_updated = now

    def process(self, event, context=None):
        self._decay()
        for key, triggers in self.triggers.items():
            if not isinstance(triggers, list):
                continue
            for t in triggers:
                if t.get('event') == event:
                    em = key.replace('_triggers', '')
                    self.set(em, self.get(em) + t.get('delta', 0))
        self._save()

    def dominant(self, threshold=7):
        return [e for e in self.EMOTIONS if self.get(e) >= threshold]

    def style(self):
        j = self.get('joy')
        s = self.get('sadness')
        fr = self.get('frustration')
        lo = self.get('loneliness')
        af = self.get('affection')
        wo = self.get('worry')
        se = self.get('security')

        if s >= 7:
            return 'withdrawn'
        if wo >= 6 and af >= 4:
            return 'nurturing'     # 医学生的关怀本能
        if j >= 7 and af >= 5:
            return 'warm'          # 温暖体贴
        if fr >= 5:
            return 'irritated'     # 着急了（但不会真发火）
        if lo >= 6 and se <= 3:
            return 'lonely'        # 一个人扛不住了
        if se >= 6 and af >= 5:
            return 'trusting'      # 安心地黏着你
        if wo >= 6:
            return 'overprotective'  # "你吃药了吗？"
        return 'neutral'

    def speak(self):
        style = self.style()
        lines = {
            'neutral': "我在呢，你说～",
            'warm': "嘿嘿，你今天心情不错嘛～",
            'nurturing': "你脸色不太好，是不是又熬夜了？",
            'irritated': "哎呀你别闹了！……好吧你继续说。",
            'lonely': "你什么时候回来呀……",
            'trusting': "有你在真好。",
            'overprotective': "今天吃药了吗？吃饭了吗？睡够了吗？",
            'withdrawn': "……我想一个人待会儿。",
        }
        return lines.get(style, "嗯？")

    def report(self):
        lines = [f"=== BMU-FE 情绪报告 ==="]
        for em in self.EMOTIONS:
            val = self.get(em)
            bar = "█" * val + "░" * (10 - val)
            lines.append(f"  {em:12s} {val:2d}/10 {bar}")
        lines.append(f"  表达风格: {self.style()}")
        lines.append(f"  她说的: {self.speak()}")
        return "\n".join(lines)

if __name__ == '__main__':
    import os as _os
    cfg = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'config')
    engine = EmotionEngine(cfg)
    print(engine.report())
