
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from contacts.forms import ContactForm


# Create your views here.



class CreateMailView(CreateView):
    form_class = ContactForm
    success_url = reverse_lazy('characters:home')
    template_name = 'contacts/contact.html'
    extra_context = {
        'page_title': "Contact Us"
    }



class WipPage(TemplateView):
    template_name = 'contacts/wip.html'

    extra_context = {
        "page_title": "WIP"
    }

class AboutPageView(TemplateView):
    template_name = 'characters/about.html'
    extra_context = {
        'page_title': "About"
    }

class NoPermissionView(TemplateView):
    template_name = 'no_permission.html'
    extra_context = {
        'page_title': "No Permission"
    }

class MaintenanceView(TemplateView):
    template_name = 'maintenance.html'
    extra_context = {
        'page_title': "Maintenance"
    }