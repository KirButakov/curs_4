from django.urls import path
from .views import (
    MailingListView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    MailingAttemptListView,
    MailingSendView,
    home,
)

app_name = "mailings"

urlpatterns = [
    path("", MailingListView.as_view(), name="mailing_list"),
    path("create/", MailingCreateView.as_view(), name="mailing_create"),
    path("update/<int:pk>/", MailingUpdateView.as_view(), name="mailing_update"),
    path("delete/<int:pk>/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("attempts/", MailingAttemptListView.as_view(), name="mailing_attempt_list"),
    path("send/<int:pk>/", MailingSendView.as_view(), name="mailing_send"),
    path("home/", home, name="home"),
]
