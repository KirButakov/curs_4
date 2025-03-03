from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Импорт кастомной модели пользователя

admin.site.register(User, UserAdmin)  # Регистрация модели пользователя
