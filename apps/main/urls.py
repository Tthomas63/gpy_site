from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^key$', views.UlxSecretKeyPage.as_view(), name='key'),
    url(r'^all_users$', views.AllUsersPage.as_view(), name='all_users'),
    # url(r'^all_users_search/?$', views.all_users_search, name='all_users_search'),
    url(r'^about$', views.AboutView.as_view(), name='about'),
    url(r'^logout', login_required(views.LogoutView.as_view(), login_url='/'), name='logout'),
    url(r'^login_page$', views.LoginPage.as_view(), name='login_page'),
    url(r'^logout_page$', login_required(views.LogoutPage.as_view()), name='logout_page'),
    # url(r'^profile/(?P<steam_id>.+)$', views.user_profile_view, name='profile'),
    # url(r'^profile_edit/(?P<steam_id>\d+)$', views.user_profile_edit_privacy, name='profile_edit'),
    url(r'^announcement/(?P<pk>\d+)/$', views.AnnouncementDetailView.as_view(), name='announcement_detail'),
    url(r'^announcement/$', views.AnnouncementDetailView.as_view(), name='announcement_detail_no_pk'),
]
