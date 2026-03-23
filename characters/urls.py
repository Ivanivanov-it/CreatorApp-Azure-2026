from django.urls import path, include

from characters.views import  LandingPageView, CharacterDeleteView, CharacterDetailView, \
    CreateCharacterView, EditCharacterView, CharactersListView

app_name = 'characters'

urlpatterns = [
    path('',LandingPageView.as_view(),name='home'),
    path('characters/',include([
        path('',CharactersListView.as_view(),name='characters_list'),
        path('<int:pk>/', include ([
            path('',CharacterDetailView.as_view(),name='character_detail'),
        path('edit/',EditCharacterView.as_view(),name='edit_character'),
        path('delete/',CharacterDeleteView.as_view(),name='delete_character')
        ])),
        path('create/',CreateCharacterView.as_view(),name='create_character')
    ]))
]