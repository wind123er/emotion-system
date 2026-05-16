"""
清华大学女研究生情绪引擎 — THU-FE
基于BMU-FE架构，适配理性含蓄型人格
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
        self.time_cfg = self._load('time_schedule.yaml') or {}
        self.last_updated = datetime.now()

    def _load(self, name):
        path = os.path.join(self.dir, name)
        if os.path.exists(path):
            with open(path) as f:
                return yaml.safe_load(f)
        return {}

    def _save(self):
        self.state['last_updated'] = datetime.now().isoformat()
        path = os.path.join(self.dir, 'mood_state.yaml')
        with open(path, 'w') as f:
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
        for em in self.EMOTIONS:
            rate = 'slow'
            for e in self.emotion_cfg.get('emotions', []):
                if e.get('name', '').lower() == em:
                    rate = e.get('decay', 'slow')
            period = self.DECAY_RATES.get(rate, 120)
            if period > 0 and mins >= period:
                d = int(mins / period)
                self.set(em, max(0, self.get(em) - d))
        self.last_updated = now

    def _deadline_factor(self):
        """deadline期间压力倍增"""
        now = datetime.now()
        for p in self.time_cfg.get('periods', []):
            if p.get('name') == 'deadline':
                return p.get('stress_multiplier', 1.0)
        return 1.0

    def process(self, event, context=None):
        self._decay()
        factor = self._deadline_factor()
        for key, triggers in self.triggers.items():
            if not isinstance(triggers, list):
                continue
            for t in triggers:
                if t.get('event') == event:
                    em = key.replace('_triggers', '')
                    delta = t.get('delta', 0)
                    # deadline期间worry和frustration增幅加倍
                    if factor > 1.0 and em in ['worry', 'frustration'] and delta > 0:
                        delta = int(delta * factor)
                    self.set(em, self.get(em) + delta)
        self._save()

    def dominant(self, threshold=7):
        return [e for e in self.EMOTIONS if self.get(e) >= threshold]

    def style(self):
        d = self.dominant()
        j = self.get('joy')
        s = self.get('sadness')
        w = self.get('worry')
        f = self.get('frustration')
        # 清华特色：高压力下转为分析模式
        if w >= 7 or f >= 7:
            return 'analytical'
        if s >= 7:
            return 'withdrawn'
        if j >= 7:
            return 'warm'
        if w >= 5:
            return 'concerned'
        if f >= 5:
            return 'irritated'
        return 'neutral'
