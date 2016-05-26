from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^sign_up/$', views.SignUp.as_view(), name="sign_up"),
    url(r'^login/$', views.Login.as_view(), name="login"),
    url(r'^refresh/$', views.Refresh.as_view(), name="refresh"),
]