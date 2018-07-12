"""DjangoServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from ChatServer.json_handler import json_handler
from ChatServer.views import image_response, voice_response

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('image/(?P<file_name>\S*)', image_response),
    re_path('voice/(?P<file_name>\S*)', voice_response),
    path('', json_handler),
]
