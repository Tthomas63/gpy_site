from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    def get(self, request):
        user = request.user
        if not user.is_staff or not user.is_admin or not user.is_superuser or not user.is_authenticated:
            return HttpResponseForbidden()
        return render(request, 'remote_admin/index.html')
