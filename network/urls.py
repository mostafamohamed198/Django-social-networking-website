
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('newpost', views.newpost, name="newpost"),
    path("follow/<str:name>", views.Users, name="follow"),
    path('like/<int:post_id>',views.like, name='like'),
    path('edit/<int:posttid>', views.edit, name='edit'),
    path('following/<int:user>', views.following, name='following')
]
