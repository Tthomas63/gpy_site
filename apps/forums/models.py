from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False)


class Thread(models.Model):
    category = models.ForeignKey('forums.Category', related_name="threads")
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    started_by = models.ForeignKey('main.SteamUser')
    title = models.CharField(max_length=255)
    include_signatures = models.BooleanField(default=False)
    last_post_date = models.DateTimeField(null=True, blank=True)


class Post(models.Model):
    thread = models.ForeignKey('forums.Thread', related_name="posts")
    date_created = models.DateTimeField()
    posted_by = models.ForeignKey('main.SteamUser')
    content = models.TextField(max_length=600)
