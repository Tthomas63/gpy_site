from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^logout', login_required(views.LogoutView.as_view(), login_url='/'), name='logout'),
    url(r'^login_page$', views.LoginPage.as_view(), name='login_page'),
    url(r'^logout_page$', login_required(views.LogoutPage.as_view()), name='logout_page'),
]