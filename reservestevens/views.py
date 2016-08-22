from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from book.models import UBStudent

import datetime
import helpers

# Create your views here.
# Functions that take user request and return html page back

@login_required
def index(request):
    first = helpers.calc_day(0).strftime('%A, %B %d %Y')
    second = helpers.calc_day(1).strftime('%A, %B %d %Y')
    context = {'first' : first, 'second': second}
    return render(request, 'index.html', context)

def register(request):
    # list of fields that will be displayed on register form
    fields = [  {'name': 'username', 'type': 'text', 'label': 'UBIT name (will be your username):', 'value': ''},
                {'name': 'ubnumber', 'type': 'text', 'label': 'UB number:', 'value': ''},
                {'name': 'email', 'type': 'email', 'label': 'Email:', 'value': ''},
                {'name': 'password', 'type': 'password', 'label': 'Password:', 'value': ''}]
    if request.method == 'GET':
        return render(request, 'register.html', {'fields': fields, })
    elif request.method == 'POST':
        # get an user object based on entered data
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(username=username, email=request.POST['email'], ubstudent__ubnumber=request.POST['ubnumber'])
        except (User.DoesNotExist, ValueError):
            return render(request, 'register.html', {'fields': fields, 'error': 'Information you entered does not match our records.'})
        if user.is_active:
            return render(request, 'register.html', {'fields': fields, 'error': 'You have registered account already.'})
        # activate user's account
        user.is_active = True
        # set password
        user.set_password(password)
        user.save()
        # create a session for user
        user = authenticate(username=username, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

def login_user(request):
    # list of fields that will be displayed on login form
    fields = [  {'name': 'username', 'type': 'text', 'label': 'Username:', 'value': ''},
                {'name': 'password', 'type': 'password', 'label': 'Password:', 'value': ''}]
    if request.method == 'GET':
        return render(request, 'login.html', {'fields': fields})
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        # authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            # create session
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {'fields': fields, 'error': 'Incorrect username or password. Please try again.'})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
