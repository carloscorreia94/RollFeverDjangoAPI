from rest_framework import serializers
from rest_auth.models import MyUser, Profile
from rest_auth.serializers import UserProfileSerializer
from spotmaniaapi import settings

class UserHeadingSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField('profile_heading')

    def profile_heading(self,user):
        profile = Profile.objects.get(account=user)
        return {
            'name' : profile.name,
            'user_photo' : settings.MEDIA_URL + str(profile.user_photo) if str(profile.user_photo) != "" else None
        }

    class Meta:
        model = MyUser
        fields = ('username','profile',)