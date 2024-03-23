from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroups, Message, UserProfile
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, SignupForm, LoginForm
from .models import UserProfile, Trip, Wishlist
from datetime import datetime

# Create your views here.

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

# remove START CODE
def trip_details(request):
    trips = Trip.objects.all()
    return render(request, 'mainapp/test.html', {'trips': trips})

# END CODE

def add_or_remove_wishlist(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        user_id = request.user.id
        trip_id = get_object_or_404(Trip, id=int(trip_id))
        user_id = get_object_or_404(UserProfile, id=int(33))

        # Check if the item is already in the wishlist
        try:
            wishlist_item = Wishlist.objects.get(trip_id=trip_id, user_id=user_id)
            wishlist_item.delete()
            message = 'Item removed from wishlist successfully.'
            action = 'remove'
        except Wishlist.DoesNotExist:
            # If the item is not in the wishlist, add it
            wishlist_id = Wishlist.objects.create(trip_id=trip_id, user_id=user_id, notes="")

            message = 'Item added to wishlist successfully.'
            action = 'add'

        # Get updated wishlist items

        return JsonResponse({'success': True, 'message': message, 'action': action})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def view_wishlist(request):
    # user_id = request.user.id
    if request.method == 'POST':
        wishlist_id = request.POST.get('wishlist_id')
        if wishlist_id:
            # breakpoint()
            wishlist_item = Wishlist.objects.get(id=int(wishlist_id))
            wishlist_item.delete()
            # return redirect('wishlist')

    user_id = get_object_or_404(UserProfile, id=int(33))
    wishlist_items = Wishlist.objects.filter(user_id=user_id)
    return render(request, 'mainapp/wishlist.html', {'wishlist_items': wishlist_items})


def view_calendar(request):
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if start_date_str and end_date_str:
            try:
                # start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                # end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

                trips = Trip.objects.filter(start_date__gte=start_date_str, end_date__lte=end_date_str)

                return render(request, 'mainapp/calendar.html', {'trips': trips})
            except ValueError:
                error_message = 'Invalid date format. Please use YYYY-MM-DD.'
        else:
            trips = Trip.objects.all()
            return render(request, 'mainapp/calendar.html', {'trips': trips})

    return render(request, 'mainapp/calendar.html', context={'trips': []})