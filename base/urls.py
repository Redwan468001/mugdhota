from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('userpost/<str:pk>/', views.userpost, name="userpost"),
    path('user-profile/<int:pk>/', views.userProfile, name="user-profile"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('create-post/', views.createUserpost, name="create-post"),
    path('update-post/<str:pk>/', views.updateUserpost, name="update-post"),
    path('delete-post/<str:pk>/', views.deleteUserpost, name="delete-post"),
    path('delete-comment/<str:pk>/', views.deleteComment, name="delete-comment"),
    path('like-post', views.like_post, name='like-post'),

    path('update-user/', views.updateUser, name="update-user"),
]













