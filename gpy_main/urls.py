from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist

from gpy_main.models import UlxSecretKey
from . import views

urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^key$', views.ulx_secret_key_communicate, name='key'),
    # url(r'^key$', views.set_key_2, name='key'),
    url(r'^key$', views.UlxSecretKeyPage.as_view(), name='key'),
]

try:
    len_keys = len(UlxSecretKey.objects.all())
    if len_keys == 0:
        new_ulx_key = UlxSecretKey.objects.create()
        print("No keys were found so one was made.")
except ObjectDoesNotExist:
    new_ulx_key = UlxSecretKey.objects.create()
    print("No keys were found so one was made.")