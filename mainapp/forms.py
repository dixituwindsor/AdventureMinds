from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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