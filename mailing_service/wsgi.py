import os
from django.core.wsgi import get_wsgi_application

# Указываем Django, где находятся настройки проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mailing_service.settings")

# Получаем WSGI-приложение
application = get_wsgi_application()
