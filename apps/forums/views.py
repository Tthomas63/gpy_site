from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .forms import PartialForumForm
from .models import Forum, ForumThread, ForumCategory, ForumReply


# Create your views here.

class IndexView(View):
    def get(self, request):
        context = dict()
        context['forums'] = Forum.objects.all()
        return render(request, 'forums/index.html', context)


class CategoryView(View):
    def get(self, request, category_pk):
        context = dict()
        try:
            context['category'] = ForumCategory.objects.get(pk=category_pk)
        except ObjectDoesNotExist:
            context['category'] = None
        return render(request, 'forums/category/view.html', context)


class ThreadView(View):
    def get(self, request, thread_pk):
        context = dict()
        try:
            context['thread'] = ForumThread.objects.get(pk=thread_pk)
        except ObjectDoesNotExist:
            context['category'] = None
        return render(request, 'forums/thread/view.html', context)


class CreateForumView(View):
    form_class = PartialForumForm
    initial = {'key': 'value'}
    template_name = 'forums/create_forum.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form.save()
            return redirect('forums:index')

        return render(request, self.template_name, {'form': form})