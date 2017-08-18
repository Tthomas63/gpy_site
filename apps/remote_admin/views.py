from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.views import View

from gpy import settings
from .rcon import RCON


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
        context = {}
        con_cmd = request.POST.get('rcon_command')
        with RCON(settings.RCON_SERVER_ADDRESS, settings.RCON_PASSWORD) as rcon:
            context["rcon_stdout"] = rcon("{}".format(con_cmd))
        context["rcon_stdout"] = "Test this is bullshit lololol"
        return render(request, 'remote_admin/rcon.html', context)
