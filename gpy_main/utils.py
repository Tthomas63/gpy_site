from django.conf import settings
from steam import SteamID
from steam.steamid import make_steam64


def steam2_to_steam64(steam2):
    steam64 = make_steam64(steam2)
    return steam64


def steam64_to_steam2(steam64):
    steam2 = SteamID(steam64).as_steam2
    return steam2


def steam64_to_steam2_zero(steam64):
    steam2 = SteamID(steam64).as_steam2_zero
    return steam2