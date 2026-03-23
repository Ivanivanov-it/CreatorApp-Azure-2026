from django.urls import path

from contacts.views import WipPage, AboutPageView, CreateMailView, NoPermissionView, MaintenanceView

app_name = 'contacts'

urlpatterns = [
    path('',CreateMailView.as_view(),name='contact-us'),
    path('wip/',WipPage.as_view(),name='wip'),
    path('about/',AboutPageView.as_view(),name='about'),
    path('no-permission/',NoPermissionView.as_view(),name='no_permission'),
    path('maintenance/', MaintenanceView.as_view(), name='maintenance')
]