from django.contrib import admin
from django.urls import path, include
from mailings.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("clients/", include("clients.urls")),
    path("mail_messages/", include("mail_messages.urls", namespace="mail_messages")),
    path("mailings/", include("mailings.urls")),
    path("", home, name="home"),
]
