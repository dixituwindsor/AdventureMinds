
import os
from random import shuffle
from uuid import uuid4

import django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic.detail import DetailView

from .forms import *
from .models import *


# sign up page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.username = form.cleaned_data['username'].lower()
            if User.objects.filter(username=user_obj.username).exists():
                form = SignupForm()
                return render(request, 'registration/signup.html',
                              {'form': form, 'msg': 'username already taken, use different one'})

            if User.objects.filter(email=user_obj.email).exists():
                form = SignupForm()
                return render(request, 'registration/signup.html', {'form': form, 'msg': 'Use different email id'})

            user_obj.password = make_password(form.cleaned_data['password'])
            user_obj.save()
            user_profile_obj = UserProfile()
            user_profile_obj.user = user_obj
            user_profile_obj.phone_number = form.cleaned_data['phone_number']
            user_profile_obj.address = form.cleaned_data['address']
            user_profile_obj.date_of_birth = form.cleaned_data['date_of_birth']
            user_profile_obj.save()
            return redirect('mainapp:login')
        else:
            form = SignupForm()
            return render(request, 'registration/signup.html', {'form': form, 'msg': 'Something went wrong, try again with different username'})
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
                login(request, user)
                return redirect('mainapp:homepage')
            else:
                form = LoginForm()
                return render(request, 'registration/login.html',
                              {'form': form, 'msg': 'Wrong credentials provided, try again'})
        else:
            form = LoginForm()
            return render(request, 'registration/login.html', {'form': form, 'msg': 'Something went wrong, try again'})
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('mainapp:login')

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            if User.objects.get(username=username):
                user_obj = User.objects.get(username=username)
                user_profile_obj = UserProfile.objects.get(user=user_obj)
                if (user_obj.email == form.cleaned_data['email']
                        and user_profile_obj.phone_number[-3:] == form.cleaned_data['last_three_digits_of_phone_number']
                        and user_profile_obj.date_of_birth == form.cleaned_data['date_of_birth']):

                    if(form.cleaned_data['new_password'] == form.cleaned_data['confirm_password']):
                        user_obj.password = make_password(form.cleaned_data['new_password'])
                        user_obj.save()
                        return redirect('mainapp:login')
                    else:
                        form = ForgotPasswordForm()
                        return render(request, 'registration/forgot_password.html',
                                      {'form': form, 'msg': 'Both password did not match'})
                else:
                    form = ForgotPasswordForm()
                    return render(request, 'registration/forgot_password.html',
                                  {'form': form, 'msg': 'Verification details did not match'})

            else:
                form = ForgotPasswordForm()
                return render(request, 'registration/forgot_password.html',
                              {'form': form, 'msg': 'Username not found'})
        else:
            form = ForgotPasswordForm()
            return render(request, 'registration/forgot_password.html',
                          {'form': form, 'msg': 'Something went wrong try again'})

    else:
        form = ForgotPasswordForm()
        return render(request, 'registration/forgot_password.html', {'form': form})


@login_required
def user_profile(request):
    user_profile_instance, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile_instance)
        if form.is_valid():
            print(form.cleaned_data)
            if 'profile_photo' in request.FILES:
                file_name = str(uuid4()) + os.path.splitext(request.FILES['profile_photo'].name)[1]
                form.instance.profile_photo.name = 'profile/' + file_name
            form.save()
            django.contrib.messages.success(request, 'Profile updated successfully.')
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
            if user_profile_instance:
                preferences = UserPreferences.objects.create(user_profile=user_profile_instance)
                for category_name, choices in cleaned_data.items():
                    category = PreferenceCategory.objects.get(name=category_name)
                    preferences.preferences.add(*choices)
                user_profile_instance.preferences = preferences
                user_profile_instance.save()

            return redirect(reverse('mainapp:profile'))
    else:
        existing_preferences = None
        if user_profile_instance and user_profile_instance.preferences:
            existing_preferences = user_profile_instance.preferences.get_selected_preferences()

        form = UserPreferencesForm(instance=user_profile_instance.preferences,
                                   initial={'existing_preferences': existing_preferences})

    return render(request, 'mainapp/userPreferences.html',{'form': form, 'existing_preferences': existing_preferences})


def homepage(request):
    template = "mainapp/homepage1.html"
    context = {}
    return render(request=request, template_name=template, context=context)


def terms_conditions(request):
    template = "mainapp/terms_conditions.html"
    context = {}
    return render(request=request, template_name=template, context=context)


