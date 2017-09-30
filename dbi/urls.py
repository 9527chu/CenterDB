from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from views import AssetView



urlpatterns = [
    url(r'asset/$', AssetView.as_view(), name='asset'),
    ]