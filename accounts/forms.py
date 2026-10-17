from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import User, UserProfile


class SignupForm(UserCreationForm):
    username = None

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
                "input mode": "email",
                "autocapitalize": "off",
                "spellcheck": "false",
                "class": "email-field",
            }
        ),
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "At least 8 characters",
                "autocomplete": "new-password",
                "class": "pw",
            }
        ),
        help_text="At least 8 characters. Longer is better.",
    )

    password2 = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Repeat your password",
                "autocomplete": "new-password",
                "class": "pw",
            }
        ),
        help_text="Enter the same password as before, for verification.",
    )
    
    class Meta(UserCreationForm.Meta):  # ty: ignore[invalid-attribute-override]
        model = User
        fields = ("email",)


