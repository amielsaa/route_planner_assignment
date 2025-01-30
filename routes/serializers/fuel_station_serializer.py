from rest_framework import serializers
from routes.models.fuel_station import FuelStation

class FuelStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelStation
        fields = "__all__"
