import pandas as pd
from geopy.geocoders import Nominatim
from django.core.management.base import BaseCommand
from routes.models import FuelStation 

geolocator = Nominatim(user_agent="amielGeoapiRoutePlanner", timeout=10)

class Command(BaseCommand):
    help = "Import fuel station data from CSV and get coordinates"

    def handle(self, *args, **kwargs):
        file_path = "fuel-prices-for-be-assessment.csv" 
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            # check for duplicates
            if FuelStation.objects.filter(name=row["Truckstop Name"]).exists():
                continue
            address = row["Address"] 
            price_per_gallon = row["Retail Price"]  
            print(f"Processing: {address}")

            # get coordinates from geocode
            location = geolocator.geocode(address)
            latitude = location.latitude if location else None
            longitude = location.longitude if location else None

            # save to database
            try:
                FuelStation.objects.create(
                    name=row["Truckstop Name"],  
                    address=address,
                    city=row["City"],
                    state=row["State"],
                    price_per_gallon=price_per_gallon,
                    latitude=latitude,
                    longitude=longitude,
                )
            except Exception as e:
                continue

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
