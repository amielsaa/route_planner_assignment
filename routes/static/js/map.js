const apiKey = window.env.API_KEY;
const region = window.env.REGION;
const style = "Standard";
const colorScheme = "Light";

const map = new maplibregl.Map({
    container: "map",
    style: `https://maps.geo.${region}.amazonaws.com/v2/styles/${style}/descriptor?key=${apiKey}&color-scheme=${colorScheme}`,
    center: [-122.3483, 47.6205], 
    zoom: 6,
});

map.addControl(new maplibregl.NavigationControl(), "top-left");

function findRoute() {
    const startLat = document.getElementById('start-lat').value;
    const startLng = document.getElementById('start-lng').value;
    const destLat = document.getElementById('dest-lat').value;
    const destLng = document.getElementById('dest-lng').value;

    const url = `/api/map_data/?start_lat=${startLat}&start_lng=${startLng}&dest_lat=${destLat}&dest_lng=${destLng}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            
            document.getElementById('distance').textContent = data.distance.toFixed(2);
            document.getElementById('duration').textContent = data.duration.toFixed(0);

            let totalFuelCost = 0;
            data.stations.forEach(station => {
                totalFuelCost += station.fuel_cost;
            });

            document.getElementById('fuel-cost').textContent = totalFuelCost.toFixed(2);

            if (map.getSource('route')) {
                map.removeLayer('route');
                map.removeSource('route');
            }

            // add line layer for the updated route
            map.addSource('route', {
                type: 'geojson',
                data: {
                    type: 'Feature',
                    geometry: {
                        type: 'LineString',
                        coordinates: data.route_geometry,
                    },
                },
            });

            map.addLayer({
                id: 'route',
                type: 'line',
                source: 'route',
                layout: {
                    'line-join': 'round',
                    'line-cap': 'round',
                },
                paint: {
                    'line-color': '#007cbf',
                    'line-width': 4,
                },
            });

            // fit map to the route bounds
            const bounds = new maplibregl.LngLatBounds();
            data.route_geometry.forEach(coord => bounds.extend(coord));
            map.fitBounds(bounds, { padding: 20 });

            // clear existing fuel station markers
            document.querySelectorAll('.fuel-marker').forEach(marker => marker.remove());

            // fuel station markers
            data.stations.forEach(station => {
                new maplibregl.Marker({ color: "red" }) 
                    .setLngLat([station.longitude, station.latitude])
                    .setPopup(new maplibregl.Popup().setHTML(`
                        <strong>${station.name}</strong><br>
                        ID: ${station.id}<br>
                        Price: $${station.price_per_gallon.toFixed(2)} per gallon
                    `))
                    .addTo(map);
            });
        })
        .catch(error => console.error("Error fetching route:", error));
}
