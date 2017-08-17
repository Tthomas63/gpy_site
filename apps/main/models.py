import uuid

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from steam import SteamID


class UlxSecretKey(models.Model):
    value = models.CharField(default=uuid.uuid4(), max_length=200)

    def __str__(self):
        return self.value


class UlxDataStore(models.Model):
    secret_key = models.ForeignKey(UlxSecretKey, related_name='ulx_secret_key')


class GpyProfile(models.Model):
    bio = models.CharField(max_length=600, default="")
    signature = models.CharField(max_length=200, default="")
    motto = models.CharField(max_length=100, default="")


class UlxUserData(models.Model):
    linked_store = models.ForeignKey(UlxDataStore, related_name="user_data")
    rank = models.CharField(max_length=50)
    steam_id = models.CharField(max_length=20, unique=True)


class SteamUserManager(BaseUserManager):
    def _create_user(self, steamid, password, **extra_fields):
        """
        Creates and saves a User with the given steamid and password.
        """
        try:
            # python social auth provides an empty email param, which cannot be used here
            del extra_fields['email']
        except KeyError:
            pass
        if not steamid:
            raise ValueError('The given steamid must be set')
        user = self.model(steamid=steamid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.get_or_create_gpy_profile()
        user.get_or_create_userdata()
        return user

    def create_user(self, steamid, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(steamid, password, **extra_fields)

    def create_superuser(self, steamid, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(steamid, password, **extra_fields)


class SteamUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'steamid'

    rank = models.CharField(max_length=50, default="user")
    steamid = models.CharField(max_length=20, unique=True)
    personaname = models.CharField(max_length=255)
    profileurl = models.CharField(max_length=300)
    avatar = models.CharField(max_length=255)
    avatarmedium = models.CharField(max_length=255)
    avatarfull = models.CharField(max_length=255)

    user_data = models.OneToOneField(UlxUserData, on_delete=models.CASCADE, null=True)
    gpy_profile = models.OneToOneField(GpyProfile, on_delete=models.CASCADE, null=True)

    # Add the other fields that can be retrieved from the Web-API if required

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = SteamUserManager()

    def get_short_name(self):
        return self.personaname

    def get_full_name(self):
        return self.personaname

    def get_steam2_id(self):
        user_steam_id = SteamID(self.steamid)
        return user_steam_id.as_steam2

    def update_rank(self, group):
        if self.rank != group:
            self.rank = group
            self.save()
            if group in settings.ULX_ADMIN_RANKS or group in settings.ULX_SUPER_RANKS:
                print("Making user {} staff/admin.".format(self.personaname))
                self.is_staff = True
                self.is_admin = True
                self.save()
                if group in settings.ULX_SUPER_RANKS:
                    print("Making user {} superadmin.".format(self.personaname))
                    self.is_superuser = True
                    self.save()
        else:
            print("User {}'s rank is staying the same".format(self.personaname))

    def get_or_create_userdata(self):
        try:
            temp_user_data = self.user_data
            return temp_user_data
        except ObjectDoesNotExist:
            temp_user_data = UlxUserData.objects.create(rank=self.rank,steam_id=self.steamid)
            self.user_data = temp_user_data
            self.save()
            return self.user_data

    def get_or_create_gpy_profile(self):
        if hasattr(self, 'gpy_profile') and self.gpy_profile != None:
            return getattr(self, 'gpy_profile')
        else:
            new_profile = GpyProfile.objects.create()
            new_profile.save()
            self.gpy_profile = new_profile
            self.gpy_profile.save()
            self.save()
            return self.gpy_profile