@login_required
def add_trip(request):
    if request.method == 'POST':
        trip_form = AddTripForm(request.POST, request.FILES, user=request.user)
        preference_form = TripPreferenceForm(request.POST)
        if trip_form.is_valid() and preference_form.is_valid():

            # Print form data for debugging
            print("Trip Form Data:", request.POST)
            print("Trip Form Files:", request.FILES)
            print("Trip Form Errors:", trip_form.errors)
            print("Preference Form Errors:", preference_form.errors)
            # Save the trip data
            trip = trip_form.save(commit=False)
            trip.uploader = request.user

            # Create a new TripPreference object
            trip_preference = TripPreference.objects.create()

            # Retrieve the selected preference choices from the form data
            selected_preferences = [int(choice_id) for field in preference_form.cleaned_data.values() for choice_id in
                                    field]

            # Get the PreferenceChoice objects corresponding to the selected preference choices
            preferences = PreferenceChoice.objects.filter(id__in=selected_preferences)

            # Associate preferences with the TripPreference object
            trip_preference.preferences.set(preferences)

            # Link the TripPreference object to the Trip object
            trip.preferences = trip_preference

            # Save the Trip object
            trip.save()

            # Save uploaded photos
            for photo in request.FILES.getlist('photos'):
                trip_photo = TripPhoto(trip=trip, photo=photo)
                trip_photo.save()

            return redirect('mainapp:homepage')  # Redirect to some success URL
    else:
        trip_form = AddTripForm(user=request.user)
        preference_form = TripPreferenceForm()
    return render(request, 'mainapp/add_trip.html', {'trip_form': trip_form, 'preference_form': preference_form})


def trip_list(request):
    if request.user.is_authenticated:
        # For logged-in users
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if not user_profile.preferences:
            return redirect('mainapp:user_preferences')

        user_preferences = user_profile.preferences.preferences.prefetch_related('preferences')

        trips = Trip.objects.all()

        # Apply search filter if query parameter exists
        query = request.GET.get('query')
        if query:
            trips = trips.filter(Q(place__name__icontains=query) | Q(place__address__icontains=query))

        # Sorting
        sort_by = request.GET.get('sort_by')
        if sort_by == 'recommendation':
            # Calculate similarity scores for each trip
            similarity_scores = {}
            for trip in trips:
                # Get the TripPreference associated with the trip
                trip_preference = trip.preferences
                if trip_preference:
                    similarity_score = calculate_similarity(user_preferences,
                                                            trip_preference.preferences.prefetch_related('preferences'))
                    similarity_scores[trip.id] = similarity_score

            # Sort trips based on similarity scores
            trips = sorted(trips, key=lambda x: similarity_scores.get(x.id, 0), reverse=True)
        elif sort_by == 'alphabetical':
            trips = trips.order_by('place__name')

        # Retrieve saved searches from cookies
        saved_searches = request.COOKIES.get('saved_searches', '').split('|')

        # Handle search query
        if query:
            # Save the search query to cookies
            saved_searches.append(query)
            saved_searches = list(set(saved_searches))[-5:]  # Limit to last 5 unique queries
            response = render(request, 'mainapp/trip_list.html',
                              {'trips': trips, 'saved_searches': saved_searches, 'query': query})
            response.set_cookie('saved_searches', '|'.join(saved_searches), max_age=3600)  # Save for 1 hour
            return response

        return render(request, 'mainapp/trip_list.html', {'trips': trips, 'saved_searches': saved_searches})
    else:
        # For guest users
        trips = Trip.objects.all()
        return render(request, 'mainapp/guest_trip_list.html', {'trips': trips})


def calculate_similarity(user_preferences, trip_preferences):
    user_pref_set = set(user_preferences.values_list('id', flat=True))
    trip_pref_set = set(trip_preferences.values_list('id', flat=True))
    # jaccard similarity
    intersection = len(user_pref_set.intersection(trip_pref_set))
    union = len(user_pref_set.union(trip_pref_set))

    if union == 0:
        return 0.0

    jaccard_similarity = intersection / union

    return jaccard_similarity


def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    return render(request, 'mainapp/trip_detail.html', {'trip': trip})


def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'mainapp/view_profile.html', {'profile_user': profile_user})








