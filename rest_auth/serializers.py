from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MyUser

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        #fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        fields = ('id', 'username', 'password', 'name', 'email')
        #write_only_fields = ('password', 'height')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data['username'], name=validated_data['name']
        )
        user.email = validated_data['email']
        user.set_password(validated_data['password'])
        user.save()

        return user
