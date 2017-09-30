from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from repository.models import User
from ..forms.account import LoginForm, RegistForm



class RegistView(View):
    pass


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'

    # def get(self, request, *args, **kwargs):
    #     return super(LoginView, self).get(request, *args, **kwargs)

    # def form_valid(self, form):
    #     email = form.cleaned_data['username']
    #     password = form.cleaned_data['password']
    #     user = User.objects.get(email=email)
    #     if user and user.check_password(password):
    #         return HttpResponseRedirect(self.get_success_url())
    #     else:
    #         return HttpResponseRedirect(reverse('login'))

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('index')


class LogoutView(View):
    pass

# class LoginView(View):
#     def get(self, request):
#         return render(request, 'login.html')
#
#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = User.objects.get(email=email)
#             if user and user.check_password(password):
#                 return HttpResponseRedirect(reverse('index'), {'form': form})
#             else:
#                 form = LoginForm()
#         return render(request, 'login.html', {'form': form})

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
