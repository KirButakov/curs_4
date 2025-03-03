from django.contrib import admin
from .models import Message  # Импорт модели

admin.site.register(Message)  # Регистрация модели в админке
