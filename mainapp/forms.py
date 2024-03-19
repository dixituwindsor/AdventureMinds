from django import forms
from .models import UserProfile, UserPreferences, Trip, PreferenceChoice, TripPreference
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserPreferences, PreferenceCategory
from multiupload.fields import MultiFileField
from .models import Trip

from mainapp.consumers import User
from mainapp.models import UserProfile, PreferenceCategory, UserPreferences, PreferenceChoice


class UserPreferencesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial_data = kwargs.pop('initial', {})
        super(UserPreferencesForm, self).__init__(*args, **kwargs)

        # Dynamically generate fields for each preference category
        categories = PreferenceCategory.objects.all()
        for category in categories:
            choices = category.preferencechoice_set.all()
            field_name = category.name
            self.fields[field_name] = forms.ModelMultipleChoiceField(
                queryset=choices,
                widget=forms.CheckboxSelectMultiple,
                required=False  # Make fields not required
            )
            # Modify choice labels to remove category name
            self.fields[field_name].label_from_instance = lambda obj: obj.value

            # Set initial values based on fetched data
            initial_values = initial_data.get(field_name, [])
            self.initial[field_name] = initial_values  # Use choice objects directly

    class Meta:
        model = UserPreferences
        fields = []  # No need to specify fields as they are dynamically generated



class AddTripForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    photos = MultiFileField(min_num=1, max_num=10, max_file_size=1024*1024*5)

    class Meta:
        model = Trip
        fields = ['place', 'start_date', 'end_date', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        trip = super().save(commit=False)
        trip.uploader = self.user
        if commit:
            trip.save()
        return trip

class TripPreferenceForm(forms.ModelForm):
    class Meta:
        model = TripPreference
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = PreferenceCategory.objects.all()
        for category in categories:
            choices = PreferenceChoice.objects.filter(category=category)
            choices_list = [(choice.pk, choice.value) for choice in choices]
            self.fields[f'{category.name}'] = forms.MultipleChoiceField(
                choices=choices_list,
                widget=forms.CheckboxSelectMultiple,
                label=category.name
            )


class TripSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


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