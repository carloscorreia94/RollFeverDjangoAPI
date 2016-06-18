from django.conf.urls import url
from django.conf.urls import include
from . import views


urlpatterns = [
    url(r'^spots/$', views.SpotList.as_view(), name='spot-list'),
    url(r'^spots/nearby/$', views.SpotsNearby.as_view()),
    url(r'^spot/(?P<spot>[0-9]+)/$', views.SpotDetail.as_view()),

    url(r'^search/spots/((?P<base64string>.+)/)?$', views.SpotSearch.as_view()),
]