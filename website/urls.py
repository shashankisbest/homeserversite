"""
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('filetransfer/', include('filetransfer.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('accounts.urls')),


    # path('logout/', include('accounts.urls')),
    #no need to specify logout because django appends urls and checks for every matching url in every app, so when it finds logout/ in accounts.urls, it will execute that view and log the user out
]
