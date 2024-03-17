from django import forms
from mainapp.models import UserProfile

class SignupForm(forms.ModelForm):
    #defined outsite to provide password widget
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name',  'last_name', 'password', 'email']
    # def save(self, commit=True):
    #     user = super(SignupForm, self).save(commit=False)
    #     user.password = make_password(self.cleaned_data['password'])
    #     if commit:
    #         user.save()
    #     return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)