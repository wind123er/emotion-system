"""
Emotion Engine - AI Character Emotion System
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
        d = self.dominant()
        j = self.get('joy')
        s = self.get('sadness')
        if s >= 7:
            return 'withdrawn'
        if j >= 7:
            return 'warm'
        if self.get('worry') >= 5:
            return 'concerned'
        if self.get('frustration') >= 5:
            return 'irritated'
        return 'neutral