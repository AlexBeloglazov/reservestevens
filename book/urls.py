# urls for our app

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<delta>[0,1])$', views.index, name='book-index'),
]
