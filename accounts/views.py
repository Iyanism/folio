from django.http import HttpRequest
from django.shortcuts import redirect, render

from accounts.forms import SignupForm


# Create your views here.
def signup(request: HttpRequest):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return None
    else:
        form = SignupForm()

        return render(request, "accounts/signup.html", {"form": form})
