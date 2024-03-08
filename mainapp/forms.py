from django import forms
from .models import UserProfile, UserPreferences


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'address', 'phone_number', 'email', 'date_of_birth']
        labels = {
            'name': 'Name',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'email': 'Email',
            'date_of_birth': 'Date of Birth'
        }
        widgets = {
            'email': forms.EmailInput(attrs={'type': 'email'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ['travel_style', 'activity_preferences', 'destination_preferences',
                  'accommodation_preferences', 'transportation_preferences', 'meal_preferences',
                  'language_preferences', 'budget_range', 'special_interests']
        labels = {
            'travel_style': 'Travel Style',
            'activity_preferences': 'Activity Preferences',
            'destination_preferences': 'Destination Preferences',
            'accommodation_preferences': 'Accommodation Preferences',
            'transportation_preferences': 'Transportation Preferences',
            'meal_preferences': 'Meal Preferences',
            'language_preferences': 'Language Preferences',
            'budget_range': 'Budget Range',
            'special_interests': 'Special Interests'
        }
