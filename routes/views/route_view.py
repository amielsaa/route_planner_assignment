from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from routes.services.route_service import get_shortest_route
import os

API_KEY = os.getenv("AWS_LOCATION_SERVICE_API")
REGION = os.getenv("AWS_REGION")


@api_view(['GET'])
def map_view(request):
    context = {
        'distance': 0,
        'duration': 0,
        "API_KEY": API_KEY,
        "REGION": REGION
    }
    return render(request, 'map.html', context)


@api_view(['GET'])
def map_view_data(request):
    start_lat = float(request.GET.get("start_lat", 47.6205))
    start_lng = float(request.GET.get("start_lng", -122.3483))
    dest_lat = float(request.GET.get("dest_lat", 37.7749))
    dest_lng = float(request.GET.get("dest_lng", -122.4194))

    route_data = get_shortest_route(start_coords=[start_lng, start_lat], destination_coords=[dest_lng, dest_lat])

    stations_data = [
        {"id": station["id"], "latitude": station['latitude'], "longitude": station['longitude'],
         "fuel_cost": int(station['price_per_gallon'])  * (int(station['distance_from_last_stop']) / 10),
         "price_per_gallon": station['price_per_gallon'], "name": station['name']}
        for station in route_data["stations"]
    ]

    data = {
        'route_geometry': route_data['route_geometry'],
        'distance': route_data['distance'],
        'duration': int(route_data['duration']) / 60, # convert to minutes
        "stations": stations_data,
    }

    return Response(data)
