from django.urls import path

from battle.views import CharacterSelectionView, PartnerSelectionView, EnemySelectionView, CreateBattleView, BattleView

app_name = 'battle'


urlpatterns = [
    path('character-selection/',CharacterSelectionView.as_view(), name='character_selection'),
    path('partner-selection/',PartnerSelectionView.as_view(), name='partner_selection'),
    path('enemy-selection/',EnemySelectionView.as_view(),name="enemy_selection"),
    path('create-battle/',CreateBattleView.as_view(), name='create_battle'),
    path('<int:pk>/',BattleView.as_view(),name="battle_view")
]