from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView

from partners.forms import PartnerCreateForm, PartnerEditForm, PartnerSearchForm
from partners.models import Partner



class PartnersListView(ListView):
    model = Partner
    template_name = 'partners/partners_page.html'
    context_object_name = 'partners'
    paginate_by = 9
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_form = PartnerSearchForm(self.request.GET or None)

        if 'query' in self.request.GET and self.search_form.is_valid():
            query = self.search_form.cleaned_data['query']
            queryset = queryset.filter(Q(name__icontains=query) | Q(title__icontains=query))

        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.search_form
        context['page_title'] = "Partners"
        return context


class PartnerDetailView(DetailView):
    model = Partner
    template_name = 'partners/partner_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"{self.object.name} Details"
        context['can_modify'] = (
                self.request.user == self.object.creator or
                self.request.user.groups.filter(name="Moderators").exists()
        )

        return context


class PartnerCreateView(LoginRequiredMixin,CreateView):
    form_class = PartnerCreateForm
    template_name = 'partners/create_partner.html'
    success_url = reverse_lazy('partners:partners_list')
    extra_context = {
        'page_title': "Create Partner",
    }

    def form_valid(self,form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class EditPartnerView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Partner
    form_class = PartnerEditForm
    template_name = 'partners/edit_partner.html'
    success_url = reverse_lazy('partners:partners_list')
    extra_context = {
        'page_title': "Edit Partner",
    }

    def test_func(self):
        partner = self.get_object()
        return (
            self.request.user == partner.creator or
            self.request.user.groups.filter(name="Moderators").exists()
        )

    def handle_no_permission(self):

        return redirect('contacts:no_permission')

class PartnerDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Partner
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('partners:partners_list')

    def test_func(self):
        partner = self.get_object()
        return (
            self.request.user == partner.creator or
            self.request.user.groups.filter(name="Moderators").exists()
        )

    def handle_no_permission(self):

        return redirect('contacts:no_permission')