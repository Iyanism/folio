from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User, UserProfile


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "you@example.com",
                "autocomplete": "email",
                "inputmode": "email",
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

    class Meta:
        model = User
        fields = ("email",)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["username", "display_name", "bio", "gender"]
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "e.g. alexander", "autocomplete": "username"}
            ),
            "display_name": forms.TextInput(
                attrs={"placeholder": "e.g. Alex", "class": "display_name"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "placeholder": "A short note about what you write or read...",
                    "class": "bio",
                }
            ),
            "gender": forms.Select(attrs={"class": "gender-select"}),
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username:
            raise forms.ValidationError("Please enter a username")
        return username.strip().lower()


class OnboardingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["display_name", "gender", "bio"]
        widgets = {
            "display_name": forms.TextInput(
                attrs={"placeholder": "e.g. Alex Smith", "class": "display_name"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "placeholder": "A short note about what you write or read...",
                    "class": "bio",
                }
            ),
            "gender": forms.Select(attrs={"class": "gender-select"}),
        }


class UsernameSetupForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "e.g. alexander", "autocomplete": "username"}
            ),
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username:
            raise forms.ValidationError("Please enter a username")
        return username.strip().lower()
