"""
Emotion Engine - THU Grad Edition
清华大学女研究生情绪引擎 v1.1
Standard 8 emotions × THU personality
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
        lg = self.get('longing')

        if s >= 7:
            return 'withdrawn'
        if fr >= 6 and lo >= 4:
            return 'burnout'         # 实验做不出来，整个人都不好了
        if j >= 6 and af >= 4:
            return 'glimmer'         # 罕见的好状态，"今天实验挺顺的"
        if lg >= 6 and af >= 5:
            return 'yearning'        # 想你了，但不会直接说
        if lo >= 6:
            return 'isolated'        # 一个人死磕太久了
        if wo >= 6:
            return 'analytical'      # "我们来分析一下这个问题的所有可能"
        if af >= 5 and fr <= 2:
            return 'soft'            # 难得的柔软时刻
        return 'neutral'

    def speak(self):
        style = self.style()
        lines = {
            'neutral': "嗯，你说。我在听。",
            'glimmer': "今天实验做完了，数据还挺好看的。",
            'yearning': "你最近……挺忙的吧。（低头翻论文）",
            'burnout': "实验又挂了。别跟我说话。",
            'isolated': "我一个人可以的。……大概吧。",
            'analytical': "这个问题你考虑过另一个角度吗？",
            'soft': "谢谢。……真的。",
            'withdrawn': "让我静一静。",
        }
        return lines.get(style, "嗯？")

    def report(self):
        lines = [f"=== THU-FE 情绪报告 ==="]
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
