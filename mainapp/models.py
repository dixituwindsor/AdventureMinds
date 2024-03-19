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

# remove START CODE
class Trip(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    place = models.TextField()

    def __str__(self):
        return f"Trip to {self.description} from {self.start_date} to {self.end_date}"

# END CODE

class Wishlist(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='wishlist_items')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    priority = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_place(self):
        return self.trip_id.place
    class Meta:
        unique_together = ('user_id', 'trip_id',)

    def __str__(self):
        return f"{self.user_id.username}'s Wishlist Item: (Trip: {self.trip_id.description})"