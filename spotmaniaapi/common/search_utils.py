from rest_auth.models import Profile, MyUser
from spots.models import Spot
from roll_sessions.models import Session
from django.db.models import Q
from roll_user.serializers import UserHeadingSerializer
from spots.serializers import SpotHeadingSerializer
from roll_sessions.serializers import SessionSerializer
def generic_search():
    print('search')

def user_search(query,my_user):
    users_profiles = Profile.objects.filter(Q(account__username__istartswith=query) | Q(account__email=query) | Q(name__istartswith=query)).values_list('account')
    users = MyUser.objects.filter(id__in = users_profiles)
    users = users.filter(username=my_user)
    serializer = UserHeadingSerializer(users, many=True)
    return serializer.data

def spot_search(query):
    #TODO: Spot Search by Country :)
    spots = Spot.objects.filter(Q(name__istartswith=query))
    serializer = SpotHeadingSerializer(spots, many=True)
    return serializer.data

def session_search(query):
    #TODO: Session Search By Following users
    spots = Session.objects.filter(Q(title__istartswith=query) | Q(spot__name__istartswith=query))
    serializer = SessionSerializer(spots, many=True)
    return serializer.data
