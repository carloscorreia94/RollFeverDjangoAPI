from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MyUser, Profile


class SignUpSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True,max_length=150)

    class Meta:
        model = MyUser
        #fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        fields = ('id', 'username', 'password', 'email','name')
        #write_only_fields = ('password', 'height')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data['username']
        )
        user.email = validated_data['email']
        user.set_password(validated_data['password'])
        user.name = validated_data['name']
        user.save()

        profile = Profile.objects.create(name=user.name, account=user)
        profile.save()

        return user

