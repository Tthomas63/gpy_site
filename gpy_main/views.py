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
        # print(request.body)
        # print(request.POST.get)
        # post = request.POST.get
        # print(post)
        # print(request.POST)
        ulxquerydict = request.POST
        ulxdict = ulxquerydict.dict()
        print(ulxdict)
        for key,value in ulxdict.items():
            # print("Key is: {}".format(key))
            # print("Value is: {}".format(value))

            print(ulxdict['ulx_ranks'])
            print(ulxdict['ulx_secret_key'])

            ulx_secret_key = ulxdict['ulx_secret_key']
            ulx_dict_groups = json.loads(ulxdict['ulx_ranks'])
            print("Ulx groups dict is: {}".format(ulx_dict_groups))

            for userdata in ulx_dict_groups.items():
                print(userdata)
                print(userdata[0])
                print(userdata[1])

            # try:
            #     site_ulx_secret_key = UlxSecretKey.objects.get(value=ulx_secret_key)
            #     print("Keys are a match. Continuing.")
            #
            #     ulx_dict_groups = json.loads(ulxdict['ulx_ranks'])
            #     print(ulx_dict_groups)
            #     for steamid, group in ulx_dict_groups:
            #         try:
            #             temp_user = SteamUser.objects.get(steamid=steamid)
            #             print("Got user")
            #             temp_user.rank = group
            #             if group == "admin" or group == "superadmin":
            #                 print("Making user staff and admin.")
            #                 temp_user.is_admin = True
            #                 temp_user.is_staff = True
            #                 temp_user.save()
            #                 if group == "superadmin":
            #                     print("Making user super")
            #                     temp_user.is_superuser = True
            #                     temp_user.save()
            #         except ObjectDoesNotExist:
            #             print("Could not find an object for the requested user.")
            #  except ObjectDoesNotExist:
            #      print("Could not find a matching key.")
        return JsonResponse({'status': True})
