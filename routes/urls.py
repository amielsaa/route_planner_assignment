from django.urls import path
from .views.route_view import map_view, map_view_data
urlpatterns = [
    path('map/', map_view, name="map_view"),
    path('map_data/', map_view_data, name="map_view_data"),
]
