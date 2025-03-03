from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from mailings.models import Mailing


class Command(BaseCommand):
    help = "Создает группу 'Менеджеры' и назначает права"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Менеджеры")
        if created:
            self.stdout.write(self.style.SUCCESS("Группа 'Менеджеры' создана."))

        # Назначаем права
        permission = Permission.objects.get(codename="can_manage_mailings")
        group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS("Права назначены группе 'Менеджеры'."))
