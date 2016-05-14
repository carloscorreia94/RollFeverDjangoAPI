from rest_framework import serializers
from .models import Spot, Thermometer
from rest_framework.validators import UniqueValidator
from django.db.models import CharField

class SpotSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Spot
        fields = ('id','name', 'description', 'lat', 'lng', 'created_by','main_pic')

        readonly_fields = ('main_pic')

class SpotDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    meter = serializers.SerializerMethodField('get_overall_meter')

    def get_overall_meter(self,spot):
        thermo = Thermometer.objects.get(spot=spot)
        average = (thermo.people + thermo.flatground + thermo.reputation) / 3
        return round(average,1)

    class Meta:
        model = Spot
        fields = ('id','name', 'description', 'lat', 'lng', 'created_by','main_pic','meter')

        readonly_fields = ('main_pic')


# Consider deleting this Serializer?
class SpotNearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = ('id','name','created_by','description','lat','lng')
