import os

from django.db.models import Q

from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import UserProfileForm, UserPreferencesForm, AddTripForm, TripPreferenceForm
from uuid import uuid4
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Place, Rating, Review, User, UserPreferences, PreferenceCategory, ChatGroup, ChatMessage, \
    TripPreference, PreferenceChoice, TripPhoto, Trip, JoinRequest
from django.contrib.auth import authenticate, login, logout
from .forms import  ReviewForm, RatingForm
from .models import UserProfile
from django.views.generic.detail import DetailView

@login_required
def user_profile(request):
    user_profile_instance, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile_instance)
        if form.is_valid():
            # Check if 'profile_photo' exists in request.FILES
            if 'profile_photo' in request.FILES:
                # Generate a unique filename
                file_name = str(uuid4()) + os.path.splitext(request.FILES['profile_photo'].name)[1]
                # Assign the unique filename to the profile_photo field
                form.instance.profile_photo.name = 'profile/' + file_name
            # Print form data before saving
            print(form.cleaned_data)
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('mainapp:profile')
    else:
        form = UserProfileForm(instance=user_profile_instance)
        user_profile_instance.user = request.user  # Set the user attribute


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
        # Retrieve user's existing preferences if they exist
        existing_preferences = user_profile_instance.preferences.get_selected_preferences() if user_profile_instance else None
        print("Existing Preferences:", existing_preferences)  # Print existing preferences for debugging
        # Pass existing preferences to the form
        form = UserPreferencesForm(instance=user_profile_instance.preferences, initial={'existing_preferences': existing_preferences})

    return render(request, 'mainapp/userPreferences.html',{'form': form, 'existing_preferences': existing_preferences})


def homepage(request):
    template = "mainapp/homepage2.html"
    context = {}
    return render(request=request, template_name=template, context=context)
    # Pass existing preferences to the template context


def terms_conditions(request):
    template = "mainapp/terms_conditions.html"
    context = {}
    return render(request=request, template_name=template, context=context)


# signup page
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

def message_button(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        second_person = get_object_or_404(User, id=user_id)
        first_person = request.user
        if first_person != second_person:
            thread, created = Thread.objects.get_or_create(
                first_person=first_person,
                second_person=second_person,
            )
            return redirect('mainapp:messages')
        else:
            return redirect('mainapp:messages')

def getusers(request):
    users = UserProfile.objects.all().values('username', 'id')
    return JsonResponse(list(users), safe=False)


class Thread:
    pass


@login_required
def messages(request):
    threads = Thread.objects.filter(Q(first_person=request.user) | Q(second_person=request.user) | Q(group__members=request.user)).prefetch_related('chatmessage_thread').order_by('timestamp').distinct()

    context = {
        'Threads': threads
    }
    return render(request, 'mainapp/messages.html', context)


def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        selected_users = request.POST.getlist('selected_users')

        group = ChatGroup.objects.create(name=group_name)
        group.members.add(request.user)
        group.members.add(*selected_users)

        first_person = request.user
        thread, created = Thread.objects.get_or_create(
            first_person=first_person,
            group_id=group.id,
        )

        return redirect('mainapp:messages')
    else:
        threads = Thread.objects.filter(Q(first_person=request.user) | Q(second_person=request.user) | Q(group__members=request.user)).prefetch_related('chatmessage_thread').order_by('timestamp')
        context = {
            'Threads': threads
        }
        return render(request, 'mainapp/create_group.html', context)


@require_POST
@csrf_exempt
def mark_messages_as_read(request):
    thread_id = request.POST.get('thread_id')
    user_id = request.POST.get('user_id')
    if not thread_id:
        return JsonResponse({'error': 'Thread ID is required'}, status=400)
    try:
        thread = Thread.objects.get(id=thread_id)
        ChatMessage.objects.filter(thread=thread).exclude(user__id=user_id).update(read=True)
        return JsonResponse({'success': True})
    except Thread.DoesNotExist:
        return JsonResponse({'error': 'Thread not found'}, status=404)

####Chirag
####

def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    join_request = None
    if request.user.is_authenticated:
        join_request = JoinRequest.objects.filter(trip=trip, user=request.user).first()
    return render(request, 'mainapp/trip_detail.html', {'trip': trip, 'join_request': join_request})


def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'mainapp/view_profile.html', {'profile_user': profile_user})



@login_required
def join_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    user = request.user

    # Check if the user has already requested to join the trip
    existing_request = JoinRequest.objects.filter(trip=trip, user=user).exists()
    if existing_request:
        messages.warning(request, "You have already requested to join this trip.")
        return redirect('mainapp:trip_detail', trip_id=trip_id)

    # Create a new join request
    join_request = JoinRequest.objects.create(trip=trip, user=user, status='pending')
    messages.success(request, "Your join request has been submitted successfully.")
    return redirect('mainapp:trip_detail', trip_id=trip_id)


def accept_join_request(request, trip_id, request_id):
    trip = get_object_or_404(Trip, id=trip_id)
    join_request = get_object_or_404(JoinRequest, id=request_id)

    # Add the user to the trip participants
    trip.participants.add(join_request.user)

    # Delete the join request
    join_request.delete()

    return redirect('mainapp:trip_detail', trip_id=trip_id)


def decline_join_request(request, trip_id, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id)

    # Delete the join request
    join_request.delete()

    return redirect('mainapp:trip_detail', trip_id=trip_id)


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'mainapp/place_detail.html'
    context_object_name = 'trip'

# @login_required
def add_review(request, place_id):
    place = Place.objects.get(id=place_id)
    reviews = Review.objects.filter(place=place)
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            reviews = review_form.save(commit=False)
            reviews.User = request.User
            reviews.place = place
            reviews.save()
            return redirect('mainapp:add_review', place_id=place.id)

    return render(request, 'mainapp/add_review.html', {'review_form': review_form, 'trip': place, 'review': reviews})

# @login_required
def add_rating(request, place_id):
    place = Place.objects.get(id=place_id)
    rating = Rating.objects.filter(place=place)
    rating_form = RatingForm()

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.place = place
            rating.save()
            return redirect('place_detail', place_id=place.id)

    return render(request, 'mainapp/add_rating.html', {'rating_form': rating_form, 'place': place, 'rating': rating})
