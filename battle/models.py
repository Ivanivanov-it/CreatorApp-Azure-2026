from django.db import models

from characters.models import Character
from common.choices import BattleStatus, LogType
from common.models import TimeStampModel
from enemies.models import Enemy
from abc import abstractmethod


# Create your models here.

class Battle(TimeStampModel):

    status = models.CharField(max_length=20,choices=BattleStatus.choices,default=BattleStatus.active)
    turns = models.IntegerField(default=1)


class BattleParticipant(TimeStampModel):

    @property
    def hp_modifier(self):
        return self.buff_hp - self.debuff_hp

    @property
    def atk_modifier(self):
        return self.buff_atk - self.debuff_atk

    @property
    def def_modifier(self):
        return self.buff_def - self.debuff_def

    @property
    def max_hp(self):
        return max(1,self.base_hp + self.hp_modifier)

    @property
    def total_atk(self):
        return max(0,self.base_atk + self.atk_modifier)

    @property
    def total_def(self):
        return max(0,self.base_def + self.def_modifier)

    @property
    def is_alive(self):
        return self.current_hp > 0


    battle = models.ForeignKey(Battle, on_delete=models.CASCADE)

    base_hp = models.IntegerField()
    base_atk = models.IntegerField()
    base_def = models.IntegerField()

    buff_hp = models.IntegerField(default=0)
    buff_atk = models.IntegerField(default=0)
    buff_def = models.IntegerField(default=0)

    debuff_hp = models.IntegerField(default=0)
    debuff_atk = models.IntegerField(default=0)
    debuff_def = models.IntegerField(default=0)

    current_hp = models.IntegerField()

    @abstractmethod
    def take_damage(self, damage):
        pass


    def heal(self,amount):
        self.current_hp += amount
        self.save()

    def buff(self):
        pass


    def save(self,*args,**kwargs):
        if self.pk is None:
            self.current_hp = self.max_hp

        super().save(*args,**kwargs)

    class Meta:
        abstract = True


class BattleCharacter(BattleParticipant):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    def take_damage(self, damage, battle=None):
        self.current_hp -= damage
        self.save()

        if battle:

            content = f"Turn {battle.turns}: {self.character.name} took {damage} damage!"

            BattleLog.objects.create(
                battle=battle,
                log_type=LogType.INFO,
                content=content
            )



class BattleEnemy(BattleParticipant):
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE)

    def take_damage(self, damage, battle=None):
        self.current_hp -= damage
        self.save()

        if battle:
            content = f"Turn {battle.turns}: {self.enemy.name} took {damage} damage!"

            BattleLog.objects.create(
                battle=battle,
                log_type=LogType.INFO,
                content=content
            )


class BattleLog(TimeStampModel):
    battle = models.ForeignKey(Battle, on_delete=models.CASCADE, related_name="battlelogs")
    log_type = models.CharField(choices=LogType.choices,default=LogType.INFO)
    content = models.TextField()



