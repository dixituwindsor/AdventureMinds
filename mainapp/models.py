from django.db import models
from django.contrib.auth.models import User


class PreferenceChoice(models.Model):
    category = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interested_places = models.ManyToManyField('Place', related_name='interested_users')

    def __str__(self):
        return self.user.username


class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class UserPreferences(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='preferences')
    travel_style = models.ForeignKey(PreferenceChoice, on_delete=models.CASCADE, related_name='user_travel_style_preferences')
    activity_preferences = models.ManyToManyField(PreferenceChoice, related_name='user_activity_preferences')
    destination_preferences = models.ManyToManyField(PreferenceChoice, related_name='user_destination_preferences')
    accommodation_preferences = models.ManyToManyField(PreferenceChoice, related_name='user_accommodation_preferences')
    transportation_preferences = models.ManyToManyField(PreferenceChoice, related_name='user_transportation_preferences')
    meal_preferences = models.ManyToManyField(PreferenceChoice, related_name='user_meal_preferences')
    language_preferences = models.ManyToManyField(PreferenceChoice, related_name='user_language_preferences')
    budget_range = models.ForeignKey(PreferenceChoice, on_delete=models.CASCADE, related_name='user_budget_range_preferences')
    special_interests = models.ManyToManyField(PreferenceChoice, related_name='user_special_interests_preferences')

    def __str__(self):
        return f'Preferences for {self.user.user.username}'


class Trip(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    travel_style = models.ForeignKey(PreferenceChoice, on_delete=models.CASCADE, related_name='trip_travel_style')
    activity_preferences = models.ManyToManyField(PreferenceChoice, related_name='trip_activity_preferences')
    destination_preferences = models.ManyToManyField(PreferenceChoice, related_name='trip_destination_preferences')
    accommodation_preferences = models.ManyToManyField(PreferenceChoice, related_name='trip_accommodation_preferences')
    transportation_preferences = models.ManyToManyField(PreferenceChoice, related_name='trip_transportation_preferences')
    meal_preferences = models.ManyToManyField(PreferenceChoice, related_name='trip_meal_preferences')
    language_preferences = models.ManyToManyField(PreferenceChoice, related_name='trip_language_preferences')
    budget_range = models.ForeignKey(PreferenceChoice, on_delete=models.CASCADE, related_name='trip_budget_range')
    special_interests = models.ManyToManyField(PreferenceChoice, related_name='trip_special_interests')
    created_at = models.DateTimeField(auto_now_add=True)


class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined')
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')


class Review(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


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

    def __str__(self):
        return f"Conversation between {self.first_person} and {self.second_person}"


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)