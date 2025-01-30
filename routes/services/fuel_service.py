from routes.models.fuel_station import FuelStation
from scipy.spatial import KDTree
from geopy.distance import geodesic
import numpy as np

def get_closest_fuel_stations(route_geometry, max_miles_per_section=250, max_distance_for_fuel=2):
    """
    Find the closest fuel stations to each route point using.
    - `route_geometry`: List of geomtery points along the route.
    - `max_miles_per_section`: Max number of miles per section.
    - `max_distance_for_fuel`: Max distance to look for fuel stations
    """
    fuel_stations = FuelStation.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
    station_coords = np.array([(fs.latitude, fs.longitude) for fs in fuel_stations])
    station_data = {fs.id: {'latitude': fs.latitude, 'longitude': fs.longitude, 'price_per_gallon': fs.price_per_gallon, 'name':fs.name} for fs in fuel_stations}

    # nearest-neighbor search
    kdtree = KDTree(station_coords)

    section_starts, distances = calc_section_indices(route_geometry, max_miles_per_section)

    # find the cheapest fuel station in each section
    cheapest_stations = []
    for i in range(len(section_starts) - 1):
        start_idx, end_idx = section_starts[i], section_starts[i + 1]
        section_points = route_geometry[start_idx:end_idx]

        # nearby fuel stations
        section_stations = []
        for idx, point in enumerate(section_points):
            lng, lat = point
            distance, index = kdtree.query([lat, lng], k=1)
            distance_miles = distance * 69  # convert degrees to miles
            
            if distance_miles <= max_distance_for_fuel:
                station_id = list(station_data.keys())[index]
                station_info = station_data[station_id]
                station_info['id'] = station_id
                station_info['distance_from_start'] = distances[start_idx + idx]
                section_stations.append(station_info)

        # pick the cheapest station in this section
        if section_stations:
            cheapest_station = min(section_stations, key=lambda s: s['price_per_gallon'])
            cheapest_station['distance_from_last_stop'] = cheapest_station['distance_from_start'] - cheapest_stations[-1]['distance_from_start'] if cheapest_stations else cheapest_station['distance_from_start'] 
            cheapest_stations.append(cheapest_station)

    return cheapest_stations


def calc_section_indices(route_geometry, max_miles_per_section=150):
    total_distance = 0
    section_starts = []  # list of starting indices for each 'max_miles_per_section'-mile section
    distances = []  # list of accumulative distances
    first_section_miles_offset = -100 # no need to look for fuel station at the first X miles.
    for i in range(1, len(route_geometry)):
        point1 = tuple(route_geometry[i - 1][::-1]) 
        point2 = tuple(route_geometry[i][::-1])  
        dist = geodesic(point1, point2).miles
        total_distance += dist
        distances.append(total_distance)

        # new section every 'max_miles_per_section' miles
        if total_distance - (distances[section_starts[-1]] if section_starts else first_section_miles_offset) >= max_miles_per_section:
            section_starts.append(i)
    return section_starts, distances
