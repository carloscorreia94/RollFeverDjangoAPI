from rest_framework import serializers
from .models import Spot
from rest_framework.validators import UniqueValidator
from django.db.models import CharField

class SpotSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spot
        fields = ('name', 'description', 'created_at', 'lat', 'lng')