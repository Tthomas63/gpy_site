from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=125, blank=False)
    description = models.CharField(max_length=300, blank=False)

    ip = models.CharField(max_length=30, blank=False)
    port = models.IntegerField(default=0)

    rcon_password = models.CharField(max_length=50)

    game = models.CharField(max_length=20)
    gamemode = models.CharField(max_length=50)
