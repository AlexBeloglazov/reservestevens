from django.shortcuts import render
from django.http import HttpResponse

import datetime
import helpers

# Create your views here.
# Functions that take user request and return html page back

def index(request):
    first = helpers.calc_day(0).strftime('%A, %B %d %Y')
    second = helpers.calc_day(1).strftime('%A, %B %d %Y')
    context = {'first' : first, 'second': second}
    return render(request, 'index.html', context)
