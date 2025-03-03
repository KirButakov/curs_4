from django.urls import path
from mail_messages.views import (
    MessageListView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
)

app_name = "mail_messages"

urlpatterns = [
    path("", MessageListView.as_view(), name="message_list"),
    path("create/", MessageCreateView.as_view(), name="message_create"),
    path("update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"),
    path("delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"),
]
