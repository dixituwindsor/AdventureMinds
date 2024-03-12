from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroups, Message, UserProfile
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, SignupForm, LoginForm, TripForm, TripPhotoForm
from .models import UserProfile, Trip, TripPhoto, UserPreferences

# Create your views here.

@login_required
def add_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        photo_formset = TripPhotoForm(request.POST, request.FILES, prefix='photos')
        if form.is_valid() and photo_formset.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            form.save_m2m()  # Save the many-to-many relationships
            for photo_form in photo_formset:
                if photo_form.cleaned_data.get('photo'):
                    TripPhoto.objects.create(trip=trip, photo=photo_form.cleaned_data['photo'])
            return redirect('mainapp:trip_list')  # Change 'trip_list' to your actual trip list URL name
    else:
        form = TripForm()
        photo_formset = TripPhotoForm(prefix='photos')
    return render(request, 'mainapp/add_trip.html', {'form': form, 'photo_formset': photo_formset})

def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'mainapp/trip_list.html', {'trips': trips})

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

@login_required
def chat_app(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create_group':
            name = request.POST['name']
            group = ChatGroups.objects.create(name=name)
            group.members.add(request.user)
            return redirect('chat_app')
        elif action == 'send_message':
            content = request.POST['content']
            group_id = request.POST.get('group_id')
            recipient_username = request.POST.get('recipient_username')
            if group_id:
                group = ChatGroups.objects.get(id=group_id)
                Message.objects.create(sender=request.user, chat_group=group, content=content)
            elif recipient_username:
                recipient = UserProfile.objects.get(username=recipient_username)
                Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return redirect('chat_app')
    groups = ChatGroups.objects.filter(members=request.user)
    return render(request, 'mainapp/messages.html', {'groups': groups})


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
        return render(request, 'mainapp/signup.html', {'form': form})


# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # user = authenticate(request, username=username, password=password)
            # if user:
            #     login(request, user)
            #     return redirect('mainapp:home')
            if UserProfile.objects.filter(username=username).exists() and UserProfile.objects.filter(username=username).get().password == password :
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
