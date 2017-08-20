from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='remote_admin_index'),
    url(r'^rcon$', views.RconView.as_view(), name='rcon'),
    url(r'^rcon_cmd/(?P<rcon_server_port>.+)/(?P<rcon_cmd>.+)$', views.RconCmdView.as_view(), name='rcon_cmd'),
    url(r'^ban_user/$', views.BanUserView.as_view(), name='ban_user'),
    url(r'^usage$', views.UsageView.as_view(), name='usage'),
    url(r'^rcon_logs/$', views.view_logs, name='usage'),
]
