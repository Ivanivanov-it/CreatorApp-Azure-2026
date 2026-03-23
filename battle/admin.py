from django.contrib import admin

from battle.models import BattleCharacter, BattleEnemy


# Register your models here.

@admin.register(BattleCharacter)
class BattleCharacterAdmin(admin.ModelAdmin):
    list_display = ["character_id","battle_id","base_hp","base_atk","base_def","buff_hp","buff_atk","buff_def","debuff_hp","debuff_atk","debuff_def","current_hp"]

@admin.register(BattleEnemy)
class BattleEnemyAdmin(admin.ModelAdmin):
    list_display = ["enemy_id", "battle_id", "base_hp", "base_atk", "base_def", "buff_hp", "buff_atk", "buff_def",
                    "debuff_hp", "debuff_atk", "debuff_def", "current_hp"]
