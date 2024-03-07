from django.shortcuts import render

# Create your views here.


def messenger(request):
    template = "mainapp/messenger.html"
    context = {}
    return render(request=request, template_name=template, context=context)



def userProfile(request):
    template = "mainapp/profile.html"
    context = {}
    return render(request=request, template_name=template, context=context)