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
    total_reviews = models.PositiveIntegerField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
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

# class Destination(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

class Trip(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    destination = models.ForeignKey(Place, on_delete=models.CASCADE)
    trip_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s trip to {self.destination.name}"

class Review(models.Model):
    # destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    # def save(self, *args, **kwargs):
    #     # Calculate average rating for user profile and update
    #     self.trip.user.total_reviews += 1
    #     self.trip.user.total_ratings += self.rating
    #     self.user.average_rating = self.trip.user.total_ratings / self.trip.user.total_reviews
    #     self.user.save()
    #     super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.trip.user.username}'s review for {self.trip.destination.name}"
