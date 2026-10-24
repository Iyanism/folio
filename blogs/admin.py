from django.contrib import admin

from blogs.models import Comment, Like, Post, Tag, Bookmark


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass