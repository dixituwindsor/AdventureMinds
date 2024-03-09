from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    date_of_birth = models.DateField()
    interested_places = models.ManyToManyField(Place)

    def __str__(self):
        return self.name


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

        return self.get_full_name()


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
        return f"{self.sender.name} -> {self.recipient.name if self.recipient else self.chat_group.name}: {self.content}"

