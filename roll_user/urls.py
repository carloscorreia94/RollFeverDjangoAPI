from django.conf.urls import url
from django.conf.urls import include
from . import views



urlpatterns = [
    url(r'^user/favorites/(?P<spot>[0-9]+)/$', views.UserFavorites.as_view()),
    url(r'^user/favorites/((?P<username>\w+)/)?((?P<spot>[0-9]+)/)?$', views.UserFavorites.as_view()),

    url(r'^user/profile/((?P<username>\w+)/)?$', views.UserProfile.as_view()),

    url(r'^user/follow/(?P<username>\w+)/$', views.FollowManagement.as_view()),
    url(r'^user/followers/((?P<username>\w+)/)?$', views.Followers.as_view()),
    url(r'^user/following/((?P<username>\w+)/)?$', views.Following.as_view()),

    url(r'^search/user/((?P<base64string>.+)/)?$', views.UserSearch.as_view()),

]

