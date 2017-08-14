from venv import logger

import sys

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import logout
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import KeyForm
from .models import UlxSecretKey
import logging
logger2 = logging.getLogger('django')
logger = logging.getLogger('gpy_site')
logger3 = logging.getLogger('gpy_main')
logger4 = logging.getLogger('web')

logger.info("Test")
logger2.info("Test")
logger3.info("Test")
logger4.info("Test")

logger.debug("Test2")
logger2.debug("Test2")
logger3.debug("test2")
logger4.debug("Test2")
print("Test 3")



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
# def ulx_secret_key_communicate(request):
#     print("My view was called.")
#     context = {}
#     ulx_secret_key = 0
#     template = loader.get_template('gpy_main/key.html')
#
#     ulx_secret_key = UlxSecretKey.objects.all()[0]
#     if request.method == "POST":
#         print("I GOT A POST REQUEST WEEEEEEEEEEEEEEEEE")
#         print(request.POST.get)
#         logger.info(request.POST.get)
#         client_key = request.POST.get("ulx_secret_key")
#         if ulx_secret_key == client_key:
#             print("Key accepted")
#             context['msg'] = "Key accepted!"
#             ulx_ranks = request.POST.get('ulx_ranks')
#             print(ulx_ranks)
#             return HttpResponse(template.render(context, request))
#         else:
#             print("Failed client key was different.")
#             logger.info("Failed client key was diff")
#             context['msg'] == "Key not accepted"
#             return HttpResponse(template.render(context, request))
#     else:
#         print("Something else failed?")
#         logger.info("Failed.")
#         return HttpResponse(template.render(context, request))

class UlxSecretKeyPage(View):
    def get(self, request):
        return render(request, 'gpy_main/key.html')

    def post(self, request):
        #print(request.body)
        print(request.POST.get)
        q = request.POST.get
        # (request.body)
        return JsonResponse({'status': True})


def set_key_2(request):
    # if this is a POST request we need to process the form data
    try:
        ulx_secret_key = UlxSecretKey.objects.all()[0]
    except ObjectDoesNotExist:
        print("Could not find a key, generate one.")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = KeyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            if form.cleaned_data['key'] == ulx_secret_key:
                print("Link success")
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = KeyForm()

    return render(request, 'gpy_main/key.html', {'form': form})
