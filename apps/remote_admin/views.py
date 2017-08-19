from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.main.models import SteamUser
from .forms import RconCmdForm, BanUserForm
from gpy import settings
from . import rcon
from .rcon import RCON
from socket import *

class UsageView(View):
    def get(self, request):
        if not request.user.is_staff or not request.user.is_superuser or not request.user.is_authenticated:
            return HttpResponseForbidden()
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
        if not request.user.is_staff or not request.user.is_superuser or not request.user.is_authenticated:
            return HttpResponseForbidden()
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
        if not request.user.is_staff or not request.user.is_superuser or not request.user.is_authenticated:
            return HttpResponseForbidden()
        context = {}
        context = run_rcon_cmd(rcon_server_port, rcon_cmd)
        return render(request, 'remote_admin/rcon_cmd.html', context)


class RconView(View):
    def get(self, request):
        user = request.user
        if not user.is_staff or not user.is_superuser or not user.is_authenticated:
            return HttpResponseForbidden()
        return render(request, 'remote_admin/rcon.html')

    def post(self, request):
        if not request.user.is_staff or not request.user.is_superuser or not request.user.is_authenticated:
            return HttpResponseForbidden()
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


class BanUserView(View):
    def get(self, request):
        if not request.user.is_staff or not request.user.is_superuser or not request.user.is_authenticated:
            return HttpResponseForbidden()
        context = dict()
        context['form'] = BanUserForm()
        context['all_users'] = SteamUser.objects.all()
        return render(request, 'remote_admin/ban_user.html', context)

    def post(self, request):
        if not request.user.is_staff or not request.user.is_superuser or not request.user.is_authenticated:
            return HttpResponseForbidden()
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = BanUserForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                rcon_server_port = form.cleaned_data['rcon_server_port']
                rcon_steam_id = form.cleaned_data['steam_id']
                # rcon_reg_steam_id = form.cleaned_data['steam_id_registered_user']
                rcon_ban_duration = int(form.cleaned_data['duration'])
                rcon_ban_reason = form.cleaned_data['reason']
                # if rcon_steam_id is None or rcon_steam_id == "" and rcon_steam_id != "":
                #     rcon_steam_id = rcon_reg_steam_id
                # elif rcon_steam_id is not None or rcon_steam_id != "" and rcon_steam_id == "":
                #     # do nothing
                #     print("Not using reg steam id.")
                # else:
                #     rcon_steam_id = rcon_steam_id
                rcon_cmd = "ulx banid {0} {1} {2}".format(rcon_steam_id, rcon_ban_duration, rcon_ban_reason)
                context = run_rcon_cmd(rcon_server_port, rcon_cmd)
                context['form'] = form
                context['all_users'] = SteamUser.objects.all()
                return render(request, 'remote_admin/ban_user.html', context)
            else:
                context = dict()
                context['form'] = BanUserForm
                context['all_users'] = SteamUser.objects.all()
                return render(request, 'remote_admin/ban_user.html', context)
        # if a GET (or any other method) we'll create a blank form
        else:
            if not request.user.is_staff or not request.user.is_superuser or not request.user.is_authenticated:
                return HttpResponseForbidden()
            else:
                form = BanUserForm()
                context = dict()
                context['form'] = form
                context['all_users'] = SteamUser.objects.all()
                return render(request, 'remote_admin/ban_user.html', context)


# def ban_user(request, rcon_server_port, steam_id, duration, reason):
#     if not request.user.is_admin():
#         return HttpResponseForbidden()
#     else:
#         if request.method == "POST":
#             try:
#                 banned_user = SteamUser.objects.get(steamid=steam_id)
#                 steam_id = banned_user.get_steam2_id()
#                 ban_cmd = "ulx banid {0} {1} {2}".format(steam_id, duration, reason)
#                 request.session['rcon_stdout'] = run_rcon_cmd(rcon_server_port, ban_cmd)
#             except ObjectDoesNotExist:
#                 print("Could not find a user for this steam_id.")
#         else:
#             return HttpResponseForbidden()

def view_logs(request):
    if not request.user.is_admin():
        return HttpResponseForbidden()
    else:
        start_rcon_session("27015")
        response = HttpResponse()
        return response


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


def start_rcon_session(rcon_server_port):
    import time
    pings = 1
    # Send ping 10 times
    while pings < 11:
        # Create a UDP socket
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        # Set a timeout value of 1 second
        clientSocket.settimeout(60)
        # Ping to server
        message = 'test'
        addr = ("45.32.224.44", 27015)
        # Send ping
        start = time.time()
        clientSocket.sendto(message, addr)
        # If data is received back from server, print
        try:
            data, server = clientSocket.recvfrom(1024)
            end = time.time()
            elapsed = end - start
            print(data + " " + pings + " " + elapsed)

            # If data is not received back from server, print it has timed out
        except timeout:
            print('REQUEST TIMED OUT')
        pings = pings - 1
    # import socket
    # try:
    #     UDP_IP = "0.0.0.0"
    #     UDP_PORT = 27015
    #     sock = socket.socket(socket.AF_INET,  # Internet
    #                          socket.SOCK_DGRAM) # UDP
    #     #sock.connect((UDP_IP, UDP_PORT))
    #     sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #     sock.bind((UDP_IP, int(UDP_PORT)))
    #     sock.sendto("START".encode(), ("45.32.224.44", 27015))
    #     #sock.send("Hello".encode())
    #     while True:
    #         data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    #         #data, addr = sock.accept()
    #         print(data)
    #         yield data
    #         # sock.listen()
    # except AttributeError:
    #     print("Could not perform selected request.")