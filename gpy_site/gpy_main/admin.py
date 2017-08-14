from django.contrib import admin
from .models import UlxSecretKey
from .models import SteamUser


@admin.register(SteamUser)
class SteamUserAdmin(admin.ModelAdmin):
    pass
# Register your models here.

admin.site.register(UlxSecretKey)