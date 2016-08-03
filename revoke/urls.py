# urls for our app

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='revoke-index'),
]
