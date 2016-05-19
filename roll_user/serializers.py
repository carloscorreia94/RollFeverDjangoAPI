from rest_framework import serializers
from rest_auth.models import MyUser, Profile
from rest_auth.serializers import UserProfileSerializer


class UserHeadingSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField('profile_heading')

    def profile_heading(self,user):
        profile = Profile.objects.get(account=user)
        return {
            'name' : profile.name,
            'user_photo' : str(profile.user_photo)
        }

    class Meta:
        model = MyUser
        fields = ('username','profile',)