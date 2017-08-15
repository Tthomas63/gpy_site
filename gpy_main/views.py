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
        ulxquerydict = request.POST
        ulxdict = ulxquerydict.dict() # Entire dictionary sent over by gmod
        # print(ulxdict)
        ulx_secret_key = ulxdict['ulx_secret_key'] # Grab key
        ulx_dict_groups = json.loads(ulxdict['ulx_ranks']) # Json serialize
        ulx_dict_online_players = json.loads(ulxdict['ulx_online_players']) # Json serialize
        # print("Ulx groups dict is: {}".format(ulx_dict_groups))

        for k,v in ulx_dict_online_players.items():
            print(k)
            print(v)
            print(v['rank'])
            print(v['nick'])
            try:
                temp_user = SteamUser.objects.get(personaname=v['nick'])
                print("Saving steamid {0} to user with nick {1}".format(v['nick'],k))
                temp_user.steamid = k
                temp_user.save()
            except ObjectDoesNotExist:
                print("Could not find nick in users.")

        for userdata in ulx_dict_groups.items():
            temp_steamid = userdata[0]
            temp_group = userdata[1]

            try:
                site_ulx_secret_key = UlxSecretKey.objects.get(value=ulx_secret_key)
                print("Keys are a match. Continuing.")
                try:
                    temp_user = SteamUser.objects.get(steamid=temp_steamid)
                    temp_user.rank = temp_group
                    if temp_group == "admin" or temp_group == "superadmin":
                        print("Making user staff/admin.")
                        temp_user.is_staff = True
                        temp_user.is_admin = True
                        if temp_group == "superadmin":
                            print("Making user superadmin.")
                            temp_user.is_superuser = True
                except ObjectDoesNotExist:
                    print("No user found for steamid: {}".format(temp_steamid))
            except ObjectDoesNotExist:
                print("Could not match keyes.")
        return JsonResponse({'status': True})
