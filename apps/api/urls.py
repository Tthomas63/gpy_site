from django.conf.urls import url

from . import views

urlpatterns = [
    # Json URLS Below
    url(r'^get_user_as_json/(?P<steam_id>\d+)$', views.get_user_from_steamid_as_json, name='get_user_as_json'),
    url(r'^get_all_announcements_and_related_types_as_json/$', views.get_all_announcements_and_related_types,
        name='get_all_announcements_and_related_types'),
]
