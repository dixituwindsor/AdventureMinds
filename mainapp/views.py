from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UserProfile, UserPreferences
from .forms import UserProfileForm, UserPreferencesForm

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, SignupForm, LoginForm

# Create your views here.

def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('mainapp:profile')
    else:
        form = UserProfileForm()
    return render(request, 'mainapp/profile.html', {'form': form})

# def user_profile(request):
#     try:
#         profile = request.user.userprofile
#     except UserProfile.DoesNotExist:
#         profile = None
#
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             user_profile = form.save(commit=False)
#             user_profile.user = request.user
#             user_profile.save()
#             return redirect('mainapp:profile')
#     else:
#         form = UserProfileForm(instance=profile)
#     return render(request, 'mainapp/profile.html', {'form': form})


def user_preferences(request):
    if request.method == 'POST':
        form = UserPreferencesForm(request.POST)
        if form.is_valid():
            preferences = form.save(commit=False)
            preferences.user_profile = request.user.userprofile
            preferences.save()
            return redirect(reverse('mainapp:profile'))
    else:
        form = UserPreferencesForm()
    return render(request, 'mainapp/userPreferences.html', {'form': form})


def messenger(request):
    template = "mainapp/messenger.html"
    context = {}
    return render(request=request, template_name=template, context=context)


# signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # loginForm = LoginForm()
            return redirect('mainapp:login')
            # return render(request, 'login.html', {'form' : loginForm})
        else:
            response = HttpResponse()
            response.write("<p>Something went wrong</p>")
            return response
    else:
        form = UserCreationForm()
        # form = SignUpForm()
        return render(request, 'mainapp/signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('mainapp:home')
            else:
                response = HttpResponse()
                response.write("<p>Wrong credentials</p>")
                return response
    else:
        form = LoginForm()
        return render(request, 'mainapp/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('mainapp:login')

