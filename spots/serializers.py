from rest_framework import serializers
from .models import Spot, Session
from rest_framework.validators import UniqueValidator
from django.db.models import CharField

class SpotSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Spot
        fields = ('name', 'description', 'created_at', 'lat', 'lng', 'created_by')


# Consider deleting this Serializer?
class SpotNearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = ('name','created_by','description','lat','lng')


class SessionSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    spot = serializers.ReadOnlyField(source='spot.name')

    class Meta:
        model = Session
        fields = ('title','start_time','end_time','created_by','spot')