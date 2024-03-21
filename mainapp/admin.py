from django.contrib import admin
from .models import UserProfile, Place, Trip, Wishlist

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Place)
admin.site.register(Trip)
admin.site.register(Wishlist)
