import math
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import User


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    body = models.TextField()
    read_minutes = models.IntegerField(default=0)
    cover_url = models.URLField(blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField("Tag", blank=True, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    class Meta:
        ordering = ["-publish_date"]

    def get_absolute_url(self):
        return reverse("post_details", kwargs={"slug": self.slug})

    @property
    def tag_line(self):
        return ", ".join(t.name for t in self.tags.all()[:2])

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:140] or "post"
            self.slug = f"{base}-{uuid.uuid4().hex[:8]}"
        self.read_minutes = max(1, math.ceil(len(self.body.split()) / 230))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) or f"tag-{uuid.uuid4().hex[:8]}"
        return super().save(*args, **kwargs)

    def clean(self):
        self.name = (self.name or "").strip()
        if Tag.objects.filter(name__iexact=self.name).exclude(pk=self.pk).exists():
            raise ValidationError({"name": "This tag already exists."})

    def __str__(self):
        return self.name

class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
    )
    comment_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["comment_at"]

    def __str__(self):
        return f"{self.user} on {self.post}: {self.body[:40]}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True ,related_name="likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name="likes", )
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_post_like"),
            models.UniqueConstraint(fields=["user", "comment"], name="unique_comment_like"),
        ]

    def __str__(self):
        return f"{self.user} - {self.post}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    bookmark_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_bookmark"),
        ]

    def __str__(self):
        return f"{self.user} - {self.post}"