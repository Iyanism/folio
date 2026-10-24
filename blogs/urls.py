from django.urls import path

from blogs import views

urlpatterns = [
    path("", views.index, name="home"),
    path("post/<slug:slug>/", views.post_details, name="post_details"),
    path("post/new/", views.post_new, name="post_new"),
    path("post/<slug:slug>/like/", views.post_like, name="post_like"),
    path("post/<slug:slug>/comment/", views.post_comment, name="post_comment"),
    path("post/<slug:slug>/comments/<int:pk>/like", views.comment_like, name="comment_like"),
    path("post/<slug:slug>/bookmark/", views.post_bookmark, name="post_bookmark"),
    path("bookmarks/", views.bookmarks_home, name="bookmarks_home"),
]
