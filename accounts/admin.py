from django.contrib import admin

from accounts.models import User, UserProfile, Following


# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    pass