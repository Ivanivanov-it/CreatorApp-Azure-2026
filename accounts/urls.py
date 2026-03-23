
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from accounts.views import RegisterView, UserProfileView, UsernameChangeView, username_change_done, EmailChangeView, \
    email_change_done, FullNameChangeView, full_name_change_done, PictureChangeView, profile_picture_change_done

app_name = 'account'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('register/', RegisterView.as_view(),name='register'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('password-change/', PasswordChangeView.as_view(
        template_name='accounts/password-change.html',
        success_url=reverse_lazy('account:password_change_done')),
        name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='accounts/password-change-done.html'),name='password_change_done'),
    path('username_change/' , UsernameChangeView.as_view(),name='username_change'),
    path('username_change_done/',username_change_done,name='username_change_done'),
path('email_change/' , EmailChangeView.as_view(),name='email_change'),
    path('email_change_done/',email_change_done,name='email_change_done'),
path('full_name_change/' , FullNameChangeView.as_view(),name='full_name_change'),
    path('full_name_change_done/',full_name_change_done,name='full_name_change_done'),
path('profile_picture_change/' , PictureChangeView.as_view(),name='profile_picture_change'),
    path('profile_picture_change_done/',profile_picture_change_done,name='profile_picture_change_done'),
]