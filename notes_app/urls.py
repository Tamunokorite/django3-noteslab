"""notes_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from decouple import config
from notes import views
from notes_app import settings

urlpatterns = [
    path(config('ADMIN_SITE_URL'), admin.site.urls),

    path('', views.index, name='index'),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    
    # Notes
    path('new/', views.newnote, name='newnote'),
    path('viewnotes/', views.viewnotes, name='mynotes'),
    path('viewnote/<int:id>', views.viewnote, name='viewnote'),
    path('deletenote/<int:id>', views.deletenote, name='deletenote'),
]

