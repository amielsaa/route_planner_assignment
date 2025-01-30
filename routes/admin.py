from django.contrib import admin
from .models import FuelStation

@admin.register(FuelStation)
class FuelStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'price_per_gallon', 'latitude', 'longitude')
    search_fields = ('name', 'city', 'state')
