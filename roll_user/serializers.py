from rest_framework import serializers
from roll_user.models import FollowerRelation
from rest_auth.models import Profile, MyUser
from rest_auth.serializers import UserProfileSerializer
from spotmaniaapi import settings

class UserHeadingSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField('profile_heading')
    numbers = serializers.SerializerMethodField('profile_numbers')

    def profile_heading(self,user):
        profile = Profile.objects.get(account=user)
        return {
            'name' : profile.name,
            'user_photo' : settings.MEDIA_URL + str(profile.user_photo) if str(profile.user_photo) != "" else None
        }

    def profile_numbers(self,user):
        user_connections = FollowerRelation.get_follow_status(user)
        return {
            'user_connections' : user_connections
        }

    class Meta:
        model = MyUser
        fields = ('username','profile','numbers')