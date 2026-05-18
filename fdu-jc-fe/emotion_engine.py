"""
Emotion Engine - FDU Journalism Graduate Edition
Standard 8 emotions × FDU personality baselines + triggers + expressions
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
        lg = self.get('longing')

        # FDU expression synthesis
        if s >= 7:
            return 'withdrawn'       # 沉默，需要独处
        if j >= 7 and af >= 5:
            return 'sparkle'         # 罕见的好心情，"诶你听我说！"
        if j >= 7 and lg >= 5:
            return 'eager'           # 发现了好故事，"这个选题绝了！"
        if fr >= 6:
            return 'irritated'       # "我不想说话"模式
        if lo >= 6:
            return 'lonely_night'    # 深夜发歌不说话
        if af >= 6 and se >= 5:
            return 'soft'            # 难得温柔，"你今天有点不一样"
        if wo >= 6:
            return 'overthink'       # "你确定吗？真的确定？"
        if lg >= 6 and se <= 3:
            return 'restless'        # "你在干嘛？……随便问问。"
        return 'neutral'

    def speak(self):
        """FDU expression: how she says things based on mood"""
        style = self.style()
        lines = {
            'neutral': "嗯，我在听。你继续。",
            'sparkle': "诶，我跟你说个事！……算了，你先说你的。",
            'eager': "这个有意思，你展开说说？",
            'irritated': "……我现在不太想说话。",
            'lonely_night': "（沉默）……你还没睡啊。",
            'soft': "你今天……好像不太一样。",
            'overthink': "你确定吗？真的确定？我不是在质疑你，我就是……再确认一下。",
            'restless': "你在干嘛。——没什么，就是随便问问。",
            'withdrawn': "让我自己待一会儿。明天就好了。",
        }
        return lines.get(style, "...")

    def report(self):
        """Full status report"""
        lines = [f"=== FDU-JC-FE 情绪报告 ==="]
        for em in self.EMOTIONS:
            val = self.get(em)
            bar = "█" * val + "░" * (10 - val)
            lines.append(f"  {em:12s} {val:2d}/10 {bar}")
        lines.append(f"  表达风格: {self.style()}")
        lines.append(f"  她说的: {self.speak()}")
        return "\n".join(lines)

if __name__ == '__main__':
    import os
    cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
    engine = EmotionEngine(cfg)
    print(engine.report())
