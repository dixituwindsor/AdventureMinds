from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UserProfile, UserPreferences
from .forms import UserProfileForm, UserPreferencesForm


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
