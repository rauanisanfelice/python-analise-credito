from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from machine.urls import *

urlpatterns = [
    path('', index.as_view(), name='index'),
]
