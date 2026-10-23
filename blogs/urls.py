from django.urls import path

from blogs import views

urlpatterns = [
    path("", views.index, name="home"),
    path("post/<slug:slug>", views.post_details, name="post_details"),
    path("post/new", views.post_new, name="post_new"),
    path("post/<slug:slug>/like", views.post_like, name="post_like"),
]