def message_button(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        second_person = get_object_or_404(User, id=user_id)
        second_person_obj = UserProfile.objects.get(user=second_person)
        first_person = request.user
        first_person_obj = UserProfile.objects.get(user=first_person)

        if first_person_obj != second_person_obj:
            chat, created = UserChat.objects.get_or_create(
                first_person=first_person_obj,
                second_person=second_person_obj,
            )
            return redirect('mainapp:messages')
        else:
            return redirect('mainapp:messages')


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


class Thread:
    pass


@login_required
def messages(request):

    user_profile = UserProfile.objects.get(user=request.user)
    last_active_userchat_id = request.session.get('last_active_userchat_id')
    userchats = UserChat.objects.filter(Q(first_person=user_profile) | Q(second_person=user_profile) | Q(group__members=user_profile)).prefetch_related('chatmessage_userchat').order_by('timestamp').distinct()

    context = {
        'userchats': userchats,
        'last_active_userchat_id': last_active_userchat_id
    }

    return render(request, 'mainapp/messages.html', context)

@login_required
def set_last_active_userchat_id(request):
    userchat_id = request.POST.get('userchat_id')
    request.session['last_active_userchat_id'] = userchat_id
    return JsonResponse({'status': 'success'})


def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        selected_users = request.POST.getlist('selected_users')

        group = ChatGroup.objects.create(name=group_name)
        first_person = request.user
        user_profile = UserProfile.objects.get(user=first_person)
        group.members.add(user_profile)

        if len(selected_users) < 1:
            return HttpResponse("<h1>Please select At least one user.</h1>")

        for selected_user in selected_users:
            profile = UserProfile.objects.get(user=selected_user)
            group.members.add(profile)

        chat, created = UserChat.objects.get_or_create(
            first_person=user_profile,
            group_id=group.id,
        )

        django.contrib.messages.success(request, 'Group created successfully.')

        return redirect('mainapp:messages')
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        userchats = UserChat.objects.filter(Q(first_person=user_profile) | Q(second_person=user_profile) | Q(group__members=user_profile)).prefetch_related('chatmessage_userchat').order_by('timestamp')
        context = {
            'userchats': userchats
        }
        return render(request, 'mainapp/create_group.html', context)


@require_POST
@csrf_exempt
def mark_messages_as_read(request):
    userchat_id = request.POST.get('userchat_id')
    user_id = request.POST.get('user_id')
    if not userchat_id:
        return JsonResponse({'error': 'UserChat ID is required'}, status=400)
    try:
        userchat = UserChat.objects.get(id=userchat_id)
        ChatMessage.objects.filter(userchat=userchat).exclude(user__id=user_id).update(read=True)
        return JsonResponse({'success': True})
    except UserChat.DoesNotExist:
        return JsonResponse({'error': 'UserChat not found'}, status=404)

@login_required(login_url='mainapp:login')
def add_trip(request):
    if request.method == 'POST':
        trip_form = AddTripForm(request.POST, request.FILES, user=request.user)
        preference_form = TripPreferenceForm(request.POST)
        print("POST request received")
        if trip_form.is_valid() and preference_form.is_valid():
            print("Forms are valid")
            trip = trip_form.save(commit=False)
            trip.uploader = request.user
            trip.save()

            trip_preference = preference_form.save(commit=False)
            trip_preference.save()

            selected_preferences = [int(choice_id) for field in preference_form.cleaned_data.values() for choice_id in field]
            preferences = PreferenceChoice.objects.filter(id__in=selected_preferences)
            trip_preference.preferences.set(preferences)
            trip.preferences = trip_preference
            trip.save()

            for photo in request.FILES.getlist('photos'):
                trip_photo = TripPhoto(trip=trip, photo=photo)
                trip_photo.save()


            return redirect('mainapp:homepage')  # Redirect to some success URL
        else:
            print("Trip form errors:", trip_form.errors)
            print("Preference form errors:", preference_form.errors)
    else:
        trip_form = AddTripForm(user=request.user)
        preference_form = TripPreferenceForm()

    return render(request, 'mainapp/add_trip.html', {'trip_form': trip_form, 'preference_form': preference_form})


from django.db.models import Avg


@login_required
def trip_list(request):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        if not user_profile.preferences:
            return redirect('mainapp:user_preferences')
        user_preferences = user_profile.preferences.preferences.prefetch_related('preferences')
        trips = Trip.objects.all()
        query = request.GET.get('query')
        if query:
            trips = trips.filter(Q(place__name__icontains=query) | Q(place__address__icontains=query) | Q(
                place__description__icontains=query))

        if 'my_trips' in request.GET:
            trips = trips.filter(uploader=request.user)

        sort_by = request.GET.get('sort_by')
        if sort_by == 'recommendation':
            similarity_scores = {}
            for trip in trips:
                trip_preference = trip.preferences
                if trip_preference:
                    similarity_score = calculate_similarity(user_preferences,
                                                            trip_preference.preferences.prefetch_related('preferences'))
                    similarity_scores[trip.id] = similarity_score

            trips = sorted(trips, key=lambda x: similarity_scores.get(x.id, 0), reverse=True)
        elif sort_by == 'alphabetical':
            trips = trips.order_by('place__name')

        saved_searches = request.COOKIES.get('saved_searches', '').split('|')

        if query:
            saved_searches.append(query)
            saved_searches = list(set(saved_searches))[-5:]  # Limit to last 5 unique queries
            response = render(request, 'mainapp/homepage2.html',
                              {'trips': trips, 'saved_searches': saved_searches, 'query': query})
            response.set_cookie('saved_searches', '|'.join(saved_searches), max_age=3600 * 24 * 7)  # Save for 1 week
            return response


        return render(request, 'mainapp/homepage2.html', {'trips': trips, 'saved_searches': saved_searches})
    else:
        trips = Trip.objects.all()
        return render(request, 'mainapp/guest_trip_list.html', {'trips': trips})


def calculate_similarity(user_preferences, trip_preferences):
    user_pref_set = set(user_preferences.values_list('id', flat=True))
    trip_pref_set = set(trip_preferences.values_list('id', flat=True))
    #jaccard similarity
    intersection = len(user_pref_set.intersection(trip_pref_set))
    union = len(user_pref_set.union(trip_pref_set))

    if union == 0:
        return 0.0

    jaccard_similarity = intersection / union

    return jaccard_similarity



def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    photo = TripPhoto.objects.all()
    join_request = None

    average_rating = Rating.objects.filter(place=trip.place).aggregate(Avg('rating'))['rating__avg']
    trip.average_rating = round(average_rating, 1) if average_rating else None
    reviews = list(Review.objects.filter(place=trip.place))
    shuffle(reviews)
    trip.reviews = reviews
    if request.user.is_authenticated:
        join_request = JoinRequest.objects.filter(trip=trip, user=request.user).first()
    return render(request, 'mainapp/trip_detail.html', {'trip': trip, 'join_request': join_request, 'photo': photo})


def view_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    return render(request, 'mainapp/view_profile.html', {'profile_user': profile_user})



@login_required
def join_trip(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    user = request.user

    existing_request = JoinRequest.objects.filter(trip=trip, user=user).exists()
    if existing_request:
        django.contrib.messages.warning(request, "You have already requested to join this trip.")
        return redirect('mainapp:trip_detail', trip_id=trip_id)

    join_request = JoinRequest.objects.create(trip=trip, user=user, status='pending')
    django.contrib.messages.success(request, "Your join request has been submitted successfully.")
    return redirect('mainapp:trip_detail', trip_id=trip_id)


def accept_join_request(request, trip_id, request_id):
    trip = get_object_or_404(Trip, id=trip_id)
    join_request = get_object_or_404(JoinRequest, id=request_id)
    trip.participants.add(join_request.user)
    join_request.delete()

    return redirect('mainapp:trip_detail', trip_id=trip_id)


def decline_join_request(request, trip_id, request_id):
    join_request = get_object_or_404(JoinRequest, id=request_id)
    join_request.delete()
    return redirect('mainapp:trip_detail', trip_id=trip_id)


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'mainapp/contact_us.html')
    else:
        form = ContactForm()
        return render(request, 'mainapp/contact_us.html', {'form': form})


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'mainapp/place_detail.html'
    context_object_name = 'trip'



# @login_required
def add_rating_and_review(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    user = request.user

    user_rating = Rating.objects.filter(place=place, user=user).first()
    user_review = Review.objects.filter(place=place, user=user).first()

    rating_form = RatingForm(instance=user_rating)
    review_form = ReviewForm(instance=user_review)

    if request.method == 'POST':
        rating_form = RatingForm(request.POST, instance=user_rating)
        review_form = ReviewForm(request.POST, instance=user_review)

        if rating_form.is_valid() and review_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = user
            rating.place = place
            rating.save()

            review = review_form.save(commit=False)
            review.user = user
            review.place = place
            review.save()

            return redirect('mainapp:user_trip_history')

    return render(request, 'mainapp/add_rating_and_review.html', {
        'rating_form': rating_form,
        'review_form': review_form,
        'place': place,
        'user_rating': user_rating,
        'user_review': user_review,
    })


@login_required
def user_trip_list(request):
    current_user = request.user
    current_date = timezone.now().date()
    upcoming_trips = Trip.objects.filter(participants=current_user, start_date__gt=current_date)
    past_trips = Trip.objects.filter(participants=current_user, end_date__lt=current_date)
    context = {
        'upcoming_trips': upcoming_trips,
        'past_trips': past_trips,
        'current_date': current_date,
    }
    return render(request, 'mainapp/user_trip_history.html', context)