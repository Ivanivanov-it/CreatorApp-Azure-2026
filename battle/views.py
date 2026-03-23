from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from accounts.models import UserBattleStats
from battle.models import Battle, BattleCharacter, BattleEnemy, BattleLog
from battle.stat_calc_functions import calc_buff_atk, calc_buff_def, calc_buff_hp, calc_debuff_atk, calc_debuff_hp, \
    calc_debuff_def
from characters.forms import CharacterSearchForm
from characters.models import Character
from common.choices import BattleStatus
from enemies.forms import EnemySearchForm
from enemies.models import Enemy
from partners.models import Partner


class CharacterSelectionView(LoginRequiredMixin,ListView):
    model = Character
    template_name = "battle/select_character.html"
    context_object_name = 'characters'
    paginate_by = 9
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_form = CharacterSearchForm(self.request.GET or None)

        if 'query' in self.request.GET and self.search_form.is_valid():
            query = self.search_form.cleaned_data['query']

            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        context['page_title'] = "Character Selection"

        return context

    def post(self,request,*args,**kwargs):
        character_id = request.POST.get("character_id")
        request.session["character_id"] = character_id

        return redirect("battle:partner_selection")


class PartnerSelectionView(LoginRequiredMixin,ListView):
    template_name = "battle/select_partner.html"
    context_object_name = 'partners'
    paginate_by = 9
    ordering = ['name']

    def dispatch(self,request,*args,**kwargs):
        if not request.session.get("character_id"):
            return redirect("battle:character_selection")
        return super().dispatch(request,*args,**kwargs)

    def get_queryset(self):
        return Partner.objects.filter(character_id=self.request.session["character_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Partner Selection"
        return context

    def post(self,request,*args,**kwargs):
        partner_id = request.POST.get("partner_id")
        request.session["partner_id"] = partner_id
        return redirect("battle:enemy_selection")

class EnemySelectionView(LoginRequiredMixin,ListView):
    model = Enemy
    template_name = "battle/select_enemy.html"
    context_object_name = 'enemies'
    paginate_by = 9
    ordering = ['name']

    def dispatch(self,request,*args,**kwargs):
        if not request.session.get("character_id"):
            return redirect("battle:character_selection")
        return super().dispatch(request,*args,**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_form = EnemySearchForm(self.request.GET or None)

        if 'query' in self.request.GET and self.search_form.is_valid():
            query = self.search_form.cleaned_data['query']

            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Enemy Selection"
        return context

    def post(self,request,*args,**kwargs):
        enemy_id = request.POST.get("enemy_id")
        request.session["enemy_id"] = enemy_id
        return redirect("battle:create_battle")


class CreateBattleView(LoginRequiredMixin,View):

    def dispatch(self, request, *args, **kwargs):
        character_id = request.session.get("character_id")
        enemy_id = request.session.get("enemy_id")

        if not character_id or not enemy_id:
            return redirect("battle:character_selection")

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        character_id = request.session.get("character_id")
        partner_id = request.session.get("partner_id", [])
        enemy_id = request.session.get("enemy_id")

        character = Character.objects.get(id=character_id)
        enemy = Enemy.objects.get(id=enemy_id)
        partner = Partner.objects.get(id=partner_id) if partner_id else None

        battle = Battle.objects.create()

        BattleCharacter.objects.create(
            battle=battle,
            character=character,
            base_hp=character.hp,
            base_atk=character.attack,
            base_def=character.defense,
            buff_hp=calc_buff_hp(character) + (partner.hp if partner_id else 0),
            buff_atk=calc_buff_atk(character) + (partner.attack if partner_id else 0),
            buff_def=calc_buff_def(character) + (partner.defense if partner_id else 0),
        )

        BattleEnemy.objects.create(
            battle=battle,
            enemy=enemy,
            base_hp=enemy.hp,
            base_atk=enemy.attack,
            base_def=enemy.defense,
            buff_hp=calc_buff_hp(enemy),
            buff_atk=calc_buff_atk(enemy),
            buff_def=calc_buff_def(enemy),
            debuff_hp=calc_debuff_hp(enemy, character),
            debuff_atk=calc_debuff_atk(enemy, character),
            debuff_def=calc_debuff_def(enemy, character)
        )

        return redirect("battle:battle_view", pk=battle.id)


class BattleView(LoginRequiredMixin,DetailView):
    template_name = "battle/battle.html"
    model = Battle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        battle = self.object

        context['character'] = battle.battlecharacter_set.first()
        context['enemy'] = battle.battleenemy_set.first()
        context['logs'] = BattleLog.objects.filter(battle=battle).all()

        return context

    def post(self,request,*args,**kwargs):
        battle = self.get_object()
        character = battle.battlecharacter_set.first()
        enemy = battle.battleenemy_set.first()

        turn = battle.turns

        if turn % 2 == 1:
            enemy.take_damage(character.total_atk, battle=battle)

        else:
            character.take_damage(enemy.total_atk, battle=battle)

        if not enemy.is_alive or not character.is_alive:

            user_stats, _ = UserBattleStats.objects.get_or_create(user=request.user)

            if character.is_alive:
                user_stats.add_win()
            else:
                user_stats.add_loss()

            battle.status = BattleStatus.finished
            battle.save(update_fields=['status'])

        if not battle.status == BattleStatus.finished:
            turn += 1

        battle.turns = turn
        battle.save()

        logs = BattleLog.objects.filter(battle=battle).all()

        context = {
            "battle": battle,
            "character": character,
            "enemy": enemy,
            "logs": logs
        }

        return render(request, self.template_name, context=context)








