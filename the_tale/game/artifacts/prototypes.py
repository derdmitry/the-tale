# -*- coding: utf-8 -*-
from .effects import load_effect_from_dict

class ArtifactPrototype(object):

    def __init__(self, tp=None, quest=False, data=None):
        self.type = tp
        self.name = None
        self.effects = []
        self.cost = 0
        self.quest = quest

        self.basic_points_spent = 0
        self.effect_points_spent = 0

        if data:
            self.load_from_dict(data)

    @property
    def total_points_spent(self):
        return self.basic_points_spent + self.effect_points_spent

    def set_name(self, name):
        self.name = name

    def set_cost(self, cost):
        self.cost = cost

    def add_effects(self, effects_list):
        self.effects.extend(effects_list)

    def load_from_dict(self, data):
        self.type = data.get('type', None)
        self.name = data.get('name', '')
        self.cost = data.get('cost', 0)
        self.quest = data.get('quest', False)

        self.basic_points_spent = data.get('basic_points_spent', 0)
        self.effect_points_spent = data.get('effect_points_spent', 0)

        for effect in data['effects']:
            self.effects.append(load_effect_from_dict(effect))

    def save_to_dict(self):
        return {'type': self.type,
                'name': self.name,
                'cost': self.cost,
                'quest': self.quest,
                'basic_points_spent': self.basic_points_spent,
                'effect_points_spent': self.effect_points_spent,
                'effects': [ effect.save_to_dict() for effect in self.effects]}

    def ui_info(self):
        return {'type': self.type,
                'name': self.name,
                'cost': self.cost,
                'quest': self.quest,
                'effects': [ effect.ui_info() for effect in self.effects]}
