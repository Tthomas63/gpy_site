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

from .forms import KeyForm
from .models import UlxSecretKey, SteamUser
import logging
logger2 = logging.getLogger('django')
logger = logging.getLogger('gpy_site')
logger3 = logging.getLogger('gpy_main')
logger4 = logging.getLogger('web')

# logger.info("Test")
# logger2.info("Test")
# logger3.info("Test")
# logger4.info("Test")
#
# logger.debug("Test2")
# logger2.debug("Test2")
# logger3.debug("test2")
# logger4.debug("Test2")
# print("Test 3")


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
        ulx_query_dict = request.POST
        ulx_dict = ulx_query_dict.dict() # Entire dictionary sent over by gmod
        ulx_secret_key = ulx_dict['ulx_secret_key'] # Grab key
        ulx_dict_groups = json.loads(ulx_dict['ulx_ranks']) # Json serialize
        ulx_dict_online_players = json.loads(ulx_dict['ulx_online_players']) # Json serialize
        try:
            site_ulx_secret_key = UlxSecretKey.objects.get(value=ulx_secret_key)
            print("Keys are a match. Continuing.")
            for steam_id,user_data in ulx_dict_online_players.items(): # Save any online players STEAMIDS to verify. k is steamid
                try:
                    temp_user = SteamUser.objects.get(personaname=user_data['nick'])
                    if temp_user.steamid != steam_id:
                        print("Saving steamid {0} and rank {1} to user with nick {2}".format(steam_id,
                                                                                             user_data['rank'],
                                                                                             user_data['nick']))
                        temp_user.steamid = steam_id
                        temp_user.rank = user_data['rank']
                        temp_user.save()
                    else:
                        # We do nothing!
                        print("User {} already has correct steamid.".format(temp_user.personaname))
                except ObjectDoesNotExist:
                    print("Could not find nick in users.")
            for user_data in ulx_dict_groups.items():
                temp_steam_id = user_data[0]
                temp_group = user_data[1]
                try:
                    temp_user = SteamUser.objects.get(steamid=temp_steam_id)
                    if temp_user.rank != temp_group:
                        temp_user.rank = temp_group
                        if temp_group == "admin" or temp_group == "superadmin" or temp_group == "developer":
                            print("Making user {} staff/admin.".format(temp_user.personaname))
                            temp_user.is_staff = True
                            temp_user.is_admin = True
                            if temp_group == "superadmin" or temp_group == "developer":
                                print("Making user {} superadmin.".format(temp_user.personaname))
                                temp_user.is_superuser = True
                    else:
                        print("User {}'s rank is staying the same".format(temp_user.personaname))
                except ObjectDoesNotExist:
                    print("No user found for steamid: {}".format(temp_steam_id))
        except ObjectDoesNotExist:
            print("Could not match keyes.")
        return JsonResponse({'status': True})
