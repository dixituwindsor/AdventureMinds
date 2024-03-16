from django.db import models
from django.contrib.auth.models import User

class Place(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.name



    def __str__(self):
        return self.user.username

class UserPreferences(models.Model):
    travel_style = models.CharField(max_length=100, choices=[
        ('Adventure Seeker', 'Adventure Seeker'),
        ('Cultural Explorer', 'Cultural Explorer'),
        ('Luxury Traveler', 'Luxury Traveler'),
        ('Budget Traveler', 'Budget Traveler'),
        ('Family Traveler', 'Family Traveler'),
        ('Solo Traveler', 'Solo Traveler'),
        ('Eco-conscious Traveler', 'Eco-conscious Traveler')
    ], null=True)  # Set null=True for default as null

    activity_preferences = models.CharField(max_length=100, choices=[
        ('Outdoor Activities', 'Outdoor Activities'),
        ('Sightseeing/Cultural Activities', 'Sightseeing/Cultural Activities'),
        ('Food and Wine Experiences', 'Food and Wine Experiences'),
        ('Relaxation/Wellness Activities', 'Relaxation/Wellness Activities'),
        ('Adventure Sports', 'Adventure Sports'),
        ('Shopping', 'Shopping')
    ], blank=True, null=True)  # Set null=True for default as null

    destination_preferences = models.CharField(max_length=100, choices=[
        ('Beach Destinations', 'Beach Destinations'),
        ('Mountain Destinations', 'Mountain Destinations'),
        ('Urban Destinations', 'Urban Destinations'),
        ('Historical/Cultural Destinations', 'Historical/Cultural Destinations'),
        ('Nature/Wildlife Destinations', 'Nature/Wildlife Destinations'),
        ('Off-the-beaten-path Destinations', 'Off-the-beaten-path Destinations')
    ], blank=True, null=True)  # Set null=True for default as null

    accommodation_preferences = models.CharField(max_length=100, choices=[
        ('Hotels', 'Hotels'),
        ('Resorts', 'Resorts'),
        ('Hostels', 'Hostels'),
        ('Vacation Rentals', 'Vacation Rentals'),
        ('Camping', 'Camping'),
        ('Boutique Hotels', 'Boutique Hotels')
    ], blank=True, null=True)  # Set null=True for default as null

    transportation_preferences = models.CharField(max_length=100, choices=[
        ('Group Tours with Transportation Included', 'Group Tours with Transportation Included'),
        ('Self-Guided Tours with Rental Car', 'Self-Guided Tours with Rental Car'),
        ('Public Transportation', 'Public Transportation'),
        ('Private Transportation (e.g., Chauffeur, Private Transfers)',
         'Private Transportation (e.g., Chauffeur, Private Transfers)')
    ], blank=True, null=True)  # Set null=True for default as null

    meal_preferences = models.CharField(max_length=100, choices=[
        ('Local Cuisine', 'Local Cuisine'),
        ('Fine Dining', 'Fine Dining'),
        ('Street Food', 'Street Food'),
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
        ('Gluten-Free', 'Gluten-Free')
    ], blank=True, null=True)  # Set null=True for default as null

    language_preferences = models.CharField(max_length=100, choices=[
        ('English', 'English'),
        ('Spanish', 'Spanish'),
        ('French', 'French'),
        ('Mandarin', 'Mandarin'),
        ('Italian', 'Italian'),
        ('Hindi', 'Hindi')
    ], blank=True, null=True)  # Set null=True for default as null

    budget_range = models.CharField(max_length=100, choices=[
        ('Budget', 'Budget'),
        ('Moderate', 'Moderate'),
        ('Luxury', 'Luxury')
    ], blank=True, null=True)  # Set null=True for default as null

    special_interests = models.CharField(max_length=100, choices=[
        ('History', 'History'),
        ('Art', 'Art'),
        ('Photography', 'Photography'),
        ('Adventure Sports', 'Adventure Sports'),
        ('Wildlife/Nature', 'Wildlife/Nature'),
        ('Wine Tasting', 'Wine Tasting')
    ], blank=True, null=True)  # Set null=True for default as null

    def __str__(self):
        return f'Preferences for {self.userprofile.user.username}'



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    date_of_birth = models.DateField()
    interested_places = models.ManyToManyField(Place)
    preferences = models.OneToOneField(UserPreferences, on_delete=models.CASCADE, null=True, blank=True)

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
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
