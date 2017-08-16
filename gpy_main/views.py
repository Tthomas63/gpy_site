from venv import logger

import sys

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import logout
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from steam import SteamID
from steam.steamid import make_steam64

from django.conf import settings

from .utils import steam2_to_steam64
from .forms import KeyForm
from .models import UlxSecretKey, SteamUser, UlxDataStore, UlxUserData
import logging
logger2 = logging.getLogger('django')
logger = logging.getLogger('gpy_site')
logger3 = logging.getLogger('gpy_main')
logger4 = logging.getLogger('web')
# Create your views here.

class IndexView(View):
    def get(self, request):
        return render(request, 'gpy_main/index.html')


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
                    user_data.linked_store = ulx_data_store
                except ObjectDoesNotExist:
                    print("No user found for steamid: {}".format(user_steamid))
        except ObjectDoesNotExist:
            print("Could not match keyes. Do you have one made?")
        return JsonResponse({'status': True})
