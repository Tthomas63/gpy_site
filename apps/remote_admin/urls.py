from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='remote_admin_index'),
    url(r'^rcon$', views.RconView.as_view(), name='rcon'),
    url(r'^rcon_cmd/(?P<rcon_server_port>.+)/(?P<rcon_cmd>.+)$', views.RconCmdView.as_view(), name='rcon_cmd'),
]