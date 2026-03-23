from django.urls import path, include

from enemies.views import  EnemyDeleteView, EnemiesListView, EnemyDetailView, CreateEnemyView, EditEnemyView

app_name = 'enemies'

urlpatterns = [
    path('', EnemiesListView.as_view(), name='enemies_list'),
    path('<int:pk>/', include([
        path('', EnemyDetailView.as_view(), name='enemy_detail'),
        path('edit/', EditEnemyView.as_view(), name='edit_enemy'),
        path('delete/', EnemyDeleteView.as_view(), name='delete_enemy'),
    ])),
    path('create/', CreateEnemyView.as_view(), name='create_enemy')
]
