from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("ping", views.ping, name="ping"),
    path("file/<file_name>", views.file, name="file"),
]
