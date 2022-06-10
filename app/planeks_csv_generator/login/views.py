from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView

from planeks_csv_generator.login.forms import LoginForm



class LoginView(FormView):

    template_name = 'login/login.html'
    form_class = LoginForm
    success_url = '/schemas/'

    def form_valid(self, form):
        data = form.cleaned_data
        user = authenticate(self.request, username=data.get("username"), password=data.get("password"))
        if user is not None:
            login(self.request, user)
        else:
            return redirect("/login/")
        return super().form_valid(form)






