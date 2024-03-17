from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroups, Message, UserProfile, Notification
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, SignupForm, LoginForm


# Create your views here.


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
                #TODO end to the group's users
            elif recipient_username:
                recipient = UserProfile.objects.get(username=recipient_username)
                Message.objects.create(sender=request.user, recipient=recipient, content=content)
                Notification.objects.create(recipient=recipient, content=content, title=request.user.username)
            return redirect(reversed('mainapp:chat_app'))
    groups = ChatGroups.objects.filter(members=request.user)
    return render(request, 'mainapp/messages.html', {'groups': groups})


# signup page
def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # loginForm = LoginForm()
            return redirect('mainapp:login')
            # return render(request, 'login.html', {'form' : loginForm})
        else:
            response = HttpResponse()
            response.write("<p>Something went wrong</p>")
            return response
    else:
        form = UserCreationForm()
        # form = SignUpForm()
        return render(request, 'mainapp/signup.html', {'form': form})


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


@login_required
def notifications_view(request):

    notifications = Notification.objects.filter(recipient__username=request.user.username).order_by('timestamp')
    return render(request, 'mainapp/notifications.html', {'notifications': notifications})
