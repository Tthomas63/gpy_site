import django
from django.middleware.csrf import CsrfViewMiddleware
# from venv import logger

import sys

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import logout
import json

from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, render_to_response
from django.template import loader, RequestContext
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.generic import UpdateView, DetailView
from django.views.generic.base import ContextMixin
from steam import SteamID
from steam.steamid import make_steam64

from django.conf import settings

from .mixins import AnnouncementMixin
from .utils import steam2_to_steam64
from .forms import GpyProfileForm
from .models import UlxSecretKey, SteamUser, UlxDataStore, UlxUserData, GpyProfile, Announcement
import logging
logger2 = logging.getLogger('django')
logger = logging.getLogger('gpy')
logger3 = logging.getLogger('main')
logger4 = logging.getLogger('web')
# Create your views here.


class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'main/announcements/detail.html'


class IndexView(View, ContextMixin):
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        annc = Announcement.objects.all()
        # for an in annc:
        #     print(an)
        #     print(an.announcement_type)
        #     print(an.announcement_type.color)
        # print("My announcements: ".format(annc))
        context['announcements'] = annc
        return context


class AboutView(View):
    def get(self, request):
        return render(request, 'main/about.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main:index')


class LogoutPage(View):
    def get(self, request):
        return render(request, 'main/logout_page.html')


class LoginPage(View):
    def get(self, request):
        return render(request, 'main/login_page.html')


class AllUsersPage(View):
    def get(self, request):
        context = dict()
        context['all_users'] = SteamUser.objects.all()
        return render(request, 'main/all_users.html', context)


def all_users_search(request):
    context = {}
    if request.method == 'GET':
        search_query = request.GET.get('search-text', None)
        try:
            list = SteamUser.objects.filter(personaname__contains=search_query)
            context['searched_users'] = list
        except ObjectDoesNotExist:
            print("Could not find any users for search")
            context['searched_users'] = 0
        return render(request, 'main/all_users_search.html', context)
    else:
        context['searched_users'] = SteamUser.objects.all()
        return render(request, 'main/all_users_search.html', context)


def user_profile_view(request, steam_id):
    context = {}

    # steam_id = SteamID(steam_id)
    #
    # steam_id_64 = steam_id.to_64()

    # if steam_id[0:5] == "STEAM":
    #     steam_id = steam2_to_steam64(steam_id)
    # try:
    #     viewed_user = SteamUser.objects.get(steamid=steam_id)
    #     context['viewed_user'] = viewed_user
    try:
        context['viewed_user'] = SteamUser.objects.get(steamid=SteamID(steam_id).as_64)
    except ObjectDoesNotExist:
        context['error'] = "Could not find a user for the requested steam id."
    return render(request, 'main/profile.html', context)


class UserProfileView(View, ContextMixin):
    model = SteamUser
    template_name = 'main/profile.html'

    def get(self, request, steam_id, *args, **kwargs):
        response = super().get()
        context = super().get_context_data()
        context['viewed_user'] = self.model.objects.get(steamid=SteamID(steam_id).as_64)
        context['my_little_message']


def user_profile_edit_privacy(request, steam_id):
    viewed_user = SteamUser.objects.get(steamid=steam_id)
    if request.method == "POST":
        viewed_user_profile = viewed_user.get_or_create_gpy_profile()
        form = GpyProfileForm(request.POST, instance=viewed_user_profile)
        if form.is_valid():
            form.save()
            viewed_user.gpy_profile.save()
            viewed_user.save()
        # process the data in form.cleaned_data as required
        return HttpResponseRedirect("/profile/{}".format(viewed_user.steamid))
    else:
        form = GpyProfileForm()
        print('poop')

    return render(request, 'main/profile_edit.html', {'form': form, 'viewed_user': viewed_user})


# @csrf_exempt
class UlxSecretKeyPage(View):
    def get(self, request):
        return render(request, 'main/key.html')

    @csrf_exempt
    def post(self, request):
        # csrf_token = django.middleware.csrf.get_token(request)
        # request.csrf_processing_done = False
        # reason = CsrfViewMiddleware().process_view(request, None, (), {})
        # if reason is not None:
        #     print("In CSRF failed")
        #     try:
        #         csrf_token_as_ulx_key = UlxSecretKey.objects.get(value=csrf_token)
        #         print("CSRF ULX TOKEN PASS")
        #         pass
        #     except ObjectDoesNotExist:
        #         print("and we failed.")
        #         return reason  # Failed the test, stop here.
        post_query_dict = request.POST
        post_dict = post_query_dict.dict() # Entire dictionary sent over by gmod
        ulx_secret_key = post_dict['ulx_secret_key'] # Grab key
        ulx_dict_groups = json.loads(post_dict['ulx_ranks']) # Json serialize
        # ulx_dict_online_players = json.loads(ulx_dict['ulx_online_players']) # Json serialize -- Depreciated
        try:
            site_ulx_secret_key = UlxSecretKey.objects.get(value=ulx_secret_key)
            print("Keys are a match. Continuing.")
            for user_data in ulx_dict_groups.items():
                user_steamid = user_data[0]
                user_group = user_data[1]
                try:
                    user = SteamUser.objects.get(steamid=steam2_to_steam64(user_steamid))
                    user.update_rank(user_group)
                    user_data = user.get_or_create_userdata()
                    try:
                        ulx_data_store = UlxDataStore.objects.get(secret_key=site_ulx_secret_key)
                    except ObjectDoesNotExist:
                        ulx_data_store = UlxDataStore.objects.create(secret_key=site_ulx_secret_key)
                    ulx_data_store.linked_store = ulx_data_store
                except ObjectDoesNotExist:
                    print("No user found for steamid: {}".format(user_steamid))
        except ObjectDoesNotExist:
            print("Could not match keyes. Do you have one made?")
        return JsonResponse({'status': True})
