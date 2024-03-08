from django import forms
from .models import UserProfile, UserPreferences
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



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

# class SignupForm(UserCreationForm):
#     class Meta:
#         model = User
#         # fields = ['username', 'password1', 'password2']
#         fields = '__all__'

# class SignUpForm(forms.Form):
#     username = forms.CharField()
#     firstname = forms.CharField()
#     lastname = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     email = forms.EmailField()
class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    email = forms.EmailField()
    phone_no = forms.CharField(max_length = 20)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    # third_password = forms.CharField(widget=forms.PasswordInput)