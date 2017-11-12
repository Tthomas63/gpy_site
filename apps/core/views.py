from django.shortcuts import render
from django.views import View
from django.views.generic.base import ContextMixin


class IndexView(View, ContextMixin):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
