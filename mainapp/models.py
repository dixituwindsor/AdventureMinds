
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile/', null=True, blank=True)
    interested_places = models.ManyToManyField(Place, null=True, blank=True)
    preferences = models.ForeignKey('UserPreferences', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username


class PreferenceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PreferenceChoice(models.Model):
    category = models.ForeignKey(PreferenceCategory, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name}: {self.value}"


class UserPreferences(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_profile', null=True, blank=True)
    preferences = models.ManyToManyField(PreferenceChoice)

    def __str__(self):
        if self.user_profile:
            return f"Preferences for {self.user_profile.user.username}"
        else:
            return "No associated user profile"

    def get_selected_preferences(self):
        return [preference.value for preference in self.preferences.all()]




class Trip(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_trips')
    title = models.CharField(max_length=100)
    description = models.TextField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    max_capacity = models.PositiveIntegerField(default=10)
    cost_per_person = models.DecimalField(max_digits=8, decimal_places=2, default=1000)  # Cost per person for the trip
    meeting_point = models.CharField(max_length=255, blank=True)  # Meeting point for the trip
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='participating_trips', blank=True)
    is_past = models.BooleanField(default=False)
    is_future = models.BooleanField(default=True)
    preferences = models.ForeignKey('TripPreference', on_delete=models.SET_NULL, null=True, blank=True)

    # Define methods to filter past and future trips
    def get_past_trips(self):
        return Trip.objects.filter(pk=self.pk, is_past=True)

    def get_future_trips(self):
        return Trip.objects.filter(pk=self.pk, is_future=True)

    def __str__(self):
        return self.title




class JoinRequest(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request to join {self.trip} by {self.user}"





class TripPhoto(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='')

    def __str__(self):
        return f"Photo for {self.trip.title}"

class TripPreference(models.Model):
    preferences = models.ManyToManyField(PreferenceChoice)



class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = models.Q(first_person=user) | models.Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE,
                               related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
