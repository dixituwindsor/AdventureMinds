from django import forms
from .models import UserProfile, UserPreferences, Trip, PreferenceChoice, TripPreference
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserPreferences, PreferenceCategory
from multiupload.fields import MultiFileField
from .models import Trip

# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']
#         labels = {
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'username': 'Username',
#             'email': 'Email',
#             'password': 'Password'
#         }
#         widgets = {
#             'password': forms.PasswordInput()
#         }
#     phone_number = forms.CharField(label='Phone Number')
#     address = forms.CharField(label='Address')
#     date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))

    # def save(self, commit=True):
    #         user = super(SignupForm, self).save(commit=False)
    #         user.password = make_password(self.cleaned_data['password'])
    #         if commit:
    #             user.save()
    #         return user

# class LoginForm(forms.Form):
#     username = forms.CharField(label='Username')
#     password = forms.CharField(widget=forms.PasswordInput, label='Password')


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