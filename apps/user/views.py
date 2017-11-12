from django.contrib.auth.views import logout
from django.shortcuts import redirect, render
from django.views import View


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:index')


class LogoutPage(View):
    def get(self, request):
        return render(request, 'core/logout_page.html')


class LoginPage(View):
    def get(self, request):
        return render(request, 'core/login_page.html')