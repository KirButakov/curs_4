from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from users.forms import ProfileForm
from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    return render(request, "users/profile.html", {"user": request.user})


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Профиль успешно обновлён!"
            )  # Сообщение об успешном обновлении
            return redirect("users:profile")  # Перенаправление на страницу профиля
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "users/profile_edit.html", {"form": form})
