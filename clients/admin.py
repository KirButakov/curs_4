from django.contrib import admin
from .models import Client  # Импорт модели

admin.site.register(Client)  # Регистрация модели в админке
