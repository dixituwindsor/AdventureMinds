from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Trip, Photo, UserPreferences


# class SignupForm(UserCreationForm):
#     class Meta:
#         model = User
#         # fields = ['username', 'password1', 'password2']
#         fields = '__all__'

class SignupForm(forms.Form):
    firstname = forms.CharField()
    lastname = forms.CharField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

# class SignupForm(UserCreationForm):
#     username = forms.CharField(max_length=20)
#     email = forms.EmailField()
#     phone_no = forms.CharField(max_length = 20)
#     first_name = forms.CharField(max_length = 20)
#     last_name = forms.CharField(max_length = 20)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'phone_no', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Trip
        fields = ['source_place', 'destination_place', 'date_of_trip', 'days_of_travel',
                  'travel_style', 'activities', 'transportation', 'meal', 'language',
                  'special_interests', 'accommodation', 'budget', 'photos']

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(TripForm, self).__init__(*args, **kwargs)
        if user_profile:
            self.instance.set_travel_style_choices(user_profile)
            self.instance.set_activities_choices(user_profile)
            self.instance.set_transportation_choices(user_profile)
            self.instance.set_meal_choices(user_profile)
            self.instance.set_language_choices(user_profile)
            self.instance.set_special_interests_choices(user_profile)
            self.instance.set_accommodation_choices(user_profile)

            self.fields['travel_style'].choices = [(self.instance.travel_style, self.instance.travel_style)]
            self.fields['activities'].choices = [(choice, choice) for choice in self.instance.activities.split(',')]
            self.fields['transportation'].choices = [(choice, choice) for choice in self.instance.transportation.split(',')]
            self.fields['meal'].choices = [(choice, choice) for choice in self.instance.meal.split(',')]
            self.fields['language'].choices = [(choice, choice) for choice in self.instance.language.split(',')]
            self.fields['special_interests'].choices = [(choice, choice) for choice in self.instance.special_interests.split(',')]
            self.fields['accommodation'].choices = [(choice, choice) for choice in self.instance.accommodation.split(',')]
