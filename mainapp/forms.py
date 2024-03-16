from django import forms
from .models import UserProfile, UserPreferences
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'date_of_birth']  # Removed 'email' field

        labels = {
            'phone_number': 'Phone Number',
            'address': 'Address',
            'date_of_birth': 'Date of Birth'
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Add fields from the User model
        if self.instance.user:
            self.fields['username'] = forms.CharField(label='Username', initial=self.instance.user.username, disabled=True)
            self.fields['first_name'] = forms.CharField(label='First Name', initial=self.instance.user.first_name, disabled=True)
            self.fields['last_name'] = forms.CharField(label='Last Name', initial=self.instance.user.last_name, disabled=True)
            self.fields['email'] = forms.EmailField(label='Email', initial=self.instance.user.email, disabled=True, required=False)

    def clean_email(self):
        return self.instance.user.email



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


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email',
            'password': 'Password'
        }
        widgets = {
            'password': forms.PasswordInput()
        }

    phone_number = forms.CharField(label='Phone Number')
    address = forms.CharField(label='Address')
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
