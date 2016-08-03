from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# Functions that take user request and return html page back

def index(request):
    return render(request, 'revoke/revoke-index.html', None)
