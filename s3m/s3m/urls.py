"""s3m URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from dmgen.views import IndexView

from .api_v1 import v1_api

admin.autodiscover()

"""
API URLS look like this on the dev machine:

http://127.0.0.1:8000/api/v1/xdboolean
or for JSON
http://127.0.0.1:8000/api/v1/xdboolean?format=json
"""
urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', IndexView.as_view(), name='home'),    
    url(r'^api/', include(v1_api.urls)),
]
