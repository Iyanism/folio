from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path(
        "login/", LoginView.as_view(template_name="accounts/login.html"), name="login"
    ),
    path("onboarding/username/", views.onboarding_username, name="onboarding_username"),
    path("onboarding/", views.onboarding, name="onboarding"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("<int:pk>/follow/", views.following, name="follow"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
