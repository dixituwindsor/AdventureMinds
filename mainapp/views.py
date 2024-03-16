from django.shortcuts import render, redirect
from django.urls import reverse
from .models import UserProfile, UserPreferences
from .forms import UserProfileForm, UserPreferencesForm

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, SignupForm, LoginForm
from .models import UserProfile, Thread, User, ChatMessage


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

def homepage(request):
    template = "mainapp/homepage.html"
    context = {}
    return render(request=request, template_name=template, context=context)

def terms_conditions(request):
    template = "mainapp/terms_conditions.html"
    context = {}
    return render(request=request, template_name=template, context=context)

# def messenger(request):
#     resonse = HttpResponse()
#     resonse.write("<h1>Hello World</h1>")
#     return resonse

def getusers(request):
    users = UserProfile.objects.all().values('username', 'id')
    return JsonResponse(list(users), safe=False)

@login_required
def chat_app(request, user_id=None):
    if user_id:
        # Assuming the logged-in user is the first person in the thread
        first_person = request.user
        second_person = get_object_or_404(User, id=user_id)
        thread, created = Thread.objects.get_or_create(
            first_person=first_person,
            second_person=second_person,
        )
        messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')
        context = {
            'thread': thread,
            'messages': messages,
        }
        return render(request, 'mainapp/messages.html', context)
    else:
        users = User.objects.all()
        context = {'users': users}
        return render(request, 'mainapp/messages.html', context)



# signup page
def user_signup(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        # form = SignupForm(request.POST)
        # if form.is_valid():
        #     user = form.save(commit= False)
        #     user.save()
            # loginForm = LoginForm()
            # return render(request, 'login.html', {'form' : loginForm})

        form = SignupForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if(UserProfile.objects.filter(username=username).exists()):
                response = HttpResponse()
                response.write("<p>Username already exists, choose different username</p>")
                return response

            userprofileobj = UserProfile()
            userprofileobj.firstname = firstname
            userprofileobj.last_name = lastname
            userprofileobj.username = username
            userprofileobj.password = password
            userprofileobj.email = email
            userprofileobj.save()
            return redirect('mainapp:login')
        else:
            response = HttpResponse()
            response.write("<p>Something went wrong</p>")
            return response
    else:
        # form = UserCreationForm()
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})


# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('mainapp:chat_app')
            else:
                response = HttpResponse()
                response.write("<p>Wrong credentials</p>")
                return response
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


# logout page
def user_logout(request):
    logout(request)
    return redirect('mainapp:login')

