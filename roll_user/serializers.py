from rest_framework import serializers
from rest_auth.models import MyUser


class UserHeadingSerializer(serializers.ModelSerializer):
    test = serializers.SerializerMethodField('test_user')

    def test_user(self,user):
        return 'um TeStE!!?'
        #thermo = Thermometer.objects.get(spot=spot)
        #average = (thermo.people + thermo.flatground + thermo.reputation) / 3
        #return round(average,1)

    class Meta:
        model = MyUser
        fields = ('username','name', 'test')