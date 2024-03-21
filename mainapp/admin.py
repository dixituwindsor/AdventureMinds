from django.contrib import admin
from .models import UserProfile, Place, Review, Rating, Trip, TripPreference, UserPreferences, PreferenceCategory, PreferenceChoice

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Place)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Trip)
admin.site.register(TripPreference)
admin.site.register(UserPreferences)
admin.site.register(PreferenceChoice)
admin.site.register(PreferenceCategory)
