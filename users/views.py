# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import views
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator

from auth.decorators import auth_required


class LoginPage(views.View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if 'authToken' in request.session:
            return redirect('/home')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        from users.models import User
        authToken, message = User.validateUser(request)
        messages.error(request, message)
        if authToken:
            request.session['authToken'] = authToken
            return redirect('/home')
        return redirect('/')


class Home(views.View):
    template_name = 'login.html'

    @method_decorator(auth_required)
    def dispatch(self, request, user, *args, **kwargs):
        return super(Home, self).dispatch(request, user, *args, **kwargs)

    def get(self, request, user, *args, **kwargs):
        return render(request, self.template_name, {'user': user})


class Logout(views.View):

    def get(self, request, *args, **kwargs):
        messages.error(request, 'You had been successfully Logout.')
        if 'authToken' in request.session:
            del request.session['authToken']
        return redirect('/')


class Register(views.View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        from users.models import User
        user, message = User.createNew(request.POST.dict())
        messages.error(request, message)
        if user:
            return redirect('/')
        return redirect('/register')
