"""
URL configuration for CySTorogoz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from TorogozApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home_view, name='home'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.registro_view, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('insertartablagenera/', views.insertar_datos, name='insertartablagenera'),
    path('homeTableM/', views.homeTableM, name='homeTableM'),
    path('tHistorial/', views.pageHistorial, name= 'tHistorial'),
    path('redirigir-a-admin/', views.redirigir_a_admin, name='redirigir_a_admin'),
    path('salir/', views.salir, name="salir")
    
   
]
