from django.db import models
from spots.models import Spot

class Favorites(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('rest_auth.MyUser', on_delete=models.CASCADE)
    spot = models.ForeignKey(Spot,on_delete=models.CASCADE)

class FollowerRelation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_created = models.ForeignKey('rest_auth.MyUser', on_delete=models.CASCADE, related_name='follower')
    user_following = models.ForeignKey('rest_auth.MyUser', on_delete=models.CASCADE, related_name='following')

    #Arguments are already VERIFIED IN ALL CASES by the views

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
    def get_follow_status(in_user):
        follows = len(FollowerRelation.objects.filter(user_created=in_user))
        following = len(FollowerRelation.objects.filter(user_following=in_user))
        return {"follows": follows, "following": following}