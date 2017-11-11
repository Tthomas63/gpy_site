import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from apps.main.models import SteamUser, Announcement, AnnouncementType


@login_required
def get_user_from_steamid_as_json(request, steam_id=None):
    try:
        found_user = SteamUser.objects.get(steamid=steam_id)
    except ObjectDoesNotExist:
        found_user = None
    finally:
        json_user = json.dumps(found_user, cls=DjangoJSONEncoder)
        return JsonResponse(json_user)


def get_all_announcements_and_related_types(request):
    announcements = Announcement.objects.all()
    pk_list = list()
    for announce in announcements:
        pk_list.append(announce.pk)
    announcement_types = AnnouncementType.objects.filter(pk__in=pk_list)

    serialized_announcements = serializers.serialize("json", announcements)
    serialized_announcement_types = serializers.serialize("json", announcement_types)

    announcements_as_json = json.loads(serialized_announcements)
    announcement_types_as_json = json.loads(serialized_announcement_types)

    for announce in announcements_as_json:
        for type in announcement_types_as_json:
            if announce['fields']['announcement_type'] == type['pk']:
                print(announce['fields']['announcement_type'])
                announce['fields']['announcement_type'] = type
                print(announce['fields']['announcement_type'])
    response = json.dumps(announcements_as_json)
    return JsonResponse(response, safe=False)
