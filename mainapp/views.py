from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import UserProfile, User, UserPreferences, PreferenceCategory, Trip, TripPreference, PreferenceChoice, \
    TripPhoto, Thread, ChatMessage
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .forms import UserProfileForm, UserPreferencesForm, AddTripForm, TripPreferenceForm, TripSearchForm, \
    ForgotPasswordForm


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
            response = render(request, 'mainapp/trip_list.html', {'trips': trips, 'saved_searches': saved_searches, 'query': query})
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
    #jaccard similarity
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



# Create your views here.
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


@login_required
def homepage(request):
    return render(request, "mainapp/homepage1.html")


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


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            form = ForgotPasswordForm()
            username = form.cleaned_data['username'].lower()

            if User.objects.get(username=username) is not None:
                userProgileObj = UserProfile.objects.get(username=username)
                if (userProgileObj.email == form.cleaned_data['email']
                    and userProgileObj.phone_number[-3:] == form.cleaned_data['last_three_digits_of_phone_number']
                    and userProgileObj.date_of_birth == form.cleaned_data['date_of_birth']):
                        # login form with message 'password changed sucessfully can be passed'
                        return redirect('mainapp:login')
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
            return render(request, 'registration/forgot_password.html', {'form': form, 'msg':'Something went wrong try again'})

    else:
        form = ForgotPasswordForm()
        return render(request, 'registration/forgot_password.html', {'form': form})

