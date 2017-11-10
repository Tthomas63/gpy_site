from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create_forum$', views.CreateForumView.as_view(), name='create_forum'),
    url(r'^category/(?P<category_pk>\d+)$', views.CategoryView.as_view(), name='category_view'),
]
