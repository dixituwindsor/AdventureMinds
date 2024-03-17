from django.contrib import admin
from .models import UserProfile, Place, Notification, Message

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Place)
admin.site.register(Notification)
admin.site.register(Message)
