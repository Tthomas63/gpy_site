from django.contrib import admin
from .models import Announcement
from .models import AnnouncementType
from .models import SteamUser
from .models import UlxSecretKey


@admin.register(SteamUser)
class SteamUserAdmin(admin.ModelAdmin):
    pass


# Register your models here.

admin.site.register(UlxSecretKey)
admin.site.register(Announcement)
admin.site.register(AnnouncementType)
