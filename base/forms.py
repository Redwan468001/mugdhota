from django.forms import ModelForm
from .models import User, UserPost
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserPostForm(ModelForm):
    class Meta:
        model = UserPost
        fields = ['content', 'image']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']