from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from accounts.forms import SignupForm, ProfileForm, UsernameSetupForm, OnboardingForm
from accounts.models import UserProfile


def signup(request: HttpRequest):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile_edit")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request: HttpRequest):
    # Safe lookup: get_or_create prevents crashes if signal missed
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "accounts/profile.html", {"profile": user_profile})


@login_required
def edit_profile(request: HttpRequest):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=user_profile)

    return render(request, "accounts/edit_profile.html", {"form": form})


