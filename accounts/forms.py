from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class SignupForm(UserCreationForm):
    username = None

    class Meta(UserCreationForm.Meta):  # ty: ignore[invalid-attribute-override]
        model = User
        fields = ("email",)
