from django import forms
from .models import UserProfile, UserPreferences
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserPreferences, PreferenceCategory


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
