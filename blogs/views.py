from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from blogs.forms import CommentForm, PostForm
from blogs.models import Comment, Like, Post, Tag


@login_required
def index(request: HttpRequest):
    base_posts = Post.objects.select_related("author__profile").prefetch_related("tags")
    filtered_posts = base_posts

    query = request.GET.get("q")
    tag_slug = request.GET.get("tag")

    if tag_slug:
        filtered_posts = filtered_posts.filter(tags__slug=tag_slug)

    if query:
        filtered_posts = filtered_posts.filter(
            Q(title__icontains=query)
            | Q(subtitle__icontains=query)
            | Q(body__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(author__profile__username__icontains=query)
            | Q(author__profile__display_name__icontains=query)
        ).distinct()

    featured = (
        base_posts.annotate(num_likes=Count("likes", distinct=True))
        .order_by("-num_likes", "-publish_date")
        .first()
    )
    trending = base_posts.annotate(
        num_likes=Count("likes", distinct=True),
        num_comments=Count("comments", distinct=True),
    ).order_by("-num_likes", "-num_comments", "-publish_date")[:3]
    latest_posts = list(base_posts.order_by("-publish_date")[:4])

    feed = filtered_posts
    if featured:
        feed = feed.exclude(pk=featured.pk)
    posts = list(feed.order_by("-publish_date"))

    tags = Tag.objects.all()
    mini_ideas = list(base_posts.order_by("-publish_date")[:3])
    return render(
        request,
        "blogs/home.html",
        {
            "featured": featured,
            "trending": trending,
            "latest_posts": latest_posts,
            "posts": posts,
            "tags": tags,
            "mini_ideas": mini_ideas,
            # handy for the template to show "results for X"
            "active_tag": tag_slug,
            "search_query": query,
        },
    )


@login_required
def post_details(request: HttpRequest, slug: str):
    post = get_object_or_404(
        Post.objects.select_related("author__profile").prefetch_related("likes"),
        slug=slug,
    )

    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(user=request.user).exists()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            parent_id = request.POST.get("parent")
            if parent_id:
                comment.parent = get_object_or_404(Comment, pk=parent_id, post=post)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect(f"{post.get_absolute_url()}#comments")
    else:
        form = CommentForm()

    comments = (
        post.comments.filter(parent__isnull=True)
        .select_related("user__profile")
        .prefetch_related("replies__user__profile")
    )

    return render(
        request,
        "blogs/post_details.html",
        {"post": post, "is_liked": is_liked, "form": form, "comments": comments},
    )


@login_required
def post_new(request: HttpRequest):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            redirect(post.get_absolute_url())
    else:
        form = PostForm()

    return render(request, "blogs/editor.html", {"form": form})


@login_required
@require_POST
def post_like(request: HttpRequest, slug: str):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect(post.get_absolute_url())


@login_required
@require_POST
def comment_like(request: HttpRequest, pk):
    comment = get_object_or_404(Comment, pk=pk)
    like, created = Like.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()
    return redirect("post_details", slug=comment.post.slug)
