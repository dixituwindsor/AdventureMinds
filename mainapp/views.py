from django.contrib.auth.hashers import make_password
from django.urls import reverse
from .models import UserPreferences, PreferenceCategory
from .forms import UserProfileForm, UserPreferencesForm, AddTripForm

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from .models import UserProfile, Thread, User, ChatMessage



# Create your views here.

@login_required
def user_profile(request):
    user_profile_instance, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile_instance)
        if form.is_valid():
            form.save()
            return redirect('mainapp:profile')
    else:
        form = UserProfileForm(instance=user_profile_instance)
    return render(request, 'mainapp/profile.html', {'form': form})


@login_required
def user_preferences(request):
    user = request.user
    try:
        user_profile_instance = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile_instance = None

    if request.method == 'POST':
        form = UserPreferencesForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print("Cleaned form data:", cleaned_data)  # Print cleaned form data

            preferences = UserPreferences.objects.create(user_profile=user_profile_instance)
            for category_name, choices in cleaned_data.items():
                category = PreferenceCategory.objects.get(name=category_name)
                preferences.preferences.add(*choices)

            return redirect(reverse('mainapp:profile'))
    else:
        form = UserPreferencesForm(instance=user_profile_instance.preferences)
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

# sign in
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # form.save()
            # commit false to save current object in db
            userobj = form.save(commit=False)
            # making some necessary change in obj then saving it in db
            userobj.username = form.cleaned_data['username'].lower()
            if UserProfile.objects.filter(username=userobj.username).exists():
                form = SignupForm()
                return render(request, 'mainapp/signup.html', {'form': form, 'msg':'username already taken, use different one'})

            if UserProfile.objects.filter(username=userobj.email).exists():
                form = SignupForm()
                return render(request, 'mainapp/signup.html', {'form': form, 'msg': 'Use different email id'})

            userobj.email = form.cleaned_data['email'].lower()
            userobj.password = make_password(form.cleaned_data['password'])
            userobj.save()
            return redirect('mainapp:login')
        else:
            form = SignupForm()
            return render(request, 'mainapp/signup.html', {'form': form, 'msg':'Something went wrong, try again'})
    else:
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

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('mainapp:homepage')
                    # return redirect('mainapp:chat_app')
                else:
                    form = LoginForm()
                    return render(request, 'mainapp/login.html',
                                  {'form': form, 'msg': 'user account is inactive'})
            else:
                form = LoginForm()
                return render(request, 'mainapp/login.html', {'form': form, 'msg': 'Wrong credentials provided, try again'})
        else:
            form = LoginForm()
            return render(request, 'mainapp/login.html', {'form': form, 'msg': 'Something went wrong, try again'})
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('mainapp:login')


@login_required
def add_trip(request):
    if request.method == 'POST':
        form = AddTripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.uploader = request.user
            trip.save()
            return redirect('mainapp:homepage')  # Assuming 'home' is the name of your home page URL
    else:
        form = AddTripForm()
    return render(request, 'mainapp/add_trip.html', {'form': form})