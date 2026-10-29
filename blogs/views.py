import math
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.views.decorators.http import require_POST

from blogs.forms import CommentForm, PostForm
from blogs.models import Comment, Like, Post, Tag, Bookmark
from accounts.models import Following
from blogs.queries import get_base_posts, apply_feed, get_followed_ids, apply_tag, apply_query, get_featured_posts, \
    get_trending_posts, get_latest_posts, get_mini_posts, get_bookmark_post_ids


def index(request: HttpRequest):
    base_posts = get_base_posts()
    tags = Tag.objects.all()
    filtered_posts = base_posts
    followed_ids = set()
    bookmark_posts = set()

    # filters
    query = request.GET.get("q")
    tag_slug = request.GET.get("tag")
    feed = request.GET.get("feed", "for_you")

    # set of author user follow
    if request.user.is_authenticated:
        followed_ids = get_followed_ids(request.user)
        bookmark_posts = get_bookmark_post_ids(request.user)

    # global posts
    featured = get_featured_posts(base_posts)
    trending = get_trending_posts(base_posts)
    latest_posts = get_latest_posts(base_posts, limit=4)
    mini_ideas = get_mini_posts(base_posts, limit=3)

    filtered_posts = apply_feed(filtered_posts, feed, request.user.is_authenticated, followed_ids)
    filtered_posts = apply_tag(filtered_posts, tag_slug)
    filtered_posts = apply_query(filtered_posts, query)

    feed_post = filtered_posts
    if featured:
        feed_post = feed_post.exclude(pk=featured.pk)
    posts = list(feed_post)

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
            "is_following": followed_ids,
            "active_tag": tag_slug,
            "search_query": query,
            "feed": feed,
            "bookmark_posts": bookmark_posts,
        },
    )


def post_details(request: HttpRequest, slug: str):
    post = get_object_or_404(
        Post.objects.select_related("author__profile").prefetch_related("likes", "bookmarks", "tags"),
        slug=slug,
    )

    form = CommentForm()

    comments = (
        post.comments.filter(parent__isnull=True)
        .select_related("user__profile")
        .prefetch_related("replies__user__profile", "likes", "replies__likes")
    ).order_by("-comment_at")

    is_following = False
    is_post_liked = False
    is_bookmarked = False
    liked_comment_ids = set()
    if request.user.is_authenticated:
        is_following = Following.objects.filter(
            follower=request.user, followed=post.author
        ).exists()
        is_post_liked = post.likes.filter(user=request.user).exists()
        is_bookmarked = post.bookmarks.filter(user=request.user).exists()
        liked_comment_ids = set(post.comments.filter(likes__user=request.user).values_list("id", flat=True))

    return render(
        request,
        "blogs/post_details.html",
        {
            "post": post,
            "is_post_liked": is_post_liked,
            "form": form,
            "comments": comments,
            "is_following": is_following,
            "liked_comment_ids": liked_comment_ids,
            "is_bookmarked": is_bookmarked,
        },
    )


@login_required
def post_new(request: HttpRequest):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.read_minutes = max(1, math.ceil(len(post.body.split()) / 230))
            post.save()
            form.save_m2m()
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()

    return render(request, "blogs/editor.html", {"form": form})

@login_required
def bookmarks_home(request: HttpRequest):
    posts_ids = get_bookmark_post_ids(request.user)
    followed_ids = get_followed_ids(request.user)
    posts = get_base_posts().filter(id__in=posts_ids)
    tags = Tag.objects.all()

    # feed filters
    query = request.GET.get("q")
    tag_slug = request.GET.get("tag")
    feed = request.GET.get("feed", "for_you")

    filtered_posts = apply_feed(posts, feed, request.user.is_authenticated, followed_ids)
    filtered_posts = apply_tag(filtered_posts, tag_slug)
    filtered_posts = apply_query(filtered_posts, query)
    posts = list(filtered_posts)

    return render(
        request,
        "blogs/bookmarks.html",
        {
            "posts": posts,
            "is_following": followed_ids,
            "tags": tags,
            "active_tag": tag_slug,
            "search_query": query,
            "feed": feed,
            "bookmark_posts": posts_ids,
        }
    )

@login_required
@require_POST
def post_bookmark(request: HttpRequest, slug: str):
    post = get_object_or_404(Post, slug=slug)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
    if not created:
        bookmark.delete()
    return redirect("bookmarks_home")

@login_required
@require_POST
def post_comment(request: HttpRequest, slug: str):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST)
    form.instance.post = post
    form.instance.user = request.user
    if form.is_valid():
        comment = form.save(commit=False)
        parent_id = request.POST.get("parent")
        if parent_id:
            comment.parent = get_object_or_404(Comment, pk=parent_id, post=post)
        comment.save()
        return redirect(f"{post.get_absolute_url()}#comments")
    else:
        return HttpResponseBadRequest(form.errors)


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
def comment_like(request: HttpRequest, pk: int):
    comment = get_object_or_404(Comment.objects.select_related("post"), pk=pk)
    like, created = Like.objects.get_or_create(comment=comment, user=request.user)
    if not created:
        like.delete()
    return redirect(comment.post.get_absolute_url())