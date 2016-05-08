from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^sign_up/$', views.SignUp.as_view(), name="sign_up"),
]