from django.db import models
from mail_messages.models import Message
from clients.models import Client
from users.models import User
from django.core.mail import send_mail
from django.utils.timezone import now


class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-start_time"]

    def __str__(self):
        return f"Рассылка {self.id}"

    def send_mailing(self):
        """Отправляет письма клиентам и записывает попытки в MailingAttempt"""
        self.status = "started"
        self.save()

        for client in self.clients.all():
            try:
                send_mail(
                    subject=self.message.subject,
                    message=self.message.body,
                    from_email="your_email@example.com",
                    recipient_list=[client.email],
                    fail_silently=False,
                )
                status = "success"
                server_response = "Письмо успешно отправлено"
            except Exception as e:
                status = "failed"
                server_response = str(e)

            MailingAttempt.objects.create(
                attempt_time=now(),
                status=status,
                server_response=server_response,
                mailing=self,
            )

        self.status = "completed"
        self.save()


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("failed", "Не успешно"),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["-attempt_time"]

    def __str__(self):
        return f"Попытка {self.id}"
