from django.db import models

class CharacterType(models.TextChoices):
    ALIEN = 'ALIEN', 'ALIEN'
    HERO = 'HERO', 'HERO'
    GOD = 'GOD', 'GOD',
    DEMON = 'DEMON', 'DEMON'
    TIME_TRAVELER = 'TIME TRAVELER', 'TIME TRAVELER'
    VILLAIN = 'VILLAIN', 'VILLAIN'
    ANGEL = 'ANGEL', 'ANGEL'
    OTHER = 'OTHER', 'OTHER'

class BattleStatus(models.TextChoices):
    active = 'Active', 'Active'
    inactive = 'Inactive', 'Inactive'
    finished = 'Finished', 'Finished'

class LogType(models.TextChoices):
    INFO = 'INFO', 'INFO'
    ATTACK = 'ATTACK', 'ATTACK'
    DEFEND = 'DEFEND', 'DEFEND'
    HEAL = 'HEAL', 'HEAL'
    SEARCH = 'SEARCH', 'SEARCH'