from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^media/upload/(?P<media_type>\w+)/(?P<content_id>[0-9]+)/$', views.UploadMedia.as_view(), name="upload_media"),
    url(r'^login/$', views.Login.as_view(), name="login"),
    url(r'^refresh/$', views.Refresh.as_view(), name="refresh"),
]