"""SocialNetworkHarvester_v1p0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^(?i)admin/?', admin.site.urls),
    url(r'^(?i)twitter/?', include('Twitter.urls')),
    url(r'^(?i)facebook/?', include('Facebook.urls')),
    url(r'^(?i)youtube/?', include('Youtube.urls')),
    url(r'^(?i)dailymotion/?', include('Dailymotion.urls')),
    url(r'^(?i)group/?', include('Group.urls')),
    url(r'^(?i)tool/?', include('tool.urls')),
    url(r'^(?i)user/?', include('AspiraUser.urls')),
    url(r'^', include('AspiraUser.urls')),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
