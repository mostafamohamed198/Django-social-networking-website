from csv import writer
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class posts(models.Model):
    post = models.CharField(max_length=500)
    writer = models.ForeignKey("User", on_delete=models.CASCADE, related_name="writer")
    timestamp = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField("User",  related_name="liker" , default= None, blank=True)
    unlikers = models.ManyToManyField ("User", related_name="unliker" , default= None, blank=True)

class likes(models.Model):
    liked_post = models.ForeignKey("posts", on_delete=models.CASCADE)
    like_user = models.ForeignKey("User", on_delete=models.CASCADE)


class follow(models.Model):
    follower = models.ForeignKey("User",on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey("User",on_delete=models.CASCADE, related_name="following")