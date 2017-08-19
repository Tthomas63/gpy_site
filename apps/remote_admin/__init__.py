import threading

from django.conf import settings

from . import rcon


def auto_sync_data():
    rcon_server_address = ("45.32.224.44", int("27015"))
    rcon.execute(rcon_server_address, str(settings.RCON_PASSWORD), "ulx gpy_sync_data")
    threading.Timer(600, auto_sync_data).start()

# start calling f now and every 60 sec thereafter
auto_sync_data()