from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import UserProfileForm, UserPreferencesForm
from .models import UserPreferences, PreferenceCategory
from .models import UserProfile, Thread, User, ChatMessage


# Create your views here.

@login_required
def user_profile(request):
    user_profile_instance, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile_instance)
        if form.is_valid():
            form.save()
            return redirect('mainapp:homepage')
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
            preferences = UserPreferences.objects.create(user_profile=user_profile_instance)
            for category_name, choices in cleaned_data.items():
                category = PreferenceCategory.objects.get(name=category_name)
                preferences.preferences.add(*choices)

            # Assign the created preferences to the UserProfile instance
            user_profile_instance.preferences = preferences
            user_profile_instance.save()

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
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # if User.objects.filter(user__username=username).exists():
        #     response = HttpResponse()
        #     response.write("<p>Username already exists, choose different username</p>")
        #     return response

        names = fullname.split()
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = names[0]
        user.last_name = names[-1]
        user.save()

        userprofileobj = UserProfile.objects.create(user=user)
        userprofileobj.save()

        return redirect('mainapp:login')
    else:
        return render(request, 'registration/signup.html')




# login page
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('mainapp:homepage')
        else:
            response = HttpResponse()
            response.write("<p>Wrong credentials</p>")
            return response
    else:
        return render(request, 'registration/login.html')


# logout page
def user_logout(request):
    logout(request)
    return redirect('mainapp:login')


