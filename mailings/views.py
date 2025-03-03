from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.mail import send_mail
from django.utils.timezone import now
from django.http import HttpResponseForbidden
from .models import Mailing, MailingAttempt
from clients.models import Client
from django.conf import settings


class MailingSendView(LoginRequiredMixin, View):
    """Класс-представление для отправки рассылки"""

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk)

        # Проверяем, является ли пользователь владельцем рассылки или имеет права
        if mailing.owner != request.user and not request.user.has_perm(
            "mailings.can_manage_mailings"
        ):
            return HttpResponseForbidden("У вас нет прав на запуск этой рассылки.")

        if mailing.status == "created":
            mailing.status = "started"
            mailing.save()

            for client in mailing.clients.all():
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
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
                    mailing=mailing,
                )

            mailing.status = "completed"
            mailing.save()

        return redirect("mailings:mailing_list")


@method_decorator(cache_page(60 * 5), name="dispatch")
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    fields = ["start_time", "end_time", "status", "message", "clients"]
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    fields = ["start_time", "end_time", "status", "message", "clients"]
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user or self.request.user.has_perm(
            "mailings.can_manage_mailings"
        )


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")

    def test_func(self):
        mailing = self.get_object()
        return mailing.owner == self.request.user or self.request.user.has_perm(
            "mailings.can_manage_mailings"
        )


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "mailings/mailing_attempt_list.html"
    context_object_name = "attempts"


def home(request):
    total_mailings = cache.get("total_mailings")
    active_mailings = cache.get("active_mailings")
    unique_clients = cache.get("unique_clients")

    if total_mailings is None or active_mailings is None or unique_clients is None:
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status="started").count()
        unique_clients = Client.objects.distinct().count()

        cache.set("total_mailings", total_mailings, 60 * 10)  # Кешируем на 10 минут
        cache.set("active_mailings", active_mailings, 60 * 10)
        cache.set("unique_clients", unique_clients, 60 * 10)

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
    }
    return render(request, "mailings/home.html", context)


def send_mailing(mailing):
    for client in mailing.clients.all():
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.body,
                settings.DEFAULT_FROM_EMAIL,
                [client.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                status="success",
                server_response="Письмо успешно отправлено",
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status="failed",
                server_response=str(e),
            )


def start_mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)
    send_mailing(mailing)
    mailing.status = "started"
    mailing.save()
    return redirect("mailings:mailing_list")
