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

class UserPreferences(models.Model):
    user_profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, related_name='preferences')
    travel_style = models.CharField(max_length=100, choices=[
        ('Adventure Seeker', 'Adventure Seeker'),
        ('Cultural Explorer', 'Cultural Explorer'),
        ('Luxury Traveler', 'Luxury Traveler'),
        ('Budget Traveler', 'Budget Traveler'),
        ('Family Traveler', 'Family Traveler'),
        ('Solo Traveler', 'Solo Traveler'),
        ('Eco-conscious Traveler', 'Eco-conscious Traveler')
    ])
    activity_preferences = models.CharField(max_length=100, choices=[
        ('Outdoor Activities', 'Outdoor Activities'),
        ('Sightseeing/Cultural Activities', 'Sightseeing/Cultural Activities'),
        ('Food and Wine Experiences', 'Food and Wine Experiences'),
        ('Relaxation/Wellness Activities', 'Relaxation/Wellness Activities'),
        ('Adventure Sports', 'Adventure Sports'),
        ('Shopping', 'Shopping')
    ], blank=True)
    destination_preferences = models.CharField(max_length=100, choices=[
        ('Beach Destinations', 'Beach Destinations'),
        ('Mountain Destinations', 'Mountain Destinations'),
        ('Urban Destinations', 'Urban Destinations'),
        ('Historical/Cultural Destinations', 'Historical/Cultural Destinations'),
        ('Nature/Wildlife Destinations', 'Nature/Wildlife Destinations'),
        ('Off-the-beaten-path Destinations', 'Off-the-beaten-path Destinations')
    ], blank=True)
    accommodation_preferences = models.CharField(max_length=100, choices=[
        ('Hotels', 'Hotels'),
        ('Resorts', 'Resorts'),
        ('Hostels', 'Hostels'),
        ('Vacation Rentals', 'Vacation Rentals'),
        ('Camping', 'Camping'),
        ('Boutique Hotels', 'Boutique Hotels')
    ], blank=True)
    transportation_preferences = models.CharField(max_length=100, choices=[
        ('Group Tours with Transportation Included', 'Group Tours with Transportation Included'),
        ('Self-Guided Tours with Rental Car', 'Self-Guided Tours with Rental Car'),
        ('Public Transportation', 'Public Transportation'),
        ('Private Transportation (e.g., Chauffeur, Private Transfers)',
         'Private Transportation (e.g., Chauffeur, Private Transfers)')
    ], blank=True)
    meal_preferences = models.CharField(max_length=100, choices=[
        ('Local Cuisine', 'Local Cuisine'),
        ('Fine Dining', 'Fine Dining'),
        ('Street Food', 'Street Food'),
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
        ('Gluten-Free', 'Gluten-Free')
    ], blank=True)
    language_preferences = models.CharField(max_length=100, choices=[
        ('English', 'English'),
        ('Spanish', 'Spanish'),
        ('French', 'French'),
        ('Mandarin', 'Mandarin'),
        ('Italian', 'Italian'),
        ('Hindi', 'Hindi')
    ], blank=True)
    budget_range = models.CharField(max_length=100, choices=[
        ('Budget', 'Budget'),
        ('Moderate', 'Moderate'),
        ('Luxury', 'Luxury')
    ], blank=True)
    special_interests = models.CharField(max_length=100, choices=[
        ('History', 'History'),
        ('Art', 'Art'),
        ('Photography', 'Photography'),
        ('Adventure Sports', 'Adventure Sports'),
        ('Wildlife/Nature', 'Wildlife/Nature'),
        ('Wine Tasting', 'Wine Tasting')
    ], blank=True)

    def __str__(self):
        return f'Preferences for {self.user.username}'


class Trip(models.Model):
    source_place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='source_trips')
    destination_place = models.CharField(max_length=100)
    date_of_trip = models.DateField()
    days_of_travel = models.IntegerField()
    travel_style = models.CharField(max_length=100, choices=[])
    activities = models.CharField(max_length=100, choices=[])
    transportation = models.CharField(max_length=100, choices=[])
    meal = models.CharField(max_length=100, choices=[])
    language = models.CharField(max_length=100, choices=[])
    speacial_interests = models.CharField(max_length=100, choices=[])
    accommodation = models.CharField(max_length=100, choices=[])
    budget = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Trip from {self.source_place} to {self.destination_place}'

    def set_travel_style_choices(self, user_profile):
        user_preferences = UserPreferences.objects.get(user_profile=user_profile)
        self.travel_style = user_preferences.travel_style

    def set_activities_choices(self, user_profile):
        user_preferences = UserPreferences.objects.get(user_profile=user_profile)
        self.activities = user_preferences.activity_preferences

    def set_transportation_choices(self, user_profile):
        user_preferences = UserPreferences.objects.get(user_profile=user_profile)
        self.transportation = user_preferences.transportation_preferences

    def set_meal_choices(self, user_profile):
        user_preferences = UserPreferences.objects.get(user_profile=user_profile)
        self.meal = user_preferences.meal_preferences

    def set_language_choices(self, user_profile):
        user_preferences = UserPreferences.objects.get(user_profile=user_profile)
        self.language = user_preferences.language_preferences

    def set_speacial_interests_choices(self, user_profile):
        user_preferences = UserPreferences.objects.get(user_profile=user_profile)
        self.speacial_interests = user_preferences.speacial_interests

    def set_accommodation_choices(self, user_profile):
        user_preferences = UserPreferences.objects.get(user_profile=user_profile)
        self.accommodation = user_preferences.accommodation_preferences


class Photo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='trip_photos/')

    def __str__(self):
        return f'Photo for Trip: {self.trip}'