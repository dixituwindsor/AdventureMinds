from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroups, Message, UserProfile
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm

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

# sign in
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # form.save()
            # commit false to save current object in db
            userobj = form.save(commit=False)
            # making some necessary change in obj then saving it in db
            userobj.username = form.cleaned_data['username'].lower()
            if UserProfile.objects.filter(username=userobj.username).exists():
                form = SignupForm()
                return render(request, 'mainapp/signup.html', {'form': form, 'msg':'username already taken, use different one'})

            if UserProfile.objects.filter(username=userobj.email).exists():
                form = SignupForm()
                return render(request, 'mainapp/signup.html', {'form': form, 'msg': 'Use different email id'})

            userobj.email = form.cleaned_data['email'].lower()
            userobj.password = make_password(form.cleaned_data['password'])
            userobj.save()
            return redirect('mainapp:login')
        else:
            form = SignupForm()
            return render(request, 'mainapp/signup.html', {'form': form, 'msg':'Something went wrong, try again'})
    else:
        form = SignupForm()
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
                form = LoginForm()
                return render(request, 'mainapp/login.html', {'form': form, 'msg': 'Wrong credentials provided, try again'})
        else:
            form = LoginForm()
            return render(request, 'mainapp/login.html', {'form': form, 'msg': 'Something went wrong, try again'})
    else:
        form = LoginForm()
        return render(request, 'mainapp/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('mainapp:login')
