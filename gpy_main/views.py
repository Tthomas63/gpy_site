from venv import logger

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
from django.views.generic import UpdateView
from steam import SteamID
from steam.steamid import make_steam64

from django.conf import settings

from .utils import steam2_to_steam64
from .forms import GpyProfileForm
from .models import UlxSecretKey, SteamUser, UlxDataStore, UlxUserData, GpyProfile
import logging
logger2 = logging.getLogger('django')
logger = logging.getLogger('gpy_site')
logger3 = logging.getLogger('gpy_main')
logger4 = logging.getLogger('web')
# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'gpy_main/index.html')


class AboutView(View):
    def get(self, request):
        return render(request, 'gpy_main/about.html')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class LogoutPage(View):
    def get(self, request):
        return render(request, 'gpy_main/logout_page.html')


class LoginPage(View):
    def get(self, request):
        return render(request, 'gpy_main/login_page.html')


def user_profile_view(request, steam_id):
    context = {}
    if steam_id[0:5] == "STEAM":
        steam_id = steam2_to_steam64(steam_id)
    try:
        viewed_user = SteamUser.objects.get(steamid=steam_id)
        context['viewed_user'] = viewed_user
    except ObjectDoesNotExist:
        print("Could not find the requested user")
        context['error'] = "Could not find a user for the requested steam id."
    return render(request, 'gpy_main/profile.html', context)


def user_profile_edit_privacy(request, steam_id):
    viewed_user = SteamUser.objects.get(steamid=steam_id)
    print("poo")
    print(request.method)
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

    return render(request, 'gpy_main/profile_edit.html', {'form': form, 'viewed_user': viewed_user})


# @csrf_exempt
class UlxSecretKeyPage(View):
    def get(self, request):
        return render(request, 'gpy_main/key.html')

    def post(self, request):
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
