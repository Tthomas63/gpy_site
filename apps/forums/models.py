from django.db import models
from apps.servers.models import Server
from apps.main.models import SteamUser

# Create your models here.


class Forum(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)

    server = models.ForeignKey(Server, related_name='related_forums', blank=True, null=True)

    logo = models.ImageField(verbose_name="Forum logo", blank=True, null=True)

    def __str__(self):
        return "Forum: {}".format(self.title)

    def get_category_count(self):
        if self.categories:
            return len(self.categories.all())


class ForumCategory(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=150, blank=True, null=True)

    forum = models.ForeignKey(Forum, related_name='categories', blank=False, null=False)

    logo = models.ImageField(verbose_name="Forum Category Logo", blank=True, null=True)

    def __str__(self):
        return "Category: {}".format(self.title)

    def get_thread_count(self):
        if self.threads:
            return len(self.threads.all())


class ForumThread(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    category = models.ForeignKey(ForumCategory, related_name='threads', null=False, blank=False)

    owner = models.ForeignKey(SteamUser, related_name='posted_threads', null=False, blank=False)
    message = models.CharField(max_length=600)

    posted = models.DateField(auto_now_add=True)
    last_edited = models.DateField(blank=True, null=True)
    last_reply = models.DateField(blank=True, null=True)

    locked = models.BooleanField(default=False)
    sticky = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return "Thread: {}".format(self.title)

    def get_participants(self):
        users = list()
        if self.replies and len(self.replies.all()) >= 1:
            for reply in self.replies.all():
                users.append(reply.owner)
        return users

    def get_reply_count(self):
        if self.replies:
            return len(self.replies.all())


class ForumReply(models.Model):
    thread = models.ForeignKey(ForumThread, related_name='replies', blank=False, null=False)

    owner = models.ForeignKey(SteamUser, related_name='posted_replies', null=False, blank=False)
    message = models.CharField(max_length=600, null=False, blank=False)

    posted = models.DateField(auto_now_add=True)
    last_edited = models.DateField(blank=True, null=True)

    def __str__(self):
        return "{0}-{1}-{2}".format(self.owner.personaname, self.thread, self.posted)
