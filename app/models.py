from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    message = models.CharField(max_length=140)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    message = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    text = models.TextField()
