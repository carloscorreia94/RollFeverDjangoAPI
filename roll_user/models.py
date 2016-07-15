from django.db import models
from spots.models import Spot
from rest_auth.models import MyUser
from spots.serializers import SpotSerializer
from django.core.exceptions import ObjectDoesNotExist


"""
DISCLAIMER:
Arguments are already VERIFIED IN ALL CASES by the views
"""

class Favorites(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('rest_auth.MyUser', on_delete=models.CASCADE)
    spot = models.ForeignKey(Spot,on_delete=models.CASCADE)

    @staticmethod
    def get_spot(in_user):
        favorites = Favorites.objects.filter(user=in_user).values_list('spot_id')
        spots = Spot.objects.filter(id__in = favorites)
        serializer = SpotSerializer(spots, many=True)
        return serializer.data

    @staticmethod
    def delete_favorite(in_user, in_spot):
        same_favorite = Favorites.objects.filter(user=in_user, spot=in_spot)

        if not same_favorite.exists():
            return False

        same_favorite.delete()
        return True

    @staticmethod
    def create_favorite(in_user, in_spot):
        same_favorite = Favorites.objects.filter(user=in_user, spot=in_spot)
        if same_favorite.exists():
            return False

        favorite = Favorites()
        favorite.user = in_user
        favorite.spot = in_spot
        favorite.save()

        return {'favorite_id': favorite.id}


class FollowerRelation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_created = models.ForeignKey('rest_auth.MyUser', on_delete=models.CASCADE, related_name='follower')
    user_following = models.ForeignKey('rest_auth.MyUser', on_delete=models.CASCADE, related_name='following')

    @staticmethod
    def do_follow(in_user,other_user):
        new_relation = FollowerRelation()
        new_relation.user_created = in_user
        new_relation.user_following = other_user
        new_relation.save()

        return FollowerRelation.get_follow_status(in_user)

    @staticmethod
    def do_unfollow(in_user,other_user):
        existing_relation = FollowerRelation.objects.filter(user_created=in_user, user_following=other_user)
        if not existing_relation.exists():
            return False

        existing_relation.delete()

        return FollowerRelation.get_follow_status(in_user)


    @staticmethod
    def get_follow_status(in_user,my_user=None):
        follows = len(FollowerRelation.objects.filter(user_created=in_user))
        following = len(FollowerRelation.objects.filter(user_following=in_user))

        temp_status = {"follows": follows, "following": following}
        if my_user is not None:
            try:
                FollowerRelation.objects.get(user_created=my_user,user_following=in_user)
                temp_status["status_following"] = True
            except ObjectDoesNotExist:
                temp_status["status_following"] = False

        return temp_status

    @staticmethod
    def get_follows(in_user,following = False):
        from .serializers import UserHeadingSerializer

        if following:
            follows = FollowerRelation.objects.filter(user_created=in_user).values_list('user_following')
        else:
            follows = FollowerRelation.objects.filter(user_following=in_user).values_list('user_created')

        users = MyUser.objects.filter(id__in = follows)
        serializer = UserHeadingSerializer(users, many=True)
        return serializer.data

    @staticmethod
    def get_following(in_user):
        return FollowerRelation.get_follows(in_user,True)