from django.db import models
from django.contrib.auth.models import User



class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    date_of_birth = models.DateField()
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
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()


    def __str__(self):
        return f"Trip to {self.place.name}"


class TripPhoto(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_photos')
    photo = models.ImageField(upload_to='')

    def __str__(self):
        return f"Photo for {self.trip.place}"



class TripPreference(models.Model):
    related_trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='preferences')
    preferences = models.ManyToManyField(PreferenceChoice)
    def __str__(self):
        return f"Preferences for {self.related_trip.place.name} by {self.related_trip.uploader}"


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = models.Q(first_person=user) | models.Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='thread_second_person')
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
