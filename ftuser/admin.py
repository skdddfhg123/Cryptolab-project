from django.contrib import admin
from .models import Ftuser, UserLocation

class FtuserAdmin(admin.ModelAdmin):
	list_display = ('userid', 'email')

admin.site.register(Ftuser, FtuserAdmin)

class LocationAdmin(admin.ModelAdmin):
	list_display = ('id',)

admin.site.register(UserLocation, LocationAdmin)