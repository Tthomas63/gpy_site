from django.contrib import admin
from .models import Forum, ForumReply, ForumCategory, ForumThread

# Register your models here.

admin.site.register(Forum)
admin.site.register(ForumReply)
admin.site.register(ForumCategory)
admin.site.register(ForumThread)