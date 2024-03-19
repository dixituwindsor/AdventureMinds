from django.contrib import admin
from .models import UserProfile, Place, Trip

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Place)
admin.site.register(Trip)
