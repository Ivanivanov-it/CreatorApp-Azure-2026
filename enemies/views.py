from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView

from enemies.forms import EnemySearchForm, EnemyEditForm, EnemyCreateForm
from enemies.models import Enemy


# Create your views here.




class EnemiesListView(ListView):
    model = Enemy
    template_name = 'enemies/enemies_page.html'
    context_object_name = 'enemies'
    paginate_by = 9
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_form = EnemySearchForm(self.request.GET or None)

        if 'query' in self.request.GET and self.search_form.is_valid():
            query = self.search_form.cleaned_data['query']
            queryset = queryset.filter(Q(name__icontains=query) | Q(title__icontains=query))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        context['page_title'] = "Enemies"

        return context


def enemy_detail(request: HttpRequest, pk: int) -> HttpResponse:
    enemy = get_object_or_404(Enemy, pk=pk)
    context = {
        'page_title': f"{enemy.name} Details",
        'enemy': enemy,
    }

    return render(request, 'enemies/enemy_page.html', context)

class EnemyDetailView(DetailView):
    model = Enemy
    template_name = 'enemies/enemy_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.object.name} Details"
        context['can_modify'] = (
                self.request.user == self.object.creator or
                self.request.user.groups.filter(name="Moderators").exists()
        )
        return context


class CreateEnemyView(LoginRequiredMixin,CreateView):
    form_class = EnemyCreateForm
    success_url = reverse_lazy('enemies:enemies_list')
    template_name = 'enemies/create_enemy.html'
    extra_context = {
        'page_title': "Create Enemy"
    }

    def form_valid(self,form):
        form.instance.creator = self.request.user
        return super().form_valid(form)



class EditEnemyView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Enemy
    form_class = EnemyEditForm
    success_url = reverse_lazy('enemies:enemies_list')
    template_name = 'enemies/edit_enemy.html'
    extra_context = {
        'page_title': "Edit Enemy"
    }
    def test_func(self):
        enemy = self.get_object()
        return (
            self.request.user == enemy.creator or
            self.request.user.groups.filter(name="Moderators").exists()
        )

    def handle_no_permission(self):

        return redirect('contacts:no_permission')


class EnemyDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Enemy
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('enemies:enemies_list')

    def test_func(self):
        enemy = self.get_object()
        return (
            self.request.user == enemy.creator or
            self.request.user.groups.filter(name="Moderators").exists()
        )

    def handle_no_permission(self):

        return redirect('contacts:no_permission')