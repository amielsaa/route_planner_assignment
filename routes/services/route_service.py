import os
import boto3
from routes.services.fuel_service import get_closest_fuel_stations

def get_shortest_route(start_coords=[-122.3483, 47.6205], destination_coords=[-122.4194, 37.7749]):
    # init AWS Location client
    client = boto3.client('location', region_name=os.getenv("AWS_REGION"))

    # call CalculateRoute API
    response = client.calculate_route(
        CalculatorName='calculator_routeplanner',
        DeparturePosition=start_coords,  
        DestinationPosition=destination_coords,
        TravelMode='Truck',  
        DistanceUnit='Miles',
        IncludeLegGeometry=True
    )

    # extract the route geometry LineString
    route_geometry = []
    for leg in response['Legs']:
        route_geometry.extend(leg['Geometry']['LineString'])

    stations = get_closest_fuel_stations(route_geometry)
    
    # route details
    route_summary = response['Summary']
    distance = route_summary['Distance']
    duration_seconds = route_summary['DurationSeconds']

    return {
        'distance': distance,
        'duration': duration_seconds,
        'route_geometry': route_geometry,
        'stations': stations
    }

