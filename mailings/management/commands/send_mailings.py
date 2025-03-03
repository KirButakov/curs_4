from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from mailings.models import Mailing, MailingAttempt
import logging

logger = logging.getLogger(__name__)


def send_mailing(mailing):
    """Функция отправки рассылки клиентам и логирования попыток."""
    for client in mailing.clients.all():
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.body,
                settings.DEFAULT_FROM_EMAIL,  # Используем EMAIL из настроек
                [client.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                status="success",
                server_response="OK",
                mailing=mailing,
            )
            logger.info(f"Письмо успешно отправлено клиенту {client.email}")
        except Exception as e:
            MailingAttempt.objects.create(
                status="failed",
                server_response=str(e),
                mailing=mailing,
            )
            logger.error(f"Ошибка при отправке письма клиенту {client.email}: {e}")


class Command(BaseCommand):
    help = "Send mailings"

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status="started")
        for mailing in mailings:
            send_mailing(mailing)
            self.stdout.write(self.style.SUCCESS(f"Рассылка {mailing.id} отправлена"))
