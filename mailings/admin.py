from django.contrib import admin
from .models import Mailing, MailingAttempt

admin.site.register(Mailing)
admin.site.register(MailingAttempt)
