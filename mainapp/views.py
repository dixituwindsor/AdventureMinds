from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatGroups, Message, UserProfile

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
            elif recipient_username:
                recipient = UserProfile.objects.get(username=recipient_username)
                Message.objects.create(sender=request.user, recipient=recipient, content=content)
            return redirect('chat_app')
    groups = ChatGroups.objects.filter(members=request.user)
    return render(request, 'mainapp/messages.html', {'groups': groups})