from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Client


class ClientListView(ListView):
    model = Client
    template_name = "clients/client_list.html"

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(CreateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    fields = ["email", "full_name", "comment"]
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("clients:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("clients:client_list")
