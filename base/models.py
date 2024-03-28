from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import uuid

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    joined = models.DateTimeField(default=datetime.now)
    coverphoto = models.ImageField(upload_to='profile_images', null=True, default="cover.jpg" )
    avatar = models.ImageField(upload_to='profile_images', null=True, default="avatar.svg" )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def UserDetails(self):
        return ",".join('name' 'email' 'location' 'joined')


class UserPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='uup_images', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    no_of_likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-updated', '-created']

    def UserPostDetails(self):
        return ",".join('author' 'content' 'created' 'updated')


class UserPostComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userpost = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=500)

    def __str__(self):
        return self.username


















