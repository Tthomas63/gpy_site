from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^key$', views.ulx_secret_key_communicate, name='key'),
    # url(r'^key$', views.set_key_2, name='key'),
    url(r'^key$', views.UlxSecretKeyPage.as_view(), name='key'),
]