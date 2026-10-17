from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.shortcuts import render


@login_required
def index(request: HttpRequest):
    return render(request, "blogs/home.html", {})

@login_required
def post_details(request: HttpRequest):
    return render(request, "blogs/post_details.html", {})

@login_required
def post_new(request: HttpRequest):
    return render(request, "blogs/editor.html", {})