"""MovieBS URL Configuration

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
from django.conf.urls import url,include
from django.views.static import serve
from film import views
from MovieBS import settings
from stark.service import v1

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^stark/', v1.site.urls),
    url(r'^login/', views.login),
    url(r'^logout', views.logout),
    url(r'^reg/', views.reg),
    url(r'^get_validCode_img/', views.get_validCode_img),
    url(r'^index/', views.index),
    url(r'^detail/', views.MovieDetail),

    # media 配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
