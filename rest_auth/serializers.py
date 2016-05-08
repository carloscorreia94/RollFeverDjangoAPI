from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MyUser

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        #fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        fields = ('id', 'username', 'password', 'height')
        write_only_fields = ('password', 'height')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data['username'], height='33'
        )
        user.height = validated_data['height']
        #user.email = validated_data['email']
        #user.first_name = validated_data['first_name']
        #user.last_name = validated_data['last_name']
        user.set_password(validated_data['password'])
        user.save()

        return user
