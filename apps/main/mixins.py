from django.views.generic.base import ContextMixin

from .models import Announcement


class AnnouncementMixin(ContextMixin):
    def get_announcements(self, **kwargs):
        all_announcements = Announcement.objects.all()
        return all_announcements
