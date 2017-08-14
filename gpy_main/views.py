from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import KeyForm
from .models import UlxSecretKey

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


@csrf_exempt
def ulx_secret_key_communicate(request):
    context = {}
    ulx_secret_key = 0
    template = loader.get_template('gpy_main/index.html')
    try:
        ulx_secret_key = UlxSecretKey.objects.all()[0]
    except ObjectDoesNotExist:
        print("Could not find a key, generate one.")
        context['msg'] = "Could not find a secret ULX key. Please generate one from Admin."
    if request.method == "POST":
        client_key = request.POST.get("ulx_secret_key")
        if ulx_secret_key == client_key:
            print("Key accepted")
            context['msg'] = "Key accepted!"
            ulx_ranks = request.POST.get('ulx_ranks')
            print(ulx_ranks)
            return HttpResponse(template.render(context, request))
        else:
            context['msg'] == "Key not accepted"
            return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(template.render(context, request))


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
