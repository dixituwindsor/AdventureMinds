from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm, SignupForm, LoginForm

# Create your views here.


def messenger(request):
    template = "mainapp/messenger.html"
    context = {}
    return render(request=request, template_name=template, context=context)

# def messenger(request):
#     resonse = HttpResponse()
#     resonse.write("<h1>Hello World</h1>")
#     return resonse


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