from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    def __str__(self):
        return self.name


class UserProfile(User):
    interested_places = models.ManyToManyField(Place)
    def __str__(self):
        return self.get_username()


class ChatGroups(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(UserProfile, related_name='chat_groups')

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    chat_group = models.ForeignKey(ChatGroups, on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username if self.recipient else self.chat_group.name}: {self.content}"

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Review(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
