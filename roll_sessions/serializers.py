from rest_framework import serializers
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    spot = serializers.ReadOnlyField(source='spot.name')

    class Meta:
        model = Session
        fields = ('title','start_time','end_time','created_by','spot')