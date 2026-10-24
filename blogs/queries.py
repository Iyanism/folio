from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q, Count

from accounts.models import Following
from blogs.models import Post, Bookmark


def get_base_posts():
    return (
        Post.objects
        .select_related("author__profile")
        .prefetch_related("tags")
    )

def apply_feed(posts: Post, feed: str, is_authenticated: bool, followed_ids):
    if is_authenticated:
        if feed == "following":
            posts = posts.filter(author__id__in=followed_ids)
    if feed == "latest":
        posts = posts.order_by("-publish_date")
    return posts


def apply_tag(posts: Post, tag_slug: str | None):
    if not tag_slug:
        return posts
    return posts.filter(tags__slug=tag_slug).order_by("-publish_date")


def apply_query(posts: Post, query: str | None):
    if not query:
        return posts
    return posts.filter(
            Q(title__icontains=query)
            | Q(subtitle__icontains=query)
            | Q(body__icontains=query)
            | Q(tags__name__icontains=query)
            | Q(author__profile__username__icontains=query)
            | Q(author__profile__display_name__icontains=query)
        ).distinct()

def get_featured_posts(posts: Post):
    return (
        posts.annotate(num_likes=Count("likes", distinct=True))
        .order_by("-num_likes", "-publish_date")
        .first()
    )

def get_trending_posts(posts: Post):
    return (
        posts.annotate(
            num_likes=Count("likes", distinct=True),
            num_comments=Count("comments", distinct=True),
        ).order_by("-num_likes", "-num_comments", "-publish_date")[:3]
    )

def get_latest_posts(posts: Post, limit: int = 4):
    return list(
        posts.order_by("-publish_date")
    )[:limit]

def get_followed_ids(user: User | AnonymousUser):
    if not user.is_authenticated:
        return set()
    return set(
        Following.objects
        .filter(follower=user)
        .values_list("followed_id", flat=True)
    )

def get_mini_posts(posts: Post, limit: int = 3):
    return list(
        posts.order_by("-publish_date")
    )[:limit]

def get_bookmark_post_ids(user: User | AnonymousUser):
    if not user.is_authenticated:
        return set()
    return set(
        Bookmark.objects
        .select_related("post")
        .filter(user=user)
        .values_list("post_id", flat=True)
    )
