from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^notify/$', views.ZRUNotifyView.as_view(), name='zru-notify'),
]
