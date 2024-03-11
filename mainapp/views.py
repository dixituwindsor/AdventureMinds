from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroups, Message, UserProfile
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, SignupForm, LoginForm
from .models import UserProfile

# Create your views here.


def messenger(request):
    template = "mainapp/messenger.html"
    context = {}
    return render(request=request, template_name=template, context=context)


def getusers(request):
    users = UserProfile.objects.all().values('username', 'id')
    return JsonResponse(list(users), safe=False)

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
