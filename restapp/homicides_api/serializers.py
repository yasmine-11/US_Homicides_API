from rest_framework import serializers
from homicides_api.models import *

class VictimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Victim
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class DispositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disposition
        fields = '__all__'

class HomicideSerializer(serializers.ModelSerializer):
    victim = VictimSerializer()
    location = LocationSerializer()
    disposition = DispositionSerializer()

    class Meta:
        model = Homicide
        fields = '__all__'
