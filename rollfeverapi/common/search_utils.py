from rest_auth.models import Profile, MyUser
from django.db.models import Q
from roll_user.serializers import UserHeadingSerializer

def generic_search():
    print('search')

def user_search(query):
    users_profiles = Profile.objects.filter(Q(account__username__istartswith=query) | Q(account__email=query) | Q(name__istartswith=query)).values_list('account')
    users = MyUser.objects.filter(id__in = users_profiles)
    serializer = UserHeadingSerializer(users, many=True)
    return serializer.data