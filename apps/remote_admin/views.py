from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from .forms import RconCmdForm
from gpy import settings
from . import rcon


class UsageView(View):
    def get(self, request):
        return render(request, 'remote_admin/usage.html')


class IndexView(View):
    def get(self, request):
        user = request.user
        if not user.is_staff or not user.is_superuser or not user.is_authenticated:
            return HttpResponseForbidden()
        return render(request, 'remote_admin/index.html')


class RconView(View):
    def get(self, request):
        user = request.user
        if not user.is_staff or not user.is_superuser or not user.is_authenticated:
            return HttpResponseForbidden()
        return render(request, 'remote_admin/rcon.html')

    def post(self, request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = RconCmdForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                rcon_server_port = form.cleaned_data['rcon_server_port']
                rcon_cmd = form.cleaned_data['rcon_cmd']
                # redirect to a new URL:
                return HttpResponseRedirect('/remote_admin/rcon_cmd/{0}/{1}'.format(rcon_server_port, rcon_cmd))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = RconCmdForm()
        return render(request, 'remote_admin/rcon.html', {'form': form})


class RconCmdView(View):
    def get(self, request, rcon_server_port, rcon_cmd):
        context = {}
        context = run_rcon_cmd(rcon_server_port, rcon_cmd)
        return render(request, 'remote_admin/rcon_cmd.html', context)


def run_rcon_cmd(rcon_server_port, rcon_cmd):
    rcon_server_address = ("45.32.224.44", int(rcon_server_port))
    local_context = dict()
    try:
        print("Trying to send command.")
        local_context['rcon_stdout'] = rcon.execute(rcon_server_address, str(settings.RCON_PASSWORD), str(rcon_cmd))
        print("We sent a command.")
    except(UnicodeDecodeError,
           rcon.RCONCommunicationError,
           rcon.RCONAuthenticationError,
           rcon.RCONMessageError,
           rcon.RCONTimeoutError
           ) as e:
        print("There was an error")
        print(e)
        local_context['error'] = e
    return local_context
