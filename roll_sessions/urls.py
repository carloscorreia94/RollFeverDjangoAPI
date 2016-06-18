from django.conf.urls import url
from django.conf.urls import include
from . import views


urlpatterns = [
    url(r'^sessions/(?P<spot>[0-9]+)/$', views.SessionList.as_view()),
    url(r'^search/sessions/((?P<base64string>.+)/)?$', views.SessionSearch.as_view()),

]