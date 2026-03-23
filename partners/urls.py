from django.urls import path, include

from partners.views import PartnerDeleteView, PartnersListView, PartnerDetailView, PartnerCreateView, EditPartnerView

app_name = 'partners'

urlpatterns = [
    path('', PartnersListView.as_view(), name='partners_list'),
    path('<int:pk>/', include([
        path('', PartnerDetailView.as_view(), name='partner_detail'),
        path('edit/', EditPartnerView.as_view(), name='edit_partner'),
        path('delete/', PartnerDeleteView.as_view(), name='delete_partner'),
    ])),
    path('create/', PartnerCreateView.as_view(), name='create_partner')
]
