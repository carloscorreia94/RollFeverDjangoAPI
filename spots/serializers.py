from rest_framework import serializers
from .models import Spot
from rest_framework.validators import UniqueValidator
from django.db.models import CharField

class SpotSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Spot
        fields = ('id','name', 'description', 'lat', 'lng', 'created_by','main_pic')

        readonly_fields = ('main_pic')

class SpotDetailSerializer(serializers.ModelSerializer):
    #TODO : Work on here
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Spot
        fields = ('id','name', 'description', 'lat', 'lng', 'created_by','main_pic')

        readonly_fields = ('main_pic')


# Consider deleting this Serializer?
class SpotNearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Spot
        fields = ('id','name','created_by','description','lat','lng')
