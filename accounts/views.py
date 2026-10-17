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
            return redirect("onboarding_username")
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


@login_required
def onboarding_username(request: HttpRequest):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if user_profile.username:
        return redirect("onboarding")

    if request.method == "POST":
        form = UsernameSetupForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("onboarding")
    else:
        form = UsernameSetupForm(instance=user_profile)

    return render(request, "accounts/onboarding_username.html", {"form": form})

@login_required
def onboarding(request: HttpRequest):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if "skip" in request.POST:
            user_profile.onboarding_completed = True
            user_profile.save()
            return redirect("home")
        form = OnboardingForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.onboarding_completed = False
            user_profile.save()
            return redirect("home")
    else:
        form = OnboardingForm(instance=user_profile)

    return render(request, "accounts/onboarding.html", {"form": form})