from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroups, Message, UserProfile, Place, TripReview
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, SignupForm, LoginForm, ReviewForm, RatingForm
from .models import UserProfile
from django.views.generic.detail import DetailView



def messenger(request):
    template = "mainapp/messenger.html"
    context = {}
    return render(request=request, template_name=template, context=context)


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

# def destination_detail(request, destination_id):
#     destination = get_object_or_404(Destination, pk=destination_id)
#     reviews = Review.objects.filter(destination=destination)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.destination = destination
#             review.user = request.user  # Assuming user is authenticated
#             review.save()
#             return redirect('destination_detail', destination_id=destination_id)
#     else:
#         form = ReviewForm()
#     return render(request, 'destination_detail.html', {'destination': destination, 'reviews': reviews, 'form': form})



# def trip_detail(request):
#     trip = Trip.objects.filter(trip_date= '2023-01-12').first()
#     reviews = Review.objects.filter(trip=trip)
#     form = ReviewForm()
#
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             #review.user = request.trip.user.userprofile
#             review.trip = trip
#             review.save()
#             return redirect('mainapp:messenger')
#
#     return render(request, 'mainapp/trip_detail.html', {'trip': trip, 'reviews': reviews, 'form': form})

# def trip_info(request,id):
#     trip = Trip.objects.get(pk=id)
#     trips = Trip.objects.filter(trip_date= trip.trip_date).exclude(id=id)
#     reviews = TripReview.objects.filter(trip=trip).order_by("-date")
#
#     average_rating = TripReview.objects.filter(trip=trip).aggregate(rating=Avg('rating'))
#     review_form = ReviewForm()
#
#     context ={
#         't': trip,
#         'trips': trips,
#         'reviews': reviews,
#         'average_rating':average_rating,
#         'review_form':review_form,
#     }
#     return render(request, 'mainapp/trip_info.html',context)
#
# def trip_detail(request, trip_id):
#     trip = get_object_or_404(Trip, pk=trip_id)
#     reviews = TripReview.objects.filter(trip=trip)
#     return render(request, 'mainapp/trip_detail.html', {'trip': trip, 'reviews': reviews})
#
# # def add_review(request,trip_id):
# #     trip = Trip.objects.get(pk=trip_id)
# #     user = request.user
# #
# #     review = TripReview.objects.create(
# #         user=user,
# #         trip=trip,
# #         review=request.POST['review'],
# #         rating=request.POST['rating'],
# #
# #     )
# #
# #     context = {
# #         'user': user.username,
# #         'review': request.POST['review'],
# #         'rating': request.POST['rating'],
# #     }
# #
# #     average_reviews = TripReview.objects.filter(trip=trip).aggregate(rating=Avg('rating'))
# #     # response = {'bool': 'True','context': context,'average_reviews': average_reviews}
# #     return render(request, 'mainapp/trip_info.html', context)
#
#     # return JsonResponse({'bool': True, 'context': context, 'average_reviews': average_reviews})
#
#
# def add_trip(request):
#     # Example data
#     trip_data = {
#         'name': 'Trip to Rome',
#         'description': 'An adventure in Italy'
#     }
#
#     # Create and save a new trip
#     trip = Trip(**trip_data)
#     # trip.save()
#
#     return HttpResponse("Trip added successfully")

class PlaceDetailView(DetailView):
    model = Place
    template_name = 'mainapp/place_detail.html'

# @login_required
def add_review(request, place_id):
    place = Place.objects.get(id=place_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.place = place
            review.save()
            return redirect('place_detail', place_id=place.id)
    else:
        form = ReviewForm()
    return render(request, 'mainapp/add_review.html', {'form': form, 'place': place})

# @login_required
def add_rating(request, place_id):
    place = Place.objects.get(id=place_id)
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.place = place
            rating.save()
            return redirect('place_detail', place_id=place.id)
    else:
        rating_form = RatingForm()
    return render(request, 'mainapp/add_review.html', {'rating_form': rating_form, 'place': place})

