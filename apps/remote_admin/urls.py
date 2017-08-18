from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='remote_admin_index'),
    url(r'^rcon$', views.RconView.as_view(), name='rcon'),
]