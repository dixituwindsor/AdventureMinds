from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import UserProfileForm, UserPreferencesForm
from .models import UserPreferences, PreferenceCategory, ChatGroup
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
