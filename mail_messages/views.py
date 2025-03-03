from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from mail_messages.models import Message


class MessageListView(ListView):
    model = Message
    template_name = "mail_messages/message_list.html"


class MessageCreateView(CreateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mail_messages/message_form.html"
    success_url = reverse_lazy("mail_messages:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    fields = ["subject", "body"]
    template_name = "mail_messages/message_form.html"
    success_url = reverse_lazy("mail_messages:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mail_messages/message_confirm_delete.html"
    success_url = reverse_lazy("mail_messages:message_list")
