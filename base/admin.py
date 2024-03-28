from django.contrib import admin
from .models import User, UserPost, UserPostComments, LikePost

# Register your models here.
@admin.register(User)
class UserDetails(admin.ModelAdmin):
    list_display = ['name', 'email', 'location', 'joined']

@admin.register(UserPost)
class UserPostDetails(admin.ModelAdmin):
    list_display = ['author', 'content', 'created', 'updated']


admin.site.register(UserPostComments)
admin.site.register(LikePost)
