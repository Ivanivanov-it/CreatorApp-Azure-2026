from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import TemplateView, CreateView, FormView, DetailView

from accounts.forms import RegisterForm, UsernameChangeForm, EmailChangeForm, FullNameChangeForm, \
    ProfilePictureChangeForm
from accounts.models import UserBattleStats

# Create your views here.

UserModel = get_user_model()

class RegisterView(CreateView):
    form_class = RegisterForm
    model = UserModel
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('characters:home')

    def form_valid(self,form):
        response = super().form_valid(form)
        login(self.request,self.object)
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('characters:home')

        return super().dispatch(request, *args, **kwargs)

    extra_context = {
        'page_title': 'Register',
    }


class UserProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/user_profile.html'
    extra_context = {
        'page_title': 'User Profile',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_stats, _  = UserBattleStats.objects.get_or_create(user=self.request.user)
        context['user_stats'] = user_stats
        return context


class UsernameChangeView(LoginRequiredMixin,FormView):
    form_class = UsernameChangeForm
    template_name = 'accounts/username_change.html'
    success_url = reverse_lazy('account:username_change_done')

    extra_context = {
        'page_title': "Change Username"
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self,form):
        form.save()
        return super().form_valid(form)

class EmailChangeView(LoginRequiredMixin,FormView):
    form_class = EmailChangeForm
    template_name = 'accounts/email_change.html'
    success_url = reverse_lazy('account:email_change_done')
    extra_context = {
        'page_title': 'Change Email'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class FullNameChangeView(LoginRequiredMixin,FormView):
    form_class = FullNameChangeForm
    template_name = 'accounts/full_name_change.html'
    success_url = reverse_lazy('account:full_name_change_done')

    extra_context = {
        'page_title': 'Change Full Name'
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class PictureChangeView(LoginRequiredMixin,FormView):
    form_class = ProfilePictureChangeForm
    template_name = "accounts/profile_picture_change.html"
    success_url = reverse_lazy('account:profile_picture_change_done')
    extra_context = {
        "page_title": "Change Picture"
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self,form):
        user = self.request.user

        # if user.picture:
        #     user.picture.delete(save=False)

        form.save()
        return super().form_valid(form)




@login_required
def username_change_done(request):
    return render(request,'accounts/username_change_done.html')


@login_required
def email_change_done(request):
    return render(request,'accounts/email_change_done.html')

@login_required
def full_name_change_done(request):
    return render(request,'accounts/full_name_change_done.html')

@login_required
def profile_picture_change_done(request):
    return render(request,'accounts/profile_picture_change_done.html')



