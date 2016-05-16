from django.conf.urls import url
from django.conf.urls import include
from . import views



urlpatterns = [
    url(r'^user/favorites/(?P<spot>[0-9]+)/$', views.UserFavorites.as_view()),
    url(r'^user/favorites/((?P<username>\w+)/)?((?P<spot>[0-9]+)/)?$', views.UserFavorites.as_view()),
]

